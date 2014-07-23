import uuid
import base64


def generate_key():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '') + r_uuid.replace('=', '')