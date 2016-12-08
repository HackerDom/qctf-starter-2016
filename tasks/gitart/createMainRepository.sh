#!/bin/bash

AMOUNT_OF_COMMITS=984

set -e

rm -rf MainRepository
mkdir MainRepository
pushd MainRepository

git init
git config --local user.name "John Doe"
git config --local user.email "licorice@coordinator.form"

cp ../GithubScreenshot/54e96209faf85710ebcc.png .
git add -A
git commit -m "Initial commit"

for i in `seq $AMOUNT_OF_COMMITS`;
do
	id=(`shuf -i 100-5000 -n 1`)
	git commit --allow-empty -m "Issue #$id: Fix"
done

git reflog expire --expire=now --all
git gc --prune=now --aggressive

popd
