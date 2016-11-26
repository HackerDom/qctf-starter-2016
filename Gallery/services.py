import hashlib

from constants import PASSWORD_SECRET
from models import Photo


class UsersService:
    def __init__(self, db_connection):
        self.conn = db_connection

    def does_username_exist(self, username):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Users WHERE Username = ?', (username,))
        return c.fetchone() is not None

    def get_user_id_by_username(self, username):
        c = self.conn.cursor()
        c.execute('SELECT Id FROM Users WHERE Username = ?', (username,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

    def get_username_by_user_id(self, user_id):
        c = self.conn.cursor()
        c.execute('SELECT Username FROM Users WHERE Id = ?', (user_id,))
        result = c.fetchone()
        if result is None:
            return None
        return result[0]

    def is_password_correct(self, username, password):
        expected_hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        c = self.conn.cursor()
        c.execute('SELECT Hash FROM Users WHERE Username = ?', (username,))
        stored_hash = c.fetchone()
        return stored_hash and stored_hash[0] == expected_hash

    def add_user(self, username, password):
        if self.does_username_exist(username):
            return None

        hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        c = self.conn.cursor()
        c.execute('INSERT INTO Users (Username, Hash) VALUES (?, ?)', (username, hash))
        new_id = c.lastrowid
        self.conn.commit()
        return new_id

    def delete_user(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Users WHERE Id = ?', (id,))
        self.conn.commit()
        return True


class PhotosService:
    def __init__(self, db_connection):
        self.conn = db_connection

    def get_photo_by_id(self, id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Photos WHERE Id = ?', (id,))
        values = c.fetchone()
        if values is None:
            return None
        return Photo(*values)

    def get_featured_photos(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Photos WHERE IsFeatured = 1')
        return [Photo(*values) for values in c]

    def get_photos_by_user_id(self, user_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Photos WHERE UserId = ?', (user_id,))
        return [Photo(*values) for values in c]

    def get_photos_by_coordinates(self, lat_ref, lat, long_ref, long):
        c = self.conn.cursor()
        c.execute(
            'SELECT * FROM Photos WHERE LatitudeRef = ? AND Latitude = ? AND LongitudeRef = ? AND Longitude = ?',
            (lat_ref, lat, long_ref, long))
        return [Photo(*values) for values in c]

    def add_photo(self, photo):
        values = (
            photo.user_id,
            photo.upload_time,
            photo.latitude_ref,
            photo.latitude,
            photo.longitude_ref,
            photo.longitude,
            photo.filename,
            photo.is_featured)
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO Photos (UserId, UploadTime, LatitudeRef, Latitude,'
            ' LongitudeRef, Longitude, Filename, IsFeatured) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
        new_id = c.lastrowid
        self.conn.commit()
        return new_id

    def delete_photo(self, photo):
        c = self.conn.cursor()
        c.execute('DELETE FROM Photos WHERE Id = ?', (photo.id,))
        self.conn.commit()
        return True
