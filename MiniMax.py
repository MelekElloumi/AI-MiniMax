import sys
import random
import time
import math

def initier():
    print("Donner le nombre de jetons au depart")
    nbj = 0
    while (nbj <= 0):
        nbj = int(input())
        if (nbj < 0):
            print("Le nombre doit etre positive. Reessayer")
    print("Donner le nom du joueur 1 (MAX)")
    global nommax
    nommax = input()
    print("Donner le nom du joueur 2 (MIN)")
    global nommin
    nommin = input()
    print("Je lance une pièce au hasard")
    time.sleep(1)
    premier = random.randint(1, 2)
    if (premier == 1):
        print("" + nommax + " commence le premier")
    else:
        print("" + nommin + " commence le premier")
    time.sleep(1)
    return nbj,premier

def initier_pc():
    print("Donner le nombre de jetons au depart")
    nbj = 0
    while (nbj <= 0):
        nbj = int(input())
        if (nbj < 0):
            print("Le nombre doit etre positive. Reessayer")
    print("Donner ton nom")
    global nommax
    nommax = input()
    print("Je lance une pièce au hasard")
    time.sleep(1)
    premier = random.randint(1, 2)
    if (premier == 1):
        print("" + nommax + " commence le premier")
    else:
        print("L'ordinateur commence le premier")
    time.sleep(1)
    return nbj,premier


def main():
    print("Jeu de piles")
    x=0
    while(x!=3):
        print('-----------------------------------------')
        print("1-Resolution du jeu")
        print("2-Jouer contre l'ordinateur")
        print("3-Quitter")
        print('-----------------------------------------')
        print('Ecrire le numéro du choix: ')
        x = int(input())
        if x == 1:
            nbj, premier = initier()
            c = 0
            while (c != 4):
                print('-----------------------------------------')
                print("1-Resolution minmax usuelle")
                print("2-Resolution minmax avec elagage")
                print("3-Reinitialiser le jeu")
                print("4-Revenir")
                print('-----------------------------------------')
                print('Ecrire le numéro du choix: ')
                c = int(input())
                if c == 1:
                    mm = Minimax()
                    mm.minmax(nbj, premier, False)
                elif c == 2:
                    mm = Minimax()
                    mm.minmax(nbj, premier, True)
                elif c == 3:
                    nbj, premier = initier()
                elif c == 4:
                    break
        elif x == 2:
            nbj,premier=initier_pc()
            mm=Minimax()
            mm.cpuminmax(nbj,premier)

        elif x == 3:
            break

class Minimax:
    nbnoeud =0

    def cpuminmax(self,nbj,premier):
        piles=[]
        piles.append(nbj)
        if (premier ==1):
            pchoix=self.max_joueur(piles)
            if (self.termine(pchoix)):
                print("Jeu termine. " + nommax + " gagne")
                return
        else:
            pchoix=piles.copy()
        while(not self.termine(pchoix)):
            pchoix=self.min_pc(pchoix,0-math.inf,math.inf)
            if(self.termine(pchoix)):
                print("Jeu termine. " + nommax + " perd")
                break
            pchoix=self.max_joueur(pchoix)
            if (self.termine(pchoix)):
                print("Jeu termine. " + nommax + " gagne")
                break

    def min_pc(self,piles,a,b):
        v = math.inf
        actions = self.diviser(piles)
        pchoix=actions[0]
        for act in actions:
            vo=v
            v = min(v, self.max_value_elagage(act, a, b))
            if (v!=vo):
                pchoix=act.copy()
            if (v <= a):
                return pchoix
            b = min(b, v)
        time.sleep(2)
        print("L'ordinateur a choisi de jouer: ")
        print(pchoix)
        time.sleep(1)
        return pchoix

    def max_joueur(self,piles):
        actions = self.diviser(piles)
        i = 1
        print("Voici vos options:")
        for act in actions:
            print(""+str(i) + "-" + str(act))
            i += 1
        ch = 0
        while (True):
            print("Donner le nombre de votre choix:")
            ch = int(input())
            if (ch in range(1,i)):
                break
            print("Resseyaer")
        print(nommax+" a choisi de jouer: ")
        print(actions[ch-1])
        return actions[ch-1]

    def minmax(self,nbj,premier,elagage):
        piles=[]
        piles.append(nbj)
        self.nbnoeud=0
        if (elagage):
            if (premier == 1):
                resultat=self.max_value_elagage(piles,0-math.inf,math.inf)
            else:
                resultat=self.min_value_elagage(piles,0-math.inf,math.inf)
        else:
            if (premier == 1):
                resultat=self.max_value(piles)
            else:
                resultat=self.min_value(piles)

        if(resultat>0):
            print(""+nommax+"(MAX) gagne")
        else:
            print("" + nommin + "(MIN) gagne")
        print("Le nombre de noeuds developpes est "+str(self.nbnoeud))

    def termine(self,piles):
        for i in piles:
            if (i!=1 and i!=2):
                return False
        return True

    def diviser(self,piles):
        actions=[]
        for i in piles:
            if (i==1 or i==2):
                continue
            for j in range(1,(i-1)//2+1):
                act=piles.copy()
                pos=act.index(i)
                act.pop(pos)
                act.insert(pos,i-j)
                act.insert(pos, j)
                actions.append(act)
        return actions


    def min_value(self,piles):
        self.nbnoeud += 1
        if (self.termine(piles)):
            return 1
        v=math.inf
        actions=self.diviser(piles)
        for a in actions:
            v=min(v,self.max_value(a))
        return v

    def max_value(self,piles):
        self.nbnoeud += 1
        if (self.termine(piles)):
            return -1
        v=0-math.inf
        actions=self.diviser(piles)
        for a in actions:
            v=max(v,self.min_value(a))
        return v

    def max_value_elagage(self,piles,a,b):
        self.nbnoeud += 1
        if (self.termine(piles)):
            return -1
        v=0-math.inf
        actions=self.diviser(piles)
        for act in actions:
            v=max(v,self.min_value_elagage(act,a,b))
            if (v>=b):
                return v
            a=max(a,v)
        return v

    def min_value_elagage(self,piles,a,b):
        self.nbnoeud += 1
        if (self.termine(piles)):
            return -1
        v=math.inf
        actions=self.diviser(piles)
        for act in actions:
            v=min(v,self.max_value_elagage(act,a,b))
            if (v<=a):
                return v
            b=min(b,v)
        return v


if __name__ == "__main__":
    main()