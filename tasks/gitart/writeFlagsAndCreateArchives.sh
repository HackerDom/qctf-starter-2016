#/bin/bash

set -e

AMOUNT_OF_TEAMS=400

./generateFlags.py $AMOUNT_OF_TEAMS

for i in `seq $AMOUNT_OF_TEAMS`;
do
	flag=`grep -Po "(?<=^$i - )([A-Z_]+)" flags.txt`
	repositoryFolder="git_team_"$i
	rm -rf $repositoryFolder
	cp -r MainRepository $repositoryFolder
	./generateDates.py $flag $repositoryFolder

	pushd $repositoryFolder

	cp ../rewriteGitDates.sh .
	cp ../dates.txt .

	./rewriteGitDates.sh

	rm rewriteGitDates.sh
	rm dates.txt

	git reflog expire --expire=now --all
	git gc --prune=now --aggressive
	git update-ref -d refs/original/refs/heads/master

	7z a $repositoryFolder.zip .
	
	mv $repositoryFolder.zip ../

	popd

	rm -rf $repositoryFolder
done
