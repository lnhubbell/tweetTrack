import time
import lettuce
from selenium import webdriver
from tweetTrack.app import app


@lettuce.before.all
def get_driver():
    site_url = 'localhost:5000'
    driver = webdriver.Firefox()
    driver.get(site_url)
    lettuce.world.map_center = driver.execute_script(
        """
        return map.getCenter();
        """
    )
    lettuce.world.driver = driver


@lettuce.after.each_scenario
def close_modals(scenario):
    driver = lettuce.world.driver
    driver.execute_script(
        """
        $("#about-modal").modal("hide");
        $("#contact-modal").modal("hide");
        $("#twitter-modal").modal("hide");
        """
    )
    time.sleep(3)

@lettuce.after.each_step
def wait(step):
    time.sleep(1)

@lettuce.after.each_feature
def close_driver(feature):
    driver = lettuce.world.driver
    driver.close()


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


@lettuce.step('And a name')
def a_name(step):
    lettuce.world.name = 'Ian'


@lettuce.step('And an email')
def a_name(step):
    lettuce.world.email = 'tester@gmail.com'


@lettuce.step('And a subject')
def a_name(step):
    lettuce.world.subject = 'BDD Testing With Selenium'


@lettuce.step('And a message')
def a_message(step):
    lettuce.world.message = 'This is only a test'


@lettuce.step('I fill out the contact form')
def fill_out_contact_form(step):
    time.sleep(2)
    driver = lettuce.world.driver
    driver.find_element_by_id('contact').click()
    time.sleep(2)
    name_field = driver.find_element_by_id('name')
    name_field.send_keys(lettuce.world.name)
    email_field = driver.find_element_by_id('email')
    email_field.send_keys(lettuce.world.email)
    subject_field = driver.find_element_by_id('subject')
    subject_field.send_keys(lettuce.world.subject)
    message_field = driver.find_element_by_id('message')
    message_field.send_keys(lettuce.world.message)


@lettuce.step('I click the send button')
def click_send(step):
    driver = lettuce.world.driver
    driver.find_element_by_id('send').click()


@lettuce.step('I receive a response')
def receive_response(step):
    driver = lettuce.world.driver
    resp = driver.find_element_by_id('contact-modal-body')
    assert 'Thanks for the message Ian' in resp.text


@lettuce.step('I click the about button')
def the_contact_button(step):
    driver = lettuce.world.driver
    driver.find_element_by_id('about').click()


@lettuce.step('Then I see the about section')
def the_contact_form(step):
    driver = lettuce.world.driver
    assert driver.find_element_by_id('about-modal-body').is_displayed()


@lettuce.step('I click the track me button')
def the_contact_button(step):
    driver = lettuce.world.driver
    driver.find_element_by_id('track').click()


@lettuce.step('Then I see the track me form')
def the_contact_form(step):
    driver = lettuce.world.driver
    assert driver.find_element_by_id('twitter-form').is_displayed()


@lettuce.step('a twitter handle')
def a_twitter_handle(step):
    lettuce.world.screen_name = 'a_Twitter_User'


@lettuce.step('I fill out the twitter form')
def fill_out_tiwitter_form(step):
    time.sleep(2)
    driver = lettuce.world.driver
    driver.find_element_by_id('track').click()
    time.sleep(2)
    screen_name_field = driver.find_element_by_id('screen_name')
    screen_name_field.send_keys(lettuce.world.screen_name)


@lettuce.step('I click the submit button')
def click_send(step):
    driver = lettuce.world.driver
    driver.find_element_by_id('submit').click()


@lettuce.step('I see a new location on the map')
def new_location(step):
    driver = lettuce.world.driver
    center = driver.execute_script(
        """
        return map.getCenter();
        """
    )
    assert center != lettuce.world.map_center
