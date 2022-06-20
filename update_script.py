
import pandas as pd
import tweepy
import datetime
from sqlalchemy import create_engine
import plotly.graph_objects as go
import time

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


forbiden_users=['FicoGutierrez','Enrique_GomezM','sergio_fajardo','JohnMiltonR_','German_Vargas','ZelenskyyUa','EnriquePenalosa','realamberheard','FranciaMarquezM','UCompensar','marcollinasvolp','AlvaroUribeVel']
for user in users:
	if user not in forbiden_users:
		user_df=pd.read_sql_query(f"""SELECT * FROM trackerdb WHERE usertw='{user}'""",engine)
		followers=user_df['followers'].tolist()
		try:
			new_followers=user_df['followers'].tolist()[-1]-user_df['followers'].tolist()[-2]
		except:
			new_followers=0
		nf_list=[]
		for i in range(1,len(followers)):
			nf_list.append(followers[i]-followers[i-1])
		if len(nf_list)>0:
			mean_followers=round(sum(nf_list)/len(nf_list),1)
		else:
			mean_followers=0
		dates_list=[i.split()[0] for i in user_df['datetw'].tolist()[1:]]
		tweet_text=f'👤 @{user} 👥:{followers[-1]}, 🆕 👥:{new_followers}, 📈: {mean_followers} seguidores nuevos/día  #EleccionesColombia'

		#print(dates_list)
		#print(nf_list)
		fig=go.Figure()
		fig.add_trace(go.Scatter(x=dates_list,y=nf_list,text=nf_list,mode='lines+markers'))
		fig.update_yaxes(title='Seguidores nuevos')
		fig.update_layout(title=f'@{user}')
		path_img='plot.png'
		fig.write_image(path_img)
		print(user)
		
		api.update_status_with_media(tweet_text,path_img )
		time.sleep(30)

#print(png_base64)








