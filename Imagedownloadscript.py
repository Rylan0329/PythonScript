import  requests
import  json
import  time
import  os
def encode_objurl(objurl):
    code_dic= {
			"w": "a",
			"k": "b",
			"v": "c",
			"1": "d",
			"j": "e",
			"u": "f",
			"2": "g",
			"i": "h",
			"t": "i",
			"3": "j",
			"h": "k",
			"s": "l",
			"4": "m",
			"g": "n",
			"5": "o",
			"r": "p",
			"q": "q",
			"6": "r",
			"f": "s",
			"p": "t",
			"7": "u",
			"e": "v",
			"o": "w",
			"8": "1",
			"d": "2",
			"n": "3",
			"9": "4",
			"c": "5",
			"m": "6",
			"0": "7",
			"b": "8",
			"l": "9",
			"a": "0",
		}
    objurl=objurl.replace("_z2C$q",":").replace("_z&e3B",".").replace("AzdH3F","/")
    res=""
    for c in objurl:
        if c in code_dic.keys():
            res+=code_dic[c]
        else:
            res+=c
    return res

def DownloadImg(keyword,mode,numbers):
    if mode.lower() not in ["small","big"]:
        print("模式输入错误!")
        return
    if int(numbers)>2000:
        print("太多了，扛不住!")
        return
    url = "https://image.baidu.com/search/acjson"
    pages=numbers//60 if numbers%60==0 else numbers//60+1
    pindex=1
    index = 1
    for pindex in range(1,pages+1):
        request_args = {
            "tn": "resultjson_com",
            "ipn": "rj",
            "ct": "201326592",
            "is": "",
            "fp": "result",
            "queryWord": keyword,
            "cl": 2,
            "lm": -1,
            "ie": "utf-8",
            "oe": "utf-8",
            "adpicid": "",
            "st": -1,
            "z": "",
            "ic": 0,
            "hd": "",
            "latest": "",
            "copyright": "",
            "word": keyword,
            "s": "",
            "se": "",
            "tab": "",
            "width": "",
            "height": "",
            "face": "0",
            "istype": 2,
            "qc": "",
            "nc": 1,
            "fr": "",
            "expermode": "",
            "force": "",
            "pn": pindex * 60,
            "rn": 60,
            "gsm": "1e",
            "1585198294921": "",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            , "Referer": "https://image.baidu.com"
        }
        response=requests.get(url=url,headers=headers,params=request_args)
        if response.status_code==200:
            data_list=list(filter(lambda x:x.keys().__len__()>0,json.loads(response.text,encoding="utf-8")["data"]))
            for item in data_list:
                imgsrc=item["thumbURL"] if mode.lower()=="small" else encode_objurl(item["objURL"])
                ext_name=imgsrc[imgsrc.rindex("."):].split("?")[0]#扩展名
                path="./"+keyword+mode.lower()+"_imgs/"
                if not os.path.exists(path):
                    os.mkdir(path)
                filename=path+keyword+str(index)+ext_name
                try:
                    with open(filename,"wb") as wstream:
                        headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                        }
                        try:
                            imgresponse = requests.get(url=imgsrc, headers=headers,timeout=4)
                            wstream.write(imgresponse.content)
                            print(filename)
                            index += 1
                        except Exception:
                            print("网络迷失了方向")
                except Exception:
                    print("出错啦,写入失败")
            print("保存了" + str(pindex) + "页," + str(index-1) + "张图片")
            time.sleep(2)
        else:
            print("网络迷失了方向")
            return

if __name__ == '__main__':
    #author：睿吉吉
    #date:2020年3月26日
    #version:1.0.0
    print("**********************Image download script**********************")
    keword=input("请输入要下载的图片关键字:")
    mode=input("请输入模式:small or big? [small 缩略图(速度杠杠滴)  big高清大图(略慢,质量杠杠滴)]")
    try:
        numbers=int(input("请输入图片下载数量:"))
        print("任务创建成功->关键字:"+keword+"   数量:"+str(numbers))
        DownloadImg(keword,mode,numbers)
        print("下载完毕，over!")
    except Exception:
        print("不要乱输入，不让你下了，拜拜┏(＾0＾)┛")
        exit(0)

