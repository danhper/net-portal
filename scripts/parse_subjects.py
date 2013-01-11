#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import re
import unicodedata
import time
import gzip
import os.path

SEEDS_PATH = '../src/courses/fixtures'
DATAFILE = "initial_data.json"

SCHOOLS_FILE = os.path.join(SEEDS_PATH, 'schools.json')
PERIODS_FILE = os.path.join(SEEDS_PATH, 'periods.json')
SUBJECTS_FILE = 'data.html.gz'

days_of_week = {
    "月": "mon",
    "火": "tue",
    "水": "wed",
    "木": "thu",
    "金": "fri",
    "土": "sat",
    "日": "sun"
}

def make_school_dict():
    with open(SCHOOLS_FILE, 'r') as f:
        schools = json.loads(f.read())
    return {s['fields']['jp_short_name']: s['pk'] for s in schools}

subjects = []
classes = []
teachers = {}
buildings = {}
classrooms = {}
schools = make_school_dict()


def get_subjects():
    start = time.time()
    open_func = lambda s: gzip.open(s, 'rb') if s.endswith(".gz") else open(s, 'r')
    with open_func(SUBJECTS_FILE) as f:
        s = f.read()
        print("Document read in {0:.5}s".format(time.time() - start))
        start = time.time()
        soup = BeautifulSoup(s, "lxml")
        print("Document parsed in {0:.5}s".format(time.time() - start))
    subjects_soup = soup.select("table.ct-vh > tbody > tr")[2:]
    reg = re.compile("^post_submit\('.+?', '(.+?)'\);$")
    for subject in subjects_soup:
        subject_obj = parse_subject(subject, len(subjects) + 1, reg)
        subjects.append(subject_obj)

def parse_subject(subject, i, reg):
    subject_obj = {
        "model": "courses.subject",
        "pk": i,
    }
    fields = {}
    info = subject("td")
    fields["year"] = int(info[0].text)
    fields["jp_name"] = info[1].text
    net_portal_id = reg.match(subject.input['onclick']).group(1)[:12]
    fields["net_portal_id"] = net_portal_id
    fields["school"] = schools[info[3].text]
    season = info[4].text
    if season in ["前期", "春期", "春"]:
        fields["term"] = "SP"
    elif season in ["後期", "秋期", "秋"]:
        fields["term"] = "AU"
    elif "冬" in season:
        fields["term"] = "WI"
    elif "夏" in season:
        fields["term"] = "SU"
    elif season == "通年":
        fields["term"] = "AY"
    else:
        fields["term"] = None
    fields["jp_description"] = fields["en_description"] = info[7].text
    fields["teachers"] = make_teachers(info)
    subject_obj["fields"] = fields
    parse_class(info, i)
    return subject_obj

def make_teachers(info):
    school = info[3].text
    teachers = []
    for teacher in info[2].text.split("／"):
        if "　" in teacher or " " in teacher:
            (last_name, first_name) = re.split("[　 ]", teacher, 1)
        elif "." in teacher or "．" in teacher:
            (last_name, first_name) = re.split("[\.．]", teacher, 1)
        else:
            (last_name, first_name) = (teacher, "")
        pk = create_teacher(first_name, last_name, school)
        teachers.append(pk)
    return teachers


def parse_class(info, subject_id):
    time_info = [s.string for s in info[5].contents if s.string]
    classroom_info = [s.string for s in info[6].contents if s.string]
    for (time, classroom) in zip(time_info, classroom_info):
        (day_of_week, start_period, end_period) = parse_time(time[3:])
        class_obj = {
            "model": "courses.class",
            "pk": None,
            "fields": {
                "subject": subject_id,
                "start_period": start_period,
                "end_period": end_period,
                "day_of_week": day_of_week,
                "classroom": parse_classroom(classroom)
            }
        }
    classes.append(class_obj)

def parse_time(time):
    global days_of_week
    if time.endswith("時限"):
        day_of_week = days_of_week[time[0]]
        start_period = end_period = to_half_width(time[1])
    elif "-" in time or "−" in time:
        day_of_week = days_of_week.get(time[0], None)
        start_period = to_half_width(time[1])
        end_period = to_half_width(time[3])
    else:
        start_period = end_period = day_of_week = None
    return (day_of_week, start_period, end_period)

def to_half_width(full_width_string):
    try:
        return unicodedata.normalize('NFKC', full_width_string)
    except:
        return None

def parse_classroom(classroom):
    if classroom == "教室未定":
        return None
    classroom = classroom[3:]

    x, y = -1, -1
    try:
        x = classroom.index("ー")
    except ValueError:
        pass
    try:
        y = classroom.index("-")
    except ValueError:
        pass
    if x == -1 and y == -1:
        a = None
    elif x == -1 or y == -1:
        a = max(x, y)
    else:
        a = min(x, y)

    if classroom.startswith("１７号館"):
        building = "17"
        name = classroom.split("　")[3]
        class_info = ''.join(classroom.split("　")[4:])
    elif classroom.startswith("無"):
        return None
    elif a and a <= 4:
        (building, name) = classroom.split(classroom[a], 1)
        for s in [")", "）", "講義室", "教室", "研究室", "(", "（"]:
            name = name.rstrip(s)
        class_info = None
        (b, n) = (to_half_width(building), to_half_width(name))
        if not n:
            m = re.match("([Ａ-Ｚａ-ｚ０-９]*)(.*)", name)
            if m:
                n = m.group(1)
                name = to_half_width(n) if to_half_width(n) else n
                class_info = m.group(2).replace("(", "").replace("（", "")
        else:
            name = n
        building = b if b else building
    else:
        building = None
        class_info = None
        name = classroom
    create_classroom(building, name, class_info)
    return classrooms[(building, name)]["pk"]

def create_teacher(first_name, last_name, school):
    if (first_name, last_name, school) in teachers:
        return teachers[(first_name, last_name, school)]["pk"]
    pk = len(teachers)
    teacher = {
        "model": "courses.teacher",
        "pk": pk,
        "fields": {
            "jp_first_name":  first_name,
            "jp_last_name": last_name,
            "en_first_name":  first_name,
            "en_last_name": last_name,
            "school": schools[school]
        }
    }
    teachers[(first_name, last_name, school)] = teacher
    return pk

def create_building(name):
    if not name or name in buildings:
        return
    building = {
        "model": "courses.building",
        "pk": len(buildings) + 1,
        "fields": {
            "jp_name": str(name),
            "en_name": str(name)
        }
    }
    buildings[name] = building

def create_classroom(building, classroom_name, info):
    if (building, classroom_name) in classrooms:
        return
    if building and not building in buildings:
        create_building(building)
    n = len(classrooms) + 1
    classroom = {
        "model": "courses.classroom",
        "pk": n,
        "fields": {
            "building": buildings[building]["pk"] if building else None,
            "jp_name": str(classroom_name),
            "en_name": str(classroom_name),
            "info": info if info else None
        }
    }
    classrooms[(building, classroom_name)] = classroom


if __name__ == '__main__':
    start = time.time()
    get_subjects()
    with open(SCHOOLS_FILE, 'r') as f:
        schools = json.loads(f.read())
    with open(PERIODS_FILE, 'r') as f:
        periods = json.loads(f.read())
    data = schools + periods
    to_normalize = [buildings, classrooms, teachers]
    for li in map(lambda x: list(x.values()), to_normalize):
        data += li
    data += subjects + classes
    with open(os.path.join(SEEDS_PATH, DATAFILE), 'w') as f:
        f.write(json.dumps(data))
        f.write("\n")
    print("Executed in {0:.5}s".format(time.time() - start))
