import datetime


with open('secrets/password_secret.txt') as f:
    PASSWORD_SECRET = f.read().strip()
with open('secrets/jwt_secret.txt') as f:
    JWT_SECRET = f.read().strip()
SESSION_LENGTH = datetime.timedelta(hours=24)
MAX_PHOTO_SIZE = 20 * 1024 * 1024