import orodja
import re
import unicodedata
import os
from pathlib import Path
import urllib

osnovni_naslov = "https://en.wikipedia.org"

def pridobi_drzave(datoteka):
    '''
    Funkcija sprejme ime datoteke in naredi slovar s ključem kratice držav in vrednostmi držav.
    '''
    with open(str(datoteka), 'r') as dat:
        drzave = dat.read()
        slovar = {}
        for drzava in drzave.split('\n')[1:]:
            if drzava == '':
                continue
            slovar[drzava.split(',')[0]] = drzava.split(',')[1]
    for kratica, drzava in slovar.items():
        drzava = drzava.replace(' ', '_')
        slovar_napacnih = {
            'German_Democratic_Republic_1955-1990':'East_Germany',
            'Federal_Republic_Of_Germany_1950-1990':'West_Germany',
            'Australasia_1908_1912':'Australasia',
            'People_S_Republic_Of_China': 'China',
            'United_States_Of_America':'United_States',
            'Russian_Federation':'Russia',
            'Burma_Until_1989':'Myanmar',
            'Ussr':'Soviet_Union',
            'The_Former_Yugoslav_Republic_Of_Macedonia':'North_Macedonia',
            'United_Team_Of_Germany_1956_1960_1964':'United_Team_of_Germany_at_the_Olympics',
            'Zaire_19711997':'Zaire',
            'Federated_States_Of_Micronesia':'Federated_States_of_Micronesia',
            'Islamic_Republic_Of_Iran':'Iran',
            'Democratic_People_S_Republic_Of_Korea':'North_Korea',
            'United_Republic_Of_Tanzania':'Tanzania',
            'Sao_Tome_And_Principe':'São_Tomé_and_Príncipe',
            'Cote_D_Ivoire':'Ivory_Coast',
            'Serbia_1912':'Kingdom_of_Serbia',
            'Lao_People_S_Democratic_Republic':'Laos',
            'St_Vincent_And_The_Grenadines':'Saint_Vincent_and_the_Grenadines',
            'Syrian Arab Republic':'Syria',
            'Hong_Kong_China':'Hong_Kong',
            'Rhodesia_Until_1968':'Rhodesia',
            'Antigua_And_Barbuda':'Antigua_and_Barbuda',
            'Saint_Kitts_And_Nevis':'Saint_Kitts_and_Nevis',
            'Bosnia_And_Herzegovina':'Bosnia_and_Herzegovina',
            'Serbia_And_Montenegro':'Serbia_and_Montenegro',
            'Trinidad_And_Tobago':'Trinidad_and_Tobago',
            'Antigua_And_Barbuda':'Antigua_and_Barbuda',
            'Republic_Of_Korea':'Republic_of_Korea',
            'Republic_Of_Moldova':'Republic_of_Moldova',
            'Samoa_Until_1996_Western_Samoa':'Samoa',
            'Democratic_Republic_Of_The_Congo':'Democratic_Republic_of_the_Congo',
            'Democratic_Republic_Of_Timor_Leste':'Democratic_Republic_of_Timor_Leste'
            }
        if drzava in slovar_napacnih:
            slovar[kratica] = slovar_napacnih[drzava]
        else:
            slovar[kratica] = drzava
    return slovar


def prenesi_html_drzave():
    '''
    Funkcija za shranitev html datoteke iz wikipedije za slike zastav.
    '''
    
    for _, drzava in slovar_drzav.items():       
        if drzava in {'Unified_Team_Ex_Ussr_In_1992','_Independent_Olympic_Athletes','Bohemia_Tch_Since_1920','British_West_Indies_Bar_Jam', 'Independant Olympic Participant', 'Refugee Olympic Team', 'International Olympic Committee', 'Independent Olympic Athletes'}:
            continue                
        naslov = osnovni_naslov + "/wiki/" + drzava
        datoteka = "{}.html".format(drzava)
        pot = os.path.join("drzave", datoteka)
        orodja.shrani(naslov, pot)

seznam = {}
koordinate = []

