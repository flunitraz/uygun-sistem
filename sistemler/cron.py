from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sqlite3
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'scraped'    # a unique code

   

    def do(self):
        ggt_pages = ["https://www.gaming.gen.tr/kategori/hazir-sistemler/page/1/",
             "https://www.gaming.gen.tr/kategori/hazir-sistemler/page/2/",
             "https://www.gaming.gen.tr/kategori/hazir-sistemler/page/3/"]

        ggt_data = []

        itopya_pages = ["https://itopya.com/HazirSistemler/?sayfa=1&stok=stokvar",
                    "https://itopya.com/HazirSistemler/?sayfa=2&stok=stokvar"]

        itopya_data = []

        tebilon_pages = ["https://www.tebilon.com/bilgisayar/hazir-sistemler/?page=1&f=n&g=sT",
                        "https://www.tebilon.com/bilgisayar/hazir-sistemler/?page=2&f=n&g=sT",
                        "https://www.tebilon.com/bilgisayar/hazir-sistemler/?page=3&f=n&g=sT",
                        "https://www.tebilon.com/bilgisayar/hazir-sistemler/?page=4&f=n&g=sT",
                        "https://www.tebilon.com/bilgisayar/hazir-sistemler/?page=5&f=n&g=sT"]

        tebilon_data = []

        for ggt_page in ggt_pages:   
            response = requests.get(ggt_page)
            soup = bs(response.text, "html.parser")
            
            url = soup.find("ul","products columns-3").find_all("a")
            data = soup.find("ul","products columns-3").find_all("li")
            price = soup.find("ul","products columns-3").find_all("span",class_="price")
            
            for ind in range(len(price)):
                
                ggt_dict = {}
                ggt_dict["islemci"]=data[ind].find("h2").text.split("/")[1].strip()
                ggt_dict["ekran_karti"]=data[ind].find("h2").text.split("/")[2].strip()
                ggt_dict["ram"]=data[ind].find("h2").text.split("/")[3].strip()
                ggt_dict["depolama"]=data[ind].find("h2").text.split("/")[4].replace("Gaming Bilgisayar","").strip()
                ggt_dict["fiyat"]=price[ind].text.split()[-2].replace(".","").split(",")[0]
                ggt_dict["satici"]="gaming.gen.tr"
                ggt_dict["url"]=url[ind].get("href")
                ggt_dict["img"]=data[ind].find("img").get("data-src")
                ggt_data.append(ggt_dict)
                
        ggt_df = pd.DataFrame(ggt_data)


        for i_page in itopya_pages:   
            response = requests.get(i_page)
            soup = bs(response.text, "html.parser")
            
            url = soup.find_all("div","product-header")
            data = soup.find_all("div","product-body")
            price = soup.find_all("div","product-footer")
            
            for ind in range(len(price)):
                
                itopya_dict = {}
                itopya_dict["islemci"]=data[ind].text.split("/")[1].strip()
                itopya_dict["ekran_karti"]=data[ind].text.split("/")[2].strip()
                itopya_dict["ram"]=data[ind].text.split("/")[3].strip()
                itopya_dict["depolama"]=data[ind].text.split("/")[4].strip()
                itopya_dict["fiyat"]=price[ind].text.strip().replace(".","").split(",")[0]
                itopya_dict["satici"]="itopya.com"
                itopya_dict["url"]="https://itopya.com"+url[ind].find("a").get("href")
                itopya_dict["img"]=url[ind].find("img").get("data-src")
                itopya_data.append(itopya_dict)
                
        itopya_df = pd.DataFrame(itopya_data)

        for t_page in tebilon_pages:   
            response = requests.get(t_page)
            soup = bs(response.text, "html.parser")

            data = soup.find_all("div",class_="showcase__products")[1].find_all(class_="showcase__title col-md-12 text-center no-padding desktopShow")
            price = soup.find_all("div",class_="showcase__products")[1].find_all("div",class_="showcase__price")
            stok_kontrol = soup.find_all("div",class_="showcase__products")[1].find_all(class_="showcase__basket")
            img = soup.find("div",class_="showcase__products").find_all(class_="showcase__image")
            
            for ind in range(len(price)):

                tebilon_dict = {}
                tebilon_dict["islemci"]=data[ind].text.split("-")[0].strip()
                tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()
                tebilon_dict["ram"]=data[ind].text.split("-")[-1].strip()
                tebilon_dict["depolama"]=data[ind].text.split("-")[-2].strip()
                tebilon_dict["fiyat"]=price[ind].text.replace("TL","").replace(".","").strip()
                tebilon_dict["satici"]="tebilon.com"
                tebilon_dict["url"]=data[ind].find("a").get("href")
                tebilon_dict["img"]=img[ind].find("img").get("src")

                if(tebilon_dict["ekran_karti"]=="ASUS DUAL"):
                    tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()+" "+data[ind].text.split("-")[2].strip()+" "+data[ind].text.split("-")[3].strip()
                elif(tebilon_dict["ekran_karti"]=="ASUS DUAL RX"):
                    tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()+" "+data[ind].text.split("-")[2].strip()+" "+data[ind].text.split("-")[3].strip()
                elif(tebilon_dict["ekran_karti"]=="TUF"):
                    tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()+" "+data[ind].text.split("-")[2].strip()+" "+data[ind].text.split("-")[3].strip()
                elif(tebilon_dict["ekran_karti"]=="ASUS TUF"):
                    tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()+" "+data[ind].text.split("-")[2].strip()+" "+data[ind].text.split("-")[3].strip()
                elif(tebilon_dict["ekran_karti"]=="DUAL"):
                    tebilon_dict["ekran_karti"]=data[ind].text.split("-")[1].strip()+" "+data[ind].text.split("-")[2].strip()+" "+data[ind].text.split("-")[3].strip()
                elif(tebilon_dict["ekran_karti"]=="MSI A320M"):
                    tebilon_dict["ekran_karti"]="-"
                elif(tebilon_dict["ekran_karti"]=="ASUS PRIME B450M"):
                    tebilon_dict["ekran_karti"]="-"
                
                
                if stok_kontrol[ind].text.strip()[0]=="İ":
                    tebilon_data.append(tebilon_dict)
                
        tebilon_df = pd.DataFrame(tebilon_data)

        for i in tebilon_df[(tebilon_df.ram.str.contains("500")) | (tebilon_df.ram.str.contains("480"))].index:
            temp = tebilon_df.loc[i].ram
            tebilon_df.loc[i].ram = tebilon_df.loc[i].depolama
            tebilon_df.loc[i].depolama = temp
        
        for i in tebilon_df[(tebilon_df.ram.str.contains("8")) & (tebilon_df.islemci.str.contains("4100"))].index:
             tebilon_df.loc[i].ekran_karti = "6500 XT"

        df = pd.concat([ggt_df,itopya_df,tebilon_df])
        df = df.reset_index(drop=True)

        def degis(before,after,col):
            for i in df[(df[col].str.contains(before))].index:
                df.loc[i,col] = after


        degis("5600X","tempx1","islemci")
        degis("3200","AMD Ryzen 3 3200G","islemci")
        degis("3600","AMD Ryzen 5 3600","islemci")
        degis("4100","AMD Ryzen 3 4100","islemci")
        degis("4500","AMD Ryzen 5 4500","islemci")
        degis("5500","AMD Ryzen 5 5500","islemci")
        degis("5600","AMD Ryzen 5 5600","islemci")
        degis("5650","AMD Ryzen 5 5650","islemci")
        degis("5700","AMD Ryzen 5 5700X","islemci")
        degis("7600","AMD Ryzen 5 7600X","islemci")
        degis("7700","AMD Ryzen 5 7700X","islemci")
        degis("tempx1","AMD Ryzen 5 5600X","islemci")

        degis("12900KS","tempx2","islemci")
        degis("10100","Intel Core I3 10100F","islemci")
        degis("10105","Intel Core I3 10105F","islemci")
        degis("10400","Intel Core I5 10400F","islemci")
        degis("11400","Intel Core I5 11400F","islemci")
        degis("12100","Intel Core I3 12100F","islemci")
        degis("12400","Intel Core I5 12400F","islemci")
        degis("12600","Intel Core I5 12600K","islemci")
        degis("12700","Intel Core I5 12700F","islemci")
        degis("12900","Intel Core I9 12900K","islemci")
        degis("tempx2","Intel Core I9 12900KS","islemci")

        degis("3060Ti","temp_ti1","ekran_karti")
        degis("3060 Ti","temp_ti1","ekran_karti")
        degis("3060 TI","temp_ti1","ekran_karti")
        degis("3070 TI","temp_ti2","ekran_karti")
        degis("3070 Ti","temp_ti2","ekran_karti")
        degis("3080 TI","temp_ti3","ekran_karti")
        degis("3080 Ti","temp_ti3","ekran_karti")
        degis("1050 TI","temp_ti4","ekran_karti")
        degis("1660 Ti","temp_ti5","ekran_karti")

        degis("6700 XT","temp_xt1","ekran_karti")
        degis("6700XT","temp_xt1","ekran_karti")
        degis("6650 XT","temp_xt2","ekran_karti")
        degis("6500 XT","temp_xt3","ekran_karti")

        degis("1650","NVIDIA GTX 1650","ekran_karti")
        degis("1660","NVIDIA GTX 1660","ekran_karti")
        degis("2060","NVIDIA RTX 2060","ekran_karti")
        degis("3050","NVIDIA RTX 3050","ekran_karti")
        degis("3060","NVIDIA RTX 3060","ekran_karti")
        degis("3070","NVIDIA RTX 3070","ekran_karti")
        degis("3090","NVIDIA RTX 3090","ekran_karti")
        degis("4080","NVIDIA RTX 4080","ekran_karti")
        degis("4090","NVIDIA RTX 4090","ekran_karti")

        degis("580","AMD RX 580","ekran_karti")
        degis("6500","AMD RX 6500","ekran_karti")
        degis("6600","AMD RX 6600","ekran_karti")
        degis("6650","AMD RX 6650","ekran_karti")
        degis("6700","AMD RX 6700","ekran_karti")
        degis("6800","AMD RX 6800","ekran_karti")

        degis("temp_ti1","NVIDIA RTX 3060 TI","ekran_karti")
        degis("temp_ti2","NVIDIA RTX 3070 TI","ekran_karti")
        degis("temp_ti3","NVIDIA RTX 3080 TI","ekran_karti")
        degis("temp_ti4","NVIDIA GTX 1050 TI","ekran_karti")
        degis("temp_ti5","NVIDIA GTX 1660 TI","ekran_karti")

        degis("temp_xt1","AMD RX 6700-XT","ekran_karti")
        degis("temp_xt2","AMD RX 6650-XT","ekran_karti")
        degis("temp_xt3","AMD RX 6500-XT","ekran_karti")

        degis("32","32 GB","ram")
        degis("16","16 GB","ram")
        degis("8","8 GB","ram")
        degis("KING","8 GB","ram")

        degis("240","240 GB","depolama")
        degis("480","480 GB","depolama")
        degis("500","500 GB","depolama")
        degis("512","512 GB","depolama")
        degis("1TB","1 TB","depolama")
        degis("WD","480 GB","depolama")
        degis("GIGA","480 GB","depolama")

        conn = sqlite3.connect('./db.sqlite3')
        
        df = df.reset_index().rename(columns = {'index':'id'})
        df.fiyat = df.fiyat.astype(int)
        
        df.to_sql("sistemler_sistem", conn,if_exists='replace', index = False)
