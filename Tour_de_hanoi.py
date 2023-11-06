#################################### IMPORTS #######################################
import turtle as tt
import copy as cp
import os
import pickle as pk
import time as tm


#le numéro d'une tour se situe entre 0 et 2
#la position d'un disque se situe en 0 et (nb_disques_sur_la_tour - 1)
#le numéro d'un disque se situe entre 1 et le nombre total de disques


def init(nb_disques):
    """création de la liste représentant la configuration initiale avant tout mouvement"""
    config_init = [[],[],[]]    
    for disque in range (nb_disques,0,-1):
        config_init[0].append(disque) #on crée la première liste qui représente la tour de gauche
    return config_init



def nombre_disques(plateau, numtour):
    """compte le nombre de disques sur une tour précisée"""
    return len(plateau[numtour])#le numéro de la tour se situe entre 0 et 2



def disque_superieur(plateau, numtour):
    """donne le numéro du disque supérieur sur la tour voulue"""
    if len(plateau[numtour]) > 0 : #on vérifie qu'il y a au moins un disque sur la tour
        return plateau[numtour][-1] #on renvoit le numéro du dernier disque, qui est celui au-dessus
    else :
        return -1



def position_disque(plateau, numdisque, position = 'plateau') :
    """ fonction qui reçoit le plateau actuel et le numéro d'un
    disque, elle retourne la tour/la position sur la tour où se trouve le disque """
    
    for tour in range(len(plateau)) :
        liste_tour = plateau[tour]
        
        for place_disque in range(len(liste_tour)) :
            if liste_tour[place_disque] == numdisque and position == 'tour' :
                return place_disque
            
            elif liste_tour[place_disque] == numdisque :
                return tour
            
    print("le disque est introuvable")
    return -1



def verifier_deplacement(plateau, numtourDep, numtourArr) : 
    """ fonction qui reçoit le plateau actuel, ainsi qu'une
    position initiale et une position finale, elle renvoit
    un booléen pour savoir si le déplacement est autorisé """
    if 0 <= numtourDep <= 2 and 0 <= numtourArr <= 2 :
        return plateau[numtourDep] != [] and (plateau[numtourArr] == [] or (plateau[numtourArr][-1] > plateau[numtourDep][-1]))
    else :
        print("il y a une erreur dans les arguments choisis")
        return False


        
def bon_nb_disques(plateau, nb_disques):
    """vérifie si le plateau contient bien le nombre de disques entré"""
    return nb_disques == (len(plateau[0]) + len(plateau[1]) + len(plateau[2]))

def verifier_victoire(plateau, nb_disques, debug = False) :#
    """ fonction qui reçoit le plateau actuel et le nombre
    de disques, et renvoit un booléen correspondant à la
    victoire """

    if debug :
        print("version debug de verifier_victoire\n")
        if not bon_nb_disques(plateau, nb_disques) :
            print("il y a un problème avec le nombre de disques dans le plateau")
            return -1

    if len(plateau[-1]) != nb_disques : # vérifie si la dernière liste est remplie
        return False
    
    drapeau = True
    place_disque = 0
    
    for num_disque in range(nb_disques, 0, -1) :
        if plateau[-1][place_disque] != num_disque :
            drapeau = False

        if debug :
            print("plateau[-1]{place_disque] = ", plateau[-1][place_disque])
            print("num_disque = ", num_disque)
            print("drapeau = ", drapeau, '\n')
            
        place_disque += 1

    return drapeau


#################################PARTIE II##########################################

def gooto(x = 0, y = 0, mode = "tp") :
    """ fonction qui permet de déplacer le curseur sans dessiner, permet de
    choisir entre la téléportation du curseur ou le déplacement simple
    avec l'argument mode
    par défaut il est en mode téléportation, dp le passe en mode déplacement"""

    if mode == "tp" :
        tt.up()
        tt.goto(x,y)
        tt.down()
    elif mode == "dp" :
        tt.up()
        tt.forward(x)
        tt.down()

    else :
        print("il y a un problème avec le mode de déplacement de la fonction gooto")
        print("erreur sur la fonction gooto")


