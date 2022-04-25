from sqlalchemy import create_engine
import pandas as pd
from dash import Dash, dcc, html
import datetime
import tweepy
import plotly.graph_objects as go

class tw_user:
	def __init__(self,postgres_con_str,consumer_key,consumer_secret,access_token,access_token_secret):
		
      #postgres stuff		
		self.engine=create_engine(postgres_con_str)
		
		
		#twitter stuff
		self.consumer_key=consumer_key
		self.consumer_secret=consumer_secret
		self.access_token=access_token
		self.access_token_secret=access_token_secret
		
	def check_user(self,user):
		df=pd.read_sql_query("SELECT usertw FROM trackerdb",self.engine)
		#self.conn.close()
		#print(df['usertw'])
		if user in df['usertw'].unique().tolist():
			return True,'Already exists'
		else:
			return False,html.Button('Track',id='add_track',n_clicks=0)
	def login(self):
		try:
			print('logueando 1')
			auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			auth.set_access_token(self.access_token, self.access_token_secret)
			print('logueando 2')
			self.api=tweepy.API(auth)
			#print('logueando 3')
			#return self.api
		except Exception as e:
			print('something happened with login ',e)
			return False

		
			
	def add_user_tw(self,user):
		print(user)
		today=datetime.datetime.now()
		#self.login()		
		
		try:
			twitter_user=self.api.get_user(screen_name=user)
			nfollowers=twitter_user.followers_count
			query=f"""INSERT INTO trackerdb (usertw,datetw,followers) VALUES ('{user}','{str(today)}',{nfollowers})"""
			connection=self.engine.raw_connection()
			cursor=connection.cursor()
			
			cursor.execute(query)
			connection.commit()
			cursor.close()
			
			
			print(query)
			return True
		except Exception as e:
			print("User doesn't exists or maybe there is a problem with twitter API or internal DB connection",e)
			return False
	def plot_followers(self,user):
		
		df=pd.read_sql_query("SELECT * FROM trackerdb",self.engine)
		df=df[df['usertw']==user]
		dates=df['datetw'].tolist()
		followers=df['followers'].tolist()
		
		fig=go.Figure()
		
		fig.add_trace(go.Scatter(x=dates,y=followers,mode='markers+lines',name=user))
		fig.update_layout(title=f'Followers for {user}')
		
		return fig,{'content':df.to_dict('records'),'cols':[{'name':i,'id':i} for i in df.columns]}
	
		
		
		
		
		
		
		
		
	
			
		
			
			
	
		
		
		
		
		
			
		
