#!/bin/bash

set -e

AMOUNT_OF_TEAMS=400

./generateFlags.py $AMOUNT_OF_TEAMS

for i in `seq $AMOUNT_OF_TEAMS`;
do
	flag=`grep -Po "(?<=^$i - )([A-Z_]+)" flags.txt`
	teamFolder="optimization_team_"$i
	rm -rf $teamFolder

	./generator.py $flag "enc.txt"

	mkdir $teamFolder
	cp simple.py $teamFolder/decrypt.py
	cp enc.txt $teamFolder/encryption

	pushd $teamFolder
	7z a $teamFolder.zip .
	mv $teamFolder.zip ../
	popd

	rm enc.txt
	rm -rf $teamFolder
done
