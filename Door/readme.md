# NTUAF - Door

## Concept
> 魯蛇或溫拿的與否，決定權終究是自己而並非他人。在許多場合我們總要經過門，現在，我們將貼上魯蛇和溫拿的標籤在門上，讓經過的同學「決定自己價值」，是要通過魯蛇門呢？還是通過溫拿門？決定自己的身分後，我們將以科技藝術的方式，給予參展人視覺聽覺以及情境上的回饋，並且透過誠實指數測驗機給予參考數據，讓參展人反思自己是否如實選擇內心的聲音，而不被他人左右。

# Technique
## Polygraph machine (/lie)
### software
- kinect
	- detect head and body
	- countdown and snapshot

- web
	- slide down question
	- read heartbeat data from file
	- count win/lose score by heartbeat, answer, and time of answering
	- write number of people for each result to firebase
	- composite photo from kinect by an bg image according to the win/lose score (by imagemagick and bat script)
	- upload image to imgur and create qrcode for user to download
	- enable user to login fb and share the composite photo 

### hardware
- heartbeat detector
- notebook, ipad, kinect

## Displayer (/tv)
### software
- web
	- read the sum of people passing winner/loser door
	- get result data from firebase
	- display all statistic data

### hardware
- people entering door detector
- pc, screen

