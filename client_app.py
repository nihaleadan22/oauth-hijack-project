from flask import Flask, request, redirect, session
import requests
import secrets

app = Flask(__name__)
app.secret_key = 'anything_secret_123'

AUTH_SERVER = "http://localhost:5000"
CLIENT_ID = "client1"
CLIENT_SECRET = "secret1"
REAL_REDIRECT = "http://localhost:8888/callback"
@app.route('/')
def home():
    if 'token' in session:
        return f"Logged in! Token: {session['token'][:20]}... <a href='/logout'>Logout</a>"
    return '<a href="/login">Login with OAuth</a>'

@app.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    session['state'] = state
    redirect_uri = REAL_REDIRECT
    auth_url = f"{AUTH_SERVER}/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&state={state}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != session.get('state'):
        return "State mismatch", 400
    
    resp = requests.post(f"{AUTH_SERVER}/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    })
    if resp.status_code == 200:
        session['token'] = resp.json()['access_token']
        return redirect('/')
    return "Token exchange failed", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5001)