def dessine_rectangle(x, y, col = "black", sens = "hg") :
    """ dessine un rectangle avec les dimensions données, peut aussi changer
    la couleur en mettant la bonne chaine de caractères en argument (col),
    peut aussi changer le sens de dessin du rectangle (par défaut départ du coin
    supérieur gauche)
    sens = "bg" : départ bas gauche
    sens = "hd" : départ haut droit
    sens = "bd" : départ bas droit """


    tt.color(col)

    if sens == "hg" :
        for i in [1, 2] :
            tt.forward(x)
            tt.right(90)
            tt.forward(y)
            tt.right(90)
    elif sens == "bg" :
        for i in [1, 2] :
            tt.forward(x)
            tt.left(90)
            tt.forward(y)
            tt.left(90)
    elif sens == "hd" :
        for i in [1, 2] :
            tt.right(90)
            tt.forward(y)
            tt.right(90)
            tt.forward(x)
    elif sens == "bd" :
        for i in [1, 2] :
            tt.left(90)
            tt.forward(y)
            tt.left(90)
            tt.forward(x)

    else :
        print("il y a un problème avec le sens de dessin du rectangle")
        print("erreur sur la fonction dessine_rectangle")

    tt.color("black")



def dessine_plateau(nb_disques) : #
    """ fonction qui reçoit le nombre de disques sur le plateau et
    le dessine """

    # initialisation des variables
    tder_disque = 40 + nb_disques * 30 # diamètre du dernier disque
    eet = tder_disque + 20 # espacement entre chaque tour
    x = -300
    y = -200

    # intialisation du curseur
    gooto(x, y)

    # dessin du plateau
    dessine_rectangle(3 * tder_disque + 3 * 20, 20)
    # dessin des tours
    gooto(x + eet / 2, y) # déplacement à la première tour
    
    for tour in range(3) :
        dessine_rectangle(6, 20 * (nb_disques + 1), sens = "bg")
        gooto(eet, mode = "dp")


# fonction auxiliaire qui trouve où se trouve le disque et sa place en fonction
def trouve_disque(numdisque, plateau, nb_disques) :#
    """ fonction qui prend en argument le numéro du disque à chercher, le plateau
    actuel et le nombre de disques et se place juste sous le disque au niveau de
    la tour """

    # initialisation des variables
    tder_disque = 40 + nb_disques * 30 # diamètre du dernier disque
    eet = tder_disque + 20 # espacement entre chaques tours
    x = -300
    y = -200

    gooto(x + eet / 2, y) # déplacement à la première tour

    for tour in range(len(plateau)) :
        for place_disque in range(len(plateau[tour])) :
            if numdisque == plateau[tour][place_disque] :
                gooto(eet * tour, mode="dp") # déplacement a la tour
                tt.left(90)
                gooto(20 * place_disque, mode="dp") # déplacement à la hauteur du disque
                tt.right(90)


def dessine_disque(numdisque, plateau, nb_disques, col="black") : #
    """ fonction qui prend le numéro de disque, la configuration du plateau et
    le nombre de disques sur le plateau et dessine le disque correspondant au
    numéro du disque donné en argument """

    # initialisation des variables
    tda = 40 + 30 * (numdisque - 1) # correspond à la taille du disque à dessiner
    x = -300
    y = -200

    trouve_disque(numdisque, plateau, nb_disques)
    gooto(tda / 2 + 3, mode="dp") # déplacement au coin inférieur droit du disque
# 0 dessiner
    dessine_rectangle(tda, 20, col, "bd")



def efface_tour(nd, plateau, n) :#
    """ fonction qui prend en argument le numéro du disque, le plateau
    et le nombre de disques, et qui va effacer la tour qui est sous le disque """

    # initialisation des variables
    tder_disque = 40 + n * 30 # diamètre du dernier disque
    eet = tder_disque + 20 # espacement entre chaque tour
    x = -300
    y = -200

    gooto(x + eet / 2, y) # déplacement à la première tour

    for tour in range(len(plateau)) :
        for place_disque in range(len(plateau[tour])) :
            if nd == plateau[tour][place_disque] :
                gooto(eet * tour, mode="dp") # déplacement à la tour
                tt.left(90)
                gooto(20 * place_disque + 1, mode="dp") # déplacement à la hauteur du disque
                tt.right(90)
                dessine_rectangle(6, 18, "white", "bg")


                
