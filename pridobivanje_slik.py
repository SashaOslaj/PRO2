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
        'rio-2016': 'BRA-2016',
        'london-2012': 'GBR-2012',
        'beijing-2008': 'CHN-2008',
        'athens-2004': 'GRE-2004',
        'sydney-2000': 'AUS-2000',
        'atlanta-1996': 'USA-1996',
        'barcelona-1992': 'ESP-1992',
        'seoul-1988': 'KOR-1988',
        'los-angeles-1984': 'USA-1984',
        'moscow-1980': 'RUS-1980',
        'montreal-1976': 'CAN-1976',
        'munich-1972': 'GER-1972',
        'mexico-1968': 'MEX-1968',
        'tokyo-1964': 'JPN-1964',
        'rome-1960': 'ITA-1960',
        'melbourne-stockholm-1956': 'AUS-1956',
        'helsinki-1952': 'FIN-1952',
        'london-1948': 'GBR-1948',
        'berlin-1936': 'GER-1936',
        'los-angeles-1932': 'USA-1932',
        'amsterdam-1928': 'NED-1928',
        'paris-1924': 'FRA-1924',
        'antwerp-1920': 'BEL-1920',
        'stockholm-1912':'SWE-1912',
        'london-1908': 'GBR-1908',
        'st-louis-1904': 'USA-1904',
        'paris-1900': 'FRA-1900',
        'athens-1896': 'GRE-1896'
    }
    sez_ikon = []
    with open('oi\oi_ikone.html', 'r', encoding='utf-8') as dat:
        vsebina = dat.read()
        for ikona in re.finditer(
            r'<li>.+?'
            r'<a href="/(?P<oi>.*?)">'
            r'.*?<picture>'
            r'.+?<img data-src="(?P<urlslike>.+?)".+? alt="" class="lazyload">'
            r'.*?</picture>'
            r'.+?</li>'
            , vsebina, flags=re.DOTALL):
            oi = ikona.group('oi')
            urlslike = ikona.group('urlslike')
            if oi in {'olympic-games', 'paris-2024', 'tokyo-2020'}:
                continue
            oi = slovar_oi[oi]
            sez_ikon.append([oi, urlslike])
            pot_slike =  os.path.join('oi', "{}.png".format(oi))
            urllib.request.urlretrieve(urlslike, pot_slike)


      
        
                   
#slovar_drzav = pridobi_drzave('seznam_drzav.csv')
#print(slovar_drzav)
#shrani_slike()
#prenesi_html_drzave()
#prenesi_url_ikon()
#shrani_ikone_oi()



       
