
import pandas as pd
import tweepy
import datetime
from sqlalchemy import create_engine

con_str=''
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

engine=create_engine(con_str)
df=pd.read_sql_query("SELECT usertw FROM trackerdb",engine)

users=df['usertw'].unique().tolist()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api=tweepy.API(auth)
today=datetime.datetime.now()
#date_tw='2022-04-25'
for user in users:
	twitter_user=api.get_user(screen_name=user)
	nfollowers=twitter_user.followers_count
	#query=f"""INSERT INTO trackerdb (usertw,datetw,followers) VALUES ('{user}','{date_tw}',{nfollowers})"""
	query=f"""INSERT INTO trackerdb (usertw,datetw,followers) VALUES ('{user}','{str(today)}',{nfollowers})"""
	connection=engine.raw_connection()
	cursor=connection.cursor()
	cursor.execute(query)
	connection.commit()
	cursor.close()


