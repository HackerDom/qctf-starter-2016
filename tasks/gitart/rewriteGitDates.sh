#!/bin/bash
#!/bin/sh

git filter-branch --env-filter '
	curr_dir=`pwd`
	cd ../..
	date=`grep -Po "(?<=$GIT_COMMIT ).*" dates.txt`
	echo " New date: \"$date\""
    export GIT_COMMITTER_DATE="$date"
    export GIT_AUTHOR_DATE="$date"
	cd $curr_dir
' --tag-name-filter cat -- --branches --tags
