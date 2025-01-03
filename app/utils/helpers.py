import jwt


def account_activation_task(email, secret):
    encoded_jwt = jwt.encode({"email": email}, secret, algorithm="HS256")
    pass
