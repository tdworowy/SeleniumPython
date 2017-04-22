import time

from Calculator.Elements.Calculator import CalculatorElements
from behave import *
from chromedriverFolder.driverPath import getDriverPath
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

server = 'http://www.calculator.net/'

class calculatorBDD:



    @given('Set up')
    def SetUp(self):
            self.remote = False
            if (self.remote):
                # self.driver = WebDriver("http://localhost:4444/wd/hub", "chrome", "ANY")
                self.driver = WebDriver("http://localhost:4444", DesiredCapabilities.CHROME)
            else:
                chromeDriverPath = getDriverPath() + '\\chromedriver.exe'
                self.driver = webdriver.Chrome(chromeDriverPath)
            self.driver.get(server)
            self.calculator = CalculatorElements(self.driver)
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)

    @when('open calculator')
    def openCalculator(self):
        self.calculator.openCalculator()
        time.sleep(1)
    @then('check calculator')
    def checkifCalculatorIsDisplayed(self):
        assert (self.calculator.scientificCalculatorCheck()) is True