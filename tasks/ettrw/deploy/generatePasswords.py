#!/usr/bin/python3

import random
import sys
import json
import string

PASSWORD_LEN = 10
CHARS = string.ascii_letters + string.digits

def main():
    random.seed(23456)

    if len(sys.argv) < 2:
        print("Usage:\n{} amount_of_teams".format(sys.argv[0]))
        sys.exit()
    amount_of_teams = int(sys.argv[1])

    ordered_passwords = []
    passwords = set()
    while len(passwords) < amount_of_teams:
        curr_pass = ''.join([random.choice(CHARS) for _ in range(PASSWORD_LEN)])
        if curr_pass not in passwords:
            ordered_passwords.append(curr_pass)
            passwords.add(curr_pass)

    passwordsByTeamId = dict()
    for i, password in enumerate(ordered_passwords):
        passwordsByTeamId[i + 1] = password

    with open('passwords.json', 'w') as f:
        data = json.dumps(passwordsByTeamId, indent=4)
        f.write(data + '\n')
    
    with open('passwords.txt', 'w') as f:
        lines = ['{} - {}\n'.format(i, f) for i, f in  passwordsByTeamId.items()]
        f.write(''.join(lines))
        
if __name__ == "__main__":
    main()
