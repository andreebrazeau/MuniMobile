from django.http import HttpResponse
from django.shortcuts import render_to_response
from MuniMobile_app.models import Notification
from MuniMobile_app.prediction import *
import nextbus_requests
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
import json, models, string, twilio.twiml

import logging

logger = logging.getLogger(__name__)


def index(request):
	return render_to_response('index.html')

def prediction(request):
	user = Notification.objects.all()
	return render_to_response('prediction.html', {'user': user})

def check_predictions(request):
	main()
	return render_to_response('check_predictions.html')

def get_all_routes(request):
	result = nextbus_requests.get_all_routes()
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_directions_of_route(request):
	route_tag = request.POST.get('route_tag', False)
	result = nextbus_requests.get_all_directions(route_tag)
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_stops(request):
	route_tag = request.POST.get('route_tag', False)
	direction_tag = request.POST.get('direction_tag', False)
	result = nextbus_requests.get_all_stops(route_tag, direction_tag)	
	data = json.dumps(result)
	return json_response(data)

@csrf_exempt
def get_predictions_for_stop(request):
	stop_id = request.POST.get('stop_id', False)
	route_tag = request.POST.get('route_tag', False)
	list_minutes = []
	predictions = nextbus_requests.get_predictions_for_stop(stop_id, route_tag)
	for prediction in predictions:
		print prediction
		list_minutes.append(prediction.minutes)
	print list_minutes
	data = json.dumps({'predictions':list_minutes})
	return json_response(data)

@csrf_exempt
def set_notification(request):
	message = Notification.create(request.POST)
	data = json.dumps(message)
	return json_response(data)

def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.code = code
    return resp
