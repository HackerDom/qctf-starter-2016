from constants import MEMCACHED_EXPIRATION_TIME, MEMCACHED_MIN_COMPRESS_LEN


def serialize_photo_list(photos):
    return ','.join(str(photo.id) for photo in photos)


def deserialize_photo_list(value):
    if not value.strip():
        return []
    return list(map(int, value.split(',')))


class PhotoCache:
    def __init__(self, memcache_client, photo_service):
        self._client = memcache_client
        self._photo_service = photo_service
        self.get_photos_by_user_id = self._wrap_photo_list_getter(
            photo_service.get_photos_by_user_id, 'users_photos:{0}')
        self.get_photos_by_coordinates = self._wrap_photo_list_getter(
            photo_service.get_photos_by_coordinates, 'photos_from_place:{1}{0}_{3}{2}')

    def _get(self, key):
        try:
            value = self._client.get(key)
        except Exception:
            value = None
        return value

    def _set(self, key, value):
        self._client.set(key, value, time=MEMCACHED_EXPIRATION_TIME, min_compress_len=MEMCACHED_MIN_COMPRESS_LEN)

    def _delete(self, key):
        self._client.delete(key)

    def _wrap_photo_list_getter(self, f, key_fmt):
        def wrapped(*args, **kwargs):
            key = key_fmt.format(*args, **kwargs)
            value = self._get(key)
            if not value:
                value = serialize_photo_list(f(*args, **kwargs))
                self._set(key, value)
            return deserialize_photo_list(value)
        return wrapped

    def get_filename_by_id(self, photo_id):
        key = 'filename:{}'.format(photo_id)
        value = self._get(key)
        if not value:
            photo = self._photo_service.get_photo_by_id(photo_id)
            if photo is not None:
                value = photo.filename
            self._set(key, value)
        return value

    def invalidate(self, updated_photo):
        self._delete('users_photos:{0}'.format(updated_photo.user_id))
        self._delete('photos_from_place:{0}{1}_{2}{3}'.format(
            updated_photo.latitude_ref,
            updated_photo.latitude,
            updated_photo.longitude_ref,
            updated_photo.longitude))
