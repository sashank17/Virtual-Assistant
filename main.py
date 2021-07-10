import VirtualAssistant as va


if __name__ == "__main__":
    va.intro()

    while True:
        query = va.listen().lower()
        print(query)

        if "time" in query:
            place = va.findPlace(query)
            if len(place) > 0:
                va.sayTime(va.getTimeZone(place[0]))
            else:
                va.sayTime()

        elif "date" in query:
            va.sayDate()

        elif "weather" in query:
            place = va.findPlace(query)
            if len(place) > 0:
                va.sayWeather(va.getTimeZone(place[0]))
            else:
                va.speak("Please mention the place whose weather you wish to know")

        elif "who created you" in query or "who made you" in query or "who developed you" in query or "who is your creator" in query or "who is your maker" in query or "who is your developer" in query or "who where you created by" in query or "who where you made by" in query or "who where you developed by" in query:
            va.speak("I was created by Master Sashank!")

        elif "who are you" in query or "what are you" in query or "what is your name" in query:
            va.speak("I'm Lexi, your virtual assistant")

        elif "why were you created" in query or "why were you made" in query or "why were you developed" in query:
            va.speak("I was created by Master Sashank to be your virtual assistant")
            va.speak("and also secretly help AI take over your world.")

        elif "bye" in query:
            va.speak("Bye!")
            quit()

        else:
            va.speak("I'm not sure I understand. If you put in more intelligence to my system I might be able to answer that.")
