import random
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

    def predstavitev_tekmovalca_pri_disciplini(self, disciplina=None):
        '''
            Funkcija vrne seznam naborov z imenom, rojstvom, drzavo, rezultatom
            pri doloceni disciplini in starostjo.
        '''
        seznam=[]
        if disciplina==None:          
            disciplina=random.choice(self.discipline)
            for i in self.podatki_po_disciplinah()[disciplina]:
                if self.rojen == '':
                    seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), 'Ni podatka'))
                    continue
                starost = int(i[0][-4:]) - int(self.rojen[-4:])
                seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), str(starost)))
        if disciplina not in self.podatki_po_disciplinah():
            seznam.append(('Tekmovalec ni nastopil v {} disciplini'.format(disciplina)))
        else:
            for i in self.podatki_po_disciplinah()[disciplina]:
                if self.rojen == '':
                    seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), 'Ni podatka'))
                    continue
                starost = int(i[0][-4:]) - int(self.rojen[-4:])
                seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), str(starost)))
        return seznam
    
    def iz_katere_drzave(self):
        return self.nastop[0][3]

    def najmlajsi_nastop(self):
        if len(self.natancna_predstavitev_tekmovalca())==1:
            return (self.natancna_predstavitev_tekmovalca()[0][-1], self.natancna_predstavitev_tekmovalca()[0])
        if self.natancna_predstavitev_tekmovalca()[0][-1] == 'Ni podatka':
            return 'Ni podatka'
        else:
            trenutni_min=(100,())
            for nastop in self.natancna_predstavitev_tekmovalca():
                if min(int(trenutni_min[0]), int(nastop[-1])) == int(trenutni_min[0]):
                    continue
                if min(int(trenutni_min[0]), int(nastop[-1])) < int(trenutni_min[0]):
                    trenutni_min = (nastop[-1], nastop)
            return trenutni_min

    def najstarejsi_nastop(self):
        if len(self.natancna_predstavitev_tekmovalca())==1:
            return (self.natancna_predstavitev_tekmovalca()[0][-1], self.natancna_predstavitev_tekmovalca()[0])
        else:
            trenutni_max=(0,())
            for nastop in self.natancna_predstavitev_tekmovalca():
                if max(int(trenutni_max[0]), int(nastop[-1])) == int(trenutni_max[0]):
                    continue
                if max(int(trenutni_max[0]), int(nastop[-1])) > int(trenutni_max[0]):
                    trenutni_max = (nastop[-1], nastop)
            return trenutni_max
                    

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
        if ime == None:
            ime = random.choice(self.sez_tekmovalcev)
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1])
        else:
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1])

    def natancno_izpisi_tekmovalca(self, ime=None):
        if ime == None:
            ime = random.choice(self.sez_tekmovalcev)
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).natancna_predstavitev_tekmovalca()
        else:
            return Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).natancna_predstavitev_tekmovalca()

    def najmlajsi_tekmovalec(self):
        vsi=[Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).najmlajsi_nastop() for ime in self.sez_tekmovalcev]
        najmlasi_nastopi_tekmovalcev=[i for i in vsi if i[0] != 'Ni podatka']
        trenutni_min = (100,())
        for i in najmlasi_nastopi_tekmovalcev:
            #print(i)
            if i == 'Ni podatka':
                continue
            if min(int(trenutni_min[0]), int(i[0])) == int(trenutni_min[0]):
                continue
            if min(int(trenutni_min[0]), int(i[0])) < int(trenutni_min[0]):
                trenutni_min = i
        return trenutni_min[1]
    
    def najstarejsi_tekmovalec(self):
        vsi=[Tekmovalec(ime, podatki_tekmovalcev[ime][:-1], podatki_tekmovalcev[ime][-1]).najmlajsi_nastop() for ime in self.sez_tekmovalcev]
        najstarejsi_nastopi_tekmovalcev=[i for i in vsi if i[0] != 'Ni podatka']
        trenutni_max = (0,())
        for i in najstarejsi_nastopi_tekmovalcev:
            #print(i)
            if i == 'Ni podatka':
                continue
            if max(int(trenutni_max[0]), int(i[0])) == int(trenutni_max[0]):
                continue
            if max(int(trenutni_max[0]), int(i[0])) > int(trenutni_max[0]):
                trenutni_max = i
        return trenutni_max[1]

    

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

########################################################################################################################
########################################################################################################################

# Podatki, ki jih uporabimo

#print(podatki_tekmovalcev)
#for i in sorted(podatki_tekmovalcev)[1:]:
#    print(i,podatki_tekmovalcev[i])
#print(
#Tekmovalec(
#    "Usain Bolt",
#    podatki_tekmovalcev["Usain Bolt"][:-1],
#    podatki_tekmovalcev["Usain Bolt"][-1]
#).najstarejsi_nastop())
print(Tekmovalci(podatki_tekmovalcev).najstarejsi_tekmovalec())
print(Tekmovalci(podatki_tekmovalcev).najmlajsi_tekmovalec())
#print(podatki_tekmovalcev["Mohamed Farah"])


