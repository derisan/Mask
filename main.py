# main.py


from tkinter import *
from tkinter import ttk
from time import sleep
import urllib
import http.client
from xml.etree import ElementTree
from myEmail import *
from Maps import *
import myemail

COLOR1 = "green"
COLOR2 = "gold"
COLOR3 = "blue"
COLOR4 = "red"
COLOR5 = "black"

class MainGUI():
    def send_email(self):
        retList = []
        for item in self.likeList:
            sp = item.find("SALE_PLC")
            addr = item.find("REFINE_LOTNO_ADDR")
            time = item.find("WRHOUSNG_TM")
            state = item.find("REMNDR_STATE_DIV_NM")
            retList.extend(list(myemail.makestr(str(sp.text), str(addr.text), str(time.text), str(state.text))))
            retList.append('\n')
        googleMail(self.emailAddr.get(), "\n".join(retList))

    ### 이름으로 검색
    def search_name(self):
        self.run_progressbar()

        pName = self.name.get()
        self.pharmacyList.clear()
        self.Lpharmacy.delete(0, END)
        self.region_entered.delete(0, END)
        conn = http.client.HTTPSConnection("openapi.gg.go.kr")
        for i in range(1, 8 + 1):
            conn.request("GET","/PubMaskSaleStus?KEY=10f20300cd90416e867ff580b1718c2d&pSize=1000&pIndex=" + str(i))
            req = conn.getresponse()

            if (req.status == 200):
                tree = ElementTree.fromstring(req.read())
                rowElements = tree.iter("row")

                for row in rowElements:
                    salePlace = row.find("SALE_PLC")
                    if salePlace.text.find(pName) >= 0:
                        self.Lpharmacy.insert(END, salePlace.text)
                        self.pharmacyList.append(row)
        self.stop_progressbar()

    ### 지역명으로 검색
    def search_region(self):
        self.run_progressbar()

        rName = self.region.get().split()
        if len(rName) == 1:
            rName.append(" ")
        self.pharmacyList.clear()
        self.Lpharmacy.delete(0, END)
        self.name_entered.delete(0, END)
        conn = http.client.HTTPSConnection("openapi.gg.go.kr")
        for i in range(1, 8 + 1):
            conn.request("GET","/PubMaskSaleStus?KEY=10f20300cd90416e867ff580b1718c2d&pSize=1000&pIndex=" + str(i))
            req = conn.getresponse()

            if (req.status == 200):
                tree = ElementTree.fromstring(req.read())
                rowElements = tree.iter("row")

                for row in rowElements:
                    lotAddr = row.find("REFINE_LOTNO_ADDR")
                    salePlace = row.find("SALE_PLC")
                    if ((rName[0] in lotAddr.text) and (rName[1] in lotAddr.text)):
                        self.Lpharmacy.insert(END, salePlace.text)
                        self.pharmacyList.append(row)
        self.stop_progressbar()
    
    ### 약국 목록의 정보 표시
    def show_information(self, event):
        self.Tinformation.config(state = 'normal')
        self.Tinformation.delete(1.0, END)
        item = event.widget.curselection()
        if item:
            sp = self.pharmacyList[item[0]].find("SALE_PLC")
            addr = self.pharmacyList[item[0]].find("REFINE_LOTNO_ADDR")
            time = self.pharmacyList[item[0]].find("WRHOUSNG_TM")
            state = self.pharmacyList[item[0]].find("REMNDR_STATE_DIV_NM")
            lat = self.pharmacyList[item[0]].find("REFINE_WGS84_LAT")
            logt = self.pharmacyList[item[0]].find("REFINE_WGS84_LOGT")

            self.Tinformation.insert(END, "< 판매장소 >\n")
            self.Tinformation.insert(END, str(sp.text) + "\n\n")
            self.Tinformation.insert(END, "< 주 소 >\n")
            self.Tinformation.insert(END, str(addr.text) + "\n\n")
            self.Tinformation.insert(END, "< 입고시간 >\n")
            self.Tinformation.insert(END, str(time.text) + "\n\n")
            self.Tinformation.insert(END, "< 재고상태 >\n")
            self.Tinformation.insert(END, str(state.text))
            self.Tinformation.tag_add("center", 1.0, "end")
            self.Tinformation.tag_config("center", justify = CENTER)
            self.Tinformation.config(state = 'disabled')
            self.drawMap(lat.text, logt.text)
 

    ### 북마크 약국의 정보 표시
    def show_information_bookmark(self, event):
        self.Tinformation.config(state = 'normal')
        self.Tinformation.delete(1.0, END)
        item = event.widget.curselection()
        if item:
            sp = self.likeList[item[0]].find("SALE_PLC")
            addr = self.likeList[item[0]].find("REFINE_LOTNO_ADDR")
            time = self.likeList[item[0]].find("WRHOUSNG_TM")
            state = self.likeList[item[0]].find("REMNDR_STATE_DIV_NM")
            lat = self.likeList[item[0]].find("REFINE_WGS84_LAT")
            logt = self.likeList[item[0]].find("REFINE_WGS84_LOGT")

            self.Tinformation.insert(END, "< 판매장소 >\n")
            self.Tinformation.insert(END, str(sp.text) + "\n\n")
            self.Tinformation.insert(END, "< 주 소 >\n")
            self.Tinformation.insert(END, str(addr.text) + "\n\n")
            self.Tinformation.insert(END, "< 입고시간 >\n")
            self.Tinformation.insert(END, str(time.text) + "\n\n")
            self.Tinformation.insert(END, "< 재고상태 >\n")
            self.Tinformation.insert(END, str(state.text))
            self.Tinformation.tag_add("center", 1.0, "end")
            self.Tinformation.tag_config("center", justify = CENTER)
            self.Tinformation.config(state = 'disabled')
            self.drawMap(lat.text, logt.text)
    
    ### 지도 그리기
    def drawMap(self, lat, logt):
        self.cMap.delete('all')

        GMap().getMap(lat, logt)

        self.mapImage = PhotoImage(file = "map.png")
        self.cMap.create_image(0, 0, anchor = NW, image = self.mapImage)
        

    ### 북마크 추가
    def addBookmark(self, event):
        item = self.Lpharmacy.curselection()
        sp = self.pharmacyList[item[0]].find("SALE_PLC")
        self.Llike.insert(END, sp.text)
        self.likeList.append(self.pharmacyList[item[0]])
        
    ### 북마크 제거
    def removeBookmark(self, event):
        item = self.Llike.curselection()
        self.Llike.delete(item[0])
        self.likeList.pop(item[0])
    
    
    ### 이름순으로 정렬한 그래프 그리기
    def drawGraphByName(self, event):
        self.cGraph.delete('histogram')
        sortedlikeList = sorted(self.likeList, key = lambda item: item.find("SALE_PLC").text)
        barWidth = 90
        i = 0
        j = 10
        
        for pharmacy in sortedlikeList:
            rs = pharmacy.find("REMNDR_STATE_DIV_NM").text
            if rs == "100개 이상": ## green
                height = 20
                color = COLOR1
            elif rs == "30개 이상 100개 미만": ## gold
                height = 50
                color = COLOR2
            elif rs == "2개 이상 30개 미만": ## blue
                height = 80
                color = COLOR3
            elif rs == "1개 이하": ## red
                height = 100
                color = COLOR4
            else: ## black
                height = 120
                color = COLOR5
            self.cGraph.create_rectangle(i*barWidth + j, height,
            (i+1)*barWidth + j, 130, tags = 'histogram', fill = color)
            self.cGraph.create_text(i*barWidth + barWidth / 2 + j, height - 7, 
            text = pharmacy.find("SALE_PLC").text, tags = 'histogram')
            i += 1
            j += 10

    def getStockValue(self, txt):
        if txt == "100개 이상":
            return 5
        elif txt == "30개 이상 100개 미만":
            return 4
        elif txt == "2개 이상 30개 미만":
            return 3
        elif txt == "1개 이하": 
            return 2
        else: 
            return 1

    def drawGraphByStock(self, event):
        self.cGraph.delete('histogram')
        sortedlikeList = sorted(self.likeList, key = lambda item: self.getStockValue(str(item.find("REMNDR_STATE_DIV_NM").text)))
        barWidth = 90
        i = 0
        j = 10
        
        for pharmacy in sortedlikeList:
            rs = pharmacy.find("REMNDR_STATE_DIV_NM").text
            if rs == "100개 이상": ## green
                height = 20
                color = COLOR1
            elif rs == "30개 이상 100개 미만": ## gold
                height = 50
                color = COLOR2
            elif rs == "2개 이상 30개 미만": ## blue
                height = 80
                color = COLOR3
            elif rs == "1개 이하": ## red
                height = 100
                color = COLOR4
            else: ## black
                height = 120
                color = COLOR5
            self.cGraph.create_rectangle(i*barWidth + j, height,
            (i+1)*barWidth + j, 130, tags = 'histogram', fill = color)
            self.cGraph.create_text(i*barWidth + barWidth / 2 + j, height - 7, 
            text = pharmacy.find("SALE_PLC").text, tags = 'histogram')
            i += 1
            j += 10

    def run_progressbar(self):
        self.progressbar['maximum'] = 100
        for i in range(101):
            sleep(0.01)
            self.progressbar['value'] = i
            self.progressbar.update()
        self.progressbar['value'] = 0

    def stop_progressbar(self):
        self.progressbar['value'] = 0

    def __init__(self):
        win = Tk()
        win.resizable(False, False)
        win.title("마스크 어디?")
        win.iconphoto(False, PhotoImage(file = 'logo.ico'))

        self.pharmacyList = []
        self.likeList = []

        ### 마스터 프레임
        # mighty = ttk.LabelFrame(win)
        # mighty.grid(column = 0, row = 0, padx = 8, pady = 4)
        

        ### mighty2 frame( 최상단 )
        mighty2 = ttk.LabelFrame(win, text = '검색')
        mighty2.grid(column = 0, row = 0, columnspan = 3)
        
        ttk.Label(mighty2, text = "이름으로 검색").grid(column = 0, row = 0)
        ttk.Label(mighty2, text = "지역으로 검색").grid(column = 2, row = 0)
        ttk.Label(mighty2, text = "이메일 발송하기").grid(column = 4, row = 0)

        self.name = StringVar()
        self.name_entered = Entry(mighty2, width = 12, textvariable = self.name, relief = 'ridge', borderwidth = 3)
        self.name_entered.grid(column = 0, row = 1)

        self.region = StringVar()
        self.region_entered = Entry(mighty2, width = 12, textvariable = self.region, relief = 'ridge', borderwidth = 3)
        self.region_entered.grid(column = 2, row = 1)

        Bname = ttk.Button(mighty2, text = "확인", command = self.search_name)
        Bname.grid(column = 1, row = 1)
        Bregion = ttk.Button(mighty2, text = "확인", command = self.search_region)
        Bregion.grid(column = 3, row = 1)

        self.emailAddr = StringVar()
        self.email_entered = Entry(mighty2, width = 20, textvariable = self.emailAddr, relief = 'ridge', borderwidth = 3)
        self.email_entered.grid(column = 4, row = 1)

        sendEmail = ttk.Button(mighty2, text = "발송", command = self.send_email)
        sendEmail.grid(column = 5, row = 1)

        self.progressbar = ttk.Progressbar(mighty2, orient = 'horizontal', mode ='determinate')
        self.progressbar.grid(column = 0, row = 2, columnspan = 6, sticky = W+E)


        ### mighty3 frame ( 약국 리스트 )
        mighty3 = ttk.LabelFrame(win, text = "약국 목록")
        mighty3.grid(column = 0, row = 1, sticky = W+N+S)

        scrollbar = Scrollbar(mighty3, orient = "vertical")
        scrollbar.pack(side = RIGHT, fill = Y)
        self.Lpharmacy = Listbox(mighty3, selectmode = 'browse', yscrollcommand = scrollbar.set, exportselection = 0, relief = 'ridge', borderwidth = 5)
        self.Lpharmacy.bind("<<ListboxSelect>>", self.show_information)
        self.Lpharmacy.bind("<Double-1>", self.addBookmark)
        self.Lpharmacy.bind('<FocusOut>', lambda e: self.Lpharmacy.selection_clear(0, END))
        self.Lpharmacy.pack(expand = True, fill = Y)
        scrollbar.config(command = self.Lpharmacy.yview)


        ### mighty4 frame ( 즐겨찾는 약국 )
        mighty4 = ttk.LabelFrame(win, text = "즐겨찾는 약국")
        mighty4.grid(column = 0, row = 2, sticky = W)
        self.Llike = Listbox(mighty4, selectmode = 'browse', exportselection = 0, relief = 'ridge', borderwidth = 5)
        self.Llike.grid(column =0 , row = 0, sticky = N+S)
        self.Llike.bind("<<ListboxSelect>>", self.show_information_bookmark)
        self.Llike.bind("<Double-1>", self.removeBookmark)
        self.Llike.bind('<FocusOut>', lambda e: self.Llike.selection_clear(0, END))
        

        #### mighty5 frame ( 약국 정보 )
        mighty5 = ttk.LabelFrame(win, text = "약국 정보")
        mighty5.grid(column = 1, row = 1, sticky = W)
        self.Tinformation = Text(mighty5, width = 30, wrap = WORD, relief = 'ridge', borderwidth = 5)
        self.Tinformation.grid(column = 0, row = 0, sticky = W+N+S, columnspan = 2)
        

        ### mighty6 frame 구현 ( 지도 )
        mighty6 = ttk.LabelFrame(win, text = "지도")
        mighty6.grid(column = 2, row = 1, sticky = W+N+S)
        self.cMap = Canvas(mighty6, width = 300, relief = 'ridge', borderwidth = 5)
        self.cMap.pack(expand= True, fill = Y)
        
        
        ### mighty7 frame ( 그래프 )
        mighty7 = ttk.LabelFrame(win, text = "그래프")
        mighty7.grid(column = 1, row = 2, sticky = W+N+S+E, columnspan = 2)
      
        tabControl = ttk.Notebook(mighty7)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text = "보기")
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text = "설정")
        tabControl.pack(expand = 1, fill = "both")

        radSort = IntVar()
        self.radSortName = Radiobutton(tab2, text = "이름순 정렬", variable = radSort, value = 1)
        self.radSortName.bind('<ButtonRelease-1>', self.drawGraphByName)
        self.radSortName.pack(side = 'left')

        self.radSortStock = Radiobutton(tab2, text = "재고순 정렬", variable = radSort, value = 2)
        self.radSortStock.bind('<ButtonRelease-1>', self.drawGraphByStock)
        self.radSortStock.pack(side = 'left')

        self.cGraph = Canvas(tab1, height = 50, relief = 'ridge', borderwidth = 5)
        self.cGraph.pack(expand = True, fill = "both")
        

        self.name_entered.focus()

        win.mainloop()

MainGUI()