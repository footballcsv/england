import requests
import csv
from datetime import datetime


standings_url ="https://fbref.com/en/comps/9/2020-2021/schedule/2020-2021-Premier-League-Scores-and-Fixtures"
data = requests.get(standings_url)

from bs4 import BeautifulSoup
soup = BeautifulSoup(data.text)


standings = soup.select('table.stats_table')[0]


main_list=[]
for team in standings.find_all('tbody'):
  rows = team.find_all('tr')
  for i in rows:
    # round and day
    round = i.find('th',{'data-stat':'gameweek'})
    if round!=None:
      Round = round.text
    day = i.find('td',{'data-stat':'dayofweek'})
    if day!= None:
      Day=day.text


    #date
    date=i.find('td',{'data-stat':'date'})
    date = date.find('a')
    if date!=None:
      Date=date.text
      #converting date formats
      date_obj = datetime.strptime(Date, "%Y-%m-%d")
      Date = date_obj.strftime("%b %d %Y")
      

    #home_team
    ht= i.find('td',{'data-stat':'home_team'})
    ht=ht.find('a')
    if ht !=None:
      Ht=ht.text
    
    #score
    sc= i.find('td',{'data-stat':'score'})
    sc=sc.find('a')
    if sc!=None:
      Sc=sc.text
    
    #away_team
    at= i.find('td',{'data-stat':'away_team'})
    at=at.find('a')
    if at!=None:
      At=at.text


      
    #each game
    if Round =='':
      continue
    game = Round + ',' + Day + ' ' + Date + ',' +Ht + ',' + Sc + ',' + At
    main_list.append(game)
  main_list.sort(key = lambda x: int(x.split(',')[0]))


with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Round", "Date", "Team 1", "FT", "Team 2"])
    for row in main_list:
        writer.writerow(row.split(','))
