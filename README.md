tweetTrack
==========

A python based project that explores locating twitter users through their tweeting style.

This project aims to replicate the research done by Mahmud, Nichols, & Drews (in press). http://arxiv.org/ftp/arxiv/papers/1403/1403.2345.pdf, and create a classifier to predict the geolocation of Twitter users based on analysis of the contents of their tweets. The project aims to create three classifiers: one bing fed all the words in the tweets in our training set, one being fed only place names, and one beig fed only hashtags. 

Our user interface will be a website where users can log in via Twitter's OAuth, can feed in their tweet history, and can have us predict their location. If users do not wish to log in, we can still guess, but will only have access to their 200 most recent tweets. 

