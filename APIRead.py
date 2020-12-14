import tweepy
from Keys import *
import datetime

def clearFiles():
	for hashtag in hashtags:
		f = open(hashtag + ".txt", 'w')
		f.write("Timestamp,Text,ID\n")
		f.close()	

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

hashtags = ["Biden2020"]
keywords = ["Donald", "Trump", "Joe", "Biden", "Kamala", "Harris", "Mike", "Pence"]
refresh_delta = datetime.timedelta(seconds=1)

day_time = datetime.timedelta(days=1)

search_filter = ""
for keyword in keywords:
	search_filter = search_filter + " OR \"" + keyword + "\""
search_filter = search_filter[3:]+" -RT"


time = datetime.datetime.utcnow()
start_time = time
startDate = datetime.datetime(2020,11,2).date()

start_days = 0
end_days = 14

searched_days = start_days

#clearFiles()

while(searched_days<end_days):

	
	for hashtag in hashtags:

		count = 0;
		
		for tweet in tweepy.Cursor(api.search,q="\"#"+hashtag+"\""+search_filter,count=100,
								   lang="en",
								   since=startDate-searched_days*day_time,
								   until=startDate-searched_days*day_time+day_time,
								   tweet_mode="extended").items():
			count = count+1
			
			if((time+refresh_delta)<datetime.datetime.utcnow()):
				time = datetime.datetime.utcnow()
				rate_limit = api.rate_limit_status()['resources']['search']['/search/tweets']
				print(str(hashtag) + "-" + str(tweet.created_at) + " - " + str(rate_limit["remaining"]) +" - " + str(datetime.datetime.fromtimestamp(rate_limit["reset"])) + " - " + str(datetime.datetime.utcnow()-start_time))#, tweet.full_text.encode("ascii", errors="ignore"),tweet.id)
			f = open(hashtag + ".txt", 'a')
			f.write(str(tweet.created_at)+","+str(tweet.full_text.encode("ascii", errors="ignore")).replace(",","_")+","+str(tweet.id)+"\n")
			f.close()
	
	print(startDate-searched_days*day_time)
	print(startDate-searched_days*day_time+day_time)
	searched_days = searched_days + 1
	

	

		


'''
user = api.get_user('andrewvh4')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)
'''

'''
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text.encode("utf-8"))
'''
'''
for tweet in tweepy.Cursor(api.search,q="#unitedAIRLINES",count=100,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text.encode("utf-8"))
'''	

'''
for tweet in tweepy.Cursor(api.user_timeline,id="joehills",count=1000,
                           lang="en",
                           since="2017-04-03").items():
    print (tweet.created_at, tweet.text.encode("utf-8"))
	
'''