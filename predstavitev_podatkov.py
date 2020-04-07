import random

from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap


########################################################################################################################
########################################################################################################################

class Tekmovalec:

    '''Razred Tekmovalcev predstavi tekmovalca in njegove rezultate'''

    def __init__(self, ime, nastopi, rojen=""):
        self.ime = ime
        self.rojen = rojen
        self.stevilo_nastopov = len(set([i[0] for i in nastopi]))
        self.drzava = nastopi[0][3]
        self.discipline = set([i[1] for i in nastopi])
        self.nastopi = nastopi
        self.spol = nastopi[0][1].split()[-1]

    def __str__(self):
        nastopi = ''
        for nastop in self.nastopi:
            if self.spol == 'men':
                nastopi += 'Na {0} olimpijskih igrah v {1} disciplini je bil na {2} mestu z rezultatom {3}, '.format(
                nastop[0], nastop[1], nastop[2], nastop[4]
                )
                rojen_rojena = 'rojen  '
            if self.spol == 'women':
                nastopi += 'Na {0} olimpijskih igrah v {1} disciplini je bila na {2} mestu z rezultatom {3}, '.format(
                nastop[0], nastop[1], nastop[2], nastop[4]
                )
                rojen_rojena = 'rojena '
        return " ime     | {0} \n {4} | {1} v {3} \n nastopi | {2} \n".format(
            self.ime, self.rojen, nastopi, self.drzava, rojen_rojena
        )

    def __repr__(self):
        return 'Tekmovalec({0},{1},{2})'.format(self.ime, self.nastopi, self.rojen)

    def natancna_predstavitev_tekmovalca(self):
        '''
            Funkcija vrne seznam naborov z imenom, rojstvom,
            drzavo, rezultatom in starostjo.
        '''
        seznam=[]
        for nastop in self.nastopi:
            if self.rojen == '':
                seznam.append((self.ime, self.rojen, self.drzava, nastop[0], nastop[1], nastop[2], nastop[4].replace('"',''), 'Ni podatka'))
                continue
            #print(nastop[0][-4:],self.rojen[-4:])
            starost = int(nastop[0][-4:]) - int(self.rojen[-4:])
            seznam.append((self.ime, self.rojen, self.drzava, nastop[0], nastop[1], nastop[2], nastop[4].replace('"',''), str(starost)))
        return seznam
            
    def podatki_po_disciplinah(self):
        '''
            Funkcija vrne slovar, kjer je kljuc disciplina in vrednost seznam
            rezultatov pri tej disciplini.
        '''
        slovar={}
        for nastop in self.nastopi:
            if nastop[1] in slovar:
                slovar[nastop[1]].append(nastop)
            else:
                slovar[nastop[1]] = [nastop]
        return slovar
    
    def iz_katere_drzave(self):
        return self.nastop[0][3]

                    

