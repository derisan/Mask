# telebot.py

import telepot
from xml.etree import ElementTree
import urllib
import http.client
import time

key = '10f20300cd90416e867ff580b1718c2d'
baseurl = 'http://openapi.gg.go.kr/PubMaskSaleStus?KEY='+key
TOKEN = '1261532498:AAH5G49y0ly7TqBfqQxx5JSuTDlI-tkc_fE'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getDataByName(name_param):
    res_list = []

    conn = http.client.HTTPSConnection("openapi.gg.go.kr")
    for i in range(1, 8 + 1):
        conn.request("GET","/PubMaskSaleStus?KEY=10f20300cd90416e867ff580b1718c2d&pSize=1000&pIndex=" + str(i))
        req = conn.getresponse()

        if (req.status == 200):
            tree = ElementTree.fromstring(req.read())
            rowElements = tree.iter("row")

            for row in rowElements:
                salePlace = row.find("SALE_PLC")
                if salePlace.text.find(name_param) >= 0:
                    res_list.append(row)

    return res_list

def getDataByRegion(loc_param):
    res_list = []

    conn = http.client.HTTPSConnection("openapi.gg.go.kr")
    for i in range(1, 8 + 1):
        conn.request("GET","/PubMaskSaleStus?KEY=10f20300cd90416e867ff580b1718c2d&pSize=1000&pIndex=" + str(i))
        req = conn.getresponse()

        if (req.status == 200):
            tree = ElementTree.fromstring(req.read())
            rowElements = tree.iter("row")

            for row in rowElements:
                addr = row.find("REFINE_LOTNO_ADDR")
                if addr.text.find(loc_param) >= 0:
                    res_list.append(row)

    return res_list

def replyDataByName(user, name_param='정왕'):
    row_list = getDataByName( name_param )
    msg = ''
    
    for row in row_list:
        sp = str(row.find("SALE_PLC").text)
        addr = str(row.find("REFINE_LOTNO_ADDR").text)
        time = str(row.find("WRHOUSNG_TM").text)
        state = str(row.find("REMNDR_STATE_DIV_NM").text)

        msg = '판매장소: ' + sp + '\n'
        msg += '주소: ' + addr + '\n'
        msg += '입고시간: ' + time + '\n'
        msg += '재고상태: ' + state + '\n\n'
        bot.sendMessage(user, msg)

    bot.sendMessage( user, '데이터 출력 완료' )


def replyDataByRegion(user, loc_param='정왕동'):
    row_list = getDataByRegion( loc_param )
    msg = ''
    
    for row in row_list:
        sp = str(row.find("SALE_PLC").text)
        addr = str(row.find("REFINE_LOTNO_ADDR").text)
        time = str(row.find("WRHOUSNG_TM").text)
        state = str(row.find("REMNDR_STATE_DIV_NM").text)

        msg = '판매장소: ' + sp + '\n'
        msg += '주소: ' + addr + '\n'
        msg += '입고시간: ' + time + '\n'
        msg += '재고상태: ' + state + '\n\n'
        bot.sendMessage(user, msg)

    bot.sendMessage( user, '데이터 출력 완료' )

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        bot.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('이름') and len(args)>1:
        print('try to 이름', args[1])
        replyDataByName( chat_id, args[1] )
    elif text.startswith('지역') and len(args) > 1:
        print('try to 지역', args[1])
        replyDataByRegion( chat_id, args[1] )
    else:
        bot.sendMessage(chat_id, '모르는 명령어입니다.\n이름 [약국명], 지역 [지역명] 중 하나의 명령을 입력하세요.')


bot = telepot.Bot(TOKEN)

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)