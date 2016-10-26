def requestDailydatafromGT(keywords, geography, date):  #parameters must be strings 
    from pytrends.request import TrendReq
    import time

    google_username = "xxxx@gmail.com"  #put your gmail account
    google_password = "xxxx"
    path = ""

    #Connect to google
    pytrend = TrendReq(google_username, google_password, custom_useragent=None)
    time.sleep(20)   #Default Sleep time is 20 seconds in order to avoid Google quota limit

    if date =='today':
        requestdate='today 3-m'

    else:
        requestdate=str(date)+' 3m'

    trend_payload = {'q': keywords,'hl': 'en-US','geo': geography, 'date': requestdate} #define parameters of the request

    results= pytrend.trend(trend_payload, return_type='dataframe').sort_index(axis=0, ascending=False) #launch request in Google trends

    return results
    
    
    
def requestAllDailyData(keywords,geography,start_date,end_date):
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import time
    
    Time_end_date=datetime(int(end_date[3:7]),int(end_date[0:2]), 1)


    dailyData=requestDailydatafromGT(keywords, geography, start_date) #we look for the first period
        
    lastDate=datetime(dailyData.index[-1].year,dailyData.index[-1].month,1) #This is the lastDate of the dailyData Frame.
    RemainingTime=lastDate-Time_end_date

    while   TimeRemaining.days >60:

        #look for the new date of the data Frame to be added at the end 
        Month=(dailyData.index[-1]-pd.DateOffset(months=2)).month
        Year=(dailyData.index[-1]-pd.DateOffset(months=2)).year
        NewDate="{0}/{1}".format(Month,Year)
        
        NewdailyData=requestDailydatafromGT(keywords, geography,NewDate)
        NewdailyData=NewdailyData[NewdailyData.index<=dailyData.index[-1]]
            
        #compute the coef in order to rescale the new data
        MatrixFullCoef= pd.DataFrame(index=NewdailyData.index, columns=NewdailyData.columns)
        MatrixFullCoef[:1]=dailyData[-1:]/NewdailyData[:1]
        
        for i in range(len(MatrixFullCoef)):
            MatrixFullCoef.iloc[i]=MatrixFullCoef.iloc[0]
        
        
        #Adjust the NewDailyData with the coef calculated before
        AdjustedNewdailyData=(NewdailyData*MatrixFullCoef)[1:]
        
        #add the new data Frame of daily datas to the existing one
        dailyData= dailyData.append(AdjustedNewdailyData,ignore_index=False)

        #return the last date of the computed dataframe of daily datas
        lastDate=datetime(dailyData.index[-1].year,dailyData.index[-1].month,dailyData.index[-1].day) 

        RemainingTime=lastDate-Time_end_date

    return dailyData


#Execution
import matplotlib.pyplot as plt
keywords='time' 
Geo='GB-ENG'
start_date="today"
end_date="01/2016"

DailyGTData=requestAllDailyData(keywords,Geo,start_date,end_date)

DailyGTData.plot()
plt.xlabel('time')
plt.ylabel(keywords)

plt.show()
