"""
    Periodically favorites tweets related to a search topic. 
"""

import os
import time
import urllib
import logging
import yaml
from splinter import Browser

logging.basicConfig(level=logging.INFO)

def twitter_login(username, password):
    """
    Log in to Twitter and returns browser object
    """

    browser = Browser()

    # Login
    browser.visit("https://www.twitter.com/")
    browser.find_by_id("signin-email").first.value = username
    browser.find_by_id("signin-password").first.value = password
    browser.find_by_css(".js-submit").first.click()

    return browser

def main():
    """
    Start the favoriting loop
    """

    logging.info("Opening configuration file")
    config = yaml.load(open(os.path.expanduser("~/favorbot.yml"), 'r'))

    logging.info("Logging into Twitter")
    browser = twitter_login(config['username'], config['password'])
    
    iteration = 0
    while True:
    
        logging.info("Starting iteration %s" % iteration)
        
        browser.visit("https://twitter.com/search/realtime?q="+urllib.quote(config['query']))
        
        time.sleep(2)
        
        # scroll to bottom
        for i in range(0,2):
            browser.execute_script("var body = document.body, html = document.documentElement; var height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight ); window.scrollTo(0,height);")
            time.sleep(1)
    
        logging.info("Favoriting %s tweets" % config['num_favorite'])
        tweets = browser.find_by_css(".tweet")
        for i, tweet in enumerate(tweets):
            try:
                tweet.click()
                tweet.find_by_css(".favorite").first.click()
            except:
                continue

            if i >= config['num_favorite']:
                break
    
        time.sleep(config['wait_period'])

        iteration += 1

if __name__ == "__main__":
    main()