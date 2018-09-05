from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']#'postgres://xjmgzqbovystmz:b59b93d8d13c724a530425e1e74b603b8ce3f7a2e56c98caa0156e7c7f5ca97e@ec2-107-22-221-60.compute-1.amazonaws.com:5432/djo19060qdtmp'

session = HTMLSession()
r = session.get('https://laundryview.com/home/17/1394839')
print(r.html)
r.html.render(wait=3,sleep=3)
# check to make sure that the html actually has rendered:
if(r.html.text.find('01 ')>0):
    # find washer and dryer availability
    print(r.html.find('span.washers')[0])
    print(r.html.find('span.dryers')[0])
    print(r.html.text)
    washersAvail = int(r.html.find('span.washers')[0].text[9:-6])
    dryersAvail = int(r.html.find('span.dryers')[0].text[8:-6])
    print(washersAvail) #Out of Order
    print(dryersAvail)
    theTime = int(round(time.time()))

    # add results to database
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO dataTable (theTime, washers, dryers) VALUES (%s, %s, %s)",(theTime, washersAvail, dryersAvail))
    conn.commit()
    cur.close()
    conn.close()

    print('Success')
else:
    print('html not rendered')
    print(r.html.text)

# print('Time: ' + str(round(time.time())))
# print('Washers: ' + washersAvail)
# print('Dryers: ' + dryersAvail)

# -------------------------------------------------

# from selenium import webdriver
# from bs4 import BeautifulSoup
# import os
# from selenium.webdriver.chrome.options import Options as ChromeOptions
#
# # set up webdriver for laundryview page
# chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
# opts = ChromeOptions()
# opts.binary_location = chrome_bin
# self.selenium = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
#
# browser = webdriver.Chrome()
# browser.get('https://laundryview.com/home/17/1394839')
#
# # get html (affected by js) and parse it
# innerHTML = browser.execute_script("return document.body.innerHTML").encode('utf-8')
# parsedHTML = BeautifulSoup(innerHTML,'html.parser')
#
# # get a list of all machine information and process it
# dataFile = open('data.txt','a+')
# machines = parsedHTML.find_all('div','list-item ng-scope')
# for machine in machines:
#     # print(machine['ng-if'].encode('utf-8') + "hi!")
#     dataFile.write(machine['ng-if'].encode('utf-8')) #will be used to identify W/D
#     timeRemainingSpan = machine.find('span','status-min ng-binding ng-scope') #only present if machine is in use
#     if(timeRemainingSpan != None):
#         dataFile.write(timeRemainingSpan.encode('utf-8')) #process this to get number of minutes left and record it
#     dataFile.write('\n')
