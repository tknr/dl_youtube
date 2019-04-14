#!/bin/bash
export IFS=$'\n'
DIR=$(cd $(dirname $0); pwd)
cd $DIR
CMDNAME=`basename $0`
FILENAME_QUEUE="queue_youtube.txt"
if [ $# -ne 0 ]; then
    ${FILENAME_QUEUE}=${1}
fi
echo "reading from "${FILENAME_QUEUE}"..."

for LINE in `cat ${FILENAME_QUEUE} | grep -v "^#"`
do

        TITLE=`echo ${LINE} | cut -d "," -f 1`
	URL=`echo ${LINE} | cut -d "," -f 2`

	if [ ${TITLE} = ${URL} ] ; then 
		TITLE=''
	fi


	echo ${TITLE}
	echo ${URL}

	echo ${#TITLE}
	echo ${#URL}

        if [ ${#URL} -lt 2 ] ; then
                continue
        fi

	if [ ${#TITLE} = 0 ] ; then
		youtube-dl --list-format ${URL} || continue
		youtube-dl --encoding utf-8 ${URL} || continue

	else
		youtube-dl --encoding utf-8 ${URL} -o ${TITLE}.mp4 || continue
	fi

	sed -i -e "s|${LINE}|#${LINE}|g" ${FILENAME_QUEUE}
done
