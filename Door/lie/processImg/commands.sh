#!/bin/bash
level=$1
filename=$2
centerX=$3
centerY=$4
anotherX=$((${centerX}-200))

path='./kinect_code/NTUAF-Recognize/NTUAF-Recognize/images/'
# windows
# convert_cmd='C:/Windows/System32/ImageMagick-7.0.1-1-portable-Q16-x64/convert.exe'
# linux
convert_cmd='convert'

# convert to png
${convert_cmd} ${path}${filename}.jpeg ${path}${filename}.png

# remove bg
# convert ./public/img/raw.jpg -fuzz 15% -transparent "rgb(255,255,255)" ./public/img/person.png

# crop the circle
${convert_cmd} ${path}${filename}.png \( +clone -threshold -1 -negate -fill white -draw "circle ${centerX},${centerY} ${anotherX},${centerY} " \) -alpha off -compose copy_opacity -composite ${path}person.png

# convert -resize 150%x150%  ${path}person.png ${path}person.png

# composite 
x=$((700-${centerX}))
y=$((540-${centerY}))
${convert_cmd} ./public/img/win_loo/win_loo_${level}.png ${path}person.png -geometry +${x}+${y} -composite ./public/img/composite.png
