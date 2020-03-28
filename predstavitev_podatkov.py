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

    def __str__(self):
        nastopi = ''
        for nastop in self.nastopi:
            nastopi += 'Na {0} olimpijskih igrah v {1} disciplini je bil/a na {2} mestu z rezultatom {3}, '.format(
                nastop[0], nastop[1], nastop[2], nastop[4]
            )
        return " ime     | {0} \n rojen   | {1} v {3} \n nastopi | {2} \n".format(
            self.ime, self.rojen, nastopi, self.drzava
        )

    def __repr__(self):
        return 'Tekmovalec({0},{1},{2})'.format(self.ime, self.nastopi, self.rojen)

    def natancna_predstavitev_tekmovalca(self):
        seznam=[]
        for nastop in self.nastopi:
            if self.rojen == '':
                seznam.append((self.ime, self.rojen, self.drzava, nastop[0], nastop[1], nastop[2], nastop[4].replace('"',''), 'Ni podatka'))
            starost = int(nastop[0][-4:]) - int(self.rojen[-4:])
            seznam.append((self.ime, self.rojen, self.drzava, nastop[0], nastop[1], nastop[2], nastop[4].replace('"',''), str(starost)))
        return seznam
            
    def podatki_po_disciplinah(self):
        slovar={}
        for nastop in self.nastopi:
            if nastop[1] in slovar:
                slovar[nastop[1]].append(nastop)
            else:
                slovar[nastop[1]] = [nastop]
        return slovar

    def predstavitev_tekmovalca_pri_disciplini(self, disciplina=None):
        seznam=[]
        if disciplina==None:          
            disciplina=random.choice(self.discipline)
            for i in self.podatki_po_disciplinah()[disciplina]:
                if self.rojen == '':
                    seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), 'Ni podatka'))
                starost = int(i[0][-4:]) - int(self.rojen[-4:])
                seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), str(starost)))
        if disciplina not in self.podatki_po_disciplinah():
            seznam.append(('Tekmovalec ni nastopil v {} disciplini'.format(disciplina)))
        else:
            for i in self.podatki_po_disciplinah()[disciplina]:
                if self.rojen == '':
                    seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), 'Ni podatka'))
                starost = int(i[0][-4:]) - int(self.rojen[-4:])
                seznam.append((self.ime, self.rojen, self.drzava, i[0], i[1], i[2], i[4].replace('"',''), str(starost)))
        return seznam
    
    def iz_katere_drzave(self):
        return self.nastop[0][3]

class Tekmovalci:

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

#Tekmovalec(
#    "Mohamed Farah", podatki_tekmovalcev["Mohamed Farah"][:-1], podatki_tekmovalcev["Mohamed Farah"][-1]
#).predstavitev_tekmovalca_pri_disciplini("5000m men")
print(Tekmovalci(podatki_tekmovalcev).natancno_izpisi_tekmovalca())
#print(podatki_tekmovalcev["Mohamed Farah"])