def efface_disque(nd, plateau, n) :
    """ fonciton qui prend le disque à effacer, le plateau et le nombre de
    disques et va effacer le disque correspondant """
    dessine_disque(nd, plateau, n, "white")
    tt.color("black")

def dessine_config(plateau, n, col="black") :
    """ fonction qui prend le plateau actuel en argument et le nombre de disques
    dans celui-ci et dessine les disques en conséquence
    on considère le plateau et les tours déjà dessinés """

    for disque in range(1, n + 1) :
        dessine_disque(disque, plateau, n, col)
        efface_tour(disque, plateau, n)


def efface_tout(plateau, n, col="white") :
    """ fonction qui reçoit le plateau actuel et le nombre total de disques et
    efface tous les disques présents """

    for disque in range(1, n + 1) :
        efface_disque(disque, plateau, n)
    dessine_plateau(n)


################################### PARTIE III #####################################

    
def check_startmoov(Plateau, start):
    """ Vérifie si le disque sélectionné en premier peut être déplacé ou non """
    if start==0:
        # vérifie si au moins 1 des disques des 2 autres tours sont supérieur à celui selectionné
        return verifier_deplacement(Plateau, start, 1) or verifier_deplacement(Plateau, start,2)
    
    elif start==1:
        # vérifie si au moins 1 des disques des 2 autres tours sont supérieur à celui selectionné
        return verifier_deplacement(Plateau, start, 0) or verifier_deplacement(Plateau, start,2)
    
    elif start==2:
        # vérifie si au moins 1 des disques des 2 autres tours sont supérieur à celui selectionné
        return verifier_deplacement(Plateau, start, 0) or verifier_deplacement(Plateau, start,1)

    else :
        return False


def lire_coords(plateau, debug = False):
    """Fonction permettant de demander et vérifier les tours selectionnées pour le déplacement d'un disque"""

    if debug :
        os.system("color A")
        print("Version debug de lire_coords\n")
        
    td = input("Entrez la tour de départ\n")
    td = int(td)
    if td == -5 :
        return -5, -5
    else :
        nb_disque = nombre_disques(plateau, td)>0
        ch_stmv = check_startmoov(plateau,td)

    #boucle while qui vérifie si la tour entrée est possible
    while td != -5 and td != -4 and td != -3 and td != -2 and td != -1 and not (0<=td<=2 and nb_disque and ch_stmv) :
        # permet d'arrêter la fonction si on choisit une des options
        if td == -2 :
            return -2, -2

        elif td == -1 :
            return -1, -1

        elif td == -3 :
            return -3, -3

        elif td == -4 :
            return -4, -4
        
        elif td == -5 :
            return -5, -5
        
        # on vérifie si la tour existe
        elif not 0<=td<=2:
            print("Erreur la tour renseignée n'existe pas !")

        #on vérifie si la tour n'est pas vide
        elif nombre_disques(plateau, td)==0:
            print("Erreur la tour numéro ",td," renseignée est vide !")

        # on vérifie si l'on peut déplacer le disque
        elif not check_startmoov(plateau, td):
            print("Vous ne pouvez pas déplacer le disque supérieur de la tour",td," sur les autres tours !")
            
        td = input("Entrez la tour de départ\n")
        td = int(td)
        
        if td >= 0 :            
            nb_disque = nombre_disques(plateau, td) > 0
            ch_stmv = check_startmoov(plateau,td)

    if debug :
        print("La tour de départ est : ", td)
        print("Elle contient : ", plateau[td])
        print("Passons à la tour d'arrivée\n")
    
    ta = input("Entrez la tour d'arrivée\n") #valeur inexécutable
    ta = int(ta)    
    verif_dep = verifier_deplacement(plateau,td,ta)

    # si on veut abandonner on tape -1 et on ne rentre pas dans la boucle while
    while ta != -5 and ta != -4 and ta != -3 and ta != -2 and ta != -1 and not (0<=ta<=2 and verif_dep) :
        # renvoit les valeurs qui permettront de vérifier si on abandonne, annule un coup
        # ou sauvegarde
        if ta == -1 :
            return -1, -1
        
        elif ta == -2 :
            return -2, -2
        
        elif ta == -3 :
            return -3, -3

        elif ta == -4 :
            return -4, -4

        elif ta == -5 :
            return -5, -5
        
        # on vérifie si la tour existe
        elif not 0<=ta<=2: 
            print("Erreur la tour renseignée n'existe pas !")

        # on vérifie si ce n'est pas la même tour saisie que celle d'avant
        elif td==ta: 
            print("Vous ne pouvez pas déplacer le même disque sur la même tour !")

        # on vérifie si l'on peut bien déplacer le disque entre ces deux tours
        elif verifier_deplacement(plateau, td, ta)==False:
            print("Le disque supérieur de la tour",ta,"est plus petit que celui voulant être déplacé !")
                                                           
        ta = input("Entrez la tour d'arrivée\n")
        ta = int(ta)

        verif_dep = verifier_deplacement(plateau,td,ta)

    if debug :
        print("La tour d'arrivée est : ", ta)
        print("Elle contient : ", plateau[ta])
        
    return td,ta

