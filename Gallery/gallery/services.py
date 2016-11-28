import hashlib

import datetime
from constants import PASSWORD_SECRET
from models import Photo


class Service:
    def __init__(self, request_db_connection):
        self.request_connection = request_db_connection

    def get_cursor(self):
        return self.request_connection().cursor()

    def commit(self):
        self.request_connection().commit()

    def execute(self, expression, params=()):
        c = self.get_cursor()
        c.execute(expression, params)
        c.close()

    def fetchone(self, expression, params=(), field_num=None):
        c = self.get_cursor()
        c.execute(expression, params)
        result = c.fetchone()
        c.close()
        if field_num is not None and result is not None:
            return result[field_num]
        return result

    def fetchall(self, expression, params=()):
        c = self.get_cursor()
        c.execute(expression, params)
        result = c.fetchall()
        c.close()
        return result


class UserService(Service):
    def __init__(self, request_db_connection):
        super().__init__(request_db_connection)

    def username_exists(self, username):
        return self.fetchone('SELECT * FROM Users WHERE Username = %s', (username,)) is not None

    def get_user_id_by_username(self, username):
        return self.fetchone('SELECT Id FROM Users WHERE Username = %s', (username,), 0)

    def get_username_by_user_id(self, user_id):
        return self.fetchone('SELECT Username FROM Users WHERE Id = %s', (user_id,), 0)

    def is_password_correct(self, username, password):
        expected_hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        stored_hash = self.fetchone('SELECT `Hash` FROM Users WHERE Username = %s', (username,), 0)
        return stored_hash == expected_hash

    def add_user(self, username, password):
        if self.username_exists(username):
            return None
        hash = hashlib.sha256((username + password + PASSWORD_SECRET).encode()).hexdigest()
        self.execute('INSERT INTO Users (Username, Hash) VALUES (%s, %s)', (username, hash))
        self.commit()

    def delete_user(self, id):
        self.execute('DELETE FROM Users WHERE Id = %s', (id,))
        self.commit()


class PhotoService(Service):
    def __init__(self, request_db_connection):
        super().__init__(request_db_connection)

    def get_photo_by_id(self, id):
        fields = self.fetchone('SELECT * FROM Photos WHERE Id = %s', (id,))
        if fields is None:
            return None
        return Photo(*fields)

    def get_all_ids(self):
        return self.fetchall('SELECT Id FROM Photos ORDER BY Id DESC')

    def get_featured_photos(self):
        return [
            Photo(*fields) for fields in
            self.fetchall('SELECT * FROM Photos WHERE IsFeatured = 1 ORDER BY Id DESC')]

    def get_photos_by_user_id(self, user_id):
        return [
            Photo(*fields) for fields in
            self.fetchall('SELECT * FROM Photos WHERE UserId = %s ORDER BY Id DESC', (user_id,))]

    def get_photos_by_coordinates(self, lat_ref, lat, long_ref, long):
        return [
            Photo(*fields) for fields in
            self.fetchall(
                'SELECT * FROM Photos WHERE LatitudeRef = %s AND Latitude = %s AND LongitudeRef = %s'
                ' AND Longitude = %s ORDER BY Id DESC', (lat_ref, lat, long_ref, long))]

    def get_last_upload_time(self):
        return self.fetchone('SELECT UploadTime FROM Photos ORDER BY Id DESC', (), 0)

    def get_last_upload_time_by_user_id(self, user_id):
        return self.fetchone('SELECT UploadTime FROM Photos WHERE UserId = %s ORDER BY Id DESC', (user_id,), 0)

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
        self.execute(
            'INSERT INTO Photos (UserId, UploadTime, LatitudeRef, Latitude,'
            ' LongitudeRef, Longitude, Filename, IsFeatured) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', values)
        self.commit()

    def delete_photo_by_filename(self, filename):
        self.execute('DELETE FROM Photos WHERE Filename = %s', (filename,))
        self.commit()
