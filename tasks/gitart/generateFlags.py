#!/usr/bin/python3

import random
import sys
import json

VALID_LETTERS = "ABCDEFGHIJKLOPQRSTUVXYZ" # The others don't look good in pixel-art
FLAG_RANDOM_PART_LEN = 8

def main():
    random.seed(37182)
    if len(sys.argv) < 2:
        print("Usage:\n{} amount_of_teams".format(sys.argv[0]))
        sys.exit()
    amount_of_teams = int(sys.argv[1])

    ordered_flags = []
    flags = set()
    while len(flags) < amount_of_teams:
        curr_flag = 'QCTF_' + ''.join([random.choice(VALID_LETTERS) for _ in range(FLAG_RANDOM_PART_LEN)])
        if curr_flag not in flags:
            ordered_flags.append(curr_flag)
            flags.add(curr_flag)

    flagsByTeamId = dict()
    for i, flag in enumerate(ordered_flags):
        flagsByTeamId[i + 1] = flag

    with open('flags.json', 'w') as f:
        data = json.dumps(flagsByTeamId, indent=4)
        f.write(data + '\n')
    
    with open('flags.txt', 'w') as f:
        lines = ['{} - {}\n'.format(i, f) for i, f in  flagsByTeamId.items()]
        f.write(''.join(lines))
        
if __name__ == "__main__":
    main()
