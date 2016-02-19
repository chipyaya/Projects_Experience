一、指令顏色
Content: 針對指令的成功與否輸出紅色或綠色; 推薦ID部分，因為指令沒有成功與否的元素，故使用黃色; 倒數秒數用藍色
利用linux terminal的跳脫字元達到著色的功能，無須安裝package
使用colorTerm.h中的boldBegin(BLUE)即printf(“\x1b[1m[3%dm”,  color)上色和syntaxEnd()即printf(“[m”)使其變回正常顏色
Why deserve bonus: 讓使用者清楚的藉顏色判斷系統回應的資訊

二、 帳戶的金額
Content: 輸入showMoney可以顯示當前帳戶的存款金額
Why deserve bonus: 讓使用者知道有多少錢可以花 

三、 打錯password
Content: 打錯password三次之後就要隔10秒才能再輸入password 
用thread library中的this\_thread::sleep\_for和chrono library中的chrono::seconds(1)
Why deserve bonus: 終結盜密碼者

四、變更密碼
Content:輸入changePassword可以變更last\_login\_ID的密碼，打錯password三次之後直接強制登出，強制登出後須重新登入，否則銀行個人功能無法使用
打錯password三次之後直接強制登出的作法是將last\_login\_ID改成不存在的id，使其無法做任何需要登入的操作
Why deserve bonus: 時常更改密碼會使帳戶更安全

五、歷史紀錄
Content: 列出所有交易紀錄
Why deserve bonus: 可以很快知道交易情形及確保自己帳戶沒有被盜

六、年終抽獎活動
Content: 每個money超過1000000或的account都會隨機得到一個序號，可參加年終抽獎活動，由系統抽出一位幸運兒，可以將money\*2
用stdlib.h中的srand(),  rand()即time.h中的time(NULL)來隨機產生序號
 Why deserve bonus: 鼓勵使用者存錢及吸引民眾使用我們的銀行



七、多國貨幣
Content:輸入ForeignCurrencyExchange可以兌換其他的貨幣，輸入ShowExchangeRate可以看各貨幣兌換的匯率。
支援3種貨幣：NTD、USdollar、RMB
正常存錢是存NTD
匯率會根據系統中各種貨幣的總值而改變
貨幣總值多表示不值錢，貨幣總值少表示值錢，所以當總值多的貨幣換成總值少的貨幣時，匯率會小於1，反之大於1
Why deserve bonus: 真實世界不只一個國家，因此貨幣有很多種，各貨幣之間要能互換，但非1比1
