#!/bin/bash

AMOUT_OF_TEAMS=400

./generateArchiveNames.py $AMOUT_OF_TEAMS

IFS=$'\n'
for line in `cat archives.txt`; do
	i=`echo $line | grep -Po "^\d+"`
	new_name=`echo $line | grep -Po "\S+$"`
	mv git_team_$i.zip $new_name
done
