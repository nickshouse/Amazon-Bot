# Setup browser settings
import os
import shutil
from time import sleep
from random import uniform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Amazon:
    def __init__(self, username, password, url, limit, seleniumdata, textBrowser):
        self.username = username
        self.password = password
        self.url = url
        self.limit = limit
        self.seleniumdata = seleniumdata
        self.textBrowser = textBrowser
        # Paths
        self.localappdata = os.environ.get("LOCALAPPDATA")
        self.chromecookies = self.localappdata + "/Google/Chrome/User Data/Default/Cookies"
        self.seleniumcookies = self.seleniumdata + "/Default"
        self.chromestorage = self.localappdata + "/Google/Chrome/User Data/Default/Local Storage"
        self.seleniumstorage = self.seleniumdata + "/Default/Local Storage"
        # Copy cookies to each instance
        try:
            shutil.copytree(self.chromestorage, self.seleniumstorage)
            shutil.copy(self.chromecookies, self.seleniumcookies)
        except:
            self.log("Please close all non-automated Chrome instances before starting a new automated one.\n")
            raise
        # Chrome installation
        self.browser = webdriver.Chrome(ChromeDriverManager().install(),options = self.chromeOptions())
        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # Assumptions
        self.mobile = True  # Assume mobile safeguard will come up
        self.tfa = True     # Assume 2FA will come up
        self.captcha = True # Assume captcha will come up

        # Flow
        self.fetch()
        self.checkAvailability()
        self.proceedToCheckout()
        #if self.checkSignIn() is False:
        #    self.signIn()
        self.signIn()
        self.placeOrder()

    # Begin and go to url
    def fetch(self):
        self.log("Visiting websites...")
        self.browser.get(self.url)
        self.captchaCheck()

    # Check stock
    def checkAvailability(self):
        self.log("Monitoring webpage for Captcha...")
        self.captchaCheck()
        sleep(uniform(1, 2))
        element = self.browser.find_element_by_class_name("a-color-price").text
        available = False
        self.log("Waiting for available stock...")
        while available is False:
            self.captchaCheck()
            if element == "Currently unavailable.":
                sleep(uniform(5, 15))
                self.browser.refresh()
            else:
                available = True
                self.log("Stock detected!")
                sleep(uniform(1, 2))
                self.priceCheck()

    # Check item price
    def priceCheck(self):
        self.log("Waiting for desired price...")
        try:
            self.elementClick(self.browser.find_element_by_id("buybox-see-all-buying-choices"))
            sleep(uniform(2, 3))
            element = self.browser.find_element_by_class_name("a-price-whole").text
            element = element.replace(",", "")
            want = False
            while want is False:
                self.elementClick(self.browser.find_element_by_id("buybox-see-all-buying-choices"))
                self.captchaCheck()
                if element < self.limit:
                    sleep(uniform(5, 15))
                    self.browser.refresh()
                    sleep(uniform(4, 5))
                else:
                    self.log("Desired price detected!")
                    want = True
                    sleep(uniform(1, 2))
                    self.addToCart()
        except:
            self.log("Could not find buyer's list, running fallback routine...")
            self.priceCheck2()

    def priceCheck2(self):
        sleep(uniform(2, 3))
        element = self.browser.find_element_by_class_name("priceBlockBuyingPriceString").text
        element = element[:len(element) - 2]
        element = element.replace("$", "")
        element = element.replace(",", "")
        element = element.replace(".", "")
        want = False
        while want is False:
            self.captchaCheck()
            if element < self.limit:
                sleep(uniform(5, 15))
                self.browser.refresh()
                sleep(uniform(4, 5))
            else:
                self.log("Desired price detected!")
                want = True
                sleep(uniform(1, 2))
                self.addToCart2()

    # Add to shopping cart
    def addToCart(self):
        self.log("Adding product to cart...")
        sleep(uniform(2, 3))
        self.elementClick(self.browser.find_element_by_id("a-autoid-2"))
        sleep(uniform(2, 3))
        self.protectionPlan()

    def addToCart2(self):
        self.log("Adding product to cart...")
        sleep(uniform(2, 3))
        self.elementClick(self.browser.find_element_by_id("add-to-cart-button"))
        sleep(uniform(2, 3))
        self.protectionPlan()

    # Check if already signed in
    def checkSignIn(self):
        self.log("Checking if signed in...")
        element = self.browser.find_element_by_id("nav-link-accountList-nav-line-1").text
        if element.startswith("Hello, Sign in"):
            self.log("Not signed in...")
            return False
        else:
            self.log("Already signed in...")
            return True

    # Sign in
    def signIn(self):
        # Click sign-in button
        self.log("Signing in...")
       # self.elementClick(self.browser.find_element_by_id("nav-link-accountList-nav-line-1"))
        # Enter email
        self.usernameType(self.browser.find_element_by_xpath("//input[@name='email']"))
        self.elementClick(self.browser.find_element_by_id("continue"))
        # Enter password
        self.passwordType(self.browser.find_element_by_xpath("//input[@name='password']"))
        self.elementClick(self.browser.find_element_by_name("rememberMe"))
        self.elementClick(self.browser.find_element_by_id("signInSubmit"))
        # Check for guards
        self.mobileSafety()
        self._2FACheck()

    # Checkout
    def proceedToCheckout(self):
        self.log("Proceeding to checkout...")
        sleep(uniform(2, 3))
        self.elementClick(self.browser.find_element_by_id("hlb-ptc-btn"))

    # Submit Order
    def placeOrder(self):
        self.elementClick(self.browser.find_element_by_id("submitOrderButtonId"))
        self.log("Item purchased!")
        sleep(60)

