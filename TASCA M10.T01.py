#!/usr/bin/env python
# coding: utf-8

# ## TASCA M10. T01

# ### EXERCICI 1
# 
# Realitza web scraping de dues de les tres pàgines web proposades utilitzant BeautifulSoup primer i Selenium després. 
# 
# - http://quotes.toscrape.com
# 
# - https://www.bolsamadrid.es
# 
# - www.wikipedia.es (fes alguna cerca primer i escrapeja algun contingut)
# 
# 

# In[85]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[8]:


#Scraping la pàgina per a imprimir amb BeautifulSoup

start_url = 'http://quotes.toscrape.com/'

def scrape_page(url):
    print('URL:' + url)
    print('\n')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_data(soup)
    next_page_link = soup.find_all('li', class_='next')
    for npa in next_page_link:
        link = npa.find("a", href= True)
        
        if next_page_link is not None:
            href = link.get('href')
            scrape_page(start_url+href)
            
        else:
            print('Done')
        
def get_data(content):
    quote_elements = soup.find_all('div', class_ ='quote')
    for quote_element in quote_elements:
        text_element = quote_element.find('span', class_ = 'text')
        author_element = quote_element.find('small', class_ = 'author')
        keyword_element = quote_element.find('meta', class_ = 'keywords')
        print(text_element.text.strip())
        print(author_element.text.strip())
        print(keyword_element['content'])
        print()
        
def main():
    scrape_page(start_url)
    

if __name__ == "__main__":
    main()


# In[75]:


# En aquest he fet la prova pasant els resultats a Dataframe, també amb BeautifulSoup

start_url = 'http://quotes.toscrape.com/'
quotes_list = []

global quotes_list  

def scrape_page(url):
    print('URL:' + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_data(soup)
    
    next_page_link = soup.find_all('li', class_='next')
    for npa in next_page_link:
        link = npa.find("a", href= True)
        
        if next_page_link is not None:
            href = link.get('href')
            scrape_page(start_url+href)
            
        else:
            print('Done')
       
        
def get_data(content):
    quote_elements = soup.find_all('div', class_ ='quote')
    for quote_element in quote_elements:
        quotes ={}
        text_element = quote_element.find('span', class_ = 'text')
        quotes['text'] = text_element.text.strip()
        author_element = quote_element.find('small', class_ = 'author')
        quotes['author'] = author_element.text.strip()
        keyword_element = quote_element.find('meta', class_ = 'keywords')['content']
        quotes['keywords'] = keyword_element
        quotes_list.append(quotes)
        
def main():
    scrape_page(start_url)
    

if __name__ == "__main__":
    main()


# In[76]:


quotes_list_pd = pd.DataFrame(quotes_list)


# In[88]:


quotes_list_pd.head()


# In[46]:


# Página de la wikipedia per extreure una taula amb BeautifulSoup

url = 'https://es.wikipedia.org/wiki/Somontano_de_Barbastro'


page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_ ='wikitable')
table_terri = tables[2]
table_rows = table_terri.find_all('tr')
headers = [header.text.strip() for header in table_terri.find_all('th')]
rows =[]
for row in table_rows:
    td = row.find_all('td')
    row = [row.text.strip() for row in td]
    rows.append(row)
rows.pop(0)
table_pd = pd.DataFrame(rows, columns =headers)   
table_pd.head()


# In[110]:


# Aquí he tret 3 taules que hi havia a la mateixa pàgina mitjançant iteració

url = 'https://es.wikipedia.org/wiki/Somontano_de_Barbastro'



def get_table(url):
        
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table', class_ ='wikitable')
    
    for i in range(3):
        locals()["lista_{}".format(i)] = []
      
    for table in tables:
        rows = table.find_all('tr')
        headers = [header.text.strip() for header in table.find_all('th')]
        
    for row in rows:
        td = row.find_all('td')
        if table ==tables[0]:
            rows_1.append([row.text.strip() for row in td])
        if table == tables[1]:
                rows_2.append([row.text.strip() for row in td])
        elif table == tables[2]:
                rows_3.append([row.text.strip() for row in td])
        
def main():
    get_table(url)
    

if __name__ == "__main__":
    main()
  


# In[102]:


print(rows_1)


# In[103]:


print(rows_2)


# In[104]:


print(rows_3)


# In[107]:


print(rows_3)


# In[ ]:


### A partir d'aquí fet amb Selenium


# In[102]:


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# In[77]:


url = 'http://quotes.toscrape.com/'

opts =Options()
opts.headless = True
browser = Firefox(options=opts)
try:
    browser.get(url)
    time.sleep(5)
except TimeoutException:
    print('new connection try')
    browser.get(url)
    time.sleep(5) 
    
quotes_list=[]
count = 0
count_Excep=0
for i in range(1,11): #Aquí también hubiera podido utilizar while True si no sé el número de páginas
    print(count)
    quote_elements =  browser.find_elements(By.XPATH, "//div[@class='quote']")
    for quote_element in quote_elements:
        quotes={}
        quotes['text'] = quote_element.find_element(By.CLASS_NAME, 'text').text
        quotes['author'] = quote_element.find_element(By.CLASS_NAME, 'author').text
        quotes['author_link'] = quote_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        quotes['tags'] = quote_element.find_element(By.CLASS_NAME, 'tags').text
        quotes_list.append(quotes)
    try:
        next_page = browser.find_element(By.CLASS_NAME,'next')                         .find_element(By.TAG_NAME,'a')
        next_page.click()
        time.sleep(10)
        count+=1
    except NoSuchElementException:
            print('I guess this is the last page')
            count_Excep+=1
            if count_Excep ==1:
                continue
            else:
                break
        
