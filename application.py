import os

import json

from flask import Flask, session
from flask_session import Session
from flask import Flask, request, render_template, jsonify
from flask import flash
import requests
from libgravatar import Gravatar
import time
from flask_socketio import SocketIO, join_room, leave_room, send, emit


app = Flask(__name__)
app.debug = True




# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)



user_list=[]
rooms={'main':{'users':[],'messages':[]}}




#login system



@app.route("/")
def index():
    
    
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return chat()


@app.route("/chat")
def chat():
    print('your room is:',session['room'])
    return render_template("index.html", current_user= session['username'], current_room= session['room'], rooms=rooms, )



@app.route('/login', methods=['POST'])
def login():
    username=request.form.get('username')
    if username not in user_list:
        session['logged_in'] = True
        session['username'] = username
        user_list.append(session['username'])
        session['room'] = 'main'
        room_users=rooms['main']['users']
        room_users.append(session['username'])
        print(user_list)
    return index()


@app.route("/logout")
def logout():
    if session['username'] in user_list:
        user_list.remove(session['username'])
    session['logged_in'] = False
    session['username'] = 'anonymous'
    session['room'] = 'main'
    print(user_list)
    return index()


@socketio.on("incoming msg")
def send_message(data):
    room = session['room']
    username=session['username']
    msg=data['msg']
    #form message dictionary
    message_line={'message': msg, 'username': username}
    #append dictionary to list which is the value of each room inside rooms dictionary
    room_messages=rooms[room]['messages']
    room_messages.append(message_line)
    print('printed:'+msg)
    #send info to js
    emit("display_message", {'username': username, 'room': room, 'msg': msg}, broadcast=True)
    print('emited:'+msg)
    print(rooms)
    return False

@socketio.on("create room")
def create_room(data):
    new_room = data['room_name']
    username=session['username']
    #form message dictionary
    print('room name received:'+ new_room)
    #send info to js
    if new_room in rooms:
        emit("room exists", broadcast=True)
        print('room already exists!')
    else:
        rooms[new_room]={'users':[],'messages':[]}
        emit("insert_room", {'new_room': new_room}, broadcast=True)
        print('room emited to js')
        print(rooms)
    return False


@socketio.on("join room")
def join_room(data):
    
    username=session['username']
    #form message dictionary
    
    room_selection = data['room_selection']
    session['room'] = data['room_selection']
    print(room_selection)
    print('current room:' + session['room'])
    print(username, 'joined:',session['room'])
    emit("change room", {'room_selection': room_selection}, broadcast=True)
    print('room change emmited to js')
    return index()

if __name__ == '__main__':
    socketio.run(app)