class Tekmovalci:

    '''Razred Tekmovalci zajame vse tekmovalce in z njimi dela poizvedbe.'''

    def __init__(self, vsi_rezultati):
        drzave=set()
        discipline=set()
        oi=set()
        for tekmovalec in vsi_rezultati:
            for nastop in vsi_rezultati[tekmovalec][:-1]:
                drzave.add(nastop[3])
                discipline.add(nastop[1])
                oi.add(nastop[0])
        self.vse_drzave=drzave
        self.vse_discipline=discipline
        self.oi=oi
        self.vsi_rezultati=vsi_rezultati
        self.sez_tekmovalcev=list(vsi_rezultati.keys())

    def __str__(self):
        return "Ta razred predstavlja rezultate {} olimpijskih iger v {} disciplinah iz {} džav.".format(
            len(self.oi), len(self.vse_discipline), len(self.vse_drzave)
            )
    def __repr__(self):
        return "Tekmovalci({})".format(self.vsi_tekmovalci)

    def izpisi_tekmovalca(self, ime=None):
        '''
        Funkcija vrne izpis podatkov za tekmovalca, ce ga podamo, sicer si ga nakljucno izbere.
        '''
        if ime == None:
            ime = random.choice(self.sez_tekmovalcev)
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1])
        else:
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1])

    def natancno_izpisi_tekmovalca(self, ime=None):
        '''
        Funkcija vrne seznam naborov z imenom, rojstvom,drzavo, rezultatom in starostjo za tekmovalca, ki ga napisemo oz
        ce ne podamo tekmovalca, ga funkcija nakljucno izbere. 
        '''
        if ime == None:
            ime = random.choice(self.sez_tekmovalcev)
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).natancna_predstavitev_tekmovalca()
        else:
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).natancna_predstavitev_tekmovalca()

    def tekmovalci_po_disciplinah(self):
        '''
        Funkcija vrne slovar, kjer so kljuci discipline in vrednosti so seznami tekmovalcev z njihovimi rezultati.
        '''
        vsi=[(
            ime,
            Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).podatki_po_disciplinah(),
            Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).rojen
            ) for ime in self.sez_tekmovalcev]
        razvrsceno_po_disciplinah={}
        for ime,nastopi,roj in vsi:
            for disc in nastopi:
                if disc in razvrsceno_po_disciplinah:
                    razvrsceno_po_disciplinah[disc].append((ime,nastopi[disc],roj))
                else:
                    razvrsceno_po_disciplinah[disc] = [(ime,nastopi[disc],roj)]
        return razvrsceno_po_disciplinah

    def leta_tekmovalcev(self):
        '''
        Funkcija vrne slovar, kjer so kljuci discipline in vrednosti so seznami tekmovalcev z njihovimi rezultati in starostmi.
        '''
        slovar={}
        for disc in self.vse_discipline:
            slovar[disc]=[]
        for disc in self.tekmovalci_po_disciplinah():
            for ime, nastopi, roj in self.tekmovalci_po_disciplinah()[disc]:
                s = []
                for nastop in nastopi:
                    nastop = list(nastop)
                    if roj != '':
                        starost = str(int(nastop[0][-4:])-int(roj[-4:]))
                    else:
                        starost = ''
                    nastop.append(starost)
                    nastop = tuple(nastop)
                    s.append(nastop)
                slovar[disc].append((ime,s))
        return slovar

    def zmagovalci_po_disciplinah(self):
        '''
        Funkcija vrne slovar, kjer so kljuci discipline in vrednosti so tekmovalci s prvih treh mest z rezultati.
        '''
        zmagovalci={}
        for disc in self.vse_discipline:
            zmagovalci[disc]=[]
        for disc in self.tekmovalci_po_disciplinah():
            for ime,nastopi,roj in self.tekmovalci_po_disciplinah()[disc]:
                sez=[(nastop[0][-4:],nastop[2],nastop[-1]) for nastop in nastopi if nastop[2] == '1' or nastop[2] == '2' or nastop[2] == '3']
                if sez != []:
                    zmagovalci[disc].append((ime,sez,roj))
        return zmagovalci

    def najmaljsi_tekmovalec_po_disciplinah(self):
        '''
        Funkcija vrne slovar, kjer so kljuci discipline in vrednost je najmlajsi tekmovalec pri tej disciplini.
        '''
        najmlajsi=set()
        for disc in self.leta_tekmovalcev():
            trenutni_min = (100, ())
            for ime, nastopi in self.leta_tekmovalcev()[disc]:
                for nastop in nastopi:
                    if nastop[-1] != '' and int(nastop[-1]) < int(trenutni_min[0]):
                        trenutni_min = (nastop[-1], (ime, disc, nastop[0][-4:],nastop[4]))
            najmlajsi.add(trenutni_min)
        return najmlajsi

    def najstarejsi_tekmovalec_po_disciplinah(self):
        '''
        Funkcija vrne slovar, kjer so kljuci discipline in vrednost je najstarejsi tekmovalec pri tej disciplini.
        '''
        najstarejsi = set()
        for disc in self.leta_tekmovalcev():
            trenutni_max = (0, ())
            for ime, nastopi in self.leta_tekmovalcev()[disc]:
                for nastop in nastopi:
                    if nastop[-1] != '' and int(nastop[-1]) > int(trenutni_max[0]):
                        trenutni_max = (nastop[-1], (ime, disc, nastop[0][-4:],nastop[4]))
            najstarejsi.add(trenutni_max)
        return najstarejsi

    def st_raz_drzav_pri_disc(self, disc):
        '''
        Funkcija vrne slovar, kjer so kljuci olimpijske igre in vrednosti so stevilo razlicnih drzav pri teh olimpijskih
        igrah in podatni disciplini.
        '''
        slovar1 = self.tekmovalci_po_disciplinah()
        slovar2={}
        for i in self.oi:
            slovar2[i]=set()
        for tekmovalec in slovar1[disc]:
            for nastop in tekmovalec[1]:
                slovar2[nastop[0]].add(nastop[3])
        for oi in slovar2:
            slovar2[oi]=len(slovar2[oi])
        return slovar2

    def tekmovalec_in_drzava(self):
        '''
        Funkcija vrne slovar, kjer so kljuci drzave in vrenosti so stevilo razlicnih tekmovalcev iz te drzave
        skozi vse olimpijske igre.
        '''
        mnozica=set()
        for ime in self.sez_tekmovalcev:
            tekmovalec=self.natancno_izpisi_tekmovalca(ime)
            nabor=(tekmovalec[0][0],tekmovalec[0][2])
            mnozica.add(nabor)
        slovar={}
        for _, drzava in mnozica:
            if drzava in slovar:
                slovar[drzava] += 1
            else:
                slovar[drzava] = 1
        return slovar
    

