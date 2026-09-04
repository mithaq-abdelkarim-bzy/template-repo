import requests
import json
import base64
import datetime
import hashlib
import hmac
import hx

def decode_string(sentence):
    '''
    Decode a brinary sentence into string.
    '''
    return sentence.decode('utf-8').replace("=", "").replace('+', '-').replace('/', '_')

def get_0auth_token():
    '''
    Create a bearer token to be used in the SpatialKey API calls.
    Currently bearer token will last for 6 min.
    '''
    
    # Get the current time in seconds
    ep = datetime.datetime(1970,1,1,0,0,0)
    x = (datetime.datetime.utcnow()- ep).total_seconds()

    # Credentials
    sk_org_api_key = hx.secrets.spatialkey_org_api_key
    sk_user_api_key = hx.secrets.spatialkey_user_api_key
    sk_secret_key = hx.secrets.spatialkey_secret_key

    # This is for the url
    # Needs to be a string for the whitespace - the otherside needs to replicate this and we'll get errors (maybe?)
    claimTemplate = f'{{"iss": "{sk_org_api_key}", "prn": "{sk_user_api_key}", "aud": "https://www.spatialkey.com", "exp": "{round(x+360)}", "iat": "{round(x)}"}}'
    header = '{"alg":"SH256"}'

    # Encode it into binary then convert it back into a string
    encodedClaimTemplate = decode_string(base64.b64encode(claimTemplate.encode("utf-8")))
    encodedHeader = decode_string(base64.b64encode(header.encode("utf-8")))

    combined = f"{encodedHeader}.{encodedClaimTemplate}"

    message = bytes(combined, 'utf-8')
    secret = bytes(sk_secret_key, 'utf-8')

    # Encrypt it with the secret key using keyed-hashing
    signature = decode_string(base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()))
    
    encodedCombined = f"{combined}.{signature}"
    
    # Get the bearer token
    url = "https://beazleyuw.spatialkey.com/SpatialKeyFramework/api/v2/oauth.json"
    headers = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        "assertion": encodedCombined
    }
    response = requests.post(url, params=headers)
    auth_token = response.json()["access_token"]
    
    return auth_token
