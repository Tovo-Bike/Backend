# API

## 使用者

### "/user"

獲得使用者歷史紀錄

* method: GET
* args: 
    * "uid" (int) - please pass with url
* return: array of json with keys below
    * "taker" : name (string)
    * "rider" : name (string)
    * "taker_score" (int)
    * "rider_score" (int)
    * "start_time" (datetime)
    * "end_time" (datetime)
    * "duration" : minutes (int)

### "/user/all"

獲得自己以外的使用者清單

* method: GET
* args:
    * "uid" (int) - please pass with url
* return: array of json
    * "uid" (int)
    * "name" (string)

### "/user/create"

註冊新使用者

* method: POST
* args:
    * "email" (string)
    * "name" (string)
    * "password" (string)
* return: none

### "/user/login"

登入

* method: POST
* args:
    * "name" (string)
    * "password" (string)
* return: json
    * "uid" : user ID (int)
    * "name" (string)

### "/user/set"

設定體重

* method: POST
* args: json
    * "uid" (int)
    * "weight" (int)
* return: none

## 旅程

### "/trip"

查看還沒有人接的單

* method: GET
* args: none
* return:
    * "tid" : trip ID (int)
    * "name" (string)
    * "weight" (int)
    * "slon" : starting longitude (float)
    * "slat" : starting latitude (float)
    * "elon" : ending longitude (float)
    * "elat" : ending latitude (float)

### "/trip/go"

新增旅程

* method: POST
* args: 
    * "uid" (int)
    * "slon" (float)
    * "slat" (float)
    * "elon" (float)
    * "elat" (float)
* return:
    * "tid" : trip ID (int)

### "/trip/accept"

接單

* method: POST
* args:
    * "uid" (int)
    * "tid" (int)
* return: none

### "/trip/start"

旅程開始

* method: POST
* args:
    * "tid" (int)
* return: none

### "/trip/end"

旅程結束

* method: POST
* args: 
    * "tid" (int)
* return: none

### "/trip/rate"

評分，自動自動判斷誰評誰

* method: POST
* args: 
    * "tid" : trip ID (int)
    * "uid" : user ID (int)
    * "point" (int)
* return: none

## 獎賞

### "/buy"

買 title

* method: POST
* args: 
    * "uid" (int)
    * "ttid" : title ID (int)
* return: none

### "/equip"

裝備 title

* method: POST
* args:
    * "uid" (int)
    * "ttid" (int)
* return none

### "/give"

轉錢

* method: POST
* args:
    * "uid" : user ID (int)
    * "u2id" : user2 ID (int)
    * "amount" (int)
    * "unit" : "gear" or "rose" (string)
* return: none

### "/titles"

查看可購買的 titles

* method: GET
* args: none
* return: array of json
    * "ttid" : title ID (int)
    * "name" (string)
    * "price" (iny)
    * "job" : "Taker" or "Rider" (string)

### "/rank/taker"

* method: GET
* args: none
* return: array of json
    * "name" (string)
    * "title" (string)
    * "gear" (int)

### "/rank/rider"

* method: GET
* args: none
* return: array of json
    * "name" (string)
    * "title" (string)
    * "rose" (int)
