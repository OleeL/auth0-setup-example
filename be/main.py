from flask import Flask, jsonify, request
from dotenv import dotenv_values
from flask_cors import CORS
import base64
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import getIdFromRequest, Auth0JWTBearerTokenValidator

env_values = dotenv_values(".env")
AUTH0_DOMAIN = env_values.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = env_values.get("AUTH0_AUDIENCE")

if AUTH0_DOMAIN is None or AUTH0_AUDIENCE is None:
    raise Exception("Environment variables were not set correctly")

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    AUTH0_DOMAIN,
    AUTH0_AUDIENCE,
)
require_auth.register_token_validator(validator)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.secret_key = env_values.get("APP_SECRET_KEY", "super-secret-key")

# Load the super secret image and convert it to base64
super_secret_image = ""
with open("./rx8cool.jpg", "rb") as img_file:
    super_secret_image = base64.b64encode(img_file.read()).decode('utf-8')

@app.route("/protected", methods=["GET"])
@require_auth(None)
def protected():
    id = getIdFromRequest(request)
    return jsonify({
        "message": "Access granted to protected content",
        "secret_image": super_secret_image,
        "other_data": id
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5999)
