from bs4 import BeautifulSoup
import requests
import string
import os
initial_site = "http://www.ufcstats.com/statistics/events/completed?page=all"

def ScrapeFighters(header_string):
    fighter_doc = open('fighters.csv', 'w')
    fighter_doc.write(header_string)
    ufc_fighters_page = 'http://ufcstats.com/statistics/fighters?char=!&page=all'
    for char in string.ascii_lowercase:
        url = ufc_fighters_page.replace('!', char)
        response = requests.get(url)
        content = BeautifulSoup(response.content, 'html.parser')
        table_rows = content.find_all('tr')
        for table_row in table_rows:
            link = table_row.find('a')
            if link is not None:
                details_response = requests.get(link['href'])
                details_content = BeautifulSoup(details_response.content, 'html.parser')
                fighter_stats = []
                name = details_content.find('span', attrs={'class':'b-content__title-highlight'})
                fighter_stats.append(name.text.lstrip().rstrip())
                stats = details_content.find('ul')
                info = stats.find_all('li', attrs={'class':'b-list__box-list-item_type_block'})
                for stat in info:
                    i = stat.find('i')
                    i.decompose()
                    fighter_stats.append(stat.text.lstrip().rstrip())        
                nickname = details_content.find('p', attrs={'class':'b-content__Nickname'})
                if nickname is not None:
                    fighter_stats.append(nickname.text.lstrip().rstrip())
                else:
                    fighter_stats.append('')
                output_string = ''
                for i in range(0, len(fighter_stats)):
                    fighter_stats[i] = fighter_stats[i].replace(',', ' ')
                    output_string += fighter_stats[i] + ','
                output_string += '\n'
                print(fighter_stats)
                fighter_doc.write(output_string)
                
if __name__ == "__main__":
    header_string = 'Name,Height,Weight,Reach,Stance,Birthday,Nickname\n'
    ScrapeFighters(header_string)