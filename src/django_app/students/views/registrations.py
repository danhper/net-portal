from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from students.models import SubjectRegistration
import json

def update(request):
    response = HttpResponse(content_type='application/json')
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.raw_post_data)
            pk = data.get('id', None)
            try:
                registration = SubjectRegistration.objects.get(pk=pk)
                registration.update(data)
                response.content = registration.to_json()
                return response
            except ObjectDoesNotExist:
                response.content = json.dumps({'error': 'non existing pk'})
        else:
            response.content = json.dumps({'error': 'bad method'})
    else:
        response.content = json.dumps({'error': 'not ajax'})
    response.status_code = 400
    return response
