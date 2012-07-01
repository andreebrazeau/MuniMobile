import nextbus, models, os, time
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
		route_tag = user.route_tag # whatever user's route tag is
		stopID = user.stop_id # whatever user's stop ID is
		text_time = user.start_time # whatever user's text time is. This is 1:36 pm
		text_time = datetime.now()
		minutes_away = user.minutes_away
		print user.route_tag
		if check_time(text_time,user.days):
			predictions = check_for_busses(stopID, route_tag, minutes_away)
			if predictions:
				if predictions[0].block == user.bus_tag:
					continue

				else:
					send_message(message(predictions), user.phone_number)
				user.bus_tag = predictions[0].block
				user.save()

def check_time(text_time, text_days):

	if datetime.now() > text_time and datetime.now() < text_time + timedelta(hours=1):
		now = datetime.now()
		if str(now.isoweekday()) in text_days:
			return True
	else: 
		print False
		return False


def check_for_busses(stopID, route_tag, minutes_away):
	predictions = nextbus.get_predictions_for_stop('sf-muni', stopID)
	checked_predictions = []
	
	# if prediction is within fifteen minutes from now, add it to checked_predictions
	if prediction.minutes <= int(minutes_away) and prediction.direction.route.tag == route_tag:
		x = 0
		while x < 3:

			for prediction in predictions.predictions:
				if prediction.route.tag == route_tag:
					checked_predictions.append(prediction)
					x += 1
	return checked_predictions

def message(predictions):
	string_predictions = ""
	for each in predictions: 
		string_predictions += str(each.minutes) + ", "

	title = predictions[0].direction.route.title
	direction = predictions[0].direction.title	
	return "The %s line going %s is arriving in %sminutes" %(title, direction, string_predictions)

def send_message(message, phone_number):
	#message = client.sms.messages.create(to=phone_number, from_="+14155992671", body=message)
	print message


def main():
	while True:
		check_for_texts()
		time.sleep(10)

if __name__ == "__main__":
	main()

'''
import MuniMobile_app.prediction
MuniMobile_app.prediction.main()
'''