######################################################################### HELPER FUNCTIONS
    # Chrome options
    def chromeOptions(self):
        option = webdriver.ChromeOptions()
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_argument("--ignore-certificate-errors") # Is this a safe arguement?
        option.add_argument("window-size=1287,842")
        option.add_argument("--user-data-dir=" + self.seleniumdata)
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")
        return option

    # Type in username
    def usernameType(self, element):
        try:
            sleep(uniform(0.1, 0.2))
            element.click()
            sleep(uniform(0.1, 0.2))
            element.clear()
            for u in self.username:  # Type like a real person
                sleep(uniform(0.1, 0.2))
                element.send_keys(u)
        except:
            self.log("One or more elements is not on this page.\n")

    # Type in password
    def passwordType(self, element):
        try:
            sleep(uniform(0.1, 0.2))
            element.click()
            sleep(uniform(0.1, 0.2))
            element.clear()
            for p in self.password:  # Type like a real person
                sleep(uniform(0.1, 0.2))
                element.send_keys(p)
        except:
            self.log("One or more elements is not on this page.\n")

    # Check for mobile safeguard
    def mobileSafety(self):
        self.log("Checking for Mobile Safeguard popup...")
        while self.mobile is True:
            try:
                mobileS = self.browser.find_element_by_id("ap-account-fixup-phone-skip-link").get_attribute("id")
            except:
                mobileS = ""
            if mobileS == "ap-account-fixup-phone-skip-link":
                self.mobile = True
                self.elementClick(self.browser.find_element_by_id("ap-account-fixup-phone-skip-link"))
            else:
                self.mobile = False

    # Check for two factor authorization
    def _2FACheck(self):
        self.log("Waiting for 2FA if present...")
        while self.tfa is True:
            try:
                sleep(uniform(1, 2))
                _2FA = self.browser.find_element_by_id("channelDetails").get_attribute("id")
            except:
                _2FA = ""
            if _2FA == "channelDetails":
                self.tfa = True
            else:
                self.tfa = False

    # Check for captcha
    def captchaCheck(self):
        while self.captcha is True:
            try:
                sleep(uniform(1, 2))
                cap = self.browser.find_element_by_class_name("a-text-right").text
            except:
                cap = ""
            if cap == "Try different image":
                self.captcha = True
            else:
                self.captcha = False

    # Check for two factor authorization
    def protectionPlan(self):
        self.log("Checking for protection plan popup...")
        try:
            sleep(uniform(1, 2))
            self.elementClick(self.browser.find_element_by_id("attachSiNoCoverage"))
        except:
            self.log("No protection plan popup found...")
            pass

    # Attempt to click element
    def elementClick(self, element):
        try:
            sleep(uniform(0.5, 1))
            element.click()
        except:
            pass

    # Logging
    def log(self, message):
        self.textBrowser.append(message)
        self.textBrowser.ensureCursorVisible()
    ##################################################################### END OF HELPER FUNCTIONS