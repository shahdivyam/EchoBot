import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


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

    def post(self, request, *args, **kwargs):
        message = json.loads(self.request.body.encode('utf-8'))

        for entry in message['entry']:
            for msg in entry['messaging']:
                print msg['message']['text']
                reply_to_message(msg['sender']['id'], msg['message']['text'])

        return HttpResponse("None")


def reply_to_message(user_id, message):
    access_token = 'EAACUZB4KE1ZBoBAC9hFsUdDjBpUCQWaI7teZCE0Y9ABhSEpvShAfKpZAndOe3Qt2WUxArYAF6n53k1g8drAHGsZBYGkq39mF6uYCFqRbKUZAprQk1ZApBWWFIqG2LcbN3wUqrgB2e9rNRthxtmNJbOJj5c5P20siDh1QDnPsLRxGAZDZD'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token

    resp = generate_response(message)
    send_resp = {"recipient": {"id": user_id}, "message": {"text": resp}}
    response_msg = json.dumps(send_resp)
    status = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    print status.json()


def generate_response(msg):
    return "Welcome to Coding Blocks :)"


