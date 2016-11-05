###########################################################################
#   IP address changer, rout traffic through Tor, it needs Tor to be running 
###########################################################################
import socket
import socks

import requests
from bs4 import BeautifulSoup

from stem import Signal
from stem.control import Controller


controller = Controller.from_port(port=9151)

def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket

def renew_tor():
    controller.authenticate()
    controller.signal(Signal.NEWNYM)

def showmyip():
    url = "http://www.showmyip.gr/"
    r = requests.Session()
    page = r.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    ip_address = soup.find("span",{"class":"ip_address"}).text.strip()
    print(ip_address)
    
#############################################################
# Random Name for custom_useragent
#############################################################

def randomName(length):
    import string
    import random
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

################################################################
# Main functions 
################################################################

def requestDailydatafromGT(keywords, geography, date):  #parameters must be strings 
    from pytrends.request import TrendReq
    import time
    from random import randint
    
    
    google_username = ""  #put your gmail account
    google_password = "" #passwrd
    mes=0
    
    if date =='today':
        requestdate='today 3-m'
    else:
        requestdate=str(date)+' 3m'
    trend_payload = {'q': keywords,'hl': 'en-US','geo': geography, 'date': requestdate} #define parameters of the request
    pytrend = TrendReq(google_username, google_password, custom_useragent=randomName(randint(5,10)) #connect to Google
    
    while mes==0:
        try:           
            results= pytrend.trend(trend_payload, return_type='dataframe').sort_index(axis=0, ascending=False) #launch request in Google tren0ds
            mes=1
        
        except Exception:
            renew_tor()
            connectTor()
            showmyip() #optional
            pytrend = TrendReq(google_username, google_password, custom_useragent=randomName(randint(5,10)) #connect to Google
            mes=0
        
    return results

def requestAllDailyData(keywords,geography,start_date,end_date):
    import numpy as np
    import pandas as pd
    from datetime import datetime
    
    Time_end_date=datetime(int(end_date[3:7]),int(end_date[0:2]), 1)
    
    dailyData=requestDailydatafromGT(keywords, geography, start_date) #we look for the first period
        
    lastDate=datetime(dailyData.index[-1].year,dailyData.index[-1].month,1) #This is the lastDate of the dailyData Frame.
    RemainingTime=lastDate-Time_end_date

    while   RemainingTime.days >0:

        #we look for the new date of the data Frame to be added at the end 
        Month=(dailyData.index[-1]-pd.DateOffset(months=2)).month
        Year=(dailyData.index[-1]-pd.DateOffset(months=2)).year
        NewDate="{0}/{1}".format(Month,Year)
        
        NewdailyData=requestDailydatafromGT(keywords, geography,NewDate)
        
        NewdailyData[NewdailyData==0]=0.00001
        NewdailyData=NewdailyData[NewdailyData.index<=dailyData.index[-1]]
           
        #compute the coef in order to adjust the new data
        MatrixFullCoef= pd.DataFrame(index=NewdailyData.index, columns=NewdailyData.columns)
        MatrixFullCoef[:1]=dailyData[-1:]/NewdailyData[:1]
        
        for i in range(len(MatrixFullCoef)):
            MatrixFullCoef.iloc[i]=MatrixFullCoef.iloc[0]
           
        #Normalize the NewDailyData with the coef calculated before
        AdjustedNewdailyData=(NewdailyData*MatrixFullCoef)[1:]
        
        #add the new data Frame of daily datas to the existing one
        dailyData= dailyData.append(AdjustedNewdailyData,ignore_index=False)

        #return the last date of the computed dataframe of daily datas
        lastDate=datetime(dailyData.index[-1].year,dailyData.index[-1].month,dailyData.index[-1].day) 

        RemainingTime=lastDate-Time_end_date

    return dailyData


##############################################
#   Execution
#############################################
import matplotlib.pyplot as plt
%matplotlib inline

keywords='trump'
Geo='US'
start_date="today"
end_date="01/2014"

DailyGTData=requestAllDailyData(keywords,Geo,start_date,end_date)

#plot the data
DailyGTData.sort_index(axis=0, ascending=True).plot()
plt.xlabel('time')
plt.ylabel(keywords)

plt.show()
