class GeoIPResolver:
    def __init__(self, ip_to_city_fn, city_to_coords_fn):
        self._load_cities(ip_to_city_fn)
        self._load_city_coords(city_to_coords_fn)

    def _load_cities(self, filename):
        self._cities = []
        with open(filename) as f:
            for line in f:
                if line:
                    ip_from, ip_to, *_, country, city = line.split()
                    if city != '-':
                        self._cities.append((int(ip_from), int(ip_to), int(city)))

    def _load_city_coords(self, filename):
        self._city_coords = {}
        with open(filename) as f:
            for line in f:
                if line:
                    city_id, *_, lat, long = line.split()
                    self._city_coords[int(city_id)] = int(float(lat)), int(float(long))

    def get_ip_coords(self, ip_string):
        from flask import request
        get_ip = request.args.get('ip')
        if get_ip is not None:
            ip_string = get_ip

        a, b, c, d = list(map(int, ip_string.split('.')))
        ip_value = a * 256**3 + b * 256**2 + c * 256 + d
        lo = 0
        hi = len(self._cities)
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            ip_from, ip_to, city = self._cities[mid]
            if ip_from <= ip_value <= ip_to:
                lo = mid
                break
            if ip_value < ip_from:
                hi = mid
            else:
                lo = mid + 1
        ip_from, ip_to, city = self._cities[lo]
        if not (ip_from <= ip_value <= ip_to):
            return None
        if not city in self._city_coords:
            return None
        lat, long = self._city_coords[city]
        return b'N', lat, b'E', long
