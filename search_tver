#!/bin/bash
export IFS=$'\n'
keyword=`urlencode $1`
for url in `requests-html-get-html "https://tver.jp/search/catchup?keyword=${keyword}" HTML | grep -Po '(?<=href=")[^"]*' | grep -e corner -e feature` ; do
	echo 'https://tver.jp'$url
done
