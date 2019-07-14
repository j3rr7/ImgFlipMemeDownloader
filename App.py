import os, time, threading, logging, json, requests
print("=========================================================")
print(" _              ___ _ _                                  ") 
print("(_)            / __) (_)                                 ")
print(" _ ____   ____| |__| |_ ____     ____   ____ ____   ____ ")
print("| |    \ / _  |  __) | |  _ \   |    \ / _  )    \ / _  )")
print("| | | | ( ( | | |  | | | | | |  | | | ( (/ /| | | ( (/ / ")
print("|_|_|_|_|\_|| |_|  |_|_| ||_/   |_|_|_|\____)_|_|_|\____)")
print("        (_____|        |_|                               ")
print("=========================================================")
try:
    how_much = int(input("[Default 100]How Much :"))
except ValueError:
    how_much = 100

api_url_imgflip = 'https://api.imgflip.com/get_memes'
datas = ''
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

logging.info("[Information] Check if data.json is exists")
if os.path.exists('data.json'):
    logging.info("[Information] Found data.json")
    with open('data.json','r') as load:
        datas = json.load(load)
    logging.info("[Information] Data Loaded")
else:
    try:
        r = requests.get(api_url_imgflip,timeout=30)
        logging.info("[Information] Awaiting Information From API Endpoint")
        datas = json.loads(r.content.decode('utf-8'))
        with open('data.json','w', encoding='utf-8') as save:
            json.dump(datas,save,ensure_ascii=False,indent=4)
        logging.info("[Information] Data Loaded")
    except Exception:
        logging.error("[ERROR] Error Parsing Data")

hasil = datas['success']

i = 1

try:
    if hasil == True:
        logging.info("[Information] Getting information from API endpoint")
        for hasil in datas['data']['memes']:
            ID = hasil['id']
            name = hasil['name']
            url = hasil['url']
            width = hasil['width']
            height = hasil['height']
            box_count = hasil['box_count']
            #filename = '{}.jpg'.format(ID)
            filename = '{0} {1} {2}x{3}.jpg'.format(i,name,width,height)
            #logging.info("[Information] Get Image Url from API")
            Picture_request = requests.get(url)
            if Picture_request.status_code == 200:
                #logging.info("[Information] Image Loaded")
                with open(filename,'wb') as savePic:
                    savePic.write(Picture_request.content)
                    logging.warn("[Information] {} Image Downloaded".format(i))
                    i += 1
                    if i-1 >= how_much:
                        break
            else:
                logging.error("[ERROR] Request Failed")
                print("Exiting...")
                time.sleep(1)
                exit()
    else:
        logging.error("[ERROR] Cannot Parse Data from Api")
        #print(datas['success'])
        print("Some hopefully-useful statement about why it failed : ")
        print(datas['error_message'])
except Exception as e:
    print(e)