def jouer_un_coup(plateau, n, td = None, ta = None) :
    """ fonction qui reçoit le plateau actuel et le nombre de disques et permet
    d'effectuer un coup """

    option = ''

    # ici on appelle la fonction pour générer td et ta s'ils ne sont pas donnés
    if td == None or ta == None :
        td, ta = lire_coords(plateau)

    # ici on vérifie si le joueur a choisi une option et on demande de confirmer
    if td == -1 :
        option = input("voulez-vous abandonner ? n/o \n")
        
    elif td == -2 :
        option = input("voulez-vous annuler le dernier coup ? n/o \n")

    elif td == -3 :
        option = input("voulez-vous sauvegarder ? n/o \n")

    elif td == -4 :
        option = input("voulez-vous récupérer votre sauvegarde ? n/o \n")

    elif td == -5 :
        option = input("voulez-vous voir la solution ? n/o \n")

    # ici on regarde si on a répondu oui à la question précédente
    if option == 'o' and td == -1 :
        return 1
    
    elif option == 'o' and td == -2 :
        return 2

    elif option == 'o' and td == -3 :
        return 3

    elif option == 'o' and td == -4 :
        return 4

    elif option == 'o' and td == -5 :
        return 5

    elif option == 'n' :
        return "azert"

    # effaçage du disque déplacé
    disque_deplacee = plateau[td][-1]
    efface_disque(disque_deplacee, plateau, n)
    tt.backward(20 + disque_deplacee * 30)

    # effaçage de la tour sous le disque déplacé
    trouve_disque(disque_deplacee, plateau, n)

        # changement du plateau
    plateau[td].remove(disque_deplacee)
    plateau[ta].append(disque_deplacee)

    # ici on doit redessiner la tour une fois que le changement du plateau
    # a été fait, puisqu'on utilise la fonction len pour connaitre la hauteur
    # de la tour à redessiner
    dessine_rectangle(6, (20 + n * 20) - len(plateau[td]) * 20, sens = "bg")

    # traçage du disque déplacé sur sa nouvelle tour
    dessine_disque(disque_deplacee, plateau, n)

    # traçage de la tour sous le disque qui est parti
    trouve_disque(disque_deplacee, plateau, n)
    tt.left(90)
    gooto(1, mode = "dp")
    tt.right(90)
    dessine_rectangle(6, 18,col = "white", sens = "bg")

    return 0 # retourne 0 pour éviter d'avoir une erreur