print(quotes_list)

browser.quit()

    


# In[78]:


quotesS_df=pd.DataFrame(quotes_list)


# In[79]:


quotesS_df.head()


# In[80]:


quotesS_df.shape


# In[86]:


quotesS_df.head(50)


# In[32]:


#Extreure la pàgina de la wikipedia amb Selenium

url = 'https://es.wikipedia.org/wiki/Somontano_de_Barbastro'

opts =Options()
opts.headless = True
browser = Firefox(options=opts)
try:
    browser.get(url)
    time.sleep(5)
except TimeoutException:
    print('new connection try')
    browser.get(url)
    time.sleep(5) 
# Numero de columnas/ filas en la tabla
rows = len(browser.find_elements(By.XPATH,"//*[@id='mw-content-text']/div[1]/table[4]/tbody/tr"))
cols = 1+len(browser.find_elements(By.XPATH,"//*[@id='mw-content-text']/div[1]/table[4]/tbody/tr[1]/th"))  

# Encabezado
headers = [header.text.strip() for header in browser.find_element(By.XPATH,"//*[@id='mw-content-text']/div[1]/table[4]/tbody/tr[1]")                                     .find_elements(By.TAG_NAME,'th')]

table =[]

for r in range(2,rows):
    data =[]
    table.append(data)
    for c in range(1,cols):
        value= browser.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr['+str(r)+']/td['+str(c)+']').text
        data.append(value)
      
browser.quit()


# In[33]:


print(table)


# In[52]:


territori_pd = pd.DataFrame(table, columns =headers)


# In[53]:


territori_pd


# ### EXERCICI 2

# El faig al word sobre les dades de la web :http://quotes.toscrape.com/

# In[ ]:





# ### EXERCICI 3
# 
# Tria una pàgina web que tu vulguis i realitza web scraping mitjançant la llibreria Selenium primer i Scrapy després. 

# In[2]:


from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


# In[182]:


# Scrape mitjançant SELENIUM

url = 'https://www.solidea.com/es/cat/calcetines/calcetines-de-prevencion'    

opts =Options()
opts.headless = True
browser = Firefox(options=opts)
try:
    browser.get(url)
    time.sleep(5)
except TimeoutException:
    print('new connection try')
    browser.get(url)
    time.sleep(5) 




sections= browser.find_elements(By.XPATH,'//html/body/main/section[2]/div/div/div[2]/div[4]/div')
num_sect = len(browser.find_elements(By.XPATH,'//html/body/main/section[2]/div/div/div[2]/div[4]/div'))
products =[]

for r in range(1,1+num_sect):
    sections= browser.find_element(By.XPATH,'//html/body/main/section[2]/div/div/div[2]/div[4]/div['+str(r)+']')
    elements={}
    elements['name'] = sections.find_element(By.TAG_NAME,'h4').text
    elements['tags'] = [tags.text.strip() for tags in sections.find_elements(By.TAG_NAME,'span')]
    elements['price'] = sections.find_element(By.CLASS_NAME,'product-price').text
    elements['colors'] = [color.get_attribute('alt') for color in sections.find_element(By.CLASS_NAME,'colors')                      .find_elements(By.TAG_NAME,'img')]
    products.append(elements)


# In[86]:


products_pd = pd.DataFrame(products)


# In[87]:


products_pd


# In[ ]:


#Scrape mitjançant Scrapy


# In[1]:


import scrapy
from scrapy.crawler import CrawlerProcess


# In[64]:


# Per poder guadar les dades en json 
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('socksresult.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# In[78]:


#Spider per fer el scraping
class StockSpider(scrapy.Spider):
    name='socks'
    start_urls=["https://www.solidea.com/es/cat/calcetines/calcetines-de-prevencion"]
    
    custom_settings = {
                  
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1},  
        'FEED_FORMAT':'json',                                  
        'FEED_URI': 'socksresult.json'             # Saves file of the result    
        }
    def parse(self,response):
        for section in response.xpath('/html/body/main/section[2]/div/div/div[2]/div[4]/div'):
            yield {
                'name':section.xpath('.//figure/img/@alt').get(),
                'price': section.xpath('.//div/a/div/div/text()').get(),
                'tags' : section.xpath('.//div/a/div/span/text()').getall(),
                'colors':section.xpath('.//ul/li/img/@alt').getall()
            }


# In[79]:



# Per evitar error ReactorAlreadyInstalledError: reactor already installed
import sys    
if "twisted.internet.reactor" in sys.modules:
    del sys.modules["twisted.internet.reactor"]

   
#Iniciar el proces de scraping

process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
process.crawl(StockSpider)
process.start()


# In[80]:


import pandas as pd
result = pd.read_json("socksresult.jl", lines=True)


# In[81]:



result


# In[ ]:




