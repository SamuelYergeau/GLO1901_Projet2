'''main.py

document principal du jeu quoridor. contient la logique du programme.
Effectue les tâches:
    - recevoir le idul d'un joueur
    - débuter la partie
    - afficher la table de jeu
    - intéragir avec le joueur pour continuer le jeu
    - intéragir avec api.py pour communiquer avec le serveur
Contient les fonctions:
    - afficher_damier_ascii (projet)
        affiche la table de jeu en fonction des informations obtenues du serveur
    - analyser_commande (projet)
        écoute le terminal pour obtenir le idul du joueur et savoir si ce dernier
        souhaire obtenir la liste de ses 20 dernières parties
    - listing (useful tools)
        obtient la liste des 20 dernières parties du joueur et les lui affichent
    - debuter (structure logique)
        effectue les opérations pour débuter une nouvelle partie
    - prompt_player (structure logique)
        intéragit avec le joueur pour obtenir les informations de son prochain coup
    - boucler (structure logique)
        effectue la logique rincipale de la partie:
        - obtenir le prochain coup
        - notifier le serveur
        - afficher le jeu
        - terminer le jeu
'''
import quoridor

def loop(joueurs, jeu):
    """loop
        Simple fonction pour tester quoridor.py
        # fonction pour le projet 1
        if __name__ == "__main__":
            #  écouter si le joueur veut commencer une partie
            COM = analyser_commande()
            # vérifier si l'argument lister a été appelé
            if 'lister' in COM and COM.lister:
                # appeler la fonction lister
                listing(COM.idul)
            else:
                # débuter la partie et storer le id de la partie
                GAME_ID += debuter(COM)
                # boucler sur la logique de la partie
                boucler()
    """
    while True:
        # Itérer sur les deux joueurs
        for n in range(1, 3):
            try:
                # afficher le jeu
                print(jeu)
                # jouer le coup du joueur 1
                if joueurs[(n - 1)] == "robot":
                    jeu.jouer_coup(n)
                else:
                    print("tout à {}".format(joueurs[(n-1)]))
                    print("indiquer le type de coup à jouer")
                    tcoup = input("[D, MH ou MH]: ").upper()
                    posx = int(input("position en x du coup: "))
                    posy = int(input("position en y du coup: "))
                    # agir selon le type de coup
                    if tcoup == 'D':
                        jeu.déplacer_jeton(n, (posx, posy))
                    elif tcoup == 'MH':
                        jeu.placer_mur(n, (posx, posy), 'horizontal')
                    elif tcoup == 'MV':
                        jeu.placer_mur(n, (posx, posy), 'vertical')
                    else:
                        print("type de coup invalide")
                        continue
                # tester si la partie est terminer
                gagnant = jeu.partie_terminée()
                if gagnant:
                    print('\n' + '~' * 39)
                    print("LA PARTIE EST TERMINÉE!")
                    print("{} À GAGNÉ!".format(gagnant))
                    print('~' * 39 + '\n')
                    print(jeu)
                    return
            except quoridor.QuoridorError as qe:
                print(qe)
                continue


ETAT_JEU = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}
    ],
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    }
}
#swag lines
print('\n' + '~' * 39)
print("BIENVENU DANS QUORIDOR!")
print('~' * 39 + '\n')
# offrir de jouer une nouvelle partie ou reprendre une partie existante
print("souhaitez vous commencer une nouvelle partie ou continuer une partie existante?")
print("1 = nouvelle partie | 2 = partie existante")
CHOIX = int(input("choix: "))
if CHOIX == 1:
    # obtenir le nom des deux joueurs
    print("veuillez entrer le nom des joueurs:")
    JOUEUR1 = input("nom du joueur1: ")
    JOUEUR2 = input("nom du joueur2: ")
    # demarrer une nouvelle partie
    JEU = quoridor.Quoridor([JOUEUR1, JOUEUR2])
    loop([JOUEUR1, JOUEUR2], JEU)
elif CHOIX == 2:
    JEU = quoridor.Quoridor(ETAT_JEU['joueurs'], ETAT_JEU['murs'])
    loop(["joueur1", "joueur2"], JEU)
else:
    print("choix invalide!")