def boucle_jeu(plateau, n, nom, debug = False) :#
    """ intérragit avec le joueur, pour déplacer les disques jusqu'a ce que le
    joueur ait gagné """

    # mise en route du chrono
    debut = tm.time()
    print("le chronomètre est lancé")

    temps = 0 # permet le calcul du temps
    compteur = 0 # permet le calcul du nombre de coups joués
    option = 0 # permet au joueur de choisir d'autres actions
    coup_max = 2 ** n - 1 # calcul du nombre de coup max
    coup_maxi = True # sers de condition pour la boucle while
    historique = {} 
    historique[0] = init(n) # l'hitorique a l'état initiale en 0

    while not verifier_victoire(plateau, n) and option != 1 and coup_maxi:
        option = jouer_un_coup(plateau, n)

        # si lors de la saisie le joueur décide d'annuler son coup, on rentre la
        if option == 2 :
            annuler_dernier_coup(historique, compteur)
            plateau = cp.deepcopy(historique[compteur - 1])
            compteur -= 1
            
        if debug :
            print("##################################################")
            print("affichage de l'historique")
            print("compteur = ", compteur)
            print(historique)
            for e in historique :
                print(historique[e])
            print("##################################################")


        # si le joueur décide de sauvegarder on rentre la
        elif option == 3 :
            fin = tm.time()
            temps = fin - debut # le temps de jeu du joueur jusqu'a maintenant
            enrg_score(nom, n, compteur, temps, historique)

        # si le joueur veut récupérer sa partie d'avant on rentre la
        elif option == 4 :
            val_histo = recup_sauvegarde(nom, n)

            if val_histo != -1 :
                historique.clear()
                historique = cp.deepcopy(val_histo)
                
                # efface l'ancien plateau
                efface_tout(plateau, n)

                # récupère les valeurs nécessaires pour la suite du code
                compteur = historique["nombre de coups"]
                plateau = cp.deepcopy(historique[compteur])

                # redessine la configuration de la sauvegarde
                dessine_config(plateau, n)

                # récupération du temps passé sur la prtie précédente et réinitialisation du chrono
                temps = historique["temps passé"]
                début = tm.time()

        elif option == 5 :
            
            liste_sol = automatisation_jeu(n)
            efface_tout(plateau, n)
            dessine_plateau(n)
            solution_turtle(n, liste_sol)

        # sinon on rentre la et on ajoute le coup à l'historique
        elif option == 0 :
            compteur += 1
            plt_instant = cp.deepcopy(plateau)
            historique[compteur] = plt_instant
            
        coup_maxi = compteur <= coup_max + 10

    # filtrage de la varialbe temps
    fin = tm.time()
    temps = temps + fin - debut
    
    return compteur, option, temps

        
       

#################################### PARTIE IV #####################################
def tour_changee(dico, n) :
    """ fonction qui récupère les tours qui ont changés """
    
    # initialisation des variables
    x = 0 # cette vartiable sers juste a repérer si on as déjà repéré une tour
    t1 = -1
    t2 = -1

    # on veut seulement parcourir les tours
    for i in range(3) :

        if dico[n][i] != dico[n - 1][i] and x == 0 :
            t1 = i
            x = 1

        elif dico[n][i] != dico[n - 1][i] :
            t2 = i

    return t1, t2

def dernier_coup(dico, n) :
    """ fonction qui reçoit le dictionnaire contenant l'historique de coups ainsi
    qu'un numéro de dernier coup et qui renvoit le dernier coup joué sous forme
    de paire (tour de départ, tour d'arrivée) """

    # on récupère les deux tours qui ont changé
    t1, t2 = tour_changee(dico, n)

    # s'il y a plus de disques après qu'avant alors ça veut dire que c'est la
    # tour d'arrivée
    if len(dico[n][t1]) > len(dico[n - 1][t1]) :
        td = t2
        ta = t1
    else :
        td = t1
        ta = t2

    return td, ta

def annuler_dernier_coup(dico, n) :
    """ fonction qui prend le dictionnaire de coups et un numéro de dernier coup
    et qui annule ce dernier coup """

    # on récupère les deux tours td et ta
    td, ta = dernier_coup(dico, n)

    # puis on joue un à l'envers
    jouer_un_coup(dico[n], len(dico[0][0]), ta, td)
    del dico[n]

    return 1


