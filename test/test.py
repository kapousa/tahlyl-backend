import secrets
import base64

secret_key = base64.b64encode(secrets.token_bytes(32)).decode()
print(secret_key)