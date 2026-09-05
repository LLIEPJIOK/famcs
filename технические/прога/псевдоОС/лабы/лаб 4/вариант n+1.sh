#!/bin/bash

if [ $# -ne 3 ]
then 
	echo "Invalid number of argument!"
	exit 1
fi

if [ -e $1 ]
then 
	if [ -f $3 ]
	then
		find -type f -name "*$2*" > $3
	else
		echo "No file to write result"
		exit 1
	fi
else
	echo "No such directory"
	exit 1
fi


