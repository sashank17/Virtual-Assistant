from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import SpeechSynthesizer, SpeechRecognizer, SpeechConfig
from datetime import datetime
from geopy import AzureMaps, Nominatim
from timezonefinder import TimezoneFinder
import pyttsx3
import pytz
import geograpy3
import requests


engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

voiceRate = 180
engine.setProperty('rate', voiceRate)

speech_config = SpeechConfig(subscription="YOUR-SUBSCRIPTION KEY", region="centralindia")
SUBSCRIPTION_KEY = "YOUR-AZURE-MAPS-SUBSCRIPTION-KEY"


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# def speak(audio):
#     audio_config = AudioOutputConfig(use_default_speaker=True)
#     synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
#     synthesizer.speak_text_async(audio)


def listen():
    # speech_config.speech_recognition_language = "hi-IN"
    speech_recognizer = SpeechRecognizer(speech_config=speech_config)
    print("Listening...")
    result = speech_recognizer.recognize_once_async().get()
    return result.text


def intro():
    speak("Hi, I'm Lexi, your virtual assistant")
    greet()
    speak("How may I help you?")


def greet():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")


def timedate(tzone=None):
    hours = datetime.now(tzone).strftime("%#H")
    mins = datetime.now(tzone).strftime("%#M")
    sec = datetime.now(tzone).strftime("%#S")
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%B")
    date = datetime.now().strftime("%d")
    if 4 <= int(date) <= 20 or 24 <= int(date) <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][int(date) % 10 - 1]
    day = datetime.now().strftime("%A")

    return [year, month, date, suffix, day, hours, mins, sec]


def getLocation(place):
    geolocator = Nominatim(user_agent="VirtualAI")
    # geolocator = AzureMaps(subscription_key=SUBSCRIPTION_KEY)
    return geolocator.geocode(place)


def getTimeZone(place):
    location = getLocation(place)
    tz = TimezoneFinder().timezone_at(lng=location.longitude, lat=location.latitude)
    return pytz.timezone(tz)


def findPlace(text):
    places = geograpy3.get_place_context(text=text.title())
    city = places.cities
    region = places.regions
    country = places.countries
    others = places.other

    return country


def sayTime(place):
    timeList = timedate(place)
    speak("It's " + timeList[5] + " hours and " + timeList[6] + " minutes")


def sayDate():
    dateList = timedate()
    speak("It's " + dateList[4] + " the " + dateList[2] + dateList[3] + " of " + dateList[1] + " " + dateList[0])


def getWeatherInfo(place):
    location = getLocation(place)
    query = '{},{}'.format(location.latitude, location.longitude)
    resp = requests.get('https://atlas.microsoft.com/weather/forecast/hourly/json?subscription-key={}&api-version=1.0&query={}&duration=1'.format(SUBSCRIPTION_KEY, query))
    return resp.json()['forecasts'][0]


    # resp = requests.get('https://atlas.microsoft.com/weather/forecast/hourly/json?subscription-key={}&api-version=1.0&query={}&duration=1'.format(SUBSCRIPTION_KEY, query))
    # # resp = requests.get('https://atlas.microsoft.com/weather/currentConditions/json?subscription-key={}&api-version=1.0&query={}'.format(SUBSCRIPTION_KEY, query))
    # for items in resp.json()['forecasts']:
    #     # print(items)
    #     for key, value in items.items():
    #         print(key, "-", value)


def sayWeather(place=None):
    data = getWeatherInfo(place)
    speak("It's " + data['iconPhrase'] + " with a temperature of " + str(round(data['temperature']['value'])) + " degree Celsius.")
    if data['rainProbability'] and data['snowProbability']:
        speak("Expect rain and snow in the coming hours.")
    elif data['rainProbability']:
        speak("Expect rain in the coming hours.")
    elif data['snowProbability']:
        speak("Expect snowfall in the coming hours.")
