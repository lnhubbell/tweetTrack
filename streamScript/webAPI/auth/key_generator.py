import uuid
import base64


def _generate_key():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


def add_key():
    key = _generate_key()