#!/usr/bin/python3

import socketio

sio = socketio.Client()

@sio.event
def message(data):
    print('I received a message!')

@sio.on('my message')
def on_message(data):
    print('I received a message!')
