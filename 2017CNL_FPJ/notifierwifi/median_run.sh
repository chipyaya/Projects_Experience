echo '[' > tmp_result
for (( i=0; i < 2; ++i ))
do
    node wifi_scan.js >> tmp_result
    echo ',' >> tmp_result
done
node wifi_scan.js >> tmp_result
echo ']' >> tmp_result

python process.py > networks.json
open -a "/Applications/Google Chrome.app" `node redirect1.js` #for macOS
#google-chrome `node redirect1.js` #for ubuntu

rm -f tmp_result