#################################### PARTIE V ######################################
def enrg_score(nom, nb_dq, nb_cp, temps = 0, histo = None) :#
    """ fonction qui prends le nom du joueur, le nombre de disque, le nombre de coups
    et le dictionnaire qui fais l'historique et la stocke dans un fichier pickle """

    if histo == None :
        # création du fichier sauvegarde_hanoi s'il n'existe pas
        if not (os.path.exists("Sauvegarde_Hanoi.txt")) :
            sauv1 = open("Sauvegarde_Hanoi", 'ab')
            sauv1.close()
        
        # récupération du dictionnaire contenue dans le fichier de sauv
        sauv = open("Sauvegarde_Hanoi", 'rb')

        # vérifie si le fichier à une taille
        if os.path.getsize("Sauvegarde_Hanoi") > 0 :
            dico_sauv = pk.load(sauv)
            
        else :
            dico_sauv = {}
            
        sauv.close()

        # ajout du nouveau score
        dico_sauv[nom + str(nb_dq)] = [nom, nb_dq, nb_cp, tm.ctime(tm.time()), temps]

        # réinsertion du dictionnaire dans la sauv
        sauv = open("Sauvegarde_Hanoi", 'wb')
        pk.dump(dico_sauv, sauv)
        sauv.close

    else :
        cp_histo = cp.deepcopy(histo)
        cp_histo["nom"] = nom
        cp_histo["nombre de disques"] = nb_dq
        cp_histo["nombre de coups"] = nb_cp
        cp_histo["temps passé"] = temps
        nom_fichier = nom + ".txt"

        pic = open(nom_fichier, "wb")
        pk.dump(cp_histo, pic)
        pic.close()

        # création du fichier de nom s'il ne l'es pas déjà
        if not (os.path.exists("Nom_sauv.txt")) :
            nom1 = open("Nom_sauv.txt", 'ab')
            nom1.close

        # sauvegarde des noms dans un fichier à pars pour vérifier les sauvegardes
        noms = open("Nom_sauv.txt", 'rb')

        # on vérifie si le fichier a une taille
        if os.path.getsize("Nom_sauv.txt") > 0 :
            dico_nom = pk.load(noms)
            
        else :
            dico_nom = {}
            
        noms.close()

        dico_nom[nom + str(nb_dq)] = nb_dq

        noms = open("Nom_sauv.txt", 'wb')
        pk.dump(dico_nom, noms)
        noms.close

def recup_sauvegarde(nom, nb_dq) :
    """ fonction qui permet de récupérer la sauvegarde d'un joueur """
    
    # test si le nom possède bien une sauvegarde
    # test si le fichier contenant les noms existe
    if os.path.exists("Nom_sauv.txt") :
        noms = open("Nom_sauv.txt", 'rb')
        dico_nom = pk.load(noms)
        noms.close()
        
    else :
        print("Le nom donné ainsi que le nombre de disques ne correspondent à aucune sauvegarde")
        return -1

    if (nom + str(nb_dq)) in dico_nom :
        # charge la sauvegarde
        reload = open(nom + ".txt", 'rb')
        histo = pk.load(reload)
        reload.close()

        return histo

    else :
        print("Le nom donné ainsi que le nombre de disques ne correspondent à aucune sauvegarde")
        return -1

def affichage_score(n) :
    """ fonction qui va recevoir le nombre de disques de cette partie et va retourner
    le tableau de score pour ce nombre de disques """

    sauv = open("Sauvegarde_Hanoi")

    # on vérifie si le fichier n'est pas vide
    if os.path.getsize("Sauvegarde_Hanoi") > 0 :
        dico = pk.load(sauv)
        dico_score = calcul_dico_score(dico, n)

        # si le dictionnaire n'est pas vide pour ce nombre de disques alors on
        # fait l'afichage
        if dico_score != {} :
            dico_rangee = dict(sorted(dico_score.items(), key = lambda t:t[1]))

            liste_prenom = dico_rangee.keys()
            liste_score = dico_rangee.values()

            # maintenant qu'on a les listes correspondant aux prénoms et noms rangées
            # on peut commencer à les parcourir pour les afficher
            print("les meilleurs scores sont : ")
            for i in range(len(liste_score) -1, 0, -1) :
                print(liste_prenom[i], liste_score[i], sep=' : ')

    print("il n'y a pas de score sauvegardé pour ce nombre de disques")
    return -1


