from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import cv2
import time
import requests
import pandas as pd
from selenium.webdriver.common.by import By
def main(chrome,url):
    df=pd.DataFrame(columns=["text","status"])
    i="WAC2390054"
    s=chrome.get(url)
    for p in range(340,650,5):
        chrome.find_element(By.ID,"receipt_number").send_keys(i+str(p))
        chrome.find_element(By.ID,"receipt_number").submit()
        time.sleep(2)
        #myElem = WebDriverWait(chrome, delay).until(EC.presence_of_element_located((By.ID, 'landing-page-header')))
        text=chrome.find_element(By.ID,"landing-page-header").text
        #body.text=i+str(p)
        #chrome.find_element(By.NAME,"initCaseSearch").
        df.loc[len(df)]=[i+str(p),text]
    #body.screenshot("foo.png")
    #im=cv2.imread("foo.png")
    #cv2.imshow("he",im)
    #cv2.waitKey(0)
    print(df)
def rvda(chrome,url):
    s=chrome.get(url)
    action=ActionChains(chrome)
    df=pd.DataFrame(columns=["DNAME","ADD","City","State","Zip","Web","Phone","Type"])
    for i in range(2):
        s=chrome.find_element(By.ID,"ctl01_TemplateBody_WebPartManager1_gwpste_container_SearchForm_ciSearchForm_CompanyStateDDL")
        action.click(s).perform()
        action.send_keys(Keys.ARROW_DOWN).perform()
        p=chrome.find_element(By.ID,"ctl01_TemplateBody_WebPartManager1_gwpste_container_SearchForm_ciSearchForm_SearchSubmit")
        action.click(p).perform()
        time.sleep(2)
        html=chrome.page_source
        soup=bs(html)
        table=soup.find("table")
        for i in table.find_all("tr"):
            try:
                for j in i.find_all("td")[0].find_all("img"):
                    print(j["alt"])
                print(i.find_all("td")[1].text.split())
            except:
                continue
            #print(i.text)
        #action.click(chrome.find_element(By.LINK_TEXT,"Return to Search")).perform()
        chrome.back()
        time.sleep(3)
def find_data(soup):
    soup=soup.find("main")
    #print(soup)
    name=soup.find("div",{"class":"prodName"}).get_text()
    drug=soup.find("div",{"class":"drug-manu"}).get_text()
    try:
        pre_re=soup.find("span",{"class":"req_Rx"}).get_text()
    except:
        pre_re=""
    best=soup.find("span",{"class","final-price"}).get_text()
    mrp=soup.find("span",{"class","price"}).get_text()
    manu=soup.find("span",{"class","drug-manu"}).get_text()
    try:
        pack=soup.find("span",{"class","drug-varient"}).get_text()
    except:
        pack=""
    try:
        intro=soup.find(id="np_tab1").text
    except:
        intro=""
    #print(intro)
    try:
        dou=soup.find(id="np_tab6").text
    except:
        dou=""
    try:
        wp=soup.find(id="np_tab9").text
    except:
        wp=""
    try:
        cate=soup.find(id="np_tab12").text
    except:
        cate=""
    data=[name,drug,pre_re,manu,pack,mrp,best,cate,intro,dou,wp]
    return data
def mg(chrome,url):
    df=pd.DataFrame(columns=["Medicine name","Saltname","Prescription required","Manufacturer","Packaging","MRP","Best price","Category","Introduction","Directions for use","Warning and precautions","URL"])
    s=chrome.get(url)
    action=ActionChains(chrome)
    #page=chrome.find_element(By.ID,"list-nav")
    try:
        for i in [a["href"] for a in bs(chrome.page_source,"html.parser").select("ul.alpha-drug-list>li>a")][31:]:
            try:
                chrome.get(i)
            except:
                continue
            name=[a["href"] for a in bs(chrome.page_source,"html.parser").select("li.product-item>a")]
            #find_elements(By.CLASS_NAME,"product-item")
            for j in name:
                try:
                    #chrome.get(j)
                    #print(j)
                    soup=requests.get(j)
                #time.sleep(2)
                    soup=bs(soup.content,features="html.parser")
                    df.loc[len(df)]=find_data(soup)+[j]
                except:
                    continue
                #time.sleep(3)
            print(df.tail(2))
            chrome.back()
            time.sleep(2)
    except Exception as e:
        print(e)
    finally:
        return df
def amazons(chrome,url):
    chrome.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = bs(chrome.page_source, 'html.parser')
    #print(soup.prettify())
    # Find the deal elements on the page
    deal_elements = soup.find_all('div[class*="a-image-container a-dynamic-image-container aok-align-center-horizontally"]')

    # Prepare a list to store the deal details
    deals = []

    # Extract the required details from the deal elements
    for deal_element in deal_elements:
        title = deal_element.find('span', {'class': 'a-text-normal'}).text.strip()
        original_price = deal_element.find('span', {'class': 'a-offscreen'}).text.strip()
        deal_price = deal_element.find('span', {'class': 'a-price'}).find('span', {'class': 'a-offscreen'}).text.strip()
        product_url = 'https://www.amazon.com' + deal_element.find('a')['href']
        image_url = deal_element.find('img', {'class': 's-image'})['src']
        deals.append({'title': title, 'original_price': original_price, 'deal_price': deal_price, 'product_url': product_url, 'image_url': image_url})

    return deals
if __name__=="__main__":
    url="https://www.amazon.in/gp/goldbox?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%252295385C000FD7E4E2D8F69FA5B305F118%2522%252C%2522dealType%2522%253A%2522DEAL_OF_THE_DAY%2522%252C%2522sorting%2522%253A%2522FEATURED%2522%257D"
    #"https://www.netmeds.com/prescriptions/"
    import undetected_chromedriver as us
    options=us.ChromeOptions()
    chrome=us.Chrome(use_subprocess=True,options=options)
    try:
        df=amazons(chrome,url)
    finally:
        print(df)
        #df.to_csv("Data2.csv",index=False,headers=False,mode="a")
        #chrome.quit()
