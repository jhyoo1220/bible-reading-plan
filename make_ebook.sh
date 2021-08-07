#!/bin/bash
#$1: kor_new_trans
#$2: false
echo "Bible type: $1"
echo "Does it have verse number? $2"

rm ./ebook/readings_*
rm ./ebook/*.epub
python3 ./bible_reading_plain/bible_reading_plain.py $1 ./ebook $2

cd ./ebook

if [ $1 = "kor_new_trans" ]
then
  python3 ../../ebookmaker/ebookmaker.py kor_new.json
elif [ $1 = "kor_revised" ]
then
  python3 ../../ebookmaker/ebookmaker.py kor_rev.json
else
  echo "Please use the following DB options:"
  echo "kor_new_trans, kor_revised"
  exit 1
fi