def calcul_temps(temps, nb_coup) :#
    """ fonction qui calcule le temps de réfelxion moyen par coup pour un joueur """
    return temps / nb_coup

def calcul_dico_score(dico, n, mode = "score") :#
    """ fonction qui calcul le dictionnaire correspondant aux meilleurs scores """

    dico_score = {}

    # on parcourt le dictionnaire
    for e in dico :
        # on regarde si le score enregistré correspond au bon nombre de disque
        if dico[e][1] == n :
            nom = dico[e][0]
            if mode == "temps" :
                dico_score[nom] = dico[e][4]
            elif mode == "moy" :
                dico_score[nom] = calcul_temps(dico[e][4], dico[e][2])
            else :
                dico_score[nom] = dico[e][2]

    return dico_score

######################################PARTIE VI#######################################
import random

def jouer_un_coup_sans_turtle(plateau, n, td, ta):
    """ fonction qui prend le plateau, le nombre de disques,
    la tour de départ et d'arrivée et met à jour le plateau """
    
    copie_plateau = cp.deepcopy(plateau)
    disque_deplace = copie_plateau[td][-1]
    copie_plateau[td].remove(disque_deplace)
    copie_plateau[ta].append(disque_deplace)
    
    return copie_plateau


def jouer_un_coup_avec_turtle(plateau, n, td, ta):
    """ fonction qui prend le plateau, le nombre de disques
    la tour de départ et d'arrivée et fait le plateau """
    
    # effaçage du disque déplacé
    print("fonction jouer_un_coup_avec_turtle :")
    print("td = ", td)
    print("plateau[td] = ", plateau[td])
    disque_deplace = plateau[td][-1]
    efface_disque(disque_deplace, plateau, n)
    tt.backward(20 + disque_deplace * 30)

    # effaçage de la tour sous le disque déplacé
    trouve_disque(disque_deplace, plateau, n)

        # changement du plateau
    plateau[td].remove(disque_deplace)
    plateau[ta].append(disque_deplace)

    # ici on doit redessiner la tour une fois que le changement du plateau
    # a été fait, puisqu'on utilise la fonction len pour connaitre la hauteur
    # de la tour à redessiner
    dessine_rectangle(6, (20 + n * 20) - len(plateau[td]) * 20, sens = "bg")

    # tracé du disque déplacé sur sa nouvelle tour
    dessine_disque(disque_deplace, plateau, n)

    # tracé de la tour sous le disque qui est parti
    trouve_disque(disque_deplace, plateau, n)
    tt.left(90)
    gooto(1, mode = "dp")
    tt.right(90)
    dessine_rectangle(6, 18,col = "white", sens = "bg")

    return 0 # retourne 0 pour éviter d'avoir une erreur

def trouver_solution(nb_disques, option = 'sol'):
    compteur = 0
    plateau = init(nb_disques)
    liste_sol = []
    tourDep = 0 #on initialise le premier coup, qui est toujours le même dans le cas optimal
    tourArr = 2
    plateau = jouer_un_coup_sans_turtle(plateau, nb_disques, tourDep, tourArr)
    liste_sol.append([tourDep,tourArr])
    
    sauv_plateau = [] #on sauvegarde la disposition du plateau à chaque coup
    tourDep_precedent = tourDep 
    tourArr_precedent = tourArr
    while not verifier_victoire(plateau, nb_disques):

        if plateau[0] == [nb_disques] and plateau[2] == [] : #on teste si le plus grand disque est le seul sur la première tour
            #et si la dernière tour est vide, alors on le déplace sur la dernière tour
            tourDep = 0
            tourArr = 2

        else :

        
            tourDep = random.randint(0,2)
            tourArr = random.randint(0,2)
        
        #on vérifie que le déplacement est possible, que la tour de départ n'est pas vide
        #et que le déplacement fait n'annule pas celui qui vient d'être effectué
            while not verifier_deplacement(plateau, tourDep, tourArr) or [tourDep,tourArr]==[tourArr_precedent,tourDep_precedent] or plateau[tourDep] == [] :

                tourArr = random.randint(0,2)
                tourDep = random.randint(0,2)
                
        tourDep_precedent = tourDep
        tourArr_precedent = tourArr
        #print('\n', plateau, '\n', sep='')
        plateau = jouer_un_coup_sans_turtle(plateau, nb_disques, tourDep, tourArr)#on met à jour le plateau
        liste_sol.append([tourDep,tourArr])#la liste prend les déplacements à chaque coup
        sauv_plateau.append(plateau)
        compteur += 1

        #if compteur >= 2**nb_disques + 10 :
            #return [1],[1]
        
        #print(liste_sol)

    if option != 'sol' :
        
        return sauv_plateau, liste_sol

    else :
        
        return liste_sol
        
        
    

