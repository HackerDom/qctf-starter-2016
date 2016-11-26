class Photo:
    def __init__(self, id, user_id, upload_time, latitude_ref, latitude, longitude_ref, longitude, filename, is_featured):
        self.id = id
        self.user_id = user_id
        self.upload_time = upload_time
        self.latitude_ref = latitude_ref
        self.latitude = latitude
        self.longitude_ref = longitude_ref
        self.longitude = longitude
        self.filename = filename
        self.is_featured = is_featured
