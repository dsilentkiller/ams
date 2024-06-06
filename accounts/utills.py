# myapp/utils.py

import jwt
from datetime import datetime, timedelta
from django.conf import settings

secret_key = settings.SECRET_KEY


def generate_jwt_token(id):
    try:
        # Define the payload and expiration
        info_obj = {
            'id': id,
        }
        expiry_info = {
            'expires_in': timedelta(days=1),
        }

        # Generate JWT token
        token = jwt.encode(
            {**info_obj, **expiry_info},
            secret_key,
            algorithm='HS256'
        )

        return token

    except Exception as e:
        return None
