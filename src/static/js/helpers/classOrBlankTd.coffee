define [
    'handlebars'
    'jquery'
    'underscore'
    'cs!helpers/trObj'
    'cs!helpers/formatClassroom'
    'hbs!templates/cnavi/timetable/timetable_class'
], (Handlebars, $, _, trObj, formatClassroom, template) ->
    Handlebars.registerHelper 'classOrBlankTd', (dow, start_period, registrations) ->

        isInPeriod = (c) ->
            unless c.start_period?
                return false
            c.day_of_week == dow && c.start_period.id == start_period

        registration = _.find registrations, (r) ->
            _.find r.subject.classes, isInPeriod
        [rowspan, classroom] = [1, ""]

        if registration
            classObj = _.find registration.subject.classes, isInPeriod
            rowspan = classObj.end_period.id - classObj.start_period.id + 1 if classObj.end_period?
            classroom = formatClassroom classObj.classroom if classObj.classroom?

        content = template(
            registration: registration
            rowspan: rowspan
            classroom: classroom
        )

        content = $('<div>').append(content).html()

        new Handlebars.SafeString(content)

