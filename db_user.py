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
		
		self.df=pd.read_sql_query("SELECT * FROM trackerdb",self.engine)
		self.df=self.df[self.df['usertw']==user]
		self.dates=self.df['datetw'].tolist()
		self.followers=self.df['followers'].tolist()
		
		fig=go.Figure()
		
		fig.add_trace(go.Scatter(x=self.dates,y=self.followers,mode='markers+lines',name=user))
		fig.update_layout(title=f'Followers')
		
		return fig,{'content':self.df.to_dict('records'),'cols':[{'name':i,'id':i} for i in self.df.columns]}
	
	def plot_variation(self):
		
		fig=go.Figure()
		
		variation=[]
		for i in range(len(self.followers)):
			try:
				variation.append(self.followers[i]-self.followers[i-1])
			except:
				pass
		variation[0]=0
			
		fig.add_trace(go.Bar(x=[i.split()[0] for i in self.dates],y=variation,text=variation,textposition='auto'))
		fig.update_xaxes(type='category')
		fig.update_layout(title='New Followers')
		
		
		return fig
		 
	

		 
	
		
		
		
		
		
		
		
		
	
			
		
			
			
	
		
		
		
		
		
			
		
