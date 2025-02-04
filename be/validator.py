import json
from urllib.request import urlopen
import jwt
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey

class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

def getIdFromRequest(request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return None
    parts = auth_header.split()
    if parts[0].lower() != 'bearer':
        return None
    elif len(parts) == 1:
        return None
    elif len(parts) > 2:
        return None
    token = parts[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload['sub']
    return user_id
