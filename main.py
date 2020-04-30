import tweepy

auth = tweepy.OAuthHandler("", "") # keys
auth.set_access_token("", "") # access tokens

api = tweepy.API(auth)

tweets = []
user = "" # user whose tweets will be retweeted
count = 5

f = open("date.txt", "r+")
date = f.read()

try:
    for tweet in api.user_timeline(id=user, count=count):
        tweets.append((tweet.created_at,tweet.id,tweet.text))

    tweetdate = int(str(tweets[0][0]).replace(":","").replace("-","").replace(" ",""))

    if tweetdate > int(date) and "RT @" not in tweets[0][2]: # compare last tweeted with user's last tweet
        api.update_status("") # sentence to comment with

    f.seek(0)
    f.write(str(tweetdate))
    f.close()

except tweepy.TweepError as e:
    if e.args[0][0]['message'] == "You have been blocked from viewing this user's profile.":
        from twitter_scraper import get_tweets

        for tweet in get_tweets(user, pages=1): # user whose tweets will be retweeted
            tweets.append((tweet["time"], tweet["isRetweet"], tweet["tweetId"]))

        tweetdate = int(str(tweets[0][0]).replace(":","").replace("-","").replace(" ",""))

        if tweetdate > int(date) and tweets[1][1] is False:
            from selenium import webdriver
            from PIL import Image
            import time

            def remove(ele): # remove unwanted elements that may appear in the screenshot
            	driver.execute_script("""
            	var element = document.getElementsByClassName(\"""" + ele + """\"), index;
            	for (index = element.length - 1; index >= 0; index--) {
            		element[index].parentNode.removeChild(element[index]);
            	}
            	""")

            # take screenshot
            driver = webdriver.Firefox()
            driver.get("https://twitter.com/" + user +  "/status/" + str(tweets[0][2]) + "?s=20")
            time.sleep(7) # why? i don't know. the whole code breaks if i don't leave this here
            remove("r-xnswec") # bottom bar
            remove("r-1siec45") # top bar
            remove("r-1xcajam") # side bars
            driver.execute_script("window.scrollTo(0,10)") # scroll up
            element = driver.find_element_by_class_name("r-eqz5dr") # tweet div
            location = element.location
            size = element.size
            driver.save_screenshot("pageImage.png")

            # crop image
            x = location['x']
            y = location['y']
            width = location['x']+size['width']
            height = location['y']+size['height']
            im = Image.open('pageImage.png')
            im = im.crop((int(x), int(y-9), int(width), int(height-9))) # for some reason the height cut is inconsistent, therefore, try to adjust it yourself
            im.save('tweet.png')

            driver.quit()

            api.update_with_media("./tweet.png", "")

        f.seek(0)
        f.write(str(tweetdate))
        f.close()
    else:
        print(e)
