import datetime

import jwt
from jwt.exceptions import DecodeError
import piexif

from constants import SESSION_LENGTH, JWT_SECRET


def encode_jwt(user_id, username, expires_at=None):
    if expires_at is None:
        expires_at = datetime.datetime.utcnow() + SESSION_LENGTH
    payload = {'user_id': user_id, 'username': username, 'expires': expires_at.timestamp()}
    return jwt.encode(payload, JWT_SECRET)


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET)


def check_jwt(token):
    try:
        payload = decode_jwt(token)
    except DecodeError:
        return False
    if payload is None or not isinstance(payload, dict) or set(payload.keys()) != {'user_id', 'username', 'expires'}:
        return False
    return datetime.datetime.utcfromtimestamp(payload['expires']) >= datetime.datetime.now()


def get_nearby_coordinates(lat_ref, lat, long_ref, long):
    for d_lat in [-1, 0, 1]:
        for d_long in [-1, 0, 1]:
            new_lat_ref = lat_ref
            new_lat = lat + d_lat
            new_long_ref = long_ref
            new_long = long + d_long
            if new_lat > 90:
                continue
            if new_lat < 0:
                new_lat *= -1
                new_lat_ref = 'N' if new_lat_ref == 'S' else 'S'
            if new_long < 0 or new_long > 180:
                new_long_ref = 'E' if new_long_ref == 'W' else 'W'
                if new_long < 0:
                    new_long *= -1
                else:
                    new_long = 360 - new_long
            if new_lat == 0:
                new_lat_ref = 'N'
            if new_long in [0, 180]:
                new_long_ref = 'W'
            yield new_lat_ref, new_lat, new_long_ref, new_long


def extract_coordinates_from_jpeg(jpeg_bytes):
    gps = piexif.load(jpeg_bytes).get('GPS')
    if not gps or len(gps) < 5:
        return None
    lat_ref, lat, long_ref, long = gps[1], gps[2], gps[3], gps[4]
    lat_ref = lat_ref.decode('utf-8')
    lat = lat[0][0]
    long_ref = long_ref.decode('utf-8')
    long = long[0][0]
    return lat_ref, lat, long_ref, long
