from flask import Flask, render_template, request, redirect, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_

from database import Team, User, Conversation, Message

from slackclient import SlackClient

import requests
import json
import os

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

CLIENT_ID = '34225236465.48252872646'
CLIENT_SECRET = '0ffec6951613805313fd2af0796dfef6'
SCOPE = 'users%3Aread+channels%3Awrite+chat%3Awrite%3Abot+chat%3Awrite%3Auser+bot'
REDIRECT_URI='http://localhost:5000/oauth/step2/'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/oauth/step1/')
def oauth2_step1():
    url = 'https://slack.com/oauth/authorize?client_id=%s&scope=%s&redirect_uri=%s' % (CLIENT_ID, SCOPE, REDIRECT_URI)
    return redirect(url)

@app.route('/oauth/step2/')
def oauth2_step2():
    
    code = request.args.get('code')
    url = 'https://slack.com/api/oauth.access?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s' % (CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
    
    r = requests.get(url)
    response = json.loads(r.text)

    s = session()
    
    team = Team(name=response['team_name'], token=response['access_token'], id=response['team_id'], bot_id=response['bot']['bot_user_id'], bot_token=response['bot']['bot_access_token'])
    s.add(team)
    
    sc = SlackClient(response['access_token'])

    user_list = sc.api_call("users.list")['members']

    for user_object in user_list:

        if user_object['deleted'] or not user_object['is_bot']:
            continue

        user_id = user_object['id']

        user_profile = user_object['profile']
        
        #first_name = user_profile['first_name']
        #last_name = user_profile['last_name']

        user = User(id=user_id, team=team)
        s.add(user)


    s.commit()

    os.system("nohup python bot/rtmbot.py %s &" % response['bot']['bot_access_token'])

    return jsonify(r.json())
    

@app.route('/conversation/', methods=['POST'])
def start_conversation():
    origin_user = request.form['origin_user']
    destination_user = request.form['destination_user']

    s = session()

    #Need to add validation here so that multiple conversations are not started by the same person
    #conversation_exists = s.query(Conversation)

    conversation = Conversation(from_user_id=origin_user, to_user_id=destination_user)
    s.add(conversation)
    s.commit()

    return "Success"



@app.route('/message/', methods=['POST', 'GET'])
def send_message():    
    origin_user = request.form['origin_user']
    message = request.form['message']
    
    #access_token = 'xoxb-48229673667-O2UeLMKPQLY9ylFhtKMVLPif'#request.form['access_token']
    
    s = session()

    s.query(Conversation).filter(Conversation.from_user == origin_user).first()

    """
    sc = SlackClient(access_token)

    im_list = sc.api_call('im.list')

    user_im_id = ''
    for im in im_list['ims']:
        if im['user'] == destination_user:
            user_im_channel = im['id']
    
    sc.rtm_connect()
    sc.rtm_send_message(channel=user_im_channel, message=message)
    """

    return "Success"
    
"""
@app.route('/rate_user/', methods=['POST'])
def rate_user():
"""

if __name__ == '__main__':
    app.run(debug=True)