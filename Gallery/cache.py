from models import CachedPhotoInfo


class PhotoCache:
    def __init__(self, memcache_client, photos_service):
        self.client = memcache_client
        self.photos_service = photos_service

        self.get_photos_by_user_id = self.wrap_photo_list_getter(
            photos_service.get_photos_by_user_id, 'users_photos:{0}')
        self.get_photos_by_coordinates = self.wrap_photo_list_getter(
            photos_service.get_photos_by_coordinates, 'photos_from_place:{1}{0}_{3}{2}')

    def get(self, key):
        try:
            value = self.client.get(key)
        except Exception:
            value = None
        print('get', key, value)
        return value

    def set(self, key, value):
        print('set', key, value)
        self.client.set(key, value, time=60, min_compress_len=1000)

    def delete(self, key):
        print('delete', key)
        self.client.delete(key)

    def get_photo_list(self, key):
        value = self.get(key)
        if not value:
            return None
        photos = []
        for photo in value.split(','):
            id, user_id = photo.split('-')
            photos.append(CachedPhotoInfo(int(id), user_id))
        return photos

    def set_photo_list(self, key, photos):
        value = ','.join('{}-{}'.format(photo.id, photo.user_id) for photo in photos)
        self.set(key, value)

    def get_filename_by_id(self, id):
        key = 'filename:{}'.format(id)
        value = self.get(key)
        if not value:
            value = self.photos_service.get_photo_by_id(id).filename
            self.set(key, value)
            value = self.get(key)
        return value

    def wrap_photo_list_getter(self, method, key_fmt):
        def wrapped(*args, **kwargs):
            key = key_fmt.format(*args, **kwargs)
            value = self.get_photo_list(key)
            if not value:
                value = method(*args, **kwargs)
                self.set_photo_list(key, value)
                value = self.get_photo_list(key)
            return value
        return wrapped
