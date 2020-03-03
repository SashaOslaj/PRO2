import orodja
import re
import unicodedata
import os
from pathlib import Path


leta = ["/rio-2016", "/london-2012", "/beijing-2008", "/athens-2004", 
        "/sydney-2000", "/atlanta-1996", "/barcelona-1992", "/seoul-1988",
        "/los-angeles-1984", "/moscow-1980", "/montreal-1976", "/munich-1972",
        "/mexico-1968", "/tokyo-1964", "/rome-1960", "/melbourne-stockholm-1956",
        "/helsinki-1952", "/london-1948", "/berlin-1936", "/los-angeles-1932",
        "/amsterdam-1928", "/paris-1924", "/antwerp-1920", "/stockholm-1912",
        "/london-1908", "/st-louis-1904", "/paris-1900", "/athens-1896"]
sport = "/athletics"
discipline = ["/10000m-men", "/100m-men", "/110m-hurdles-men", "/1500m-men",
              "/200m-men", "/20km-walk-men", "/3000m-steeplechase-men",
              "/400m-hurdles-men", "/400m-men", 
              
              "/4x100m-relay-men", "/4x400m-relay-men", 
              "/5000m-men", "/50km-walk-men", "/800m-men",
              "/decathlon-men", "/discus-throw-men", "/hammer-throw-men",
              "/high-jump-men", "/javelin-throw-men", "/long-jump-men",
              "/marathon-men", "/pole-vault-men", "/shot-put-men", "/triple-jump-men",

              "/10000m-women", "/100m-hurdles-women", "/100m-women", 
              "/1500m-women", "/200m-women", "/20km-race-walk-women",
              "/3000m-steeplechase-women", "/400m-hurdles-women", "/400m-women",
              "/4x100m-relay-women", "/4x400m-relay-women", 
              "/5000m-women",
              "/800m-women", "/discus-throw-women", "/hammer-throw-women",
              "/heptathlon-women", "/high-jump-women", "/javelin-throw-women",
              "/long-jump-women", "/marathon-women", "/pole-vault-women",
              "/shot-put-women", "/triple-jump-women"]
mostva = {"/4x100m-relay-men", "/4x100m-relay-women", "/4x400m-relay-men", "/4x400m-relay-women"}
osnovni_naslov = "https://www.olympic.org"


def podatki_posameznik(datoteka, olimpijske, disciplina):
    '''
    Funkcija sprejme ime datoteke, olimpijske igre in disciplino in naredi seznam
    slovarjev v katerih so rezultati tekmovalca.
    '''

    with open(str(datoteka), encoding='utf-8') as f:
        vsebina = f.read()

        stevec = 0
        for tekmovalec in re.finditer(
            r'<tr>.+?<td class="col1">(?P<mesto>.+?)</td>.+?<td class="col2">'
            r'.+?<a href="/(?P<ime>.+?)">.+?<span class="picture">'
            r'.+?<span.*?>(?P<drzava>\D{3})</span>'
            r'.+?<td class="col3">(?P<rezultat>.+?)</td>.+?</tr>'
        ,vsebina, flags=re.DOTALL):
                
            mesto = tekmovalec.group('mesto')
            x = re.search('\d+', mesto)
            if x:
                mesto = x.group()
            else:
                if re.search('G', mesto):
                    mesto = '1'
                elif re.search('S', mesto):
                    mesto = '2'
                elif re.search('B', mesto):
                    mesto = '3'
                else:
                    mesto = ''
            
            stevec += 1
            if str(stevec) != mesto or mesto == '':
                continue

            ime = tekmovalec.group('ime')
            if ime not in tekmovalci:
                    tekmovalci.add(ime)
            ime = ime.replace("-", " ")
            ime = ime.title()

            drzava = tekmovalec.group('drzava')

            rezultat = tekmovalec.group('rezultat')
            rezultat = rezultat.strip()
            rezultat = rezultat.replace("\n", "")

            igre = olimpijske[1:]
            igre = igre.replace("-", " ")
            igre = igre.capitalize()

            # za vsakega nastopajočega ustvarimo slovar
            nastop = {}
            nastop['igre'] = igre
            nastop['disciplina'] = disciplina
            nastop['mesto'] = mesto
            nastop['ime'] = ime
            nastop['drzava'] = drzava
            nastop['rezultat'] = rezultat
            rezultati.append(nastop)
            sez.add(tekmovalec.group('ime'))


