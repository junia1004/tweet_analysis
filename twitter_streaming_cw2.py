import twitter,json,csv
import time



CONSUMER_KEY =
CONSUMER_SECRET =
OAUTH_TOKEN =
OAUTH_TOKEN_SECRET =

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# setup a file to write to
csvfile = open('trump_tweets_cw2_3.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter='|')

#  heres a function that takes out characters that can break
#  our import into Excel and replaces them with spaces
#  it also does the unicode bit

def getVal(val):
    clean = ""
    if val:
        val = val.replace('|', ' ')
        val = val.replace('\n', ' ')
        val = val.replace('\r', ' ')
        clean = val.encode('utf-8')
    return clean

q = "Trump, Impeachment, TrumpImpeachment" #Comma-separated list of terms represented as a single string can go here
print 'Filtering the public timeline for track="%s"' % (q,)

twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

stream = twitter_stream.statuses.filter(track=q)

#headers
csvwriter.writerow(["created_at","user_name","text","user_location","user_id","geo_enabled",
                    "verified","user_statuses","user_followers","user_friends",
                    "retweeted","retweets_count","coords","time_zone_user","place_name"])
count = 0
for tweet in stream:
    # write the values to file
    try: #exception to let the script going in case of error
        if tweet['truncated']:
            tweet_text = tweet['extended_tweet']['full_text']
        else:
            tweet_text = tweet['text']

            retweeted=False
        if "retweeted_status" in set (tweet.keys()):
            retweeted=True
            #retweeted_count = tweey["retweeted_status"]["retweeted_count"]

        try:
            place_name = tweet['place']['name']
            #place_full_name = tweet['place']['full_name']
            #place_country = tweet['place']['country']
            #place_type = tweet['place']['type']
            print("!!!!!!!!!!! PLACE FOUND !!!!!!!!!!!!")
        except:
            place_name = None
            #place_full_name = None
            #place_country = None
            #place_type = None




        # write the values to file
        csvwriter.writerow([
            tweet['created_at'],
            getVal(tweet['user']['screen_name']),
            getVal(tweet_text),
            getVal(tweet['user']['location']),
            tweet['user']['id'],
            tweet['user']['geo_enabled'],
            tweet['user']['verified'],
            tweet['user']['statuses_count'],
            tweet['user']['followers_count'],
            tweet['user']['friends_count'],
            retweeted,
            tweet['retweet_count'],
            tweet['coordinates'],
            tweet['user']['time_zone'],
            place_name,
            #place_full_name,
            #place_country,
            #place_type
            ])
        # print something to the screen, mostly so we can see what is going on...
        count+=1
        print str(count) + " - " + tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8')
    except:
        print("!!! Error found - tweet skipped !!!")
        #time.sleep(5)
        pass
