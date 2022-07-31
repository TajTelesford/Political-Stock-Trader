from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import time
import asyncio
from tqdm import tqdm, trange

options = webdriver.ChromeOptions()
options.add_argument('headless')

#grabbing the figure id's
def figure_id(div):
    idList = []
    FigureId = div.find_all(name="article")
    for id in FigureId:
        item = id['class']
        idList.append(item[4][4:])
    return idList


#getting page source 
async def get_page_source(url):
    d = webdriver.Chrome(options=options)
    d.get(url)
    time.sleep(1.5)
    page = d.page_source
    d.close()

    return page

#getting the figure's stock trades/types/dates
async def figure_stock(idList):
    
    figureUrl = "https://www.capitoltrades.com/politicians/"
    Stock_List = []
    Stock_Date = []
    Stock_Type = []
    
    for i in tqdm(range(len(idList)), desc="LOADING STOCKS>>>", maxinterval=100):
        url = figureUrl+f"{idList[i]}"

        task = asyncio.create_task(get_page_source(url))
        page = await task
        
        doc = BeautifulSoup(page, "html.parser")
        stock = doc.find_all("h3", {"class":"q-fieldset issuer-name"})
        date = doc.find_all("div", {"class": "q-value"})
        trade_type = doc.find_all(class_=re.compile("q-field tx-type tx-type"))
        for items in stock:
            Stock_List.append(items.a.string)

        for d in date:
            Stock_Date.append(d.string)
        
        for type in trade_type:
            Stock_Type.append(type.string)

        for ( s , t , d ) in zip(Stock_List, Stock_Type, Stock_Date):
            print(f"{s} {t} {d}")

async def main():

    timePeriod = 30
    url = f"https://www.capitoltrades.com/politicians?txDate={timePeriod}d"

    page = requests.get(url).text
    document = BeautifulSoup(page, "html.parser")

    div = document.find(class_="q-cardlist__content")
    # # ContentCard = div.find_all(name='h2')
    # # print(ContentCard)
    # ID_LIST = figure_id(div)
    # figure_stock(ID_LIST, driver)
    await figure_stock(figure_id(div))
    

    


asyncio.run(main())





    


