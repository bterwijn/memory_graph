#!/bin/bash
#
# install:
#
#   sudo apt install imagemagick

name="$1"
files=$(ls $name*.png)
echo "creating gif with:"
echo "$files"

largest_size=$(identify -format "%Wx%H %f\n" $name*.png | sort -nr | head -n1)
echo "largest_size: $largest_size"

echo "resizing images"
mogrify -resize $largest_size -background white -gravity center -extent $largest_size $name*.png
echo "creating file: $name.gif"
convert -delay 150 -loop 0 $name*.png $name.gif
echo "done"
