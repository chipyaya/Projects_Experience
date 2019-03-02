# Usage

```
$ npm i
$ npm start
```

go to <strong>localhost:3000/</strong> in your browser

# view image on terminal
```
eog bg-over.png
```

# jpg to png
```
//one
convert XX.jpg XX.png
mogrify -format png XX.jpg
//all
mogrify -format png *.jpg
```

# ImageMagick
```
convert green.jpg -fuzz 30% -transparent "rgb(0,255,0)" trans.png	//green->transparent

convert -flatten img1.png img1-white.png						//transparent->white

convert -rotate -10 snake.gif snake-10.gif

convert -fill OOO.png white opaque green XXX.png	//all green to white

convert -fill OOO.png white opaque green XXX.png	//all green to white

convert blackHat.png -fuzz 30% -alpha set -channel RGBA -fill none -opaque white result.png	//white to transparent

convert person.png -resize 400% person2.png							 //resize

convert bg.png person2.png -geometry +400+800 -composite bg-over.png //composite!!

convert -crop 500x800+280+150 chiou2.png tmp.png	// crop subimage ([size]+startx+starty)

convert ./public/img/raw.png -fill "rgb(251, 188)" -colorize 20%  ./public/img/person.png	//mask yellow

convert ./kinect_code/kinect_test_data/images/${filename}.png \( +clone -threshold -1 -negate -fill white -draw "circle ${centerX},${centerY} ${anotherX},${centerY} " \) -alpha off -compose copy_opacity -composite ./public/img/person.png	//crop circle

convert ./public/img/raw.jpg -fuzz 15% -transparent "rgb(255,255,255)" ./public/img/person.png	//remove bg
```

# Magick++
```
g++ `Magick++-config --cxxflags --cppflags` test.cpp `Magick++-config --ldflags --libs`
```

