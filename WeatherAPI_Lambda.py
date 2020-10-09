from botocore.vendored import requests

import time
import os
import logging

# from datetime import datetime


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



def get_weather_forecast(intent_request):
    
    try:
        location = intent_request['currentIntent']['slots']['city']
    except KeyError:
        location = intent_request['currentIntent']['slots']['City']

    source = intent_request['invocationSource']
    slots = intent_request['currentIntent']['slots']

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


    if source == 'DialogCodeHook':
        if slots['city'] is None:
            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                'city',
                {
                    'contentType':'PlainText',
                    'content':'Please enter city or country name to get weather informations about (or you can enter lattitude and longitude of location respectively)'
                }
            )
        return delegate(session_attributes, slots)
        

    if source == 'FulfillmentCodeHook':
        response = ""
    
        current_weather = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(location, OWM_API_KEY)).json()
    
        response += "Current weather condition in %s:  %s," % (intent_request['currentIntent']['slots']['city'],
            current_weather['weather'][0]['main']) + "\n Temperature {:.2f} degree celsius, \n Winds {} mph, \n Pressure level {} millibars, \n Humidity {}%".format(
            current_weather['main']['temp'] - 273.15,
            current_weather['wind']['speed'],
            current_weather['main']['pressure'],
            current_weather['main']['humidity']
        )
        
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': response
            }
        )
            
            
def get_weather_now(intent_request):
    source = intent_request['invocationSource']
    slots = intent_request['currentIntent']['slots']
    
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if source == 'DialogCodeHook':
        if slots['lat'] is None or slots['lon'] is None:
            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                'city',
                {
                    'contentType':'PlainText',
                    'content':'Please enter lattitude and longitude respectively'
                }
            )
            
        elif ('-90' > slots['lat'] > '90') or ('-180' > slots['lon'] > '180'):
            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                'lon',
                {
                    'contentType':'PlainText',
                    'content':'Lattitude or Longitude value invalid. lat(-90 to 90), lon(-180 to 180)'
                }
            )
        
        
    if source == 'FulfillmentCodeHook':
        lattitude = intent_request['currentIntent']['slots']['lat']
        longitude = intent_request['currentIntent']['slots']['lon']
        
        response = ""
    
        current_weather = requests.get("http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,alerts,minutely,current&appid={}".format(lattitude, longitude, OWM_API_KEY)).json()
    
        # current_date = ""
    
        # date_list = []
        # for i in range(len(current_weather['daily'])):
        #     date_list = datetime.fromtimestamp(current_weather['daily'][i]['dt'])
            
        
        # for item in current_weather['daily']:
        #     date = datetime.fromtimestamp(dt[item])
            
    
        response += "Weather forecast for tomorrow in location coordinates %s and %s:--- " % (intent_request['currentIntent']['slots']['lat'],
            intent_request['currentIntent']['slots']['lon'])  + " \n Temperature: {:.2f} degree celsius,\n Winds: {} mph,\n Pressure level: {} millibars, \n Humidity: {}% ".format(
            # current_weather['daily'][0]['weather'][0]['main'],
            current_weather['daily'][1]['temp']['day'] - 273.15,
            current_weather['daily'][1]['wind_speed'],
            current_weather['daily'][1]['pressure'],
            current_weather['daily'][1]['humidity']
        )
            
        
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
        return get_weather_forecast(intent_request)
        
    elif intent_name == 'WeatherNow':
        return get_weather_now(intent_request)
    
    raise Exception('Intent with name ' + intent_name + ' not supported')




def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)

