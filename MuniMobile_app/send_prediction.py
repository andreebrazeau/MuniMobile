import nextbus, models, os, time, string
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import logging

os.environ['DJANGO_SETTINGS_MODULE'] = "MuniMobile.settings"

def check_for_texts(): # get all users from the database
    # each user has: text_time, busline, direction, stop, phone_num
    for user in models.Notification.objects.filter(activated=True):
        route_tag = user.route_tag # whatever user's route tag is
        stopID = user.stop_id # whatever user's stop ID is
        start_time = user.start_time # whatever user's text time is.
        finish_time = user.finish_time
        minutes_away = user.minutes_away
        text_days = user.days
        print check_time(start_time,finish_time,text_days, now)
        if check_time(start_time,finish_time,text_days, now):
            predictions = check_for_busses(stopID, route_tag, minutes_away)
            if predictions:
                if predictions[0].block == user.bus_tag and predictions[0].minutes<=minutes_away:
                    continue
                else:
                    logging.info("send message to: %r, predictions: %s" %(user.phone_number, predictions) )
                    send_message(message(predictions), user.phone_number)
                user.bus_tag = predictions[0].block
                user.save()

def check_time(start_time, finish_time, text_days, now):
    start_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + start_time, "%Y:%m:%d:%H:%M")
    finish_str = datetime.strptime(str(now.year) + ":" +str(now.month) + ":" +str(now.day) + ":" + finish_time, "%Y:%m:%d:%H:%M")
    if now > start_str and now < finish_str:
        print "now", now, "start_str", start_str, "finish_str", finish_str
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
    for prediction in predictions.predictions:
        if prediction.direction.route.tag == route_tag and x < 3:
            checked_predictions.append(prediction)
            x += 1
    return checked_predictions

def message(predictions):
    list_pred = [str(each.minutes) for each in predictions]
    string_predictions = ', '.join(list_pred)
    title = predictions[0].direction.route.title
    direction = predictions[0].direction.title
    return "The %s line going %s is arriving in %s minutes, to cancel your schedule, reply 'muni'." %(title, direction, string_predictions)

def get_notification(now):
    models.Notification.notification_in_periode(now)

def main(request):
    now = datetime.now()
    list_notif = get_notification(now)
    print list_notif
    


'''
import MuniMobile_app.prediction
import datetime
MuniMobile_app.prediction.main()
MuniMobile_app.prediction.check_time('7:00', '11:00', [1,2,3,4,5,6,7], datetime.datetime.now())
'''



