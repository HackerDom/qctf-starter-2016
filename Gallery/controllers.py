import functools
import datetime
import random
import hashlib

from flask import render_template, redirect, request

from models import Photo
from utils import encode_jwt, decode_jwt, check_jwt, extract_coordinates_from_jpeg, get_nearby_coordinates
from constants import MAX_PHOTO_SIZE


def require_login(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not check_jwt(request.cookies.get('jwt')):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper


def current_user_id():
    token = request.cookies.get('jwt')
    if not check_jwt(token):
        return None
    payload = decode_jwt(token)
    if not isinstance(payload, dict):
        return None
    return payload.get('user_id')


def invalidate_cache(photo, photo_cache):
    photo_cache.delete('users_photos:{0}'.format(photo.user_id))
    photo_cache.delete(
        'photos_from_place:{1}{0}_{3}{2}'
        .format(photo.latitude_ref, photo.latitude, photo.longitude_ref, photo.longitude))


class Controllers:
    def __init__(self, app, users_service, photos_service, photos_cache, geoip_resolver):
        self.app = app
        self.users_service = users_service
        self.photos_service = photos_service
        self.photos_cache = photos_cache
        self.geoip_resolver = geoip_resolver

    def login(self):
        if check_jwt(request.cookies.get('jwt')):
            return redirect('/my')
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('login.html')
        if not self.users_service.is_password_correct(username, password):
            return render_template('login.html', error_message='Incorrent credentials')

        response = self.app.make_response(redirect('/my'))
        response.set_cookie('jwt', encode_jwt(self.users_service.get_user_id_by_username(username), username))
        return response

    def logout(self):
        response = self.app.make_response(redirect('/login'))
        response.set_cookie('jwt', '', expires='')
        return response

    def register(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('register.html')
        if self.users_service.does_username_exist(username):
            return render_template('register.html', error_message='Username already exists')

        if not self.users_service.add_user(username, password):
            return render_template('register.html', error_message='Could not register')

        response = self.app.make_response(redirect('/my'))
        response.set_cookie('jwt', encode_jwt(self.users_service.get_user_id_by_username(username), username))
        return response

    @require_login
    def root(self):
        return redirect('/my')

    def show_photos(self, title, cached_photos):
        filenames = []
        for cached_photo in cached_photos:
            filename = self.photos_cache.get_filename_by_id(cached_photo.id)
            if not filename:
                filename = self.photos_service.get_photo_by_id(cached_photo.id).filename
            filenames.append(filename)
        username = self.users_service.get_username_by_user_id(current_user_id())
        return render_template('photos.html', title=title, filenames=filenames, username=username)

    @require_login
    def my(self):
        photos = self.photos_cache.get_photos_by_user_id(current_user_id())
        if not photos:
            photos = self.photos_service.get_photos_by_user_id(current_user_id())
        return self.show_photos('My photos', photos)

    @require_login
    def featured(self):
        return self.show_photos('Featured photos',
            self.photos_service.get_featured_photos())

    @require_login
    def nearby(self):
        results = []
        current_coordinates = self.geoip_resolver.get_ip_coords(request.remote_addr)
        if current_coordinates is not None:
            for nearby_coordinates in get_nearby_coordinates(*current_coordinates):
                photos = self.photos_cache.get_photos_by_coordinates(*nearby_coordinates)
                if not photos:
                    photos = self.photos_service.get_photos_by_coordinates(*nearby_coordinates)
                results.extend(photos)
        return self.show_photos('Nearby photos', results)

    @require_login
    def upload(self):
        if request.method == 'GET':
            return render_template('upload.html')

        file = request.files.get('file')
        if not file or not file.filename:
            return render_template('upload.html', error_message='No file provided')
        if not file.filename.endswith('.jpg') and not file.filename.endswith('jpeg'):
            return render_template('upload.html', error_message='Sorry, only JPEG images are currently supported')
        file_bytes = file.read(MAX_PHOTO_SIZE + 1)
        if len(file_bytes) == MAX_PHOTO_SIZE + 1:
            return render_template('upload.html', error_message='Image is too large (>{} bytes)'.format(MAX_PHOTO_SIZE))

        try:
            coords = extract_coordinates_from_jpeg(file_bytes)
        except Exception:
            return render_template('upload.html', error_message='Failed to extract a geotag from the photo')
        if coords is None:
            return render_template('upload.html', error_message='Your photo doesn\'t have a geotag')

        user_id = current_user_id()
        upload_time = datetime.datetime.utcnow()
        filename = hashlib.sha256(str(random.random()).encode()).hexdigest()[:10] + '.jpg'
        with open('static/photos/' + filename, 'wb') as f:
            f.write(file_bytes)
        photo = Photo(None, user_id, upload_time, *coords, filename, False)
        if self.photos_service.add_photo(photo) is None:
            return render_template('upload.html', error_message='Failed to upload the photo')
        invalidate_cache(photo, self.photos_cache)
        return redirect('/my')
