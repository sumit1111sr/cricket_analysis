from bs4 import BeautifulSoup
import requests
import pandas as pd

url = ("https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season")

r = requests.get(url)

# Parsing with beautiful soup

soup = BeautifulSoup(r.content,'html.parser')

result = soup.find('table')

data = result.find_all('tr',class_='data1')

li =[]
for d in data:
    res = {
        'Team 1': d.find_all('td')[0].get_text(),
        'Team 2': d.find_all('td')[1].get_text(),
        'Winner': d.find_all('td')[2].get_text(),
        'Margin': d.find_all('td')[3].get_text(),
        'Ground': d.find_all('td')[4].get_text(),
        'Match Date': d.find_all('td')[5].get_text(),
        'id': d.find_all('td')[6].get_text()

    }
    li.append(res)

match_result = pd.DataFrame(li)
# print(match_result)
    
match_result.to_csv(r'C:\Users\sumit\OneDrive\Desktop\WorldCup2022\raw_data\match_result.csv',index=False)
