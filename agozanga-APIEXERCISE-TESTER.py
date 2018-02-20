from google.cloud import vision
import io, os
import tweepy
import wget
import glob
import time

def module(twitter_handle, number_tweets):

    # Twitter
    #----------------------------------------------------------------------------------------------------# 

    # Consumer Information
    consumer_key = 'NFDMpk1Fg8ceijtkGERJc2Z2a'
    consumer_secret = '8tvTg2rnY53XzSdrpKFcZruVOSJSHWPdutwMRg6U8XddoqPx3y'
    access_token = '956294196301791233-tzh1DeLpyEh3i7sVinidNTzUK7A6pRy'
    access_secret = 'DCavGa4IkSQDviwhFimXzqYu2gELIQU6F5DtqErberFlT'
    # Authorization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    DIRECTORY = os.getcwd()

    # Checking if there is already an output movie file
    os.system('rm output.mp4')
    

    # Gathering twitter data
    try:
        tweets = api.user_timeline(screen_name=twitter_handle,          # Gather first set of tweets
                               count=number_tweets, include_rts=False,
                               exclude_replies=True)
    except:
        print('The given username does not exist. \n')
        return 0

    max_id = tweets[-1].id


    # Traversing tweets and finding those with images
    media_files = set()
    for status in tweets:
        if len(media_files) > 10:           # Maxes out a 10 images
            break
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])

    # Downloading images
    if len(media_files) == 0:
        print('There are no images in these tweets')
        return 0

    for media_file in media_files:
        wget.download(media_file)



    #FFMPEG
    #-----------------------------------------------------------------------------------------------------#
    # Converting all images that were downloaded into a single video file
    os.system('cat *.jpg | ffmpeg -f image2pipe -framerate .5 -i - output.mp4')



    #Google
    #-----------------------------------------------------------------------------------------------------#
    # For Google API authorization, set GOOGLE_APPLICATION_CREDENTIALS within .bash file
    labels_dict = {}
    path = glob.glob('*.jpg')
    client = vision.ImageAnnotatorClient()
    count = 0

    for img in path:
        with io.open(img, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        labels_dict[count] = []

        for label in labels:
            labels_dict[count].append(label.description)
        count += 1

    print(labels_dict)

#if __name__ == '__main__':
   # module('neiltyson', 100)


def test1():
# basic errorchecking for 20 tweets
    start_time = time.time()
    module('realDonaldTrump',10)
    elapsed_time = time.time() - start_time
    print('The time has taken for 20 tweets is ')
    print(elapsed_time)



def test2():
    #error checking for 200 tweets
    start_time = time.time()
    module('realDonaldTrump',200)
    elapsed_time = time.time() - start_time
    print('The time has taken for 200 tweets is ')
    print(elapsed_time)


def test3():
    #error checking for no pictures
    module('apapadakuni',10)




if __name__ == '__main__':
    test1()
    test2()
    test3()










