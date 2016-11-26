import functools
import datetime
import random
import hashlib

from flask import request, render_template, make_response, redirect

from models import Photo
from utils import encode_jwt, decode_jwt, check_jwt, extract_coordinates_from_jpeg, get_nearby_coordinates
from constants import MAX_PHOTO_SIZE, USERNAME_RE, PHOTO_DIR


def is_logged_in():
    return check_jwt(request.cookies.get('jwt'))


def current_user_id():
    if not is_logged_in():
        return None
    return decode_jwt(request.cookies.get('jwt'))['user_id']


class Controllers:
    def __init__(self, user_service, photo_service, photo_cache, geoip_resolver):
        self.user_service = user_service
        self.photo_service = photo_service
        self.photo_cache = photo_cache
        self.geoip_resolver = geoip_resolver

        self.root = self.require_login(self.root)
        self.my = self.require_login(self.my)
        self.featured = self.require_login(self.featured)
        self.nearby = self.require_login(self.nearby)
        self.upload = self.require_login(self.upload)

    def log_in(self, username):
        user_id = self.user_service.get_user_id_by_username(username)
        response = make_response(redirect('/my'))
        response.set_cookie('jwt', encode_jwt(user_id, username))
        return response

    def log_out(self):
        response = make_response(redirect('/login'))
        response.set_cookie('jwt', '')
        return response

    def require_login(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not is_logged_in():
                return redirect('/login')
            user_id = decode_jwt(request.cookies.get('jwt'))['user_id']
            if self.user_service.get_user_by_user_id(user_id) is None:
                return self.log_out()
            return f(*args, **kwargs)
        return wrapper

    def login(self):
        if is_logged_in():
            return redirect('/my')
        if request.method == 'GET':
            return render_template('login.html')

        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('login.html', error_message='Username and password should be non-empty')
        if not self.user_service.is_password_correct(username, password):
            return render_template('login.html', error_message='Incorrect credentials')

        return self.log_in(username)

    def logout(self):
        return self.log_out()

    def register(self):
        if request.method == 'GET':
            return render_template('register.html')

        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('register.html', error_message='Username and password should be non-empty')
        if not USERNAME_RE.match(username):
            return render_template(
                'register.html',
                error_message='Username should be 4 or more digits, numbers, dashes or underscores')
        if self.user_service.username_exists(username):
            return render_template('register.html', error_message='Username already exists')
        if not self.user_service.add_user(username, password):
            return render_template('register.html', error_message='Could not register')

        return self.log_in(username)

    def root(self):
        return redirect('/my')

    def show_photos(self, title, ids=None, photos=None):
        if ids is None:
            if photos is None:
                raise ValueError('Neither ids nor photos is provided')
            ids = [photo.id for photo in photos]
        filenames = [self.photo_cache.get_filename_by_id(id) for id in ids]
        username = self.user_service.get_username_by_user_id(current_user_id())
        return render_template('photos.html', title=title, filenames=filenames, username=username)

    def my(self):
        return self.show_photos('My photos', ids=self.photo_cache.get_photos_by_user_id(current_user_id()))

    def featured(self):
        return self.show_photos('Featured photos', photos=self.photo_service.get_featured_photos())

    def nearby(self):
        ids = []
        current_coordinates = self.geoip_resolver.resolve(request.remote_addr)
        if current_coordinates is not None:
            for nearby_coordinates in get_nearby_coordinates(*current_coordinates):
                ids.extend(self.photo_cache.get_photos_by_coordinates(*nearby_coordinates))
        return self.show_photos('Nearby photos', ids=ids)

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
        with open(PHOTO_DIR + filename, 'wb') as f:
            f.write(file_bytes)
        photo = Photo(None, user_id, upload_time, *coords, filename, False)
        if self.photo_service.add_photo(photo) is None:
            return render_template('upload.html', error_message='Failed to upload the photo')
        try:
            self.photo_cache.invalidate(photo)
        except Exception:
            pass
        return redirect('/my')
