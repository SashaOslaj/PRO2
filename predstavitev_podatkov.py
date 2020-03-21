
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
        for nastop in self.nastopi:
            starost = int(nastop[0][-4:]) - int(self.rojen[-4:])
            print(
                " ime        | {0} \n rojen/a    | {1} v {2} \n oi         | {3} \n disciplina | {4} \n mesto      | {5} \n rezultat   | {6} \n starost    | {7} \n".format(
                    self.ime, self.rojen, self.drzava, nastop[0], nastop[1], nastop[2], nastop[4].replace('"',''), str(starost)
                )
            )

    def podatki_po_disciplinah(self):
        slovar={}
        for nastop in self.nastopi:
            if nastop[1] in slovar:
                slovar[nastop[1]].append(nastop)
            else:
                slovar[nastop[1]] = [nastop]
        return slovar


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

#for i in sorted(podatki_tekmovalcev)[1:]:
#    print(Tekmovalec(i, podatki_tekmovalcev[i][:-1], podatki_tekmovalcev[i][-1]))

Tekmovalec(
    "Mohamed Farah", podatki_tekmovalcev["Mohamed Farah"][:-1], podatki_tekmovalcev["Mohamed Farah"][-1]
).natancna_predstavitev_tekmovalca()



