from flask import request

from constants import SERVER_DEBUG


class GeoIpResolver:
    def __init__(self, ip_to_city_path, city_to_coords_path):
        self._load_ips(ip_to_city_path)
        self._load_cities(city_to_coords_path)

    def _load_ips(self, filename):
        self._ips = []
        with open(filename, encoding='utf-8') as f:
            for line in f:
                if line:
                    ip_from, ip_to, *_, country, city = line.split()
                    if city != '-':
                        self._ips.append((int(ip_from), int(ip_to), int(city)))

    def _load_cities(self, filename):
        self._cities = {}
        with open(filename, encoding='utf-8') as f:
            for line in f:
                if line:
                    city_id, *_, lat, long = line.split()
                    self._cities[int(city_id)] = int(float(lat)), int(float(long))

    def resolve(self, ip):
        if SERVER_DEBUG and 'ip' in request.args:
            ip = request.args['ip']
        a, b, c, d = list(map(int, ip.split('.')))
        ip_value = a * 256**3 + b * 256**2 + c * 256 + d

        if not self._ips:
            return None
        lo = 0
        hi = len(self._ips)
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            ip_from, ip_to, city = self._ips[mid]
            if ip_from <= ip_value <= ip_to:
                lo = mid
                break
            elif ip_value < ip_from:
                hi = mid
            else:
                lo = mid + 1
        ip_from, ip_to, city = self._ips[lo]
        if not (ip_from <= ip_value <= ip_to):
            return None
        if city not in self._cities:
            return None
        lat, long = self._cities[city]
        return 'N', lat, 'E', long
