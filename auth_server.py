from flask import Flask, request, redirect, jsonify
import secrets

app = Flask(__name__)

CLIENTS = {
    "client1": {
        "secret": "secret1",
        "allowed_redirects": ["http://localhost:5001/callback"]
    }
}

codes = {}

@app.route('/authorize')
def authorize():
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')
    
    if client_id not in CLIENTS:
        return "Invalid client", 400
    
    # For attack demo: no redirect_uri validation (vulnerable mode)
    
    code = secrets.token_urlsafe(16)
    codes[code] = client_id
    return redirect(f"{redirect_uri}?code={code}&state={state}")

@app.route('/token', methods=['POST'])
def token():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    code = request.form.get('code')
    
    if client_id not in CLIENTS or CLIENTS[client_id]["secret"] != client_secret:
        return jsonify({"error": "bad client"}), 401
    if code not in codes:
        return jsonify({"error": "bad code"}), 400
    
    del codes[code]
    access_token = secrets.token_urlsafe(32)
    return jsonify({"access_token": access_token})

if __name__ == '__main__':
    app.run(port=5000)