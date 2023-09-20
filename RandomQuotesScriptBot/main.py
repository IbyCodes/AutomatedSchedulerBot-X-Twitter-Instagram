# Twitter/X bot + Instagram bot 
# Mohammad Ibrahim Khan (IbyCodes)
# Random Quote of The Day
#WORKING WITH picsum

import tweepy
import keys
import requests

# for temp config file (see below for more detail)
import os 
import shutil

import schedule # to schedule the tweets to be sent at a specific time every day
import time # to help with scheduling the tweets

from instabot import Bot # for the instagram bot 

# Defining the quote API endpoint URL (provided to me on gitHub: https://github.com/pprathameshmore/QuoteGarden#get-a-random-quote)
quote_api_url = 'https://quote-garden.onrender.com/api/v3/quotes/random'

# defining the image API endpoint URL (provided by: https://picsum.photos/)
image_api_url = 'https://picsum.photos/800/600?grayscale'  

# Initializing the instagram bot (Thanks to tutorialspoint for inspiration of this bot: https://www.tutorialspoint.com/post-a-picture-automatically-on-instagram-using-python#:~:text=In%20conclusion%2C%20by%20harnessing%20the,add%20captions%2C%20and%20log%20out.)
bot = Bot()

# Thanks to imak on the following thread for this solution on how to post images: https://stackoverflow.com/questions/70891698/how-to-post-a-tweet-with-media-picture-using-twitter-api-v2-and-tweepy-python
def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

# to initialize/set up the account to be tweeted on with all of its developer premissions (I needed both versions to successfully tweet the image on X)
client_v1 = get_twitter_conn_v1(keys.api_key, keys.api_key_secret, keys.access_token, keys.access_token_secret)
client_v2 = get_twitter_conn_v2(keys.api_key, keys.api_key_secret, keys.access_token, keys.access_token_secret)


# made it into a method to retrieve the quote
def getQuote(): 
    # Sending a GET request to the QuoteGarden API
    quotesReponse = requests.get(quote_api_url)

    # Checking to make sure the request was successful 
    if quotesReponse.status_code == 200:

        # Collecting the data retrieved
        data = quotesReponse.json()
    
        # Extracting what we need from the quote, which is the quote itself and the author's name (if provided)
        quote_text = data['data'][0]['quoteText']
        author_name = data['data'][0]['quoteAuthor']

        # Checking if the author's name is empty as not all quotes have known authors
        if author_name:
            return f'"{quote_text}"- {author_name}'
        else:
            return f'"{quote_text}"- Unknown'
    
    else:
        print(f"Failed to retrieve a random quote. Status code: {quotesReponse.status_code}")
        return None

# Will schedule the tweet and instagram post with a random image 
def post_scheduled_quote():
    quote_text = getQuote()
    if quote_text:
        image_response = requests.get(image_api_url) # will get the random image 
        if image_response.status_code == 200: # if the image has been retrieved correctly, then we can continue with the posting 
            # Saving the image to a local file (there are ways to do this without saving the file, but its very easy to run into errors)
            with open('temp_image.jpg', 'wb') as f:
                f.write(image_response.content)
            
            media_path = "temp_image.jpg"
            media = client_v1.media_upload(filename=media_path)
            media_id = media.media_id

            # Uploading the image and tweeting it along with the quote
            client_v2.create_tweet(text=quote_text, media_ids=[media_id])
            print("The post has been tweeted to X successfully!")

            # Logging to the Instagram account
            if bot.login(username= keys.insta_user, password= keys.insta_pass):
                # Uploading the picture
                bot.upload_photo(media_path, caption=quote_text)
                print("The post has been uploaded to Instagram successfully!")
                # Logging out from your account
                bot.logout()

        
        # Deleting the "config" folder thats created from the instagram post
        # I've added this code to the main code as there will be times where the instagram account refuses to post another image until both the 'config' folder and 
        # the 'temp_file_name.REMOVE_ME' files are removed from the directory
        # (This is a bit buggy at the moment)
        # Temporary solution is to just end the script once tweet+instagram post have been made, delete these two files, then restart script. 
            ''''
            time.sleep(5)
            config_folder = 'config'
            temp_file_name = 'temp_image.jpg.REMOVE_ME'
            if os.path.exists(config_folder):
                shutil.rmtree(config_folder)
                print("Removed config folder")
            
            time.sleep(5)
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)
                print("Removed temp_image.jpg.REMOVE_ME file")
           '''
    else:
        print(f"Failed to retrieve an image/quote correctly. Status code: {image_response.status_code}")

post_scheduled_quote() # for now, im going to set it so that every time I run this script it automatically posts right away. Of course, you can comment this out if you wish to schedule it.

# Scheduling the post to be uploaded to both Instagram and X/Twitter every day at ____ PM (System is a 24 H Clock)
schedule.every().day.at("17:26").do(post_scheduled_quote)

# Keeping the script running (If you wanted to post every day, it will require the script to run at all times. However, make sure to deal with instagram config files as required! Instabot is very buggy with this) 
while True:
    schedule.run_pending()
    time.sleep(1)