def dobi_tabelo_slike_in_koordinate(datoteka):
    '''
    Funkcija sprejme datoteko in iz nje izbere podatke url slike, geografsko sirino in geografsko visino.
    '''
    sez = {}
    with open(str(datoteka), 'r', encoding='utf-8') as dat:
        vsebina = dat.read()
        for tabela in re.finditer(
            r'<table class="infobox geography vcard" style="width:22em;font-size:88%;"><tbody>'
            r'.+?'
            r'<img alt=".*?" src="(?P<slika>.+?)"'
            r'(.+?<span class="latitude">(?P<geo_visina>.+?)</span>)?'
            r'(.+?<span class="longitude">(?P<geo_sirina>.+?)</span>)?'
            r'.+?</tbody></table>'
            ,vsebina, flags=re.DOTALL):
            drzava = str(datoteka)[7:-5]
            slika = tabela.group('slika')
            geo_visina = tabela.group('geo_visina')
            geo_sirina = tabela.group('geo_sirina')
            for kratica, dolgo in slovar_drzav.items():
                if not isinstance(drzava, str):
                    continue
                elif drzava in {'Unified_Team_Ex_Ussr_In_1992','_Independent_Olympic_Athletes','Bohemia_Tch_Since_1920','British_West_Indies_Bar_Jam', 'Independant Olympic Participant', 'Refugee Olympic Team', 'International Olympic Committee', 'Independent Olympic Athletes'}:
                    continue
                elif drzava == dolgo:
                    seznam[kratica] = [slika, geo_visina, geo_sirina]
                    sez['kratica_drzave'] = kratica
                    sez['geo_visina'] = geo_visina
                    sez['geo_sirina'] = geo_sirina
                    koordinate.append(sez)
    return seznam

def shrani_slike():
    '''
    Funkcija shrani slike in naredi csv datoteko s podatki o geografski sirin in visini.
    '''
    for krat, dat in slovar_drzav.items():
        if dat in {'Unified_Team_Ex_Ussr_In_1992','_Independent_Olympic_Athletes','Bohemia_Tch_Since_1920','British_West_Indies_Bar_Jam', 'Independant Olympic Participant', 'Refugee Olympic Team', 'International Olympic Committee', 'Independent Olympic Athletes'}:
            continue
        datoteka = "{}.html".format(dat)
        pot = os.path.join("drzave", datoteka)
        pot_slike = os.path.join("slike", "{}.png".format(krat))
        podatki = dobi_tabelo_slike_in_koordinate(pot)
        pod = podatki.get(krat)
        if pod:
            naslov = pod[0]
            slika = 'https:{}.png'.format(naslov[:-8])
            urllib.request.urlretrieve(slika, pot_slike)
            orodja.zapisi_tabelo(koordinate, ['kratica_drzave', 'geo_visina', 'geo_sirina'], 'koordinate.csv')

def prenesi_url_ikon():
    pot = os.path.join('oi', 'oi_ikone.html')
    orodja.shrani('https://www.olympic.org/summer-games', pot)

def shrani_ikone_oi():
    '''
    Funkcija shrani slike ikon olimpijskih iger.
    '''
    slovar_oi = {
        'rio-2016': 'BRA',
        'london-2012': 'GBR',
        'beijing-2008': 'CHN',
        'athens-2004': 'GRE',
        'sydney-2000': 'AUS',
        'atlanta-1996': 'USA',
        'barcelona-1992': 'ESP',
        'seoul-1988': 'KOR',
        'los-angeles-1984': 'USA',
        'moscow-1980': 'RUS',
        'montreal-1976': 'CAN',
        'munich-1972': 'GER',
        'mexico-1968': 'MEX',
        'tokyo-1964': 'JPN',
        'rome-1960': 'ITA',
        'melbourne-stockholm-1956': 'AUS',
        'helsinki-1952': 'FIN',
        'london-1948': 'GBR',
        'berlin-1936': 'GER',
        'los-angeles-1932': 'USA',
        'amsterdam-1928': 'NED',
        'paris-1924': 'FRA',
        'antwerp-1920': 'BEL',
        'stockholm-1912':'SWE',
        'london-1908': 'GBR',
        'st-louis-1904': 'USA',
        'paris-1900': 'FRA',
        'athens-1896': 'GRE'
    }
    sez_ikon = []




      
        
                   
#slovar_drzav = pridobi_drzave('seznam_drzav.csv')
#print(slovar_drzav)
#shrani_slike()
#prenesi_html_drzave()




       
