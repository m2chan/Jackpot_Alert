# Retrieves lotto data for Lotto Max and Lotto 649

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import time
from datetime import datetime, date

def retrieve_data():
    '''
    Pulls the lotto data from given link
    '''

    # Set up SSL certs options
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    lottery_url = 'https://www.wclc.com/winning-numbers/lotto-max-extra.htm'
    
    html = urllib.request.urlopen(lottery_url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Search scraped HTML for fields
    raw_date = soup.find_all('div', attrs={'class':'nextJackpotDateDate'})
    raw_jackpot = soup.find_all('div', attrs={'class':'nextJackpotPrizeAmount'})
    raw_secondary_jackpot = soup.find_all('span', attrs={'class':'nextJackpotSecondaryPrize'})

    # Initialize dict to store lottery information
    lottery_data = {'lotto_649':{}, 'lotto_max':{}}

    for index, lotto in enumerate(lottery_data.keys()):

        # Clean date input - Convert date text strings to usable format
        lotto_raw_date = raw_date[index].text
        lotto_raw_date = lotto_raw_date.split(',')
        lotto_day_of_week = lotto_raw_date[0].strip()
        lotto_month = lotto_raw_date[1].split()[0]
        lotto_month = datetime.strptime(lotto_month,'%B').month
        lotto_day = int(lotto_raw_date[1].split()[1])
        lotto_year = int(lotto_raw_date[2])

        # Clean jackpot input - Sometimes there are special characters in the secondary jackpot scrame
        lotto_raw_secondary_jackpot = raw_secondary_jackpot[index].text
        lotto_clean_secondary_jackpot = ''.join(e for e in lotto_raw_secondary_jackpot if e.isalnum()) 
        
        # Fill in lottery_data dictionary for current lottery
        lottery_data[lotto]['day_of_week'] = lotto_day_of_week
        lottery_data[lotto]['date'] = date(lotto_year, lotto_month, lotto_day)
        lottery_data[lotto]['jackpot'] = raw_jackpot[index].text
        lottery_data[lotto]['secondary_jackpot'] = lotto_clean_secondary_jackpot

    return lottery_data

if __name__ == '__main__':
    print(retrieve_data())
    # driver = webdriver.Chrome(ChromeDriverManager().install())


'''
Want to track the lotto name, the grand prize, max millions, draw date
Output of this module is just the lotto data for today that we use to determine if we should be sending a notification to users
Writes this data to a database
'''

