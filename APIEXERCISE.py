import tweepy
from tweepy import OAuthHandler
import json
import wget

import os
from base64 import b64encode
from os import makedirs
from os.path import join,basename
from sys import argv
import requests

import io
from PIL import Image, ImageDraw, ImageFont

from google.cloud import vision
from google.cloud.vision import types



twitterusername = input('Enter the twitter username handle: ')

consumer_key = 'NFDMpk1Fg8ceijtkGERJc2Z2a'
consumer_secret = '8tvTg2rnY53XzSdrpKFcZruVOSJSHWPdutwMRg6U8XddoqPx3y'
access_token = '956294196301791233-tzh1DeLpyEh3i7sVinidNTzUK7A6pRy'
access_secret = 'DCavGa4IkSQDviwhFimXzqYu2gELIQU6F5DtqErberFlT'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = api.user_timeline(screen_name=twitterusername,
                           count=200, include_rts=False,
                           exclude_replies=True)
last_id = tweets[-1].id
 
while (True):
    more_tweets = api.user_timeline(screen_name=twitterusername,
                                count=200,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)
# There are no more tweets
    if (len(more_tweets) == 0):
          break
    else:
        last_id = more_tweets[-1].id-1
        tweets = tweets + more_tweets



media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if(len(media) > 0):
        media_files.add(media[0]['media_url'])


counter = -1;


for media_file in media_files:
    if counter <200:
        counter = counter +1 
        location = '/Users/apapadak/Desktop/EC500' + str(counter) + '.jpg'
    #if (counter < 10):
        wget.download(media_file, location)

      #  counter = counter + 1



counter2=0

client = vision.ImageAnnotatorClient()    #line of code given by Google Vision API

for num in range(0, counter+1):
    counter2 = counter2 + num
    filename = str(counter2) + '.jpg'
    path = os.getcwd()
    with io.open(path + '/' + filename, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content = content)
    
    response = client.label_detection(image = image)

    labels = response.label_annotations

    new = 'new' + str(counter2)+'.jpg'
    image = Image.open(filename)

    drawing = ImageDraw.Draw(image)
    yplace = 80;
    for item in labels:
        text = item.description

        yplace = yplace+10
        drawing.text((20, yplace), text = text, fill = (0,0,0))
        #print(text) error checking


    image.save(new)
    rmcommand = 'rm ' + filename
    print(rmcommand)
    os.system(rmcommand)



#making the final video
os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' output.mp4")















