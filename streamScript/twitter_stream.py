import time
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from header import consumer_key, consumer_secret, access_token, access_token_secret


req_tok_url = 'https://api.twitter.com/oauth/request_token'
oauth_url = 'https://api.twitter.com/oauth/authorize'
acc_tok_url = 'https://api.twitter.com/oauth/access_token'


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self):

        self.hashtags_count = 0
        self.data_count = 0
        self.location_count = 0
        self.seattle_count = 0
        self.count = 0
        self.start_time = time.clock()

    def on_data(self, data):

        json_data = json.loads(data)
        text = json_data.get('text', None)
        try:
            hashtags = [i['text'] for i in json_data.get('entities', None).get('hashtags', None)]
        except AttributeError:
            print "I HAD THIS ERROR"
            return
        created_at = json_data.get('created_at', None)
        screen_name = json_data.get('user', None).get('screen_name', None)
        location = json_data.get('geo', None)
        if location:
            _location = location.get('coordinates', None)
            self.location_count += 1
        language = json_data.get('lang', None)

        place = json_data.get('place', None)
        if place:
            country_code = place.get('country_code', None)

        if location and (language == 'en') and country_code:
            self.count += 1
            end_time = time.clock()
            #print json_data
            print "Twitter Name: ", screen_name
            print "Language: ", language
            print "Hashtags: ", hashtags
            print "Text: ", text
            print "Time: ", created_at
            print "Location: ", _location
            print "Country code: ", country_code

            with open("output.txt", "a") as myfile:
                myfile.write("Twitter Name: {}\n".format(screen_name))
                # myfile.write("Language: {}\n".format(language))
                # myfile.write("Hashtags: {}\n".format(hashtags))
                # myfile.write("Text: {}\n".format(text))
                # myfile.write("Time: {}\n".format(created_at))
                # myfile.write("Time Zone: {}\n".format(t_zone))
                # myfile.write("Place name: {}\n".format(place_name))
                # myfile.write("Country code: {}\n".format(country_code))
                # myfile.write("Bounding box: {}\n".format(bounding_box))
                # myfile.write("***************************************************\n")
            print "*" * 20
            time_elapsed = (end_time - self.start_time)
            print time_elapsed
            if time_elapsed >= 1.0:
                print "*" * 10
                print "*" * 10
                print self.count, " tweets in ", time_elapsed, " seconds!"
                print "*" * 10
                print "*" * 10

    def on_error(self, status):
        error_counter = 0
        if status == 420:
            time.sleep(15)
            print "Made too many requests!"
            with open("output.txt", "a") as myfile:
                myfile.write("Made too many requests!")
                myfile.write("\n")
            print '*' * 20
            error_counter += 1
            print "Errors: ", error_counter

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(locations=[-124.848974, 24.396308, -66.885444, 49.384358])
