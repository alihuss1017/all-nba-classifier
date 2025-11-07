import requests
import csv
import os
import time
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, years: list[int]):
        self.years = years
    
    

    def stat_scraper(self, year: int):

        '''
        #----------------------------------------------------------

        SCRAPES REGULAR SEASON PER GAME STATS OF THE NBA SEASON 
        FOR A GIVEN YEAR. STORES IT IN A CSV FILE IN A Data/{year}
        PATH. 

        #----------------------------------------------------------
        '''

        data_categories = ['per_game', 'advanced']

        for category in data_categories:

            # GET request for a given year, utf-8 encoding for names with special characters. 
            response = requests.get(
                f'https://www.basketball-reference.com/leagues/NBA_20{year}_{category}.html'
                )
            response.encoding = 'utf-8'

            # soupify and find all table rows in the page
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')

            # list that will contain all row entry data.
            data = []

            for idx, row in enumerate(rows):
                entry = []

                # if it's the first row, use th attribute for column names, 
                if idx == 0:
                    cols = row.find_all('th', attrs = {'data-stat': True})

                # else, use td attribute for column values.
                else:
                    cols = row.find_all('td', attrs = {'data-stat': True})

                # appends all column text values excluding "Rk" column name
                for col in cols:
                    if col.text == "Rk":
                        continue
                    entry.append(col.text)

                # appends each entry row to the data list.
                data.append(entry)

            # writes data to CSV file, first row contains features, rest contains data.
            with open(f'data/20{year}/{category}.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data[0])

                # excludes last row which has league averages
                csv_writer.writerows(data[1: len(data) - 1])



    def target_scraper(self, year: int):

        '''
        #----------------------------------------------------------

        SCRAPES THE NAMES OF PLAYERS WHO'VE MADE AN ALL-NBA TEAM 
        FOR A GIVEN YEAR. STORES IT IN A CSV FILE IN A Data/{year}
        PATH. 

        #----------------------------------------------------------
        '''   


        # GET response for a given year, utf-8 encoding for names with special characters.
        response = requests.get(
            f'https://www.basketball-reference.com/awards/awards_20{year}.html'
        )
        response.encoding = 'utf-8'

        # soupify response, extract 1st Team, 2nd Team, and 3rd Team content. 
        soup = BeautifulSoup(response.text, 'html.parser')
        start_tag = soup.find('tr', id = 'start_1T_all_nba')
        end_tag = soup.find('tr', id = 'start_ORV_all_nba')

        x = start_tag
        data = []

        # while loop to append all tags between start tag and end tag.
        # if either x is empty or x is at the end, it terminates.
        while x and x != end_tag:
            entry = []

            try:
                y = x.find('td', attrs = {'data-stat': 'player'})
                # excludes all empty spaces and newlines
                if y.text not in ['\n', '']:
                    entry.append(y.text)
                    data.append(entry)

            except:
                pass
            
            # moves onto next tag. 
            x = x.next_sibling

        # writes all data into a CSV file.
        with open(f'data/20{year}/targets.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Player'])
            csv_writer.writerows(data)
    


    def scraper(self):


        '''
        #----------------------------------------------------------

        CALLS stat_scraper(), target_scraper(). PERFORMS A CHECK 
        TO SEE IF 2026 IS AN INCLUDED YEAR TO AVOID PERFORMING 
        target_scraper(). 

        #----------------------------------------------------------
        '''   


        for idx, year in enumerate(self.years):
            # create path if it doesn't exist
            os.makedirs(f'data/20{year}', exist_ok = True)

            self.stat_scraper(year)
            if year != 26:
                self.target_scraper(year)

            print(f"Scraped 20{year - 1}-20{year} data.")

            # to avoid hitting rate limits
            if (idx + 1) != len(self.years):
                time.sleep(10)


  
    def __call__(self):
        self.scraper()



# Scraper(list(range(21,26)))()
