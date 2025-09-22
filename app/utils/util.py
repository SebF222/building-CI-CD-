import jwt 
from datetime import datetime, timezone, timedelta  
from functools import wraps
from flask import request, jsonify 
import jwt
import jose
import os 

SECRET_KEY = os.environ.get('SECRET_KEY') or 'super secret secrets' #grabbing my secret key from enviornment 

def encode_token(mechanic_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(mechanic_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token 


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None 

        if 'Authorization' in request.headers:

            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'missing token'}), 401
            
            try:

                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print(data)
                mechanic_id = data['sub']
            except jwt.ExpiredSignatureError as e:
                return jsonify({'message': 'token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'invalid token'}), 401
            
            return f(mechanic_id, *args, **kwargs)
        
        else: 
            return jsonify({'message': 'you must be logged in to access this.'}), 401
    return decorated
