from bs4 import BeautifulSoup
import requests
import string
import os
initial_site = "http://www.ufcstats.com/statistics/events/completed?page=all"

def ScrapeFightCards():
    response = requests.get(initial_site)
    content = BeautifulSoup(response.content, 'html.parser')
    fight_doc = open('fights.csv', 'w')
    header = ""
    for i in range(0, len(fight_stats_names)):
        header += fight_stats_names[i]
        if i < len(fight_stats_names)-1:
            header += ','
    fight_doc.write(header + '\n')
    table_body = content.find('tbody')
    table_rows = table_body.find_all('tr')
    table_rows = table_rows[2:]
    for table_row in table_rows:
        upcoming = table_row.find('img')
        if upcoming is None:
            fight_card_url = table_row.find('a')
            fight_card = fight_card_url.text.lstrip().rstrip()
            date = table_row.find('span', attrs={'class':'b-statistics__date'}).text.lstrip().rstrip().replace(',', '')
            location = table_row.find('td', attrs={'class':
                'b-statistics__table-col b-statistics__table-col_style_big-top-padding'}
                ).text.lstrip().rstrip().replace(',', '')
            fight_card_info = [fight_card_url['href'], fight_card, date, location]
            ScrapeFights(fight_card_info, fight_doc)
            break

def ScrapeFights(fight_card_info, fight_doc):
    response = requests.get(fight_card_info[0])
    content = BeautifulSoup(response.content, 'html.parser')
    table_body = content.find('tbody')
    table_rows = table_body.find_all('tr')
    for table_row in table_rows:
        fighters = table_row.find('td', attrs={'style':'width:100px',
        'class':'b-fight-details__table-col l-page_align_left'})
        winner = fighters.find('p').text.lstrip().rstrip()
        weightclass = table_row.find_all('td', attrs={
            'class':'b-fight-details__table-col l-page_align_left'
        })
        weightclass = weightclass[1].find('p').text.lstrip().rstrip()
        this_fight = list.copy(fight_card_info)
        this_fight.append(winner)
        this_fight.append(weightclass)
        print(this_fight)
        ScrapeStats(table_row.get('data-link'), this_fight, fight_doc)
        break

def ScrapeStats(url, fight_card_info, fight_doc):
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'html.parser')

    #Scrape Fight
    names = content.find_all('h3', attrs={'class':'b-fight-details__person-name'})
    for i in range(0, len(names)):
        names[i] = names[i].text.lstrip().rstrip()
    
    referee = content.find('div', attrs={'class':'b-fight-details__content'})
    referee = referee.find_all('span')
    referee = referee[0].text.lstrip().rstrip()

    #Scrape Rounds    
    red_corner = []
    blue_corner = []    
    tables = content.find_all('table')
    for table in tables:
        bodies = table.find_all('tbody')
        for body in bodies:
            rows = body.find_all('tr')
            for row in rows:
                list1 = []
                list2 = []
                stats = row.find_all('td', attrs={'class':'b-fight-details__table-col'})
                for stat in stats:
                    values = stat.find_all('p')
                    for i in range(0, len(values)):
                        values[i] = values[i].text.lstrip().rstrip()
                        if ' of ' in values[i]:
                            values[i] = values[i].split(' of ')
                    list1.append(values[0])
                    list2.append(values[1])
                red_corner.append(list1)
                blue_corner.append(list2)

    fight_stats_output = f"{fight_card_info[1]},{fight_card_info[2]},{fight_card_info[3]},,{referee},,,{fight_card_info[4]},{fight_card_info[5]},"
    for i in range(0, len(red_corner)/2):
        pass
    fight_doc.write(fight_stats_output)

def order_corner_stats(stat_totals, sig_strikes):
    pass

