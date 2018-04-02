from google.cloud import vision
import io, oscurl
import tweepy
import wget
import glob
import os
import pymongo

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
        return 'The given username does not exist.'

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
        return 'There are no images in these tweets'

    for media_file in media_files:
        wget.download(media_file)
        print(media_file)



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

    #print(labels_dict)
    return labels_dict 



def MakeDataBase(text,name):
#This part reads the json file from the github link provided
#Then stores it in an array called data

#Now we demonstrate how to create that data in our own mongodb database
    sup = []
    client = pymongo.MongoClient()
    db = client.TwitterData
    for i in text:
        sup.append({"Picture #" : i, "Descirption labels" : text[i]})
    data = {"Twitter handle": name, "Picture Details": sup}
    db.TwitterData.insert(data)

    
if __name__ == '__main__':
    name = raw_input('What is the twitter handle you want to check: ')
    text = module(name, 10)
    os.system("mongod")
    MakeDataBase(text, name)
    print("Done\n")
