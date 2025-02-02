from flask import Flask, request, jsonify, redirect, session
from authlib.integrations.flask_client import OAuth
from dotenv import dotenv_values
from typing import Dict
import jwt  # PyJWT
from jwt import PyJWKClient

# Load environment variables
env_values = dotenv_values(".env")
app = Flask(__name__)
app.secret_key = env_values.get("APP_SECRET_KEY", "super-secret-key")

# Auth0 Configuration
AUTH0_DOMAIN = env_values["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = env_values["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = env_values["AUTH0_CLIENT_SECRET"]
AUTH0_CALLBACK_URL = env_values.get("AUTH0_CALLBACK_URL", "http://localhost:5999/callback")

if AUTH0_DOMAIN is None or AUTH0_CLIENT_ID is None or AUTH0_CLIENT_SECRET is None:
    raise Exception("Environment variables were not set correctly")

# Configure Auth0 OAuth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=f'https://{AUTH0_DOMAIN}',
    access_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
    authorize_url=f'https://{AUTH0_DOMAIN}/authorize',
    client_kwargs={'scope': 'openid profile email'}, # This is the information we want to get from auth0
)
if auth0 is None:
    raise Exception("auth 0 could not initialize")

# JWKS client for token verification
jwks_client = PyJWKClient(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')

def validate_auth0_token(token: str) -> Dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=AUTH0_CLIENT_ID,
        issuer=f'https://{AUTH0_DOMAIN}/'
    )

@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)

@app.route("/callback")
def callback():
    try:
        token = auth0.authorize_access_token()
        user_info = auth0.get('userinfo').json()

        # Store user in session
        session['user'] = {
            'access_token': token['access_token'],
            'id_token': token['id_token'],
            'user_info': user_info
        }

        return redirect('http://localhost:5173/logged-in')
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route("/protected", methods=["GET"])
def protected():
    user = session.get('user')
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Validate the access token
        decoded = validate_auth0_token(user['access_token'])
        return jsonify({
            "message": "Access granted",
            "user_info": user['user_info'],
            "token_info": decoded
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f'https://{AUTH0_DOMAIN}/v2/logout?'
        f'returnTo={request.host_url}&'
        f'client_id={AUTH0_CLIENT_ID}'
    )

if __name__ == "__main__":
    app.run(debug=True, port=5999)
