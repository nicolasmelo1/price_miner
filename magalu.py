import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
import sys
import time

sys.setrecursionlimit(10000)
driver = webdriver.Firefox()

# magalu
'''
def getData(driver, url, data, max_number):

    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "lxml")
    soup.prettify()
    if (data[data['title'].str.contains(soup.title.text)].empty == False):                 
        print("already exists in dataframe")           
        next_item = soup.find_all("li", class_="showcase__product-box js-suggestion slick-slide slick-current slick-active")
        return getData(driver, [a['href'] for a in next_item[randint(0, len(next_item)-1)].find_all("a", href=True)][0], data, max_number)

    dados = {
        "title": [soup.title.text], 
        "dados": [soup.find("div",class_="price-template").text]
    }

    df = pd.DataFrame(dados,columns=["title", "dados"])
    data = pd.concat([data, df])
    next_item = soup.find_all("li", class_="showcase__product-box js-suggestion slick-slide slick-current slick-active stewie-carousel-1-1")
    if not next_item:
        next_item = soup.find_all("li", class_="showcase__product-box js-suggestion slick-slide slick-current slick-active")
    
    print(len(data))
    if len(data) == max_number:
        return data
    try:
        return getData(driver, [a['href'] for a in next_item[randint(0, len(next_item)-1)].find_all("a", href=True)][0], data, max_number)
        
    except Exception as e:
        print("error: " + str(e))
        next_item = soup.find_all("li", class_="showcase__product-box js-suggestion slick-slide slick-current slick-active stewie-carousel-1-1")
        if not next_item: 
            next_item = soup.find_all("li", class_="showcase__product-box js-suggestion slick-slide slick-current slick-active")
        return getData(driver, [a['href'] for a in next_item[randint(0, len(next_item)-1)].find_all("a", href=True)][0], data, max_number)
    

data = pd.read_csv('magalu_notebooks.csv', sep=';')    
df = getData(
    driver, 
    "https://www.magazineluiza.com.br/notebook-hp-240-g5-14-polegadas-i3-6006u-4gb-500gb-dvdrw-win-10-pro/p/7280842/in/note/", 
    data, 70)
magalu = df
magalu['title'] = magalu['title'].str.replace('\\t', '')
magalu['marca'] = magalu['title'].apply(lambda x: x.split(' ')[2] if x.split(' ')[1].lower() == 'gamer' else (x.split(' ')[4] if x.split(' ')[0].lower() == 'macbook' else x.split(' ')[1]))
magalu['Processador'] = magalu['title'].apply(lambda x: x.split(' ')[x.split(' ').index('Core')-2:x.split(' ').index('Core')+2] if 'Core' in x.split(' ') else ('i7' if 'i7' in x.split(' ') else []))
magalu['Processador1'] = magalu['Processador'].apply(lambda x: 'i7' if 'i7' in x else ('i5' if 'i5' in x else ('i3' if 'i3' in x else ' '.join(x))))
magalu['De'] = magalu['dados1'].apply(lambda x: x.split('<')[1].split('>')[0].replace('$', '').replace('.','') if x.split('<')[0] == ' ' else '0,0')
magalu['Por'] = magalu['dados1'].apply(lambda x: x.split('>')[1].replace('$', '').replace('.',''))
magalu['dados1'] = magalu['dados'].str.replace('por', '>').str.replace('em', '>').str.replace('R','').str.replace('até','>').str.replace('à','>').str.replace('de','>')
magalu['Parcelas'] = magalu['dados1'].apply(lambda x: '10x' if ' 10x ' in x.split('>') else ('12x' if ' 12x ' in x.split('>') else ('6x' if ' 6x ' in x.split('>') else ('9x' if ' 9x ' in x.split('>') else '8x'))))
magalu.to_csv('magalu_notebooks.csv', sep=';', index=False)
'''

