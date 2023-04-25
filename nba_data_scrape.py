import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_url(start, end):
    urls = []
    for i in range(start, end+1):
        url = f'https://www.basketball-reference.com/leagues/NBA_{i}_per_game.html'
        urls.append(url)
    return urls

def get_basketball_reference(player, urls, start):
    full_history = {}
    for url in urls:
        """Fetching data"""
        r = requests.get(url)
        r_html = r.text
        
        """Extracting raw player_stats data"""
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all(class_="full_table")
        
        """ Extracting List of column names"""
        head=soup.find(class_="thead")
        column_names_raw=[head.text for item in head][0]
        column_names_polished=column_names_raw.replace("\n",",").split(",")[2:-1]

        """Extracting full list of player_data"""
        players=[]
        for i in range(len(table)):
            for td in table[i].find_all("td"):
                if td.text == player:
                    for td in table[i].find_all("td"):
                        players.append(td.text)
            
        """Creating Player Dictionary"""     
        player_dict={}
        Player=[players[0]]
        Pos=[players[1]]
        Age=[players[2]]
        Tm=[players[3]]
        G=[int(players[4])] 
        GS=[int(players[5])] 
        MP=[float(players[6])]
        FG=[float(players[7])]
        FGA=[float(players[8])]
        FG_perc=[players[9]]
        Three_point=[float(players[10])]
        Three_point_A=[float(players[11])]
        Three_point_perc=[players[12]]
        Two_point=[float(players[13])] 
        Two_point_A=[float(players[14])] 
        Two_point_perc=[players[15]]
        eFG_perc=[players[16]]
        FT=[float(players[17])]
        FTA=[float(players[18])]
        FT_perc=[players[19]]
        ORB=[float(players[20])]
        DRB=[float(players[21])]
        TRB=[float(players[22])] 
        AST=[float(players[23])] 
        STL=[float(players[24])]
        BLK=[float(players[25])]
        TOV=[float(players[26])]
        PF=[float(players[27])]
        PPG=[float(players[28])]
        
        player_dict={
                    "Player":Player,
                    "Pos":Pos,
                    "Age":Age,
                    "Tm":Tm,
                    "G":G,
                    "MP":MP,
                    "FG":FG,
                    "FGA":FGA,
                    "FG%":FG_perc,
                    "3P":Three_point,
                    "3PA":Three_point_A,
                    "3P%":Three_point_perc,
                    "2P":Two_point,
                    "2PA":Two_point_A,
                    "2P%":Two_point_perc,
                    "eFG%":eFG_perc,
                    "FT":FT,
                    "FTA":FTA,
                    "FT%":FT_perc,
                    "ORB":ORB,
                    "DRB":DRB,
                    "TRB":TRB,
                    "AST":AST,
                    "STL":STL,
                    "BLK":BLK,
                    "TOV":TOV,
                    "PF":PF,
                    "PPG":PPG}
        #print(player_dict)
        full_history[start] = player_dict
        start += 1
    print(full_history)
    return full_history

def convert_to_panda(full_history):
    df = pd.DataFrame.from_dict(full_history, orient='index')
    df = df.reset_index().rename(columns={'index': 'Year'})
    df = df[['Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PPG']]
    print(df)
    df.to_csv('example.csv', index=False)


#name = input("For which basketball player would you like to get updated stats?: ")
#start_year = input("Starting in what year? ")
#end_year = input("Ending in what year? ")
urls = get_url(int(2019), int(2022))

data = get_basketball_reference("Stephen Curry", urls, 2019)
convert_to_panda(data)