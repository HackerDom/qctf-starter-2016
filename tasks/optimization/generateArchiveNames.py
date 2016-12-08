#!/usr/bin/python3

import random
import sys
import json
import string
from hashlib import md5

SALT = "c742bf0fea369014f325de781a5109f2"

def main():
    if len(sys.argv) < 2:
        print("Usage:\n{} amount_of_teams".format(sys.argv[0]))
        sys.exit()
    amount_of_teams = int(sys.argv[1])

    namesByTeamId = {}
    for i in range(1, amount_of_teams + 1):
        namesByTeamId[i] = md5((str(i) + SALT).encode()).hexdigest() + '.zip'
    
    with open('archives.json', 'w') as f:
        data = json.dumps(namesByTeamId, indent=4)
        f.write(data + '\n')

    with open('archives.txt', 'w') as f:
        for k, v in namesByTeamId.items():
            f.write('{} - {}\n'.format(k, v))
    
if __name__ == "__main__":
    main()
