import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
import string

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        access_token = ""
        access_token_secret = ""
        consumer_key = ""
        consumer_secret = ""

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

print("running")
# creating object of TwitterClient Class
api = TwitterClient()
# calling function to get tweets
tweets = api.get_tweets(query = 'Modi', count = 200)
# picking positive tweets from tweets
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# percentage of positive tweets
pst1=100*len(ptweets)/len(tweets)
pst1=round(pst1,2)

print("\n\n\n"+" "*40+"BJP"+"\n")

print("Positive tweets percentage: {} %".format(pst1))
# picking negative tweets from tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# percentage of negative tweets
ngt1=100*len(ntweets)/len(tweets)
ngt1=round(ngt1,2)
print("Negative tweets percentage: {} %".format(ngt1))
# percentage of neutral tweets
nut1=100-(pst1+ngt1)
nut1=round(nut1,2)
print("Neutral tweets percentage: {} % ".format(nut1))


filename="modipos.txt"
file1 = open(filename,"a")
upload=""
# printing first 5 positive tweets
print("\n\nPositive tweets:")
for tweet in ptweets:
    # print(tweet['text'])
    upload+=tweet['text']
    upload+='\n'
    upload+='\n'

print(upload)
try:
    file1.write(upload)
    file1.close()
except:
    print()

# printing first 5 negative tweets
upload2=""
filename2="modineg.txt"
file2 = open(filename2,"a")
print("\n\nNegative tweets:")
for tweet in ntweets:
    # print(tweet['text'])
    upload2+=tweet['text']
    upload2+='\n'
    upload2+='\n'
print(upload2)

try:
    file2.write(upload2)
    file2.close()
except:
    print()

print("\n\n\n"+" "*40+"CONGRESS"+"\n")

tweets2 = api.get_tweets(query = 'Rahul Gandhi', count = 200)
# picking positive tweets from tweets
ptweets2 = [tweet2 for tweet2 in tweets2 if tweet2['sentiment'] == 'positive']
# percentage of positive tweets
pst2=100*len(ptweets2)/len(tweets2)
pst2=round(pst2,2)
print("Positive tweets percentage: {} %".format(pst2))
# picking negative tweets from tweets
ntweets2 = [tweet2 for tweet2 in tweets2 if tweet2['sentiment'] == 'negative']
# percentage of negative tweets
ngt2=100*len(ntweets2)/len(tweets2)
ngt2=round(ngt2,2)
print("Negative tweets percentage: {} %".format(ngt2))
# percentage of neutral tweets
nut2=100-(pst2+ngt2)
nut2=round(nut2,2)
print("Neutral tweets percentage: {} % ".format(nut2))

upload3=""
filename3="rahul-pos.txt"
file3 = open(filename3,"a")
print("\n\nPositive tweets:")
for tweet2 in ptweets2:
    # print(tweet2['text'])
    upload3+=tweet2['text']
    upload3+='\n\n'
print(upload3)
try:
    file3.write(upload3)
    file3.close()
except:
    print()


# printing first 5 negative tweets
upload4=""
filename4="rahulneg.txt"
file4 = open(filename4,"a")
print("\n\nNegative tweets:")
for tweet2 in ntweets2:
    # print(tweet2['text'])
    upload4+=tweet2['text']
    upload4+='\n\n'
print(upload4)
try:
    file4.write(upload4)
    file4.close()
except:
    print()

print("\n\n\n"+" "*40+"STATISTICS\n")

arr=[['Opinion','BJP','Congress'],['Positive',pst1,pst2],['Negative',ngt1,ngt2],['Nuetral',nut1,nut2]]
df1=pd.DataFrame(arr,)
print((df1.to_string(index=False)))


#################################################################################

import tkinter as tk
top = tk.Tk()
tit=(" "*10)+"POLITICS POLL"
top.title(tit)
top.geometry('350x180+900+320')
l00=tk.Label(top,text="OPINION",font=("Arial ",14))
l00.grid(row=0,column=0)

l01=tk.Label(top,text="BJP",font=("Arial ",14))
l01.grid(row=0,column=1)

l02=tk.Label(top,text="CONG",font=("Arial ",14))
l02.grid(row=0,column=2)

l10=tk.Label(top,text="POSITIVE",font=("Arial ",14))
l10.grid(row=1,column=0)

l11=tk.Label(top,text=pst1,font=("Arial ",14))
l11.grid(row=1,column=1)

l12=tk.Label(top,text=pst2,font=("Arial ",14))
l12.grid(row=1,column=2)

l20=tk.Label(top,text="NEGATIVE",font=("Arial ",14))
l20.grid(row=2,column=0)

l21=tk.Label(top,text=ngt1,font=("Arial ",14))
l21.grid(row=2,column=1)

l22=tk.Label(top,text=ngt2,font=("Arial ",14))
l22.grid(row=2,column=2)

l30=tk.Label(top,text="NUETRAL",font=("Arial ",14))
l30.grid(row=3,column=0)

l31=tk.Label(top,text=nut1,font=("Arial ",14))
l31.grid(row=3,column=1)

l32=tk.Label(top,text=nut2,font=("Arial ",14))
l32.grid(row=3,column=2)
print("finished")

import matplotlib.pyplot as plt
plt.figure(1)
# x-coordinates of left sides of bars
left = [1, 2, 3, 4, 5, 6]

# heights of bars
height = [pst1, ngt1, nut1, pst2, ngt2, nut2]

# labels for bars
tick_label = ['+ve BJP', '-ve BJP', 'nuetral BJP', '+ve CONG', '-ve CONG', 'nuetral CONG']

# plotting a bar chart
abc=plt.bar(left, height, tick_label = tick_label,
            width = 0.6, color = ['green', 'red' ,'blue' ])

# naming the x-axis
plt.xlabel('Parties-->')
# naming the y-axis
plt.ylabel('Percentage--->')
# plot title
plt.title('Results on Tweet Analysis')

# function to show the plot

#################################################################################
#tkinter module
# import matplotlib.pyplot as plt
bjptot=(pst1*1)+(ngt1*-0.8)+(nut1*0.2)
congtot=(pst2*1.2)+(ngt2*-0.5)+(nut2*0.2)
bjpratio=(bjptot*100)/(bjptot+congtot)
bjpratio=round(bjpratio,2)
congratio=(congtot*100)/(bjptot+congtot)
congratio=round(congratio,2)
plt.figure(2)
labels = 'BJP', 'CONGRESS'
sizes = [bjpratio,congratio]
colors=['orange','blue']
explode = (0.1, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')



#################################################################################
#writing statistics data int csv file

import csv

csvData = [[bjpratio,congratio]]

with open('stats.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()
##################################################################################################################################################################

#DISPLAY GRAPHS

plt.show(1)

plt.show(2)

top.mainloop()