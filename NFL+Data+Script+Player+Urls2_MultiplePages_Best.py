#Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
#Type "help", "copyright", "credits" or "license()" for more information.

 

import time
import datetime
import sys
import os
from bs4 import BeautifulSoup
import lxml
import random
import requests
import pandas as pd
 

print("start: " + str(datetime.datetime.now().strftime("%I:%M %p")))
#here we keep the base url string from the website. The difference between Rushing and Passing and Receiving are all slightly different
base_url_string = "https://www.nfl.com"
 
##I got all of these variasions by inspecting the element of each nav bar on the NFL site that you showed me. Notice that I changed the year out for a {0} in each of the addresses. We will an F string later to replace this {0} with the year.
##um Remark the base url variations for whatever you want. Currently its just reaching out to "Passing" + "Rushing"
base_url_variations = {
'Passing':"/stats/player-stats/category/passing/{0}/reg/all/passingyards/desc" 
,'Receiving':"/stats/player-stats/category/receiving/{0}/reg/all/receivingreceptions/desc"
,'Rushing':"/stats/player-stats/category/rushing/2022/reg/all/rushingyards/desc"
,'Kickoff Returns':"/stats/player-stats/category/kickoff-returns/{0}/reg/all/kickreturnsaverageyards/desc"
,'Punting':"/stats/player-stats/category/punts/{0}/reg/all/puntingaverageyards/desc"
,'Punt Returns':"/stats/player-stats/category/punt-returns/{0}/reg/all/puntreturnsaverageyards/desc"
,'Field Goals':"/stats/player-stats/category/field-goals/{0}/reg/all/kickingfgmade/desc"
,'Team Defense Passing':"/stats/team-stats/defense/passing/{0}/reg/all" 
,'Team Offense Passing':"/stats/team-stats/offense/passing/{0}/reg/all" 
,'Team Special Scoring':"/stats/team-stats/special-teams/scoring/{0}/reg/all"
,'Team Defense rushing':"/stats/team-stats/defense/rushing/{0}/reg/all"
,'Team Defense scoring':"/stats/team-stats/defense/scoring/{0}/reg/all"
,'Fumbles':"/stats/player-stats/category/fumbles/{0}/reg/all/defensiveforcedfumble/desc"
,'Interceptions':"/stats/player-stats/category/interceptions/{0}/reg/all/defensiveinterceptions/desc"
,'Team Defense downs':"/stats/team-stats/defense/downs/{0}/reg/all"
,'Fumbles':"/stats/player-stats/category/fumbles/{0}/reg/all/defensiveforcedfumble/desc"
,'Interceptions':"/stats/player-stats/category/interceptions/{0}/reg/all/defensiveinterceptions/desc"

####------------------------------------------------------------------------------------------------------------------------------------------------------------------   

## ,'Tackles':"/stats/player-stats/category/tackles/{0}/reg/all/defensivecombinetackles/desc"

## ,'Kickoffs':"/stats/player-stats/category/kickoffs/{0}/reg/all/kickofftotal/desc"
## ,'Team Defense Passing':"/stats/team-stats/defense/passing/{0}/reg/all" 
##'Team Offense Passing':"/stats/team-stats/offense/passing/{0}/reg/all" 
## ,'Team Special Scoring':"/stats/team-stats/special-teams/scoring/{0}/reg/all"
##'Team Defense rushing':"/stats/team-stats/defense/rushing/{0}/reg/all"
##'Team Defense scoring':"/stats/team-stats/defense/scoring/{0}/reg/all"
##'Team Defense downs':"/stats/team-stats/defense/downs/{0}/reg/all"
##'Team Defense receiving':"/stats/team-stats/defense/receiving/{0}/reg/all"
##'Team Defense tackles':"/stats/team-stats/defense/tackles/{0}/reg/all"
}

##create the session
s = requests.Session()

#########################################################################################################################----------------------PATH TO FILES
##Change this to match the location on your home PC. Make sure to leave the {0} in there because thats where the file name will replace with the .Format()
Location_for_file_export = r'C:\Users\Brian\NFL Stats\{0}'

# To put csv files in the directory containing the python.
##Location_for_file_export = r'{0}'

for variation in base_url_variations.keys():
#this is the first layer of the loop that will hold the variations for us
#at this layer we will create a blank list so that we can hold all of the pandas DFs
    print("Working to get " + variation + " data")
    df_holder=[]
#########################################################################################################################----------------------YEAR INDICATION
    ##Change These years to whatever range you want. Right now its 2021-2023
    # for yr in range(1965,2023):
    for yr in range(2018,2024):
    #this is the second layer of the loop that will loop over each year that we ask it to
        try:
            
            print("getting " + variation+ " data for year: " + str(yr))
            URL = base_url_string + base_url_variations[variation].format(str(yr))
            while True:
                print(URL)
                # r= s.get(URL, headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'})
                #soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
                # soup = BeautifulSoup(r.text, "html.parser")

                core_data_from_website = pd.read_html(URL)[0]

                #         for body in soup.find_all("tbody"):
                #                     # body.unwrap()
                #                     print("LOOP")
                #                     print(pd.read_html(body)) # NOT GETTING ANYTHING
                #                     core_data_from_website=pd.concat(pd.read_html(str(body), flavor="bs4"))
                ##Add in our year column
                core_data_from_website['YEAR'] = str(yr)
                ##Add in our variation column
                core_data_from_website['Stat_Type'] = variation
                ##Add this df to the list of Dfs. We will combine them later.
                if 'player-stats' in URL:
                    player_names = core_data_from_website['Player']
                    player_urls = ["https://www.nfl.com/players/" + '-'.join(str(name).split()) + "/" for name in player_names]
                    core_data_from_website['PlayerURL'] = player_urls
                    #https://www.nfl.com/players/Troy-Aikman/

                df_holder.append(core_data_from_website)

                r = s.get(URL)
                soup = BeautifulSoup(r.text, "html.parser")
                anchors = soup.find_all("a", attrs={'title': 'Next Page'})
                if len(anchors) == 1:
                    URL = anchors[0].get('href')
                    URL = "https://www.nfl.com" + URL
                    r = s.get(URL)
                    soup = BeautifulSoup(r.text, "html.parser")
                else:
                    break

                   
                #sleep(1) ##You can add a sleep timer to wait a period of time between requests, that way you dont get banned from the site.
                  
        except Exception as e:
                  print(e)
            ##finally:
                    ##print("all ok")
              ##Put all of the pandas DFs into 1 dataframe    
    result = pd.concat(df_holder,axis=0)
          ##This saves the pandas df to the
    result.to_csv(Location_for_file_export.format(variation + '.csv'))
    # result.to_csv(r'C:\Coding\Gigs\BrianJ-Python\data.csv')
      


print("end: " + str(datetime.datetime.now().strftime("%I:%M %p")))
