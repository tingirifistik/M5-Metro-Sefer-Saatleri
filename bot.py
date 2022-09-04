import requests
from os import environ

token = environ.get("TOKEN")

def trtoeng(text):
    harf = {"ç":"c", "ğ":"g", "ı":"i", "ö":"o", "ş":"s", "ü":"u", "-":"", " ":""}
    for i in text:
        if i in harf.keys():
            text = (text.replace(i, harf[i]))
    return(text)
        
duraklar = {
    "uskudar": "122",
    "fistikagaci": "123",
    "baglarbasi": "124",
    "altunizade": "125",
    "kisikli": "126",
    "bulgurlu": "127",
    "umraniye": "128",
    "carsi": "129",
    "yamanevler": "130",
    "cakmak": "131",
    "ihlamurkuyu": "132",
    "altinsehir": "133",
    "imamhatip": "134",
    "dudullu": "135",
    "necipfazil": "136",
    "cekmekoy": "137"
}


def getUpdate():
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
    r = requests.get(url)
    x = 0
    while 1 :
        try:
            r.json()["result"][x]
            x+=1
        except IndexError:
            return (r.json()["result"][x-1]["message"]["chat"]["id"]), r.json()["result"][x-1]["message"]["text"], (r.json()["result"][x-1]["message"]["date"])

def sendMessage(text, id):
    requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text=" + text, timeout=3)
    
date_list = []
while 1:
    try:
        id, text, date = getUpdate()
        if text == "/saat" and date not in date_list:
            setcookie = requests.get("https://www.metro.istanbul:443/SeferDurumlari/SeferDetaylari")
            kod = str(setcookie.text).split("kod")[1].split(")")[0].split("'")[1]
            aspnet = str(setcookie.cookies["ASP.NET_SessionId"])
            date_list.append(date)
            sendMessage("Hangi durakta bekliyorsunuz? ", id)
            while True:
                id, text, date = getUpdate()
                if date not in date_list:
                    date_list.append(date)
                    durak = duraklar[trtoeng(text.lower())]
                    sendMessage("Hangi yöne gitmek istiyorsunuz ?", id)
                    while 1:
                        id, text, date = getUpdate()
                        if date not in date_list:
                            date_list.append(date)
                            yonsec = trtoeng(text.lower())
                            if yonsec == "cekmekoy" or yonsec == "uskudar":
                                if yonsec == "cekmekoy":
                                    yon = "40"
                                elif yonsec == "uskudar":
                                    yon = "41"
                                url = "https://www.metro.istanbul/SeferDurumlari/AJAXSeferGetir"
                                cookies = {"ASP.NET_SessionId": aspnet}
                                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "X-Requested-With": "XMLHttpRequest", "Content-Type": "multipart/form-data; boundary=---------------------------", "Origin": "https://www.metro.istanbul", "Dnt": "1", "Referer": "https://www.metro.istanbul/SeferDurumlari/SeferDetaylari", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers"}
                                data = f"-----------------------------\r\nContent-Disposition: form-data; name=\"secim\"\r\n\r\n1\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"saat\"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"dakika\"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"tarih1\"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"tarih2\"\r\n\r\n04.09.2022\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"station\"\r\n\r\n{durak}\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"route\"\r\n\r\n{yon}\r\n-----------------------------\r\nContent-Disposition: form-data; name=\"kod\"\r\n\r\n{kod}\r\n-----------------------------\r\n"
                                jsonfile = requests.post(url, headers=headers, cookies=cookies, data=data)
                                saatler = ""
                                x = 0
                                while 1:
                                    try:
                                        saatler+=(str(jsonfile.json()["sefer"][x]["zaman"])+"\n")
                                        x+=1
                                    except:
                                        break
                                sendMessage(saatler, id)
                                break
                            else:
                                sendMessage("Geçerli bir yön yazınız!", id)
                                break
                elif text != "/saat" and trtoeng(text.lower()) not in duraklar.keys():
                    if yonsec != "":
                        break
                    date_list.append(date)
                    sendMessage("Geçerli bir durak ismi yazınız!", id)
                    break
                elif text != "/saat" and date in date_list:
                    break
        
        elif text == "/start" and date not in date_list:
            date_list.append(date)
            sendMessage("Benim görevim size metronun durağa geliş saatini söylemek.\nKomutlarımı görmek için '/help' yazınız.", id)   
        
        elif text == "/help" and date not in date_list:
            date_list.append(date)
            sendMessage("/saat --> Metronun durağa geliş saatini söyler.", id)
                                
        elif text != "/saat" and text != "/start" and text != "/help" and date not in date_list:
            date_list.append(date)
            sendMessage("Yazdığınızı anlayamadım.", id)                
    except:
        pass