"""

elif nb_disques in plateau[2] and (disque_superieur(plateau,2) - 1) == disque_superieur(plateau,0):
            
            tourDep = 0
            tourArr = 2

        elif nb_disques in plateau[2] and (disque_superieur(plateau,2) - 1) == disque_superieur(plateau,1) :

            tourDep = 1
            tourArr = 2

        

        elif plateau[0] == [nb_disques] and plateau[2] == [1] :
            
            tourDep = 2
            tourArr = 1

        elif plateau[1] == [nb_disques] and plateau[2] == [1] :
            
            tourDep = 2
            tourArr = 0 

        else :

        

        elif [] in plateau and [tourDep,tourArr]==[tourArr_precedent,tourDep_precedent] :

            for tour in range(3) :

                if plateau[tour] == [] :
                    tourArr = tour
                    
                elif disque_superieur(plateau,tour) != 1 :
                    tourDep = tour"""


def automatisation_jeu(nb_disques):
    liste_sol_optimale = trouver_solution(nb_disques)

    #on filtre les déplacements jusqu'à qu'il y en ait le minimum
    while len(liste_sol_optimale) <= (2**nb_disques + 10) and liste_sol_optimale == [1] :
        liste_sol_optimale = trouver_solution(nb_disques)
        
    return liste_sol_optimale

x = automatisation_jeu(4)
print(x)
print(len(x))


def solution_turtle(nb_disques, liste_deplacements):
    print("##################################################")
    print("fonction sol_turtle")
    print("liste_dep = ", liste_deplacements)
    print("##################################################")
    plateau = init(nb_disques)
    for coup in liste_deplacements :
        jouer_un_coup_avec_turtle(plateau,nb_disques,coup[0],coup[1])

        


###################################### MAIN ########################################

tt.speed(100)

print("Bonjour et bienvenue dans le jeu de la tour d'hanoi \n")
print("-1 pour abandonner")
print("-2 pour annuler le dernier coup")
print("-3 pour sauvegarder")
print("-4 pour récupérer une sauvegarde")
print("-5 pour voir la solution \n")
print("Comment vous appelez vous ?")
nom = input()
nb_disque = int(input("Avec combien de disques voulez vous jouer ? \n"))

plateau = init(nb_disque)
dessine_plateau(nb_disque)
dessine_config(plateau, nb_disque)
compteur, abb, temps = boucle_jeu(plateau, nb_disque, nom)

if abb == 1 :
    print("\nVous avez abandonné après ", compteur, "coups")
else :
    print("\nVous avez gagné, vous avez fait un score de ", compteur)
    sauv_fin = input("Voulez-vous sauvegarder votre score ? n/o \n")

    if sauv_fin == 'o' :
        enrg_score(nom, nb_disque, compteur, temps)
        print("Partie sauvegardée")
    else :
        print("Partie non sauvegardé")

tableau = input("Voulez-vous afficher le tableau des scores ? n/o \n")

if tableau == 'o' :
    print("Comment voulez-vous l'afficher ?")
    print("1 pour l'affichage par score")
    print("2 pour l'affichage par temps")
    print("3 pour l'affichage par moyenne de temps par coups")
    print("une autre entrée pour sortire du jeu")
    mode_aff = int(input())