########################################################################################################################
########################################################################################################################

def plot_evolve(slovar, disciplina):
    '''
    Spreminjanje rezultatov skozi cas pri podani disciplini.
    '''

    seznam1,seznam2,seznam3=[[],[],[]]
    leto1,leto2,leto3=[[],[],[]]
    rezultat1,rezultat2,rezultat3=[[],[],[]]

    for _,sez,_ in slovar[disciplina]:
        for s in sez:
            if s[2]=='':
                continue
            s2=''
            r=0
            # Resimo problem, ker so pri disciplinah z dalsimi casi nekonsistentni zapisi.
            for i in s[2]:
                if i == 'h':
                    s2 += ':'
                if i=='-':
                    s2+=':'
                if i == '"':
                    continue
                if i != 'h' and i != '-' and i != '"':
                    s2 += i
            # Zapis v urah pri disciplinah z daljsimi progami
            for j,i in enumerate(s2.split(':')):
                if j == 0:
                    r += float(i)
                if j == 1:
                    r += float(i)/60
                if j == 2:
                    r += float(i)/3600
            # Resimi problem pri dolocenih disciplinah
            if disciplina=='long jump men' and s[0]=='1900':
                continue
            if disciplina=='decathlon men' and s[0]=='2004':
                continue
            if disciplina=='heptathlon women' and s[0]=='2004':
                continue
            else:
                if s[1] == '1':
                    try:
                        seznam1.append((float(s[0]),float(r)))
                    except:
                        continue
                if s[1] == '2':
                    try:
                        seznam2.append((float(s[0]),float(r)))
                    except:
                        continue
                if s[1] == '3':
                    try:
                        seznam3.append((float(s[0]),float(r)))
                    except:
                        continue

    # Naredimo sezname potrebne za risanje grafa
    for i, j in sorted(seznam1[::-1]):
        leto1.append(i)
        rezultat1.append(j)
    for i, j in sorted(seznam2[::-1]):
        leto2.append(i)
        rezultat2.append(j)
    for i, j in sorted(seznam3[::-1]):
        leto3.append(i)
        rezultat3.append(j)

    # Izris oz shranitev grafa
    fig = plt.figure()

    plt.plot(leto1, rezultat1, marker='o',color='gold',markeredgecolor = 'white',zorder=0,label="1.mesto")
    plt.plot(leto2, rezultat2, marker='o',color='gray',markeredgecolor = 'white',zorder=0,label="2.mesto")
    plt.plot(leto3, rezultat3, marker='o',color='brown',markeredgecolor = 'white',zorder=0,label="3.mesto")

    plt.title("Spreminjanje rezultatov skozi cas pri disciplini {}".format(disciplina))
    plt.xlabel("Leta")
    plt.ylabel("Rezultati")
    plt.legend(loc='best')
    plt.close()
    #plt.show()
    fig.savefig('grafi_za_oi/rezultati_skozi_cas_pri_{}_disciplini.pdf'.format(disciplina))

