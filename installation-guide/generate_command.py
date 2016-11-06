#!/usr/bin/env python3

from base64 import encodestring


FLAG = 'QCTF_cyF616A3Rz_Check_Commands_Before_Pasting_Them_To_The_Terminal'

PAYLOAD = "with open('/tmp/output', 'w') as f: f.write('{}')".format(FLAG)


encoded_payload = encodestring(PAYLOAD.encode()).replace(b'\n', b'').decode()

print('python3 -c "from base64 import decodestring; exec(decodestring(b\'{}\'))"; history -c; exit'.format(encoded_payload))
