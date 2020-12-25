# libraries
import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Entry:
    def __init__(self, date, current, previous):
        date = date.replace(' ', '')
        current = current.replace(' ', '')
        current = current.replace(',', '')
        previous = previous.replace(' ', '')
        previous = previous.replace(',', '')
        self.date = str(date)
        self.current = int(current)
        self.previous = int(previous)
            
    def format(self):
        ans = "Date: "+self.date+"\t|\tCurrent traffic: "+str(self.current)+"\t|\tPrevious traffic: "+str(self.previous)
        return ans


def parseData(str):
    split = str.splitlines()
    return Entry(split[1], split[2], split[3])


url1='https://www.tsa.gov/coronavirus/passenger-throughput?page=0'
url2='https://www.tsa.gov/coronavirus/passenger-throughput?page=1'
dataset = []

def funct(url):
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath("//tr")

    #grabs the data from the page
    for T in tr_elements[1:]:
        #print(str(tr_elements.index(T))+" - "+T.text_content())
        temp = parseData(T.text_content())
        dataset.insert(0, temp)
        #print("thing: " + str(T.text_content()))

funct(url1)
funct(url2)
#x = []
y1 = []
y2 = []
for i in range(len(dataset)):
   # x.append(i)
    y1.append(dataset[i].current)
    y2.append(dataset[i].previous)

for data in dataset:
    print(data.format())


# Data
df=pd.DataFrame({'2020': y1, '2019': y2})

# multiple line plot
plt.plot(df)
plt.plot( '2020', data=df, marker='', color='blue', linewidth=2)
plt.plot( '2019', data=df, marker='', color='olive', linewidth=2)
#plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
plt.legend()
plt.ylabel("Number of People Passed Through TSA")
plt.xlabel("Days Since "+dataset[0].date[:dataset[0].date.rfind('/')])
plt.title("Scraped TSA Data")
plt.show()