fight_stats_names = [
    'Fight_Card',
    'Date',
    'Location',
    'Title_Fight',
    'Referee',
    'Bonus',
    'Decision',
    'Winner',
    'Weightclass',
    'R_Fighter',
    'R_Knockdowns',
    'R_Sig_Str_Landed',
    'R_Sig_Str_Thrown',
    'R_Str_Landed',
    'R_Str_Thrown',
    'R_Takedowns_Landed',
    'R_Takedowns_Attempted',
    'R_Sub_Attempted',
    'R_Passes',
    'R_Reversals',
    'R_Sig_Str_Head_Landed',
    'R_Sig_Str_Head_Attempted',
    'R_Sig_Str_Body_Landed',
    'R_Sig_Str_Body_Attempted',
    'R_Sig_Str_Leg_Landed',
    'R_Sig_Str_Leg_Attempted',
    'R_Sig_Str_Distance_Landed',
    'R_Sig_Str_Distance_Attempted',
    'R_Sig_Str_Clinch_Landed',
    'R_Sig_Str_Clinch_Attempted',
    'R_Sig_Str_Ground_Landed',
    'R_Sig_Str_Ground_Attempted',
    'R_Ro1_Knockdowns',
    'R_Ro1_Sig_Str_Landed',
    'R_Ro1_Sig_Str_Thrown',
    'R_Ro1_Str_Landed',
    'R_Ro1_Str_Thrown',
    'R_Ro1_Takedowns_Landed',
    'R_Ro1_Takedowns_Attempted',
    'R_Ro1_Sub_Attempted',
    'R_Ro1_Passes',
    'R_Ro1_Reversals',
    'R_Ro1_Sig_Str_Head_Landed',
    'R_Ro1_Sig_Str_Head_Attempted',
    'R_Ro1_Sig_Str_Body_Landed',
    'R_Ro1_Sig_Str_Body_Attempted',
    'R_Ro1_Sig_Str_Leg_Landed',
    'R_Ro1_Sig_Str_Leg_Attempted',
    'R_Ro1_Sig_Str_Distance_Landed',
    'R_Ro1_Sig_Str_Distance_Attempted',
    'R_Ro1_Sig_Str_Clinch_Landed',
    'R_Ro1_Sig_Str_Clinch_Attempted',
    'R_Ro1_Sig_Str_Ground_Landed',
    'R_Ro1_Sig_Str_Ground_Attempted',
    'R_Ro2_Knockdowns',
    'R_Ro2_Sig_Str_Landed',
    'R_Ro2_Sig_Str_Thrown',
    'R_Ro2_Str_Landed',
    'R_Ro2_Str_Thrown',
    'R_Ro2_Takedowns_Landed',
    'R_Ro2_Takedowns_Attempted',
    'R_Ro2_Sub_Attempted',
    'R_Ro2_Passes',
    'R_Ro2_Reversals',
    'R_Ro2_Sig_Str_Head_Landed',
    'R_Ro2_Sig_Str_Head_Attempted',
    'R_Ro2_Sig_Str_Body_Landed',
    'R_Ro2_Sig_Str_Body_Attempted',
    'R_Ro2_Sig_Str_Leg_Landed',
    'R_Ro2_Sig_Str_Leg_Attempted',
    'R_Ro2_Sig_Str_Distance_Landed',
    'R_Ro2_Sig_Str_Distance_Attempted',
    'R_Ro2_Sig_Str_Clinch_Landed',
    'R_Ro2_Sig_Str_Clinch_Attempted',
    'R_Ro2_Sig_Str_Ground_Landed',
    'R_Ro2_Sig_Str_Ground_Attempted',
    'R_Ro3_Knockdowns',
    'R_Ro3_Sig_Str_Landed',
    'R_Ro3_Sig_Str_Thrown',
    'R_Ro3_Str_Landed',
    'R_Ro3_Str_Thrown',
    'R_Ro3_Takedowns_Landed',
    'R_Ro3_Takedowns_Attempted',
    'R_Ro3_Sub_Attempted',
    'R_Ro3_Passes',
    'R_Ro3_Reversals',
    'R_Ro3_Sig_Str_Head_Landed',
    'R_Ro3_Sig_Str_Head_Attempted',
    'R_Ro3_Sig_Str_Body_Landed',
    'R_Ro3_Sig_Str_Body_Attempted',
    'R_Ro3_Sig_Str_Leg_Landed',
    'R_Ro3_Sig_Str_Leg_Attempted',
    'R_Ro3_Sig_Str_Distance_Landed',
    'R_Ro3_Sig_Str_Distance_Attempted',
    'R_Ro3_Sig_Str_Clinch_Landed',
    'R_Ro3_Sig_Str_Clinch_Attempted',
    'R_Ro3_Sig_Str_Ground_Landed',
    'R_Ro3_Sig_Str_Ground_Attempted',
    'R_Ro4_Knockdowns',
    'R_Ro4_Sig_Str_Landed',
    'R_Ro4_Sig_Str_Thrown',
    'R_Ro4_Str_Landed',
    'R_Ro4_Str_Thrown',
    'R_Ro4_Takedowns_Landed',
    'R_Ro4_Takedowns_Attempted',
    'R_Ro4_Sub_Attempted',
    'R_Ro4_Passes',
    'R_Ro4_Reversals',
    'R_Ro4_Sig_Str_Head_Landed',
    'R_Ro4_Sig_Str_Head_Attempted',
    'R_Ro4_Sig_Str_Body_Landed',
    'R_Ro4_Sig_Str_Body_Attempted',
    'R_Ro4_Sig_Str_Leg_Landed',
    'R_Ro4_Sig_Str_Leg_Attempted',
    'R_Ro4_Sig_Str_Distance_Landed',
    'R_Ro4_Sig_Str_Distance_Attempted',
    'R_Ro4_Sig_Str_Clinch_Landed',
    'R_Ro4_Sig_Str_Clinch_Attempted',
    'R_Ro4_Sig_Str_Ground_Landed',
    'R_Ro4_Sig_Str_Ground_Attempted',
    'R_Ro5_Knockdowns',
    'R_Ro5_Sig_Str_Landed',
    'R_Ro5_Sig_Str_Thrown',
    'R_Ro5_Str_Landed',
    'R_Ro5_Str_Thrown',
    'R_Ro5_Takedowns_Landed',
    'R_Ro5_Takedowns_Attempted',
    'R_Ro5_Sub_Attempted',
    'R_Ro5_Passes',
    'R_Ro5_Reversals',
    'R_Ro5_Sig_Str_Head_Landed',
    'R_Ro5_Sig_Str_Head_Attempted',
    'R_Ro5_Sig_Str_Body_Landed',
    'R_Ro5_Sig_Str_Body_Attempted',
    'R_Ro5_Sig_Str_Leg_Landed',
    'R_Ro5_Sig_Str_Leg_Attempted',
    'R_Ro5_Sig_Str_Distance_Landed',
    'R_Ro5_Sig_Str_Distance_Attempted',
    'R_Ro5_Sig_Str_Clinch_Landed',
    'R_Ro5_Sig_Str_Clinch_Attempted',
    'R_Ro5_Sig_Str_Ground_Landed',
    'R_Ro5_Sig_Str_Ground_Attempted',
    'B_Fighter',
    'B_Knockdowns',
    'B_Sig_Str_Landed',
    'B_Sig_Str_Thrown',
    'B_Str_Landed',
    'B_Str_Thrown',
    'B_Takedowns_Landed',
    'B_Takedowns_Attempted',
    'B_Sub_Attempted',
    'B_Passes',
    'B_Reversals',
    'B_Sig_Str_Head_Landed',
    'B_Sig_Str_Head_Attempted',
    'B_Sig_Str_Body_Landed',
    'B_Sig_Str_Body_Attempted',
    'B_Sig_Str_Leg_Landed',
    'B_Sig_Str_Leg_Attempted',
    'B_Sig_Str_Distance_Landed',
    'B_Sig_Str_Distance_Attempted',
    'B_Sig_Str_Clinch_Landed',
    'B_Sig_Str_Clinch_Attempted',
    'B_Sig_Str_Ground_Landed',
    'B_Sig_Str_Ground_Attempted',
    'B_Ro1_Knockdowns',
    'B_Ro1_Sig_Str_Landed',
    'B_Ro1_Sig_Str_Thrown',
    'B_Ro1_Str_Landed',
    'B_Ro1_Str_Thrown',
    'B_Ro1_Takedowns_Landed',
    'B_Ro1_Takedowns_Attempted',
    'B_Ro1_Sub_Attempted',
    'B_Ro1_Passes',
    'B_Ro1_Reversals',
    'B_Ro1_Sig_Str_Head_Landed',
    'B_Ro1_Sig_Str_Head_Attempted',
    'B_Ro1_Sig_Str_Body_Landed',
    'B_Ro1_Sig_Str_Body_Attempted',
    'B_Ro1_Sig_Str_Leg_Landed',
    'B_Ro1_Sig_Str_Leg_Attempted',
    'B_Ro1_Sig_Str_Distance_Landed',
    'B_Ro1_Sig_Str_Distance_Attempted',
    'B_Ro1_Sig_Str_Clinch_Landed',
    'B_Ro1_Sig_Str_Clinch_Attempted',
    'B_Ro1_Sig_Str_Ground_Landed',
    'B_Ro1_Sig_Str_Ground_Attempted',
    'B_Ro2_Knockdowns',
    'B_Ro2_Sig_Str_Landed',
    'B_Ro2_Sig_Str_Thrown',
    'B_Ro2_Str_Landed',
    'B_Ro2_Str_Thrown',
    'B_Ro2_Takedowns_Landed',
    'B_Ro2_Takedowns_Attempted',
    'B_Ro2_Sub_Attempted',
    'B_Ro2_Passes',
    'B_Ro2_Reversals',
    'B_Ro2_Sig_Str_Head_Landed',
    'B_Ro2_Sig_Str_Head_Attempted',
    'B_Ro2_Sig_Str_Body_Landed',
    'B_Ro2_Sig_Str_Body_Attempted',
    'B_Ro2_Sig_Str_Leg_Landed',
    'B_Ro2_Sig_Str_Leg_Attempted',
    'B_Ro2_Sig_Str_Distance_Landed',
    'B_Ro2_Sig_Str_Distance_Attempted',
    'B_Ro2_Sig_Str_Clinch_Landed',
    'B_Ro2_Sig_Str_Clinch_Attempted',
    'B_Ro2_Sig_Str_Ground_Landed',
    'B_Ro2_Sig_Str_Ground_Attempted',
    'B_Ro3_Knockdowns',
    'B_Ro3_Sig_Str_Landed',
    'B_Ro3_Sig_Str_Thrown',
    'B_Ro3_Str_Landed',
    'B_Ro3_Str_Thrown',
    'B_Ro3_Takedowns_Landed',
    'B_Ro3_Takedowns_Attempted',
    'B_Ro3_Sub_Attempted',
    'B_Ro3_Passes',
    'B_Ro3_Reversals',
    'B_Ro3_Sig_Str_Head_Landed',
    'B_Ro3_Sig_Str_Head_Attempted',
    'B_Ro3_Sig_Str_Body_Landed',
    'B_Ro3_Sig_Str_Body_Attempted',
    'B_Ro3_Sig_Str_Leg_Landed',
    'B_Ro3_Sig_Str_Leg_Attempted',
    'B_Ro3_Sig_Str_Distance_Landed',
    'B_Ro3_Sig_Str_Distance_Attempted',
    'B_Ro3_Sig_Str_Clinch_Landed',
    'B_Ro3_Sig_Str_Clinch_Attempted',
    'B_Ro3_Sig_Str_Ground_Landed',
    'B_Ro3_Sig_Str_Ground_Attempted',
    'B_Ro4_Knockdowns',
    'B_Ro4_Sig_Str_Landed',
    'B_Ro4_Sig_Str_Thrown',
    'B_Ro4_Str_Landed',
    'B_Ro4_Str_Thrown',
    'B_Ro4_Takedowns_Landed',
    'B_Ro4_Takedowns_Attempted',
    'B_Ro4_Sub_Attempted',
    'B_Ro4_Passes',
    'B_Ro4_Reversals',
    'B_Ro4_Sig_Str_Head_Landed',
    'B_Ro4_Sig_Str_Head_Attempted',
    'B_Ro4_Sig_Str_Body_Landed',
    'B_Ro4_Sig_Str_Body_Attempted',
    'B_Ro4_Sig_Str_Leg_Landed',
    'B_Ro4_Sig_Str_Leg_Attempted',
    'B_Ro4_Sig_Str_Distance_Landed',
    'B_Ro4_Sig_Str_Distance_Attempted',
    'B_Ro4_Sig_Str_Clinch_Landed',
    'B_Ro4_Sig_Str_Clinch_Attempted',
    'B_Ro4_Sig_Str_Ground_Landed',
    'B_Ro4_Sig_Str_Ground_Attempted',
    'B_Ro5_Knockdowns',
    'B_Ro5_Sig_Str_Landed',
    'B_Ro5_Sig_Str_Thrown',
    'B_Ro5_Str_Landed',
    'B_Ro5_Str_Thrown',
    'B_Ro5_Takedowns_Landed',
    'B_Ro5_Takedowns_Attempted',
    'B_Ro5_Sub_Attempted',
    'B_Ro5_Passes',
    'B_Ro5_Reversals',
    'B_Ro5_Sig_Str_Head_Landed',
    'B_Ro5_Sig_Str_Head_Attempted',
    'B_Ro5_Sig_Str_Body_Landed',
    'B_Ro5_Sig_Str_Body_Attempted',
    'B_Ro5_Sig_Str_Leg_Landed',
    'B_Ro5_Sig_Str_Leg_Attempted',
    'B_Ro5_Sig_Str_Distance_Landed',
    'B_Ro5_Sig_Str_Distance_Attempted',
    'B_Ro5_Sig_Str_Clinch_Landed',
    'B_Ro5_Sig_Str_Clinch_Attempted',
    'B_Ro5_Sig_Str_Ground_Landed',
    'B_Ro5_Sig_Str_Ground_Attempted',
]

if __name__ == '__main__':
    ScrapeFightCards()