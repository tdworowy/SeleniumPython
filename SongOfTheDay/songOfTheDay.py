import calendar
import datetime
import os
import random
import time
from datetime import date

from selenium import webdriver

from SkypeBot.skypeBot import skypeBot
from SongOfTheDay.Songs import updateSongs
from Utils.utils import log
from chromedriverFolder.driverPath import getDriverPath


class songOfTheDay():
    def __init__(self):
        self.setUp()

    def mesageByTime(self):
        now = datetime.datetime.now()
        today7 = now.replace(hour=7, minute=0, second=0, microsecond=0)
        today16 = now.replace(hour=16, minute=0, second=0, microsecond=0)
        today20 = now.replace(hour=20, minute=0, second=0, microsecond=0)
        dateToday = date.today()
        print("Today is: ",calendar.day_name[dateToday.weekday()]," ",date.today())
        if dateToday.month == 12:
            if dateToday.day == 24: return "Piosenka na wigilie[Auto]"
            if dateToday.day == 25: return "Piosenka na pierwszy dzień świąt bożego narodzenia[Auto]"
            if dateToday.day == 26: return "Piosenka na drugi dzień świąt bożego narodzenia[Auto]"
            if dateToday.day == 31: return "Piosenka na Sylwestra ![Auto]"
        if dateToday.month == 1 and dateToday.day == 1:return "Piosenka na nowy rok ![Auto]"
        if calendar.day_name[dateToday.weekday()] is "Saturday" : return"Piosenka na sobote[Auto]"
        if calendar.day_name[dateToday.weekday()] is "Sunday": return"Piosenka na niedziele[Auto]"
        if today7 <= now <= today16 : return  "Piosenka dnia[Auto]"
        if today16 <  now <= today20: return "Piosenka na wieczór[Auto]"
        if  now > today20: return "Piosenka na noc[Auto]"



    def findSong(self, song):
        self.driver.get('https://www.youtube.com')
        input = self.driver.find_element_by_id("masthead-search-term")
        searchButton = self.driver.find_element_by_css_selector("button[type='submit']")
        input.click()
        input.send_keys(song)
        searchButton.click()
        time.sleep(2)
        firstResoult = self.driver.find_element_by_css_selector("h3 a")
        firstResoult.click()
        time.sleep(1)

        return self.driver.current_url

    def sentSong(self, autentycation, songURL):
        #self.skypeBot.loginFacebook(autentycation)
        self.skypeBot.login(autentycation)

        self.skypeBot.select("Echo")
        self.skypeBot.select("A smiechom i szopom nie było konca")
        log(self.mesageByTime())
        log(songURL)
        self.skypeBot.sendMessageToSelected(self.mesageByTime())
        self.skypeBot.sendMessageToSelected(songURL)

    def setUp(self):
        updateSongs()
        chromeDriverPath =getDriverPath()+'\\chromedriver.exe'
        self.driver = webdriver.Chrome(chromeDriverPath)
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)
        self.skypeBot = skypeBot(self.driver)
        #Songs.getSongs() #it takes lot of time

    def tearDown(self):
        self.driver.quit()



def main(login, password):
    try:

        song = songOfTheDay()
        f = open(os.path.dirname(os.path.abspath(__file__))+'\\file.txt', 'r')
        log("Get random song")
        songsList = f.read();
        songsList=songsList.split("\n")
        autentycation = [login, password]

        ran= random.randrange(len(songsList))
        log(songsList[ran])
        url = song.findSong(songsList[ran].strip())
        song.sentSong(autentycation, url)
        #song.sentSong(autentycation, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        song.tearDown()

    except Exception  as err:
        log(str(err))

    finally:
        quit()



if __name__ == '__main__':
    # var1 = input("Login: ")
    #var2 = input("Pass: ")
   f= open(os.path.dirname(os.path.abspath(__file__))+'\\aut.txt')
   main(f.readline().strip(), f.readline().strip())

