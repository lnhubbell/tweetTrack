import time
import lettuce
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import url_for
from tweetTrack.app import app


@lettuce.before.all
def get_driver():
    site_url = 'localhost:5000'
    driver = webdriver.Firefox()
    driver.get(site_url)
    time.sleep(1)
    driver.execute_script('$("#about-modal").modal("hide");')
    time.sleep(2)
    lettuce.world.driver = driver


@lettuce.step('a user')
def a_user(step):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['logged_in'] = False
        lettuce.world.client = client


@lettuce.step('I click the Contact button')
def the_contact_button(step):
    driver = lettuce.world.driver
    driver.find_element_by_id('contact').click()


@lettuce.step('I see the Contact Form')
def the_contact_form(step):
    driver = lettuce.world.driver
    assert driver.find_element_by_id('contact-form').is_displayed()