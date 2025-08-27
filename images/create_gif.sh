#!/bin/bash
#
# install:
#
#   sudo apt install imagemagick

name="$1"
files=$(ls -v $name*.png | tr '\n' ' ')
files_gv=$(ls -v $name*.gv | tr '\n' ' ')
echo "creating gif with:"
echo "$files"

largest_size=$(identify -format "%H %Wx%H %f\n" $name*.png | sort -nr | head -n1| awk '{print $2}')
echo "largest_size: $largest_size"

echo "resizing images"
mogrify -resize $largest_size -background white -gravity center -extent $largest_size $files

echo "creating file: $name.gif"
convert -delay 150 -dither None -loop 0 $files $name.gif

if [ "$2" = "-d" ]; then
    echo "deleting: $files $files_gv"
    rm $files $files_gv
fi

echo "done"
