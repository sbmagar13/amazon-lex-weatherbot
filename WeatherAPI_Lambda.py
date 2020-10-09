from botocore.vendored import requests

import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

OWM_API_KEY = "d9c63d9f66edfc2c2b3a87d5abf9f64e"


def build_response(message):
    return {
        "dialogAction":{
            "type":"Close",
            "fulfillmentState":"Fulfilled",
            "message":{
                "contentType":"PlainText",
                "content": message
            }
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }



def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def try_ex(func):
    try:
        return func()
    except KeyError:
        return None



def get_weather(intent_request):
    try:
        location = intent_request['currentIntent']['slots']['city']
    except KeyError:
        location = intent_request['currentIntent']['slots']['City']

    # source = intent_request['invocationSource']
    # slots = intent_request['currentIntent']['slots']

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


#     if source == 'DialogCodeHook':
#         if slots['city'] is None:
#             return elicit_slot(
#                 intent_request['currentIntent']['name'],
#                 slots,
#                 'city',
#                 'Please enter city name'
#             )
#         return delegate(session_attributes, slots)
#
#     if source == 'FulfillmentCodeHook':
#         result = weather_api_call(OWM_API_KEY, slots['city'])
#         return build_response(result)
#
#
# def weather_api_call(OWM_API_KEY, location):
#     url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(slots['city'], OWM_API_KEY)
#     r = requests.get(url)
#     return r.json()


    # complete_location = requests.get("api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + OWM_API_KEY)

    response = ""

    # Add Current Conditions to Response
    current_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(location, OWM_API_KEY)).json()

    response += "Currently in %s, it is %.1f degrees fahrenheit, with winds %s. " % (
        intent_request['currentIntent']['slots']['city'],
        current_weather['main']['temp_min'],
        current_weather['wind']['speed']
    )

    # Add Forecast to Response
    # forecast = requests.get("http://api.wunderground.com/api/%s/forecast/%s.json" % (
    #     OWM_API_KEY,
    #     location_quick_link
    # )).json()
    #
    # response += "The forecast for today from openweathermap has %s" % forecast['forecast']['txt_forecast']['forecastday'][0]['fcttext']


    # Submit Response back to Lex

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': response
        }
    )


def dispatch(intent_request):
    # logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'WeatherForecast':
        return get_weather(intent_request)
        raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
