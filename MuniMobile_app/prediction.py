import nextbus, models, os, time, string
from twilio.rest import TwilioRestClient
from datetime import datetime, timedelta
from pytz import timezone
import pytz
os.environ['DJANGO_SETTINGS_MODULE'] = "MuniMobile.settings"

account = os.environ['twilio_account']
token = os.environ['twilio_token']
print account, token
client = TwilioRestClient(account, token)


def check_for_texts(): # get all users from the database
    now = datetime.now()
    # each user has: text_time, busline, direction, stop, phone_num
    for user in models.user_form.objects.filter(activated=True):
        route_tag = user.route_tag # whatever user's route tag is
        stopID = user.stop_id # whatever user's stop ID is
        start_time = user.start_time # whatever user's text time is.
        finish_time = user.finish_time
        minutes_away = user.minutes_away
        text_days = user.days
        if check_time(start_time,finish_time,text_days, now):
            predictions = check_for_busses(stopID, route_tag, minutes_away)
            if predictions:
                if predictions[0].block == user.bus_tag and predictions[0].minutes<=minutes_away:
                    continue
                else:
                    send_message(message(predictions), user.phone_number)
                user.bus_tag = predictions[0].block
                user.save()

def check_time(start_time, finish_time, text_days, now):
    start_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + start_time, "%Y:%m:%d:%H:%M")
    finish_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + finish_time, "%Y:%m:%d:%H:%M")
    if now > start_str and now < finish_str:
        if str(now.isoweekday()) in text_days:
            return True
        else : 
            return False
    else:
        return False


def check_for_busses(stopID, route_tag, minutes_away):
    predictions = nextbus.get_predictions_for_stop('sf-muni', stopID)
    checked_predictions = []
    x = 0
    while x < 3:
        for prediction in predictions.predictions:
            if prediction.direction.route.tag == route_tag:
                checked_predictions.append(prediction)
                x += 1
    return checked_predictions

def message(predictions):
    list_pred = [str(each.minutes) for each in predictions]
    string_predictions = ', '.join(list_pred)
    title = predictions[0].direction.route.title
    direction = predictions[0].direction.title
    return "The %s line going %s is arriving in %sminutes, to cancel your schedule, reply 'muni'." %(title, direction, string_predictions)

def send_message(message, phone_number):
    print message
    message = client.sms.messages.create(to=phone_number, from_="+16502314762", body=message)

def main():
    check_for_texts()

if __name__ == "__main__":
    main()

'''
import MuniMobile_app.prediction
import datetime
MuniMobile_app.prediction.main()
MuniMobile_app.prediction.check_time('7:00', '11:00', [1,2,3,4,5,6,7], datetime.datetime.now())
'''



