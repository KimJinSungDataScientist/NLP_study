import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta


html = 'https://www.weather.go.kr/weather/observation/currentweather.jsp?auto_man=m&stn=0&type=t99&reg=109&tm='
parm = '.00%3A00&x=31&y=9'

not_snow = ['05','06','07','08','09','10']

weather = [] #날씨
temp = [] # 온도
apparent_temp = [] # 체감온도
precipitation = [] # 강수량
amount_of_snowfall = [] # 적설량
humidity = [] # 습도
wind_direction = [] # 풍향
wind_speed = [] # 풍속
wind_speed_edit = [] # 풍속 전처리


# 2020년 모든 날짜 가져오는 부분
def date_range(start, end):
    start = datetime.strptime(start, "%Y.%m.%d")
    end = datetime.strptime(end, "%Y.%m.%d")
    dates = [(start + timedelta(days=i)).strftime("%Y.%m.%d") for i in range((end-start).days+1)]
    return dates

dates = date_range("2020.01.01", "2020.01.05")


# 2020년도 날짜별 데이터 크롤링 부분
for i in dates:
    source = requests.get(html + i + parm)
    soup = BeautifulSoup(source.content, "html.parser")
    table = soup.find('table', {'class': 'table_develop3'})
    ls = table.find_all('tr')[5].find_all('td')

    if i[5:7] in not_snow:
        snow = -1
        amount_of_snowfall.append(0)
    else:
        snow = 0
        amount_of_snowfall.append(ls[8].text)

    time.sleep(0.1)
    weather.append(ls[1].text)
    temp.append(ls[5].text)
    apparent_temp.append(ls[7].text)
    precipitation.append(ls[8].text)
    humidity.append(ls[10 + snow].text)
    wind_direction.append(ls[11 + snow].text)
    wind_speed.append(ls[12 + snow].text)
    print(i)

# 풍속 데이터 전처리 부분
for i in wind_speed:
    try:
        wind_speed_edit.append(i.split('\'')[1])
    except:
        wind_speed_edit.append(0)


df = pd.DataFrame([ x for x in zip(dates,weather,temp,apparent_temp,precipitation,amount_of_snowfall,humidity,wind_direction,wind_speed_edit)],columns=['날짜','날씨','기온','체감온도','강수량','적설량','습도','풍향','풍속'])
df = df.apply(lambda x : x.replace(u'\xa0',u'0.0'),axis=1)
df.to_csv('2020_seoul_weather.csv',encoding='cp949',index=False)