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
a = 1
battingSummary = []
for link in links:
    req = requests.get(link)
    response = BeautifulSoup(req.content,'html.parser')

    # print(response)
    # break
    # teams playing
    if response.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize") == []:
        # print("Match Do not played")
        continue
    else:
        teams = response.find_all('span',class_="ds-text-title-xs ds-font-bold ds-capitalize")
        team = teams[0].text + " VS "+ teams[1].text
    # break

    # inning
    inning_team = response.find_all("span",class_="ds-text-title-xs ds-font-bold ds-capitalize")
    # position of the players
    pos_1 = 1
    inning = ["Inning1","Inning2"]
    table = response.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")
    if table == []:
        # print("Match Do not played")
        continue
    else:
        
        for val in table[0].find_all('tr',class_=""):
            if val.find("a",class_="ds-inline-flex ds-items-start ds-leading-none") != None:
                batsman = val.find("a",class_="ds-inline-flex ds-items-start ds-leading-none").text.replace("\xa0","").strip()
            else:
                break
            
            
            dismissal = val.find("td",class_="ds-min-w-max !ds-pl-[100px]").text.replace("†","").strip()

            right_text = val.find_all('td',"ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right")
            
            runs = right_text[0].text.strip()

            balls = right_text[1].text.strip()
            maiden = right_text[2].text.strip()

            fours = right_text[3].text.strip()
            sixes = right_text[4].text.strip()
            strike_rate = right_text[5].text.replace("-","0").strip()


                
            
            battingSummary.append({"team":team,"teamInnings":inning_team[0].text,"inning":inning[0],"position":pos_1,"batsman" : batsman,"dismissal":dismissal,"runs":runs,"balls":balls,'M':maiden,"4s":fours,"6s":sixes,"SR":strike_rate})

            pos_1 = pos_1+1




        # second inning
        pos_2 = 1
        for val in table[1].find_all('tr',class_=""):
            if val.find("a",class_="ds-inline-flex ds-items-start ds-leading-none") != None:
                batsman = val.find("a",class_="ds-inline-flex ds-items-start ds-leading-none").text.replace("\xa0","").strip()
            else:
                break
            
            
            dismissal = val.find("td",class_="ds-min-w-max !ds-pl-[100px]").text.replace("†","").strip()

            right_text = val.find_all('td',"ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right")
            
            runs = right_text[0].text.strip()

            balls = right_text[1].text.strip()
            maiden = right_text[2].text.strip()

            fours = right_text[3].text.strip()
            sixes = right_text[4].text.strip()
            strike_rate = right_text[5].text.replace("-","0").strip()


                
            
            battingSummary.append({"team":team,"teamInnings":inning_team[1].text,"inning":inning[1],"position":pos_2,"batsman" : batsman,"dismissal":dismissal,"runs":runs,"balls":balls,'M':maiden,"4s":fours,"6s":sixes,"SR":strike_rate})

            pos_2 = pos_2+1
     
    # break
        # dataframe = pd.DataFrame(battingSummary)
        # print(dataframe)
        # print(a)
        # print()
        # print()
        # a = a+1

df = pd.DataFrame(battingSummary)
df.to_csv(r'C:\Users\sumit\OneDrive\Desktop\WorldCup2022\raw_data\battingsummery.csv',index=False)


    