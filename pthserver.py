#!/usr/bin/env python3

import io
import os
from time import sleep
import pantilthat
from sys import exit

try:
    from flask import Flask, render_template, send_file, jsonify
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/position')
def getPosition():
    return jsonify(
        pan=pantilthat.get_pan()+90,
        tilt=pantilthat.get_tilt()+90
    )

@app.route('/api/<direction>/<int:angle>')
def movecam(direction, angle):
    if angle < 0 or angle > 180:
        return "{'error':'out of range'}"
    angle=angle-90

    if(angle<-90 or angle>90):
        return getPosition()


    print("PANTILT: Operation:["+direction+"], Angle:["+str(angle)+"]")
    if direction == 'pan':
        pantilthat.pan(angle)
    elif direction == 'tilt':
        pantilthat.tilt(angle)
    
    return getPosition()

if __name__ == "__main__":
    listen_port = os.environ['UI_SERVER_PORT']
    if listem_port == "":
        listen_port = 9595
    listen_addr = os.environ['UI_SERVER_ADDR']
    if listem_addr == "":
        listen_addr = '0.0.0.0'
    debug_on = os.environ['UI_SERVER_DEBUG'] != ""
    
    print "Starting listener: " + listen_addr + ":" + listen_port
    print "Debug: " + debug_on
    app.run(host=listen_addr, port=listem_port, debug=debug_on)
