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

bowlingSummary = []
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
    # print(team)
    # break
    
    # inning
    inning_team = response.find_all("span",class_="ds-text-title-xs ds-font-bold ds-capitalize")

    inning = ["Inning1","Inning2"]
    bowling_table = response.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto")


    # First Inning Bowling
    if bowling_table == []:
        # print("Match Do not played")
        pass
    else:
       for val in bowling_table[0].find_all('tr',class_=""): 

            if val.th:
                continue
            else:
                # print(val)
                bowler = val.find("td",class_="ds-min-w-max").text

                # wicket 
                wicket = val.find("td",class_='ds-w-0 ds-whitespace-nowrap ds-text-right').text

                # getting other stats related to bowler
                stat = val.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')

                over = stat[0].text
                maiden = stat[1].text
                runs = stat[2].text
                economy = stat[3].text
                zeros = stat[4].text
                fours = stat[5].text
                sixes = stat[6].text
                wide = stat[7].text
                no_ball = stat[8].text
                



                
                
            bowlingSummary.append(
                {
                "match":team,
                "bowlingTeam":inning_team[1].text,
                "bowler":bowler,
                "over":over,
                'maiden':maiden,
                "runs":runs,
                "wicket":wicket,
                "economy":economy,
                "0s":zeros,
                "4s":fours,
                "6s":sixes,
                "wide":wide,
                "NB":no_ball})
            # break

    # First Inning Bowling
    if bowling_table == []:
        # print("Match Do not played")
        pass
    else:
       for val in bowling_table[1].find_all('tr',class_=""): 

            if val.th:
                continue
            else:
                # print(val)
                bowler = val.find("td",class_="ds-min-w-max").text

                # wicket 
                wicket = val.find("td",class_='ds-w-0 ds-whitespace-nowrap ds-text-right').text

                # getting other stats related to bowler
                stat = val.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')

                over = stat[0].text
                maiden = stat[1].text
                runs = stat[2].text
                economy = stat[3].text
                zeros = stat[4].text
                fours = stat[5].text
                sixes = stat[6].text
                wide = stat[7].text
                no_ball = stat[8].text
                             
                
            bowlingSummary.append(
                {
                "match":team,
                "bowlingTeam":inning_team[0].text,
                "bowler":bowler,
                "over":over,
                'maiden':maiden,
                "runs":runs,
                "wicket":wicket,
                "economy":economy,
                "0s":zeros,
                "4s":fours,
                "6s":sixes,
                "wide":wide,
                "NB":no_ball})

    # print(bowlingSummary)
    # break
        
dataframe = pd.DataFrame(bowlingSummary)
dataframe.to_csv(r'C:\Users\sumit\OneDrive\Desktop\WorldCup2022\raw_data\bowlingSummary.csv',index=False)