def posameznik_rojstni_dan(datoteka, sportnik):
    '''
    Funkcija sprejme ime datotekein ime tekmovalca in naredi dva seznama.
    V enem so slovarji z imenom tekmovalca in njegovim rojstnim dnem. V drugem
    so slovarji z kratico in polnim imenom drzave.
    '''
    with open(str(datoteka), encoding='utf-8') as f:
        vsebina = f.read()

        for tekmovalec in re.finditer(
            r'<div class="flag-image">'
            r'.+?<span>(?P<kratica>\D\D\D)</span>'
            r'.+?<div class="frame">'
            r'.+?<strong class="title">Country </strong>.+?'
            r'<a (itemprop="url" )?href="/(?P<drzava>.+?)">.+?</a>'
            r'.+?<strong class="title">(Born|Lived)</strong>(?P<datum>.+?)</div>'
        , vsebina, flags=re.DOTALL):

            ime = sportnik
            ime = ime.replace("-", " ")
            ime = ime.title()

            datum = tekmovalec.group('datum')
            datum = datum.replace("\n", "")
            
            meseci = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 
                      'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 
                      'Nov':'11', 'Dec':'12'}
            

            nastopajoci = {}
            nastopajoci['ime'] = ime
            if '01 Jan 0001' == datum[:11]:
                nastopajoci['datum'] = ''
            else:
                datum = datum[:11] # nekateri imajo naveden še datum smrti
                st = meseci[datum[3:6]]
                nastopajoci['datum'] = datum[:2] + '.' + st + '.' + datum[-4:]
            roj_dan_tekmovalcev.append(nastopajoci)

            kratica = tekmovalec.group('kratica')
            drzava = tekmovalec.group('drzava')
            drzava = drzava.replace("-", " ")
            drzava = drzava.title()

            if kratica not in drz:
                drz.add(kratica)
                drzave_s_kratico = {}
                drzave_s_kratico['kratica'] = kratica
                drzave_s_kratico['drzava'] = drzava
                drzave.append(drzave_s_kratico)


def podatki_skupine(datoteka, olimpijske, disciplina):
    '''
    Funkcija sprejme ime datoteke, olimpijske igre in disciplino in naredi seznam
    slovarjev v katerih so podatki skupine.
    '''

    with open(str(datoteka), encoding='utf-8') as f:
        vsebina = f.read()

        stevec = 0
        for tekmovalec in re.finditer(
            r'<tr>.+?<td class="col1">.+?<span class=".+?">(?P<mesto>.+?)</span>.+?<td class="col2">'
            r'.+?<div class="image">.+?<div class="flag45 (?P<drzava>.+?)">.+?<span class="mask"></span>'
            r'.+?<td class="col3">(?P<rezultat>.+?)?</td>.+?</tr>'
        ,vsebina, flags=re.DOTALL):
                
            mesto = tekmovalec.group('mesto')
            if len(mesto) > 5:
                mesto = ""
            elif mesto == 'G':
                mesto = '1.'
            elif mesto == 'S':
                mesto = '2.'
            elif mesto == 'B':
                mesto = '3.'
            mesto = mesto.strip(".")
            mesto = mesto.strip("\n")

            stevec += 1
            if str(stevec) != mesto or mesto == '':
                continue

            drzava = tekmovalec.group('drzava')
            drzava = drzava.replace("-", " ")
            drzava = drzava.upper()

            rezultat = tekmovalec.group('rezultat')
            rezultat = rezultat.strip()
            rezultat = rezultat.replace("\n", "")

            igre = olimpijske[1:]
            igre = igre.replace("-", " ")
            igre = igre.capitalize()

            # za vsakega nastopajočega ustvarimo slovar
            nastop = {}
            nastop['igre'] = igre
            nastop['disciplina'] = disciplina
            nastop['mesto'] = mesto
            nastop['ime'] = ""
            nastop['drzava'] = drzava
            nastop['rezultat'] = rezultat
            rezultati.append(nastop)


