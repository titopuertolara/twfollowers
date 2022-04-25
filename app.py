from dash import Dash, dcc, html, Input, Output,State
import os
import pandas as pd
from db_user import tw_user
import plotly.graph_objects as go
from dash import Dash, dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True,title='Followers tracker')

server = app.server
con_str=''
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

db_object=tw_user(con_str,consumer_key,consumer_secret,access_token,access_token_secret)

app.layout = html.Div([
    html.H2('Twitter followers tracker'),
    html.Div([
    	html.Div(children=[dcc.Input(id='tw_user',placeholder=' e.g @aestebanp',type='text')],style={'display':'inline-block'}),
    	html.Div(children=[html.Button('Check',id='check_user',n_clicks=0)],style={'display':'inline-block'})    	  
    ]),
    
    html.Div(id='tracker-div'),
    html.Div(id='track-answ-div'),
    dcc.Loading(
                    id="loading-2",
                    children=[html.Div(dcc.Graph(id='user_plot'))],
                    type="circle",
                ),
    
    html.Div(dash_table.DataTable(
    	id='user-table',
    	style_cell={'textAlign':'left'},
    	style_header={'textAlign':'left','backgroundColor':'#0047AB','fontWeight': 'bold','color':'white'},
    	export_format='csv',
    	page_size=10
    	
    
    ))
    
   
])

@app.callback(Output('tracker-div','children'),
              Output('user_plot','figure'),
              Output('user-table','columns'),
              Output('user-table','data'),

              [Input('check_user','n_clicks'),
              State('tw_user','value')])
def render_user(n_clicks,user):
	fig=go.Figure()
	dummy=pd.DataFrame().to_dict('records')
	cols=[{'name':'','id':''}]
	if n_clicks>0 and user is not None:
		user=user.strip()
		if user[0]=='@':
			user=user.replace('@','')
		track_user_flag,response=db_object.check_user(user)
		if not track_user_flag:
			return html.Div([f'{user} is not in our DB, you can add a tracker',html.Br(),response]),fig,cols,dummy
		else:
			fig,table_dict=db_object.plot_followers(user)
			return response,fig,table_dict['cols'],table_dict['content']
	else:
		return '',fig,cols,dummy
		
@app.callback(Output('track-answ-div','children'),
              Output('tracker-div','style'),
              [Input('add_track','n_clicks'),
               State('tw_user','value')])
def track(n_clicks,tw_user):
	
	if n_clicks>0:
		tw_user=tw_user.strip()
		if tw_user[0]=='@':
			tw_user=tw_user.replace('@','')
		db_object.login()
		confirmation=db_object.add_user_tw(tw_user)
		
		if confirmation:
			return 'User tracked (you can check followers # with check button again)',{'display':'none'}
		else:
			return "This user appears not be registered on twitter if problem persists contact us",{'display':'none'}
	else:
		return '',{'display':'inline-block'}     


if __name__ == '__main__':
    app.run_server(debug=True)