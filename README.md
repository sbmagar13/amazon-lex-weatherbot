# amazon-lex-weatherbot
""" An weather forecast and information chatbot, Created with AWS Lex and AWS lambda"""

## **_`About Lex BOT`_**

   AWS Lex projects have three objects:
    
    Bot
    Intents
    Slots
    
 The intent is what the user asks for, and will be executed whenever the intent is selected by the NLU module and all required slots are filled up. Intents are defined by a set of sample sentences, which are used to train the model, and slots. The sentences should be defined in such a way that they contain slots.

For example, if we have a slot type City, then one of our sentences could be Show me the weather in {city}. Now, the underlying ML uses this combination of sentences and slot types to train the model.

Slots are used to fetch the parameters required by the intent to fulfill the user request. There are two types of slots: the predefined and the custom ones. Amazon Lex supports built-in slot types from the Alexa Skills Kit.


## **`My Demo App`**

 The demo application I wrote is in Python and made use of Lambda for the state management, conditions, decision trees and the like. Lex expects the Lambda function to receive a JSON payload. Subsequently the Lambda function needs to return a JSON payload to Lex. The connection can be tested via the text console and the JSON payload is visible during testing.
 
 I have created two intents: **1) WeatherNow, 2) WeatherForecast**.
 One for current weather condition of different cities input by user, and second one is for forecast data of weather. 
 
 In this demo I used OpenWeatherMap's API for weather data. Since only Lattitude and Longitude values are supported for forecasting weather(free members), I have used lattitude and longitude values as slots in lex for forecasting weather, While City name or location name is used for current(today's) weather informations.
 
 I used aws' built-in confirmation prompt features. Single "Lambda function" source code is used for fulfillment response plus initialization and validation of one of the intents.
 
 
 For slots: city is defined with built-in 'AMAZON.AT_CITIES' slot type to match the city the user is asking about, and both lat and long are defined with built-in 'AMAZON.NUMBER'.
 
 
 
 
 