def prenesi_html():
    '''
    Funcija za shranitev html datoteke za tekme. Sklicuje se na funkcijo
    shrani iz datoteke orodja.
    '''

    for olimpijske in leta:
        for disciplina in discipline:
            naslov = osnovni_naslov + olimpijske + sport + disciplina
            datoteka = "rezultati_{}_{}.html".format(olimpijske, disciplina)
            orodja.shrani(naslov, datoteka)


def prenesi_html_tekmovalca():
    '''
    Funcija za shranitev html datoteke za vsakega tekmovalca. Sklicuje se
    na funkcijo shrani iz datoteke orodja.
    '''

    for tekmovalec in tekmovalci:
        tekmovalec.replace('\n', '')
        naslov = osnovni_naslov + "/" + tekmovalec
        datoteka = "{}.html".format(tekmovalec)
        pot = os.path.join("tekmovalci", datoteka)
        orodja.shrani(naslov, pot)


def preberi_podatke():
    '''
    Funkcija shrani rezultate tekmovalcev v seznam s pomocjo zgornjih dveh
    funkcij: podatki_posameznik in podatki_skupine.
    '''

    for olimpijske in leta:
        for disc in discipline:

            disciplina = disc
            disciplina = disciplina.replace("-", " ")
            disciplina = disciplina.replace("/", "")

            mapa = Path("rezultati_{}_".format(olimpijske))
            dat = mapa / "{}.html".format(disc[1:])

            if disc in mostva:
                podatki_skupine(dat, olimpijske, disciplina)
            else:
                podatki_posameznik(dat, olimpijske, disciplina)


def preberi_podatke_tekmovalcev():
    '''
    Funkcija shrani rojstne dneve tekmovalcev in kratice in polna imena drzav v
    seznam s pomocjo zgornje funkcije posameznik_rojstni_dan.
    '''

    tekm = set()
    f = open('tekmovalci.txt', 'r')
    for line in f:
        tekm.add(line)
    f.close()

    mnozica_tekmovalcev = [tekmovalec[:-1] for tekmovalec in tekm]

    for tekmovalec in mnozica_tekmovalcev:
        dat = Path("tekmovalci")
        pot = dat / "{}.html".format(tekmovalec)
        posameznik_rojstni_dan(pot, tekmovalec)


def zapisi_tekmovalce(tekmovalci):
    '''
    Funkcija v datoteko tekmovalci.txt zapise vsa imena tekmovalcev iz seznama.
    '''

    f = open("tekmovalci.txt", "w+", encoding='utf-8')
    for tekmovalec in tekmovalci:
        f.write(tekmovalec + "\n")
    f.close()


rezultati = []
tekmovalci = set()
roj_dan_tekmovalcev = []
sez = set()
drz = set()
drzave = []


#prenesi_html()
#prenesi_html_tekmovalca()

#preberi_podatke()

#zapisi_tekmovalce(tekmovalci)
#preberi_podatke_tekmovalcev()

#orodja.zapisi_tabelo(rezultati, ['igre', 'disciplina', 'mesto', 'ime', 'drzava', 'rezultat'], 'rezultati.csv')
#orodja.zapisi_tabelo(roj_dan_tekmovalcev, ['ime', 'datum'], 'roj_dan_tekmovalcev.csv')
#orodja.zapisi_tabelo(drzave, ['kratica', 'drzava'], 'seznam_drzav.csv')
