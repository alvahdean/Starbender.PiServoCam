#!/usr/bin/env python3

import io
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
    app.run(host='0.0.0.0', port=9595, debug=True)