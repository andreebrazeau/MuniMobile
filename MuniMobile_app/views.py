from django.http import HttpResponse
from django.shortcuts import render_to_response
from MuniMobile_app.models import user_form
from MuniMobile_app.prediction import *
from json_data import *
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json, models, string, twilio.twiml

def index(request):
	return render_to_response('index.html')

def prediction(request):
	user = user_form.objects.all()
	return render_to_response('prediction.html', {'user': user})

def check_predictions(request):
	main()
	return render_to_response('check_predictions.html')

def get_all_routes(request):
	result = json_get_all_routes()
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_directions_of_route(request):
	route_tag = request.POST.get('route_tag', False)
	result = json_get_all_directions(route_tag)
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_stops(request):
	route_tag = request.POST.get('route_tag', False)
	direction_tag = request.POST.get('direction_tag', False)
	result = json_get_all_stops(route_tag, direction_tag)	
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_predictions_for_stop(request):
	stop_id = request.POST.get('stop_id', False)
	route_tag = request.POST.get('route_tag', False)
	result = json_get_predictions_for_stop(stop_id, route_tag)
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def set_notification(request):
	phone_number = request.POST.get('phone_number', False)
	stop_id = request.POST.get('stop_id', False)
	route_tag = request.POST.get('route_tag', False)
	start_time = request.POST.get('start_time', False)
	finish_time = request.POST.get('finish_time', False)
	days = request.POST.get('days', False)
	minutes_away = request.POST.get('minutes_away', False)
	direction_tag = request.POST.get('direction_tag', False)

	new_user = user_form(
		phone_number = phone_number,
	    route_tag = route_tag,
	    stop_id = stop_id,
	    start_time = start_time,
	    finish_time = finish_time,
	    days = days,
	    minutes_away = minutes_away
	)
	new_user.save()
	result = { 'message': 'Success!' }
	data = json.dumps(result)
	return json_response(data)

def sms(request):
    body = request.GET.get('Body', None)
    from_number = request.GET.get('From', None)
    if 'muni' in string.lower(body):
        for user in models.user_form.filter(phone_number=from_number):
            user.activated = False
            user.save()
        resp = twilio.twiml.Response()
        resp.sms("MuniMobile, we've removed all your scheduled SMS request. \
        	To schedule more request, visite our website.")
    return str(resp)


def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.code = code
    return resp
