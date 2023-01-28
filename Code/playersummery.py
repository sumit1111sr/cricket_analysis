from bs4 import BeautifulSoup
import requests
import pandas as pd

url = ("https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=2022%2F23;trophy=89;type=season")

r = requests.get(url)

# Parsing with beautiful soup

soup = BeautifulSoup(r.content,'html.parser')

result = soup.find('table')

data = result.find_all('tr',class_='data1')

links = []
for d in data:
    for p in d.find_all('td')[6].find_all('a'):
        links.append("https://stats.espncricinfo.com"+p.get('href'))

player_info_link = set()
player_biodata = []
for link in links:
        
    req = requests.get(link)
    response = BeautifulSoup(req.content,'html.parser')
    
    table =  response.find_all("div",class_="ds-rounded-lg ds-mt-2")
    
    if table == []:
        # print("Match Do not played")
        pass
    else:

        for player in table[0].find_all('a',class_="ds-inline-flex ds-items-start ds-leading-none"):
            # for p in player:
            p = "https://www.espncricinfo.com/cricketers/"+player.get('href')
           
            # break
            if len(p)<85:
                player_info_link.add(p)

            
                # print(player_data)
        # player_info = table.find_all("a",class_="ds-inline-flex ds-items-start ds-leading-none")
        
        # for player_info in table.find_all("a",class_="ds-inline-flex ds-items-start ds-leading-none"):
        #     print(player_info)
        
        # break

        for player in table[1].find_all('a',class_="ds-inline-flex ds-items-start ds-leading-none"):
            # for p in player:
            name = player.text
            p = "https://www.espncricinfo.com"+player.get('href')
            if len(p)<85:
                player_info_link.add(p)



for url in player_info_link:

    req = requests.get(url)

    response = BeautifulSoup(req.content,'html.parser')

    data = response.find("div",class_="ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8")
    name_tag = response.find("div",class_="ds-pt-8 ds-px-6 ds-pb-2 ds-text-raw-white")
    

    # break

    if data is None:
        pass
    else:

        personal_info = data.find_all("span",class_="ds-text-title-s ds-font-bold ds-text-typo")
        name = name_tag.find("h1",class_="ds-text-title-l ds-font-bold").text
        # break
        team = response.find("span",class_="ds-cursor-pointer ds-inline-flex ds-items-start ds-leading-none").text
        battingStyle = personal_info[3].text
        bowlingStyle = personal_info[4].text
        if len(personal_info)!=6: 
            playingRole = None
        else:
            playingRole = personal_info[5].text

        

        player_biodata.append({
            "name":name,
            "team":team,
            "battingStyle":battingStyle,
            "bowlingStyle":bowlingStyle,
            "playingRole":playingRole

        })


df = pd.DataFrame(player_biodata)

print(df)

df.to_csv(r'C:\Users\sumit\OneDrive\Desktop\WorldCup2022\raw_data\playersummery.csv',index=False)
    
print("Thankyou")

