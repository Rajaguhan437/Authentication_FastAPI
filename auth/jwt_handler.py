# %%
import time
import jwt
from decouple import config
from datetime import datetime, timedelta
# %%
JWT_ACCESS_SECRET = config("acc_secret")
JWT_REFRESH_SECRET = config("ref_secret")
JWT_ALG = config("alg")

# %%
def encodeJWT(username: str, password: str, role: str, access_expire_time=None, refresh_expire_time=None):

    if not access_expire_time:
        access_expire_time = time.time() + 60 * 20
    if not refresh_expire_time:
        refresh_expire_time = time.time() + 60 * 60 * 24 * 7
    
    access_payload = {
        "username": username,
        "password": password,
        "role": role,
        "exp" : access_expire_time
        #"exp" : access_expire_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    refresh_payload = {
        "username": username,
        "password": password,
        "role": role,
        "exp" : refresh_expire_time
        #"exp" : refresh_expire_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    access_token = jwt.encode(access_payload, JWT_ACCESS_SECRET, algorithm=JWT_ALG)
    refresh_token = jwt.encode(refresh_payload, JWT_REFRESH_SECRET, algorithm=JWT_ALG)

    return {
        "access_token" : access_token,
        "refresh_token": refresh_token
    }


def decodeJWT(token: str, type='access'):
    try:
        if type == 'refresh':
            decode_token = jwt.decode(token, JWT_REFRESH_SECRET, algorithms=JWT_ALG)
            return decode_token if decode_token['exp']>= time.time() else None
        elif type == 'access':
            decode_token = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=[JWT_ALG])
            return decode_token if decode_token['exp']>= time.time() else None
    except Exception as e:
        return {}
    
# %%
import time
print(time.time())