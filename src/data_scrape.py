# libraries
import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

numbers = ['0','1','2','3','4','5','6','7','8','9']

class Entry:
    def __init__(self, date, y21, y20, y19):
        date = date.replace(' ', '')
        y21 = y21.replace(' ', '').replace(',','')
        y20 = y20.replace(' ', '').replace(',','')
        y19 = y19.replace(' ', '').replace(',','')
        self.date = str(date)
        self.y21 = int(y21)
        self.y20 = int(y20)
        self.y19 = int(y19)
            
    def format(self):
        ans = "Date: "+self.date+"\t|\t2021 traffic: "+str(self.y21)+"\t|\t2020 traffic: "+str(self.y20)+"\t|\t2019 traffic: "+str(self.y19)
        return ans


def parseData(str):
    split = str.splitlines()
    print("split: "+split[1]+" | "+split[2]+" | "+split[3]+" | "+split[4])
    res = [ele for ele in numbers if(ele in split[2])] 
    if(len(res) == 0):
        return Entry(split[1], "0", split[3], split[4])
    return Entry(split[1], split[2], split[3], split[4])


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
y3 = []
for i in range(len(dataset)):
   # x.append(i)
    y1.append(dataset[i].y19)
    y2.append(dataset[i].y20)
    y3.append(dataset[i].y21)

for data in dataset:
    print(data.format())


# Data
df=pd.DataFrame({'2019': y1, '2020': y2, '2021': y3})

# multiple line plot
plt.plot(df)
plt.plot( '2019', data=df, marker='', color='blue', linewidth=2)
plt.plot( '2020', data=df, marker='', color='olive', linewidth=2)
plt.plot( '2021', data=df, marker='', color='green', linewidth=2)
#plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
plt.legend()
plt.ylabel("Number of People Passed Through TSA")
plt.xlabel("Days Since "+dataset[0].date[:dataset[0].date.rfind('/')])
plt.title("Scraped TSA Data")
plt.show()
