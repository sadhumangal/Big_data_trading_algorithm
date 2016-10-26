# Daily GoogleTrends Data


This little script enables to scrap and aggregate daily data from Google Trends over a long period.

The code is based on the unofficial API for Google Trends, available here: https://github.com/GeneralMills/pytrends

This is my first script as I am new in coding. Please feel free to contribute. 
You may have issue with Google request quota, try to adjust the sleeping time. 


First you need to install PyTrends : 
```pip install pytrends```

### Execution

* keywords: must be string
  example: 'Pizza, salad, tomato'
* start_date: must be string
  'today' or 'mm/yyyy'
* end_date: must be string 
  'mm/yyyy'

### Connect to Google

Parameters
* username
  - *Required*
  - a valid gmail address
* password
  - *Required*
  - password for the gmail account
* custom_useragent
  - name to identify requests coming from your script
  
### API Payload Keys

Many API methods use `payload` here is a set of known keys that can be used.

* `q`
  - keywords to get data for
  - Example ```{'q': 'Pizza'}```
  - Up to five terms in a comma seperated string: ```{'q': 'Pizza, Italian, Spaghetti, Breadsticks, Sausage'}```
    * Advanced Keywords
      - When using Google Trends dashboard Google may provide suggested narrowed search terms. 
      - For example ```"iron"``` will have a drop down of ```"Iron Chemical Element, Iron Cross, Iron Man, etc"```. 
      - Find the encoded topic by using the get_suggestions() function and choose the most relevant one for you. 
      - For example: ```https://www.google.com/trends/explore#q=%2Fm%2F025rw19&cmpt=q```
      - ```"%2Fm%2F025rw19"``` is the topic "Iron Chemical Element" to use this with pytrends
* `hl`
  - Language to return result headers in
  - Two letter language abbreviation
  - For example US English is ```{'hl': 'en-US'}```
  - Defaults to US english
* `cat`
  - Category to narrow results
  - Find available cateogies by inspecting the url when manually using Google Trends. The category starts after ```cat=``` and ends before the next ```&```
  - For example: ```"https://www.google.com/trends/explore#q=pizza&cat=0-71"```
  - ```{'cat': '0-71'}``` is the category
  - Defaults to no category
* `geo`
  - Two letter country abbreviation
  - For example United States is ```{'geo': 'US'```
  - Defaults to World
  - More detail available for States/Provinces by specifying additonal abbreviations
  - For example: Alabama would be ```{'geo': 'US-AL'}```
  - For example: England would be ```{'geo': 'GB-ENG'}```
* `tz`
  - Timezone using Etc/GMT
  - For example US CST is ```{'tz': 'Etc/GMT+5'}```
* `date`
  - Date to start from
  - Defaults to all available data, 2004 - present.
  - Custom Timeframe Pattern:
    - By Month: ```{'date': 'MM/YYYY #m'}``` where # is the number of months from that date to pull data for
      - For example: ``{'date': '10/2009 61m'}`` would get data from October 2009 to October 2014
      - Less than 4 months will return Daily level data
      - More than 36 months will return monthly level data
      - 4-36 months will return weekly level data
  - Current Time Minus Time Pattern:
    - By Month: ```{'date': 'today #-m'}``` where # is the number of months from that date to pull data for
      - For example: ``{'date': 'today 61-m'}`` would get data from today to 61months ago
      - 1-3 months will return daily intervals of data
      - 4-36 months will return weekly intervals of data
      - 36+ months will return monthly intervals of data
      - **NOTE** Google uses UTC date as *'today'*
    - Daily: ```{'date': 'today #-d'}``` where # is the number of days from that date to pull data for
      - For example: ``{'date': 'today 7-d'}`` would get data from the last week
      - 1 day will return 8min intervals of data
      - 2-8 days will return Hourly intervals of data
      - 8-90 days will return Daily level data
    - Hourly: ```{'date': 'now #-H'}``` where # is the number of hours from that date to pull data for
      - For example: ``{'date': 'now 1-H'}`` would get data from the last hour
      - 1-3 hours will return 1min intervals of data
      - 4-26 hours will return 8min intervals of data
      - 27-34 hours will return 16min intervals of data
* `gprop`
  - What search data we want
  - Example ```{'gprop': 'images'}```
  - Defaults to web searches
  - Can be ```images```, ```news```, ```youtube``` or ```froogle``` (for Google Shopping results)

##Credits
* Based on unofficial Google trends API Pytrends
    - https://github.com/GeneralMills/pytrends
