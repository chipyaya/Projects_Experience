#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "usage : $0 [studentID]"
	echo "example : $0 b03902123"
	exit 0
fi

mkdir $1
cp *.cpp *.h Makefile $1 || (rm -r $1 && exit 0)
tar jcvf $1.tar.bz2 $1 || (rm -r $1 && exit 0)
rm -r $1
echo "***[Done.]***"
