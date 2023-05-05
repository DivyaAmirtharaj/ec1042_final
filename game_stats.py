import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_urls(start, end):
    urls = []
    for i in range(start, end+1):
        url = f'https://www.basketball-reference.com/players/m/mccanra01/gamelog/{i}'
        urls.append(url)
    return urls

def get_season_games(urls, player):
    total_df = pd.DataFrame()
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'id': 'pgl_basic'}) # find the table with id 'pgl_basic'

        headers = []
        for th in table.find('thead').findAll('th'):
            if th.text.strip() == "Rk":
                pass
            else:
                headers.append(th.text.strip()) # get the table headers
        headers = [header.lower() for header in headers] # convert headers to lowercase for consistency

        data = []
        for row in table.find('tbody').findAll('tr'): # iterate through each row in the table
            player_data = []
            for td in row.findAll('td'): # iterate through each cell in the row
                player_data.append(td.text.strip()) # get the data for the player
            data.append(player_data)

        player_stats = []
        for row in data:
            game_stats = {}
            for i, stat in enumerate(row):
                game_stats[headers[i]] = stat
            player_stats.append(game_stats)

        #print(player_stats)
        df = pd.DataFrame(player_stats)
        if total_df.empty:
            total_df = df
        else:
            total_df = pd.concat([total_df, df])

    total_df.to_csv(f"playoff_game_stats/{player}.csv", index=True)

def get_playoff_games(player, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'pgl_basic_playoffs'}) # find the table with id 'pgl_basic_playoffs'

    headers = []
    for th in table.find('thead').findAll('th'):
        if th.text.strip() == "Rk":
                pass
        else:
            headers.append(th.text.strip()) # get the table headers
    data = []
    for row in table.find('tbody').findAll('tr'): # iterate through each row in the table
        player_data = []
        for td in row.findAll('td'): # iterate through each cell in the row
            player_data.append(td.text.strip()) # get the data for the player
        data.append(player_data)

    df = pd.DataFrame(data, columns=headers) # create a pandas dataframe with the scraped data
    print(df) # print the first few rows of the dataframe
    df.to_csv(f"playoff_game_stats/{player}.csv", index=True)

def run_reg(player, start, end):
    urls = get_urls(start, end)
    get_season_games(urls, player)

def reg_season():
    run_reg("Rashad McCants", 2006, 2009)
    run_reg("Lamar Odom", 2000, 2013)
    run_reg("Kris Humphries", 2005, 2017)
    run_reg("James Harden", 2010, 2023)
    run_reg("Tristan Thompson", 2012, 2023)
    run_reg("Blake Griffin", 2011, 2023)
    run_reg("Ben Simmons", 2018, 2023)
    run_reg("Devin Booker", 2015, 2023) 

get_playoff_games("Devin Booker", 'https://www.basketball-reference.com/players/b/bookede01/gamelog-playoffs/')