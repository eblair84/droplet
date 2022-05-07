import socketio
 
sio = socketio.Client()
 
@sio.on('connect', namespace='/all-filings')
def on_connect():
    print("Connected to https://api.sec-api.io:3334/all-filings")
 
@sio.on('filing', namespace='/all-filings')
def on_filings(filing):
    print(filing)
 
sio.connect('https://api.sec-api.io:3334?apiKey=e1f5ceeb0ae98386533088b0c1ab2b06ff9d21046c49f331426febf0b91c17bc', namespaces=['/all-filings'])
sio.wait()