def bar_st_drzav_po_disc(slovar, disciplina):
    '''
    Stevilo drzav pri doloceni disciplini
    '''

    olimpijske_igre=[]
    st_drzav=[]

    # Naredimo sezname potrebne za risanje grafa
    for oi in slovar:
        if slovar[oi] != 0:
            olimpijske_igre.append(float(oi[-4:]))
            st_drzav.append(slovar[oi])

    # Izris oz shranitev grafa
    fig=plt.figure(figsize=(6,10))

    plt.barh(olimpijske_igre,st_drzav,color='gray',edgecolor='white')
    plt.title('Stevilo drzav pri {} disciplini'.format(disciplina))
    plt.ylabel('Olimpijske igre')
    plt.xlabel('Stevilo drzav')
    plt.close()
    #plt.show()
    fig.savefig('grafi_za_oi/stevilo_drzav_skozi_cas_pri_{}_disciplini.pdf'.format(disciplina))

def st_tek_iz_drzav(slovar):
    '''
    Stevilo tekmovalcev iz posameznih drzav, kjer je stevilo vecje od 100.
    '''

    drzave = []
    st_tekmovalcev = []

    # Naredimo sezname potrebne za risanje grafa
    for drzava in slovar:
        if slovar[drzava] >= 100:
            drzave.append(drzava)
            st_tekmovalcev.append(slovar[drzava])

    # Izris oz shranitev grafa
    fig=plt.figure(figsize=(6,10))

    plt.barh(drzave, st_tekmovalcev, color='gray',edgecolor='white')
    plt.title('Stevilo tekmovalcev iz posameznih drzav, kjer je stevilo vecje od 100')
    plt.xlabel('Drzave')
    plt.ylabel('Stevilo tekmovalcev')

    fig.autofmt_xdate()
    plt.close()
    #plt.show()
    fig.savefig('grafi_za_oi/St_tek_iz_pos_drzave.pdf')

def men_vs_women(slovar, mendisciplina, womendisciplina):
    '''
    Primerjava moskih in zenskih zmagovalcev skozi cas pri doloceni disciplini.
    '''

    seznam1,seznam2=[[],[]]
    leto1,leto2=[[],[]]
    rezultat1,rezultat2=[[],[]]
    
    for _,sez,_ in slovar[mendisciplina]:
        sez
        for s in sez:
            if s[2]=='':
                continue
            s2=''
            r=0
            # Resimo problem, ker so pri disciplinah z dalsimi casi nekonsistentni zapisi.
            for i in s[2]:
                if i == 'h' or i == '-':
                    s2 += ':'
                if i == '"':
                    continue
                else:
                    s2 += i
            # Zapis v urah pri disciplinah z daljsimi progami
            for j,i in enumerate(s2.split(':')):
                if j == 0:
                    r += float(i)
                if j == 1:
                    r += float(i)/60
                if j == 2:
                    r += float(i)/3600
            # Resimi problem pri doloceni disciplini
            if mendisciplina=='long jump men' and s[0]=='1900':
                continue
            else:
                if s[1] == '1':
                    try:
                        seznam1.append((float(s[0]),float(r)))
                    except:
                        continue

    for _,sez,_ in slovar[womendisciplina]:
        sez
        for s in sez:
            if s[2]=='':
                continue
            s2=''
            r=0
            # Resimo problem, ker so pri disciplinah z dalsimi casi nekonsistentni zapisi.
            for i in s[2]:
                if i == 'h' or i == '-':
                    s2 += ':'
                if i=='"':
                    continue
                else:
                    s2 += i
            # Zapis v urah pri disciplinah z daljsimi progami
            for j,i in enumerate(s2.split(':')):
                if j == 0:
                    r += float(i)
                if j == 1:
                    r += float(i)/60
                if j == 2:
                    r += float(i)/3600
            # Resimi problem pri doloceni disciplini
            if womendisciplina=='long jump men' and s[0]=='1900':
                continue
            else:
                if s[1] == '1':
                    try:
                        seznam2.append((float(s[0]),float(r)))
                    except:
                        continue

    # Naredimo sezname potrebne za risanje grafa
    for i, j in sorted(seznam1[::-1]):
        leto1.append(i)
        rezultat1.append(j)
    for i, j in sorted(seznam2[::-1]):
        leto2.append(i)
        rezultat2.append(j)

    # Izris oz shranitev grafa
    fig = plt.figure()

    plt.plot(leto1, rezultat1, marker='o',color='gold',markeredgecolor = 'white',zorder=0,label="moski")
    plt.plot(leto2, rezultat2, marker='o',color='gray',markeredgecolor = 'white',zorder=0,label="zenske")
    
    plt.title("Primerjava moskih in zenskih zmagovalcev skozi cas pri disciplini {}".format(mendisciplina[:-4]))
    plt.xlabel("Leta")
    plt.ylabel("Rezultati")
    plt.legend(loc='best')

    plt.close()
    #plt.show()
    fig.savefig('grafi_za_oi/Primerjava moskih in zenskih zmagovalcev skozi cas pri disciplini {}.pdf'.format(mendisciplina[:-4]))

