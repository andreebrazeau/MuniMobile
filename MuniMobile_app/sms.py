from twilio.rest import TwilioRestClient
import twilio_token

account = twilio_token.account
token = twilio_token.token
client = TwilioRestClient(account, token)

def receive_sms(request):
    body = request.GET.get('Body', None)
    from_number = request.GET.get('From', None)
    if body and 'muni' in string.lower(body):
        for user in Notification.objects.filter(phone_number=from_number[2:]):
            user.activated = False
            user.save()
        # response doesn't work now, so use send_message() instead of this
        # resp = twilio.twiml.Response()
        # resp.sms("MuniMobile, we've removed all your scheduled SMS request. \
        #   To schedule more request, visite our website.")
        message = "MuniMobile, we've removed all your scheduled SMS request. To schedule more request, visite our website."
        send_message(message, from_number)
    return None

def send_sms(message):
    def send_message(message, phone_number):
    print message
    message = client.sms.messages.create(to=phone_number, from_="+16502314762", body=message)