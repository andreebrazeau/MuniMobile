from django.http import HttpResponse
from django.shortcuts import render_to_response
from MuniMobile_app.models import user_form
from MuniMobile_app.prediction import *

def prediction(request):
	user = user_form.objects.all()
	return render_to_response('prediction.html', {'user': user})

def check_predictions(request):
    main()
    return render_to_response('check_predictions.html')