def narisi_zemlevid(slovar_kolicin, slovar_koordinat):
    '''
    Funkcija izrise zemljevid in velicina pik oznacuje stevilo tekmovalcev iz te
    drzave.
    '''

    drzave=[]
    kolicina=[]
    longitudes=[]
    latitudes=[]

    for drzava in slovar_kolicin:
        if drzava in slovar_koordinat:
            drzave.append(drzava)
            kolicina.append(slovar_kolicin[drzava])
            latitudes.append(slovar_koordinat[drzava][0])
            longitudes.append(slovar_koordinat[drzava][1])

    fig=plt.figure(figsize=(16,11))

    map = Basemap()
    map.drawcoastlines()
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='coral', lake_color='aqua')

    for i in range(len(drzave)):
        
        plt.scatter(longitudes[i],latitudes[i],marker='o',s=kolicina[i], c='white',edgecolors='gray',zorder=2*(len(drzave)-1-i))

    plt.title('Od kod prihajajo atleti')
    plt.ylabel('Country latitude')
    plt.xlabel('Country longitude')    
    
    plt.close()
    #plt.show()
    fig.savefig('grafi_za_oi/Od kod prihajajo atleti.pdf')
    
    


########################################################################################################################
########################################################################################################################

# V slovar podatki_tekmovalcev shranimo: ključ je tekmovalec in za vrednost imamo seznam vseh njegovih rezutlatatov na
# oi in njegov rojstni dan ter iz katere države je.

podatki_tekmovalcev={}

with open('rezultati.csv', 'r', encoding="utf-8") as dat:
    vrstice = dat.readlines()
    for vrstica in vrstice[1:]:
        razdeljeno = vrstica.split(',')
        if razdeljeno[0] == '\n':
            continue
        if razdeljeno[1] in ['4x100m relay men','4x400m relay men','4x100m relay women','4x400m relay women']:
            continue
        else:
            if razdeljeno[3] in podatki_tekmovalcev:
                podatki_tekmovalcev[razdeljeno[3]].append(
                    (razdeljeno[0], razdeljeno[1], razdeljeno[2], razdeljeno[4], razdeljeno[5][:-1])
                )
            else:
                podatki_tekmovalcev[razdeljeno[3]] = [
                    (razdeljeno[0], razdeljeno[1], razdeljeno[2], razdeljeno[4], razdeljeno[5][:-1])
                ]

with open('roj_dan_tekmovalcev.csv', 'r', encoding="utf-8") as dat:
    vrstice = dat.readlines()
    for vrstica in vrstice:
        razdeljeno = vrstica.split(',')
        if razdeljeno[0] in podatki_tekmovalcev:
            podatki_tekmovalcev[razdeljeno[0]].append(razdeljeno[1][:-1])

