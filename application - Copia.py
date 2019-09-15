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
rooms={'main':[]}

#rooms= {main:[{message:hello,user:artur}]}
#add new message to list
#message_line={message:1,user:x}
#rooms[main].append(message_line)
#add new room to rooms
#rooms rooms[name of new room] = []





#login system



@app.route("/")
def index():
    

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("index.html", current_user= session['username'])


@app.route('/login', methods=['POST'])
def login():
    username=request.form.get('username')
    if username not in user_list:
        session['logged_in'] = True
        session['username'] = username
        session['room'] = 'main'
        user_list.append(session['username'])
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
    #add new message to list
    msg=data['msg']
    username=session['username']
    message_line={'message': msg, 'username': username}
    rooms[room].append(message_line)
    
    current_history= rooms.get(room)
    
    print('printed:'+msg)
    emit("display_message", {'username': username, 'msg': msg}, broadcast=True)
    print('emited:'+msg)
    print(rooms)
    return False


if __name__ == '__main__':
    socketio.run(app)