#casas bahia
'''
def getData(driver, url, data, max_number, links):

    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    soup.prettify()
    if (data[data['title'].str.contains(soup.title.text)].empty == False):                 
        print("already exists in dataframe")    
        time.sleep(5)       
        next_item = soup.find("ul", class_="vitrineProdutos")
        next_link = [a['href'] for a in next_item.find_all("a", href=True)]

        links.append(next_link[randint(0,len(next_link)-1)])
        return getData(driver, next_link[randint(0,len(next_link)-1)], data, max_number, links)
    elif 'notebook' not in soup.title.text.lower():
        print('not a notebook')
        return getData(driver, links[randint(0,len(links)-1)], data, max_number, links)
    dados = {
        "title": [soup.title.text], 
        "dados": [soup.find("div",class_="descricaoAnuncio cbGrA").text]
    }
    df = pd.DataFrame(dados,columns=["title", "dados"])
    data = pd.concat([data, df])
    next_item = soup.find("ul", class_="vitrineProdutos")
    print(len(data))
    if len(data) == max_number:
        return data
    try:
        next_link = [a['href'] for a in next_item.find_all("a", href=True)]
        links.append(next_link[randint(0,len(next_link)-1)])
        return getData(driver, next_link[randint(0,len(next_link)-1)], data, max_number, links)
        
    except Exception as e:
        print("error: " + str(e))
        return getData(driver, links[randint(0,len(links)-1)], data, max_number, links)
    

data = pd.read_csv('casasbahia_notebooks.csv', sep=';')    
df = getData(
    driver, 
    "https://www.casasbahia.com.br/Informatica/Notebook/notebook-gamer-avell-titanium-g1513-mx7-geforce-gtx-1050ti-intel-core-i7-16gb-sshd-1tb-156-fhd-12117686.html?recsource=busca-int&rectype=busca-57", 
    data, 60, [])
df['title'] = df['title'].str.replace('\\n', '')
df['dados'] = df['dados'].str.replace('\\n', '')
casas_bahia=df
casas_bahia['title'] = casas_bahia['title'].str.replace('\\t', '')
casas_bahia['title'] = casas_bahia['title'].str.replace('Notebook', '')
casas_bahia['marca'] = casas_bahia['title'].apply(lambda x: x.split(' ')[2] if x.split(' ')[1].lower() == 'gamer' else (x.split(' ')[4] if x.split(' ')[1] == '2' else x.split(' ')[1]))
casas_bahia['Processador'] = casas_bahia['title'].apply(lambda x: ' '.join([x.split(' ')[2],x.split(' ')[3]]))
casas_bahia['RAM'] = casas_bahia['title'].apply(lambda x: x.split(' ')[4])
casas_bahia['Memoria'] = casas_bahia['title'].apply(lambda x: x.split(' ')[5])
casas_bahia['dados1'] = casas_bahia['dados'].str.replace('De:', '>').str.replace('Por:', '>').str.replace('ou', '>').str.replace('R','').str.replace('até','>').str.replace('de','>')
casas_bahia['De'] = casas_bahia['dados1'].apply(lambda x: float(x.split('>')[1].replace('.','').replace(',','.').replace('$','').replace(' ','')))
casas_bahia['Por'] = casas_bahia['dados1'].apply(lambda x: x.split('>')[2].replace('.','').replace(',','.').replace('$','').replace(' ',''))
casas_bahia['Por'][casas_bahia['Por'] == ''] = '0.00'
casas_bahia['Por'] = casas_bahia['Por'].astype(float)
casas_bahia['Diferenciacao'] = 0.0
casas_bahia['Diferenciacao'][casas_bahia['Por'] != 0.0] = casas_bahia['De'] - casas_bahia['Por']
casas_bahia['Parcelas'] = casas_bahia['dados1'].apply(lambda x: x.split('>')[3] if x.split('>')[2] == ' ' else x.split('>')[4])
casas_bahia['De'] = casas_bahia['De'].astype(str).str.replace('.',',')
casas_bahia['Por'] = casas_bahia['Por'].astype(str).str.replace('.',',')
casas_bahia['Diferenciacao'] = casas_bahia['Diferenciacao'].astype(str).str.replace('.',',')
casas_bahia.to_csv('casasbahia_notebooks.csv', sep=';', index=False)
'''

# americanas 
def getData(driver, url, data, max_number, links):

    driver.get(url)
    time.sleep(5)   
    soup = BeautifulSoup(driver.page_source, "lxml")
    soup.prettify()
    if (data[data['title'].str.contains(soup.title.text)].empty == False):                 
        print("already exists in dataframe")         
        next_item = soup.find("div", class_="slick-list")
        next_link = [a['href'] for a in next_item.find_all("a", href=True)]

        links.append('https://www.americanas.com.br' + next_link[randint(0, len(next_link)-1)])
        return getData(driver, 'https://www.americanas.com.br' + next_link[randint(0, len(next_link)-1)], data, max_number, links)
    elif 'notebook' not in soup.title.text.lower():
        print('not a notebook')
        return getData(driver, links[randint(0, len(links)-1)], data, max_number, links)
    dados = {
        "title": [soup.title.text], 
        "dados": [soup.find("div",class_="main-price").text]
    }
    df = pd.DataFrame(dados,columns=["title", "dados"])
    data = pd.concat([data, df])
    next_item = soup.find("div", class_="slick-track")
    print(len(data))
    if len(data) == max_number:
        return data
    try:
        next_link = [a['href'] for a in next_item.find_all("a", href=True)]
        links.append('https://www.americanas.com.br' + next_link[randint(0,len(next_link)-1)])
        return getData(driver, 'https://www.americanas.com.br' + next_link[randint(0,len(next_link)-1)], data, max_number, links)
        
    except Exception as e:
        print("error: " + str(e))
        return getData(driver, links[randint(0,len(links)-1)], data, max_number, links)
    

data = pd.read_csv('americanas_notebooks.csv', sep=';')

df = getData(
    driver, 
    "https://www.americanas.com.br/produto/132381423/notebook-lenovo-2-em-1-yoga-520-intel-core-i7-8gb-1tb-tela-14-windows-10-platinum?DCSext.recom=RR_item_page.rr1-ClickCP&nm_origem=rec_item_page.rr1-ClickCP&nm_ranking_rec=13", 
    data, 10, [])
americanas = df
americanas['title'] = americanas['title'].str.replace('\\t', '')
americanas['marca'] = americanas['title'].apply(lambda x: x.split(' ')[2] if x.split(' ')[1].lower() == 'gamer' else (x.split(' ')[4] if x.split(' ')[0].lower() == 'macbook' else x.split(' ')[1]))
americanas['Processador'] = americanas['title'].apply(lambda x: x.split(' ')[x.split(' ').index('Core')-2:x.split(' ').index('Core')+2] if 'Core' in x.split(' ') else ('i7' if 'i7' in x.split(' ') else []))
americanas['Processador1'] = americanas['Processador'].apply(lambda x: 'i7' if 'i7' in x else ('i5' if 'i5' in x else ('i3' if 'i3' in x else ' '.join(x))))
americanas['dados1'] = americanas['dados'].str.replace('por', '>').str.replace('em', '>').str.replace('R','').str.replace('até','>').str.replace('à','>').str.replace('de','>')
americanas['De'] = americanas['dados1'].apply(lambda x: (x.split('>')[0].split(',')[0] + "," + x.split('>')[0].split(',')[1][:2]).replace('$','').replace('.',''))
americanas['Parcelas'] = americanas['dados1'].apply(lambda x: x.split('>')[0].split(',')[1][2:].replace('$','').replace(' ',''))

americanas.to_csv('americanas_notebooks_1.csv', sep=';', index=False)