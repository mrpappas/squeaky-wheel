import datetime
import json
import time
import tweepy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Config(object):

    with open("config.json", "r") as j:
        config = json.load(j)

        # set download, upload, isp, twitter api data, and other defaults in config.json

        download = float(config["bandwidth"]["download"])
        upload = float(config["bandwidth"]["upload"])
        margin = float(config["margin"])
        isp = config["isp"]

        twitter_token = config["twitter"]["twitter_token"]
        twitter_token_secret = config["twitter"]["twitter_token_secret"]
        twitter_consomer_key = config["twitter"]["twitter_consumer_key"]
        twitter_consumer_secret = config["twitter"]["twitter_consumer_secret"]

        log = config["log"]["name"]

        date = ("Data logged: {:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))

        def get_download(self):
            return self.download

        def get_upload(self):
            return self.upload

        def get_margin(self):
            return self.margin

        def get_isp(self):
            return self.isp


class Log(object):

    config = Config()

    def write_to_log(self, input):
        with open(self.config.log, "a") as f:
            f.write(input)


class SpeedTest(object):

    download = ""
    upload = ""
    latency = ""
    jitter = ""
    log = Log()

    def init_driver(self):
        driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 5)
        return driver

    def run_test(self, driver):

        driver.get("https://www.measurementlab.net/p/ndt-ws.html")

        try:
            button = driver.wait.until(EC.element_to_be_clickable(
                (By.ID, "start-button")))
            button.click()

        except TimeoutException:
            self.log.write_to_log("-- Button not found --")

    def get_data(self):

        try:
            self.upload = str(driver.find_element_by_id("upload-speed").text)
        except TimeoutException:
            self.log.write_to_log("-- upload not found --")

        try:
            self.download = str(driver.find_element_by_id("download-speed").text)
        except TimeoutException:
            self.log.write_to_log("-- download not found --")

        try:
            self.latency = driver.find_element_by_id("latency").text
        except TimeoutException:
            self.log.write_to_log("-- latency not found --")

        try:
            self.jitter = driver.find_element_by_id("jitter").text
        except TimeoutException:
            self.log.write_to_log("-- jitter not found --")


class Twitter(object):

    log = Log()
    config = Config()

    auth = tweepy.OAuthHandler(config.twitter_consomer_key,
                               config.twitter_consumer_secret)
    auth.set_access_token(config.twitter_token,
                          config.twitter_token_secret)

    try:
        api = tweepy.API(auth)
    except:
        self.log.write_to_log("-- " + config.date + " --\n"
                              "Twitter Auth failed \n"
                              "-------------------- \n")

    def test_results(self):

        config = self.config
        config_download = config.get_download()
        config_upload = config.get_upload()
        margin = config.get_margin()
        isp = config.get_isp()

        speedtest_download = speedtest.download
        speedtest_upload = speedtest.upload

        if (float(speedtest_download) < config_download * margin or
                float(speedtest_upload) < config_upload * margin):

                try:

                    self.api.update_status(isp + " Hey what gives!  I pay for " +
                                           str(config_download) + " Mbps download and " +
                                           str(config_upload) + " Mbps upload. Why am I only getting " +
                                           speedtest_download + " Mbps down and " +
                                           speedtest_upload + " Mbps up?")

                    self.log.write_to_log("-- " + config.date + " --\n"
                                          "- ERROR: Bandwidth not in spec - \n"
                                          "Download: " + speedtest_download + " Mbps \n"
                                          "Upload: " + speedtest_upload + " Mbps \n"
                                          "Latency: " + speedtest.latency + " msec round trip time \n"
                                          "Jitter: " + speedtest.jitter + " msec \n"
                                          "-------------------- \n")

                except:
                    self.log.write_to_log("-- " + config.date + " --\n"
                                          "Twitter post / logging failed \n"
                                          "-------------------- \n")

        else:
            self.log.write_to_log("-- " + config.date + " --\n"
                                  "- Bandwidth in spec - \n"
                                  "Download: " + speedtest_download + " Mbps \n"
                                  "Upload: " + speedtest_upload + " Mbps \n"
                                  "Latency: " + speedtest.latency + " msec round trip time \n"
                                  "Jitter: " + speedtest.jitter + " msec \n"
                                  "-------------------- \n")


if __name__ == "__main__":
    speedtest = SpeedTest()
    driver = speedtest.init_driver()
    speedtest.run_test(driver)
    # instead of sleep could set a driver.wait
    time.sleep(35)
    speedtest.get_data()
    driver.quit()
    twitter = Twitter()
    twitter.test_results()
