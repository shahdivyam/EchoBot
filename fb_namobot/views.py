import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

# NamoBotView class inheriting from generic.View class
class NamoBotView(generic.View):
    def get(self, request, *args, **kwargs):
        print self.request.GET
        if self.request.GET.get('hub.verify_token') == '123456789':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)
                    reply_to_message(message['sender']['id'], message['message']['text'])

def reply_to_message(user_id, message):
    access_token = 'EAACUZB4KE1ZBoBABUCxM3kAZCeOkyTBKnpxhff03zuLhLrStImIcZALaMifUwQrWDqCc02QiHZCTKCDfs9rShZACw1wy3ZAg3kicyzueVfMahNQlhYkXZCW4pSFz8ZBGIWe9pKLxQK8GIlFhdhInf9YY7QJdWFF1ZAAcFT3HZBVVzYa7QZDZD'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

    resp = generate_response(message)
    send_resp = {"recipient": {"id": user_id}, "message": {"text": resp}}
    response_msg = json.dumps(send_resp)
    status = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    print status.json()


def generate_response(msg):
    return msg


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+'EAACUZB4KE1ZBoBABUCxM3kAZCeOkyTBKnpxhff03zuLhLrStImIcZALaMifUwQrWDqCc02QiHZCTKCDfs9rShZACw1wy3ZAg3kicyzueVfMahNQlhYkXZCW4pSFz8ZBGIWe9pKLxQK8GIlFhdhInf9YY7QJdWFF1ZAAcFT3HZBVVzYa7QZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print status.json()