drzave_s_koordinatami={}
with open('koordinate.csv', 'r', encoding="utf-8") as dat:
    vrstice=dat.readlines()
    for vrstica in vrstice[1:]:
        if vrstica=='\n':
            continue
        drzava, geo_dolzina, geo_sirina = vrstica.split(',')
        geo_sirina=geo_sirina[:-1]
        drzave_s_koordinatami[drzava]=(geo_dolzina,geo_sirina)

for drzava in drzave_s_koordinatami:
    geo_dolzina,geo_sirina = drzave_s_koordinatami[drzava]
    longitude=0
    if geo_dolzina != '':
        stopinje, preostalo1 = geo_dolzina.split('°')
        if len(preostalo1) != 1:
            minute, preostalo2 = preostalo1.split("′")
            if len(preostalo2) != 1:
                sekunde, preostalo3 = preostalo2.split('″')
                if preostalo3 == 'N':
                    longitude = float(stopinje) + float(minute)/60 + float(sekunde)/3600
                else:
                    longitude = -1*(float(stopinje) + float(minute)/60 + float(sekunde)/3600)                    
            else:
                if preostalo2 == 'N':
                    longitude = float(stopinje) + float(minute)/60
                else:
                    longitude = -1*(float(stopinje) + float(minute)/60)
        else:
            if preostalo1 == 'N':
                longitude = float(stopinje)
            else:
                longitude = -1*(float(stopinje))
    latitude=0
    if geo_sirina != '':
        stopinje, preostalo1 = geo_sirina.split('°')
        if len(preostalo1) != 1:
            minute, preostalo2 = preostalo1.split("′")
            if len(preostalo2) != 1:
                sekunde, preostalo3 = preostalo2.split('″')
                if preostalo3 == 'E':
                    latitude = float(stopinje) + float(minute)/60 + float(sekunde)/3600
                else:
                    latitude = -1*(float(stopinje) + float(minute)/60 + float(sekunde)/3600)                    
            else:
                if preostalo2 == 'E':
                    latitude = float(stopinje) + float(minute)/60
                else:
                    latitude = -1*(float(stopinje) + float(minute)/60)
        else:
            if preostalo1 == 'E':
                latitude = float(stopinje)
            else:
                latitude = -1*(float(stopinje))
    drzave_s_koordinatami[drzava]=(longitude, latitude)


########################################################################################################################
########################################################################################################################

# Podatki, ki jih uporabimo

# za izris zemljevida
slovar_kolicin=Tekmovalci(podatki_tekmovalcev).tekmovalec_in_drzava()
narisi_zemlevid(slovar_kolicin,drzave_s_koordinatami)


slovar1=Tekmovalci(podatki_tekmovalcev).zmagovalci_po_disciplinah()

# za funkcijo plot_evolve
discipline1=['marathon women','marathon men','10000m women','10000m men',
             '5000m women','5000m men','1500m women','1500m men',
             '50km walk men','20km walk men','hammer throw men','triple jump women',
             '100m hurdles women','hammer throw women','400m men','400m women',
             '400m hurdles men','400m hurdles women','triple jump men']
for disciplina in discipline1:
    plot_evolve(slovar1, disciplina)

# za funkcijo bar_st_drzav_po_disc
discipline2=['discus throw women','long jump men','high jump women','800m women',
             'marathon men','100m women','discus throw men','100m men']
for disciplina in discipline2:
    slovar2=Tekmovalci(podatki_tekmovalcev).st_raz_drzav_pri_disc(disciplina)
    bar_st_drzav_po_disc(slovar2, disciplina)

# za funkcijo st_tek_iz_drzav
drzave=Tekmovalci(podatki_tekmovalcev).tekmovalec_in_drzava()
st_tek_iz_drzav(drzave)

# za funkcijo men_vs_women
seznam3=[('shot put men','shot put women'),('100m men','100m women'),
        ('200m men','200m women'),('javelin throw men','javelin throw women'),
        ('long jump men','long jump women'),('high jump men', 'high jump women'),
        ('discus throw men','discus throw women')]
for men, women in seznam3:
    men_vs_women(slovar1,men,women)




