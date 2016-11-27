import hashlib

from constants import PASSWORD_SECRET
from models import Photo


class UserService:
    def __init__(self, request_db_connection):
        self.request_connection = request_db_connection

    def get_cursor(self):
        return self.request_connection().cursor()

    def commit(self):
        self.request_connection().commit()

    def get_user_by_user_id(self, user_id):
        c = self.get_cursor()
        c.execute('SELECT * FROM Users WHERE Id = %s', (user_id,))
        result = c.fetchone()
        c.close()
        if result is None:
            return None
        return result[0]

    def username_exists(self, username):
        c = self.get_cursor()
        c.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        result = c.fetchone()
        c.close()
        return result is not None

    def get_user_id_by_username(self, username):
        c = self.get_cursor()
        c.execute('SELECT Id FROM Users WHERE Username = %s', (username,))
        result = c.fetchone()
        c.close()
        if result is None:
            return None
        return result[0]

    def get_username_by_user_id(self, user_id):
        c = self.get_cursor()
        c.execute('SELECT Username FROM Users WHERE Id = %s', (user_id,))
        result = c.fetchone()
        c.close()
        if result is None:
            return None
        return result[0]

    def is_password_correct(self, username, password):
        expected_hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        c = self.get_cursor()
        c.execute('SELECT `Hash` FROM Users WHERE Username = %s', (username,))
        stored_hash = c.fetchone()
        c.close()
        return stored_hash and stored_hash[0] == expected_hash

    def add_user(self, username, password):
        if self.username_exists(username):
            return None

        hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        c = self.get_cursor()
        c.execute('INSERT INTO Users (Username, Hash) VALUES (%s, %s)', (username, hash))
        new_id = c.lastrowid
        c.close()
        self.commit()
        return new_id

    def delete_user(self, id):
        c = self.get_cursor()
        c.execute('DELETE FROM Users WHERE Id = %s', (id,))
        c.close()
        self.commit()
        return True


class PhotoService:
    def __init__(self, request_db_connection):
        self.request_connection = request_db_connection

    def get_cursor(self):
        return self.request_connection().cursor()

    def commit(self):
        self.request_connection().commit()

    def get_photo_by_id(self, id):
        c = self.get_cursor()
        c.execute('SELECT * FROM Photos WHERE Id = %s', (id,))
        values = c.fetchone()
        c.close()
        if values is None:
            return None
        return Photo(*values)

    def get_all_ids(self):
        c = self.get_cursor()
        c.execute('SELECT Id FROM Photos ORDER BY Id DESC')
        result = c.fetchall()
        c.close()
        return result

    def get_featured_photos(self):
        c = self.get_cursor()
        c.execute('SELECT * FROM Photos WHERE IsFeatured = 1 ORDER BY Id DESC')
        result = [Photo(*values) for values in c]
        c.close()
        return result

    def get_photos_by_user_id(self, user_id):
        c = self.get_cursor()
        c.execute('SELECT * FROM Photos WHERE UserId = %s ORDER BY Id DESC', (user_id,))
        c.close()
        result = [Photo(*values) for values in c]
        return result

    def get_photos_by_coordinates(self, lat_ref, lat, long_ref, long):
        c = self.get_cursor()
        c.execute(
            'SELECT * FROM Photos WHERE LatitudeRef = %s AND Latitude = %s AND LongitudeRef = %s'
            ' AND Longitude = %s ORDER BY Id DESC', (lat_ref, lat, long_ref, long))
        c.close()
        result = [Photo(*values) for values in c]
        return result

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
        c = self.get_cursor()
        c.execute(
            'INSERT INTO Photos (UserId, UploadTime, LatitudeRef, Latitude,'
            ' LongitudeRef, Longitude, Filename, IsFeatured) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', values)
        new_id = c.lastrowid
        c.close()
        self.commit()
        return new_id

    def delete_photo_by_filename(self, filename):
        c = self.get_cursor()
        c.execute('DELETE FROM Photos WHERE Filename = %s', (filename,))
        c.close()
        self.commit()
        return True
