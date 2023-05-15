import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import smtplib
from smtplib import SMTP
import time
import json
import re
import sys
from html import unescape
from datetime import date
from urllib.parse import unquote
import gspread

# check if the first page has any private owner listings.
apartments_url = []
private_links = []
def check_page():
    s = requests.session()
    thisurl = 'https://www.immoweb.be/nl/zoeken/appartement/te-koop?countries=BE&isNewlyBuilt=false&maxBedroomCount=3&maxPrice=200000&maxSurface=130&minBedroomCount=1&minPrice=100000&minSurface=65&postalCodes=2000,2018,2060,2140,2170,2600,2610,2627,2640,2650,2660,2845,2850,2900,2980&page=1&orderBy=newest'
    # print  (thisurl)
    response1 = s.get(thisurl).text
    # print (s.cookies)
    data = json.loads(unescape(re.search(r":results='(.*?)'", response1).group(1)))
    # print (data)
    for p in data:
        apartments_url.append("https://www.immoweb.be/en/classified/{}".format(p["id"]))

    # print (apartments_url)

# this function will filter out the private listings
def check_priv():
    for i in apartments_url:
        r = requests.get(i)
        soup = BeautifulSoup(r.content,'html.parser')
        try:
            script = soup.find_all('script')[1].text.strip()[29:-2]
            data = json.loads(script)
            customer = data['customer'] 
            if customer["family"] == 'private':
                check_sheet(i,soup)
        except:
            pass


# This function will check whether the link is in sheets or not
def check_sheet(link,soup):
    gc = gspread.service_account(filename='creds.json') 
    sh = gc.open('scrapetosheets').sheet1
    gsheet_data = sh.get_all_records()
    if sh.findall(link) == []:             #if the link is not in sheets
        update_sheet(link,soup)
        print ("found a link")
        send_email(link)

        
# This function will update the sheets if one of the private links were not in sheets
def update_sheet(i,soup):
    title = soup.title.string[:-10]
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('scrapetosheets').sheet1
    Data = {'Title':title, 'Link':i , 'Date':d4}
    sh.append_row([Data['Title'],Data['Link'],Data['Date']])
    
# This function will send email if private listing are avail
def send_email(i):
    try:
        server= smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('email', 'password here')   #Email address from which you want to send email
        subject="[BOT] New Private Property Found!"
        body="Hello, A new private property listing is found. Check it under the mentioned link before it sell out."
        link = f"Link =>  {i}"
        msg = f"Subject:{subject}\n\n{body} \n {link}"
        server.sendmail( 'xyz@gmail.com','abc@gmail.com',msg)
    except Exception as e:
        print ("Error in sending email", e)
        server.sendmail( 'xyz@gmail.com','xyz@gmail.com','Error in sending email')
    server.quit()

print ('script started working at', time.ctime())
check_page()
check_priv()
print ('script ended working at', time.ctime(),' \n')
