import nextbus, models, os
from twilio.rest import TwilioRestClient
from datetime import datetime, timedelta
from pytz import timezone
import pytz
os.environ['DJANGO_SETTINGS_MODULE'] = "MuniMobile.settings"

account = "ACd650b87a38605c19fe98bed15d6997b9"
token = "e65c7326a7a1fa7f048070fd6f862b98"
client = TwilioRestClient(account, token)


def check_for_texts(): # get all users from the database
	# each user has: text_time, busline, direction, stop, phone_num
	for user in models.user_form.objects.all():
		route_tag = user.bus_line # whatever user's route tag is
		stopID = user.stop_id # whatever user's stop ID is
		text_time = user.started_time # whatever user's text time is. This is 1:36 pm
		text_time = datetime.now()
		bus_tag = None
		if check_time(text_time):
			predictions = check_for_busses(stopID, route_tag)
			if predictions.prediction[0].block == bus_tag:
				continue
			if predictions:
				send_message(message(predictions), user.phonenumber)

def check_time(text_time):

	if datetime.now() > text_time and datetime.now() < text_time + timedelta(hours=1):
		return True
	else: 
		print False
		return False


def check_for_busses(stopID, route_tag):
	predictions = nextbus.get_predictions_for_stop('sf-muni', stopID)
	checked_predictions = []
	for prediction in predictions.predictions:
		# if prediction is within fifteen minutes from now, add it to checked_predictions
		if prediction.minutes <= 15 and prediction.direction.route.tag == route_tag:
			checked_predictions.append(prediction)
	return checked_predictions

def message(predictions):
	string_predictions = ""
	for each in predictions: 
		string_predictions += str(each.minutes) + ", "

	title = predictions[0].direction.route.title
	direction = predictions[0].direction.title
	print "The %s line going %s is arriving in %sminutes" %(title, direction, string_predictions)
	return "The %s line going %s is arriving in %sminutes" %(title, direction, string_predictions)

def send_message(message, phone_number):
	message = client.sms.messages.create(to=phone_number, from_="+14155992671", body=message)



def main():
	check_for_texts()

if __name__ == __main__:
	main()