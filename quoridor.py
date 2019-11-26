#1)Fonctionnement de base de la classe Quoridor (30%)

#1.1)On peut construire une instance de la classe en spécifiant une liste de deux noms de joueurs. 
#Cette instance est construite avec l'état initial d'une nouvelle partie.

#1.2)On peut afficher en art ascii une représentation de l'état actuel de la partie en passant l'instance directement à la fonction print, 
#tel que décrit par l'énoncé.

#1.3)On peut récupérer le dictionnaire de l'état actuel de la partie grâce à la méthode état_parti, tel que décrit par l'énoncé.

#1.4)Avec des numéros de joueur et des positions valides, on peut déplacer les jetons des joueurs et placer des murs grâce aux méthodes
#  déplacer_jeton et placer_mur, tout en maintenant l'état de la partie à jour et conforme à l'énoncé.

#1.5)Lorsqu'un joueur gagne la partie, on peut le savoir grâce à la méthode partie_terminée, tel que décrit par l'énoncé.

#2)Initialisation d'une partie en cours (10%)
#2.1)On peut construire une instance de la classe Quoridor à partir de joueurs et de murs déjà positionnés à des emplacements valides


#3)Détection des erreurs (10%)
#3.1)Une classe QuoridorError est bien définie dans le module quoridor
#Les méthodes de la classe Quoridor soulèvent bien une instance de QuoridorError, 
#pour toutes les combinaisons invalides de leurs arguments.


#4) Choix automatique du prochain coup (10%)
#4.1)La méthode jouer_coup choisit toujours un coup valide pour le joueur spécifié, peu importe l'état actuel de la partie.

""" Quoridor.py
Module qui enferme les classes d'encapsulation
de la structure du jeu
contient les classes:
    - Quoridor
    - QuoridorError(Exception)
"""
import networkx as nx
import unittest
import matplotlib.pyplot as plt
import copy


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class QuoridorError(Exception):
    """QuoridorError    
    Classe pour gérer les exceptions survenue dans la classe Quoridor    
    Arguments:
        Exception {[type]} -- [description]
    """
    pass


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        __init__
        Initialisation de la classe Quoridor
        Arguments:
            joueurs {list}
                -- Une liste de 2 joueurs. chaque joueur est: (dict) ou (str)
                    - (str): nom du joueur
                    - (dict)
                        + 'nom' (str)   -- Nom du joueur
                        + 'murs' (int)  -- Nombre de murs que le joueur peut encore placer
                        + 'pos' (tuple) -- position (x, y) du joueur
        Keyword Arguments:
            murs {dict} (default: {None})
            -- 'horzontaux': [list of tuples]
                Une liste de tuples (x, y) représentant la position des différents
                murs horizontaux dans la partie
        TODO: faire une copie profonde au lieu d'unne copie normale (voir fil 1764)
        *** copy.deepcopy(x[,memo]) ou memo est le dictionnaire des objets déjà copié"""
        # définir les attribut de classes que nous allons utiliser
        self.joueurs = [{'nom':'', 'murs': 0, 'pos':(0,0)},
                        {'nom':'', 'murs': 0, 'pos':(0,0)}]
        self.murh = []
        self.murv = []
        starting_position = [(5, 1), (5, 9)]
        #faire un copie profonde de ce qui a besoin d'être copié
        self.joueurs = copy.deepcopy(self.joueurs)
        self.murh = copy.deepcopy(self.murh)
        self.murv = copy.deepcopy(self.murv)
        starting_position = copy.deepcopy(starting_position)
        # vérifier si un dictionnaire de murs est présent
        if murs:
            # vérifier si murs est un tuple
            if not(isinstance(murs, dict)):
                raise QuoridorError("murs n'est pas un dictionnaire!")
            # itérer sur chaque mur horizontal
            for mur in murs['horizontaux']:
                # Vérifier si la position du mur est valide
                if 1 < mur[0] > 8 and 2 < mur[1] > 9:
                    raise QuoridorError("position du mur non-valide!")
                self.murh += [mur]
            # itérer sur chaque mur vertical
            for mur in murs['verticaux']:
                if 2 < mur[0] > 9 and 1 < mur[1] > 8:
                    raise QuoridorError("position du mur non-valide!")
                self.murv += [mur]
        # vérifier que joueurs est itérable et de longueur 2
        if len(joueurs) != 2:
            raise QuoridorError("Il n'y a pas exactement 2 joueurs!")
        # itérer sur chaque joueur
        for numero, joueur in enumerate(joueurs):
            # Vérifier s'il s'agit d'un string ou d'un dictionnaire
            if isinstance(joueur, str):
                # ajouter le nom au dictionnaire
                self.joueurs[numero]['nom'] = joueur
                # ajouter 10 murs à placer au joueur
                self.joueurs[numero]['murs'] = 10
                # placer le joueur au bon endroit sur le jeu
                self.joueurs[numero]['pos'] = starting_position[numero]
            else:
                # vérifier que les murs sont legit
                if  0 < joueur['murs'] > 10:
                    raise QuoridorError("mauvais nombre de murs!")
                # Vérifier que la position du joueur est valide
                if 1 < joueur['pos'][0] > 9 and 1 < joueur['pos'][1] > 9:
                    raise QuoridorError("position du joueur invalide!")
                # updater la valeur de joueur
                self.joueurs[numero] = joueur
        # Vérifier que le total des murs donne 20
        if (len(self.murh) + len(self.murv) + self.joueurs[0]['murs'] + self.joueurs[1]['murs']) != 20:
            raise QuoridorError("mauvaise quantité totale de murs!")
        

    def __str__(self):
        """
        __str__
        Produit la représentation en art ascii correspondant à l'état actuel de la partie
        Returns:
            board (str)
        """
        # définition des contraintes du tableau de jeu
        # permet de modifier la taille du jeu si désiré
        board_positions = 9
        spacing_horizontal = ((board_positions * 4) - 1)
        # tableaux d'équivalences entre les adresses du jeu et notre tableau
        game_pos_x = range(1, (board_positions * 4), 4)
        game_pos_y = range(((board_positions - 1) * 2), -1, -2)
        # Création du tableau de jeu
        # en-tête
        légende = "légende: 1={} 2={}\n".format(self.joueurs[0]['nom'], self.joueurs[1]['nom'])
        légende += (' ' * 3) + ('-' * spacing_horizontal) + '\n'
        board = [légende]
        # game board
        for i in reversed(range((board_positions * 2) - 1)):
            if (i % 2) == 0:
                # check if more than 10 positions for better formatting
                board += ["{}{}|".format((((i + 1) // 2) + 1),
                                         (' ' * (1 - ((((i + 1) // 2) + 1) // 10))))]
                board += [' ', '.']
                board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
                board += [' ', '|\n']
            else:
                board += ["  |"]
                board += ([' '] * spacing_horizontal)
                board += ['|\n']
        # bottom lines
        board += "--|" + ('-' * spacing_horizontal) + '\n'
        board += (' ' * 2) + '| '
        for i in range(1, board_positions):
            board += str(i) + (' ')
            board += (' ' * (2 - (i // 10)))
        board += "{}\n".format(board_positions)
        # insertion des joueurs dans board
        for num, joueur in enumerate(self.joueurs):
            # obtention de la position en [x, y] du joueur
            position = joueur["pos"]
            # vérification que la position est dans les contraintes
            if ((0 > position[0] > board_positions) or
                    (0 > position[1] > board_positions)):
                raise IndexError("Adresse du joueur invalide!")
            # calcul du décallage relatif au tableau
            indice = (game_pos_x[(position[0] - 1)] +
                    (game_pos_y[(position[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # Insérer le personnage dans le tableau de jeu
            board[indice] = str(num + 1)
        # insertion des murs horizontaux dans board
        for murh in self.murh:
            # vérification que la position est dans les contraintes
            if ((1 > murh[0] > (board_positions - 1)) or
                    (2 > murh[1] > board_positions)):
                raise IndexError("Position du mur horizontal invalide!")
            indice = ((game_pos_x[(murh[0] - 1)] - 1) +
                    ((game_pos_y[(murh[1] - 1)] + 1) * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # itérer pour placer les 5 murs
            for i in range(7):
                board[(indice + i)] = '-'
        # insertion des murs verticaux
        for murv in self.murv:
            # vérification que la position est dans les contraintes
            if (2 > murv[0] > board_positions) or (1 > murv[1] > board_positions):
                raise IndexError("Position du mur vertical invalide!")
            indice = ((game_pos_x[(murv[0] - 1)] - 2) +
                    (game_pos_y[(murv[1] - 1)] * spacing_horizontal))
            decallage = ((((indice + 1) // spacing_horizontal) * 2) + 2)
            indice += decallage
            # itérer pour placer les 3 murs
            for i in range(3):
                board[(indice - (i * (spacing_horizontal + 2)))] = '|'
        # afficher le jeu sous forme d'une chaine de caractères
        return ''.join(board)


    def déplacer_jeton(self, joueur, position):
        #ÉNONCÉ : appelées par jouer_coup, mais ce n'est pas elles qui implantent la stratégie de jeu.

        """
        déplacer_jeton
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée
        """
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # Vérifier que la position du joueur est valide
        if not(1 <= position[0] <= 9 or 1 <= position[1] <= 9):
            raise QuoridorError("position invalide!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # vérifier si le mouvement est valide
        if not(position in list(graphe.successors(self.joueurs[(joueur - 1)]['pos']))):
            raise QuoridorError("mouvement invalide!")
        # Changer la position du joueur
        self.joueurs[(joueur - 1)]['pos'] = position


    def état_partie(self):
        """
        état_partie        
        Produit l'état actuel du jeu sous la forme d'un dictionnaire
        input: None
        Return:
            une copie de l'état actuel du jeu sous la forme d'un dictionnaire
            {
                'joueurs': [
                    {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                    {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                ]
                'Murs': {
                    'horizontaux': [...],
                    'verticaux': [...],
                }
            }
        """
        return {"joueurs": [self.joueurs],
                "murs":{
                        "horizontaux": self.murh,
                        "verticaux": self.murv
                        }}


    def jouer_coup(self, joueur):
        #ÉNONCÉ : Notez que votre méthode jouer_coup doit analyser l'état actuel du jeu afin de choisir automatiquement 
        # le prochain coup du joueur spécifié. À cette étape, vous pouvez vous contenter d'implanter une méthode qui joue 
        # sans intelligence, en respectant simplement les règles du jeu.

        #ÉNONCÉ : Pour connaître l'ensemble des déplacements admissibles d'un joueur, il suffit d'interroger le graphe orienté en lui 
        #         demandant de nous retourner les positions qui sont adjacentes à celle d'une certaine pastille. 
        #         La méthode pour ça se nomme successors. 

        #        Par exemple, pour connaître les déplacements possibles pour le joueur 1 situé en  (5,6) : (list(graphe.successors((5,6))))

        """
        jouer_coup        
        Pour le joueur spécifié, jouer automatiquement son meilleur
        coup pour l'état actuel de la partie. Ce coup est soit le déplacement de son jeton,
        soit le placement d'un mur horizontal ou vertical.
        Arguments:
            joueur {int} -- un entier spécifiant le numéro du joueur (1 ou 2)
        NOTE: version temporaire et stupide! à optimiser!
        """
        # objectifs
        objectifs = ['B1', 'B2']
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # Vérifier si la partie est déjà terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        coup_a_jouer = nx.shortest_path(graphe, self.joueurs[(joueur - 1)]['pos'], objectifs[(joueur - 1)])[1]
        # jouer le coup
        # TODO: compléter pour faire plus que juste bouger le jeton
        self.déplacer_jeton(joueur, coup_a_jouer)


    def partie_terminée(self):
        #ÉNONCÉ : Un joueur gagne la partie dès qu'il ateint la tuile qui précède immédiatement son objectif
        """
        partie_terminée        
        [extended_summary]
        """
        # definir les conditions de victoire
        condition_de_victoire = [9, 1]
        # itérer sur chaque joueurs
        for numero, joueur in enumerate(self.joueurs):
            # Vérifier si le joueur rempli les conditions de victoires
            if joueur['pos'][1] == condition_de_victoire[numero]:
                # Retourner le nom du joueur gagnant
                return joueur['nom']


    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        #ÉNONCÉ : appelées par jouer_coup, mais ce n'est pas elles qui implantent la stratégie de jeu.

        #ÉNONCÉ : Pour savoir si un état de jeu enferme un joueur (lorsqu'on ajoute un mur), il suffit d'interroger networkx en lui demandant
        #         s'il existe un chemin dans le graphe entre la position actuelle du joueur et son objectif. Pour ce faire, il s'agit 
        #         d'appeler la fonction has_path.
        #         Par exemple, pour le joueur 1 qui est en  (5,6)  et dont l'objectif est 'B1':  (nx.has_path(graphe, (5,6), 'B1'))

        """
        placer_mur        
        pour le joueur spécifié, placer un mur à la position spécifiée
        Arguments:
            joueur {int} -- Le numéro du joueur (1 ou 2)
            position {tuple} -- le tuple (x, y) de la position du mur
            orientation {str} -- l'orientation du mur: 'horizontal' ou 'vertical'
        """
        # définir les objectifs de chaque joueurs
        objectif = ['B1', 'B2']
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # Vérifier si le joueur ne peut plus placer de murs
        if self.joueurs[(joueur - 1)]['murs'] <= 0:
            raise QuoridorError("le joueur ne peut plus placer de murs!")
        # Si le mur est horizontal
        if orientation == 'horizontal':
            # vérifier si les positions sont dans les limites du jeu
            if 1 > position[0] > 8 or 2 > position[1] > 9:
                raise QuoridorError("position du mur invalide!")
            # vérifier si l'emplacement est déjà occupé
            if (position[0], position[1]) in self.murh:
                raise QuoridorError("Il y a déjà un mur!")
            # Prendre en compte le décalage des murs
            if ((position[0] + 1), position[1]) in self.murh:
                raise QuoridorError("Il y a déjà un mur!")
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                (self.murh + [position]),
                self.murv
            )
            # vérifier si placer ce mur enfermerais le joueur
            # TODO: itérer pour vérifier pour chaque joueurs
            if not(nx.has_path(graphe, (self.joueurs[(joueur - 1)]['pos']), objectif[(joueur - 1)])):
                raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murh += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1
        # Si c'est un mur vertical
        else:
            # vérifier si les positions sont dans les limites du jeu
            if 2 > position[0] > 9 or 1 > position[1] > 8:
                raise QuoridorError("position du mur invalide!")
            # vérifier si l'emplacement est déjà occupé
            if (position[0], position[1]) in self.murv:
                raise QuoridorError("Il y a déjà un mur!")
            # Prendre en compte le décalage des murs
            if (position[0], (position[1] + 1)) in self.murv:
                raise QuoridorError("Il y a déjà un mur!")
            # créer un graphe des mouvements possible à jouer avec le mur ajouté
            graphe = construire_graphe(
                [joueur['pos'] for joueur in self.joueurs],
                self.murh,
                (self.murv + [position])
            )
            # vérifier si placer ce mur enfermerais le joueur
            # TODO: itérer pour vérifier pour chaque joueurs
            if not(nx.has_path(graphe, (self.joueurs[(joueur - 1)]['pos']), objectif[(joueur - 1)])):
                raise QuoridorError("ce coup enfermerait un joueur")
            # placer le mur
            self.murv += [position]
            # retirer un mur des murs plaçables du joueurs
            self.joueurs[(joueur - 1)]['murs'] -= 1


#NOTE: J'ai changé le nom de la classe pour que celle-ci soit plus significative
#NOTE: les noms des fonctions doivent obligatoirement commencer par le mot "test" avec un t MINUSCULE
#NOTE: les fonctions de tests n'ont pas d'arguments autre que self car elles doivent contenir toutes les états de tests possible à l'intérieur d'elles
class TestQuoridor(unittest.TestCase):
    
    def test__init__(self):
        """test la fonction __init
        """
        # Dresser des tableaux connus pour des constructions connues
        nouveau_jeu = ("légende: 1=foo 2=bar\n" +
                        "   -----------------------------------\n" +
                        "9 | .   .   .   .   2   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "8 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "7 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "6 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "5 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "4 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "3 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "2 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "1 | .   .   .   .   1   .   .   .   . |\n" +
                        "--|-----------------------------------\n" +
                        "  | 1   2   3   4   5   6   7   8   9\n")
        partie_existante_tableau = ("légende: 1=foo 2=bar\n" +
                        "   -----------------------------------\n" +
                        "9 | .   .   .   .   .   .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "8 | .   .   .   .   .   . | .   .   . |\n" +
                        "  |        ------- -------|-------    |\n" +
                        "7 | .   .   .   .   2   . | .   .   . |\n" +
                        "  |                                   |\n" +
                        "6 | . | .   .   .   1   . | .   .   . |\n" +
                        "  |   |-------            |           |\n" +
                        "5 | . | .   . | .   .   . | .   .   . |\n" +
                        "  |           |                       |\n" +
                        "4 | .   .   . | .   .   .   .   .   . |\n" +
                        "  |            -------                |\n" +
                        "3 | .   .   .   .   . | .   .   .   . |\n" +
                        "  |                   |               |\n" +
                        "2 | .   .   .   .   . | .   .   .   . |\n" +
                        "  |                                   |\n" +
                        "1 | .   .   .   .   .   .   .   .   . |\n" +
                        "--|-----------------------------------\n" +
                        "  | 1   2   3   4   5   6   7   8   9\n")
        partie_existante_etat = {
                                    "joueurs": [
                                        {"nom": "foo", "murs": 7, "pos": [5, 6]},
                                        {"nom": "bar", "murs": 3, "pos": [5, 7]}
                                    ],
                                    "murs": {
                                        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
                                        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
                                    }
                                }
        # Test de création d'une partie nouvelle
        self.assertEqual(str(Quoridor(["foo", "bar"])), nouveau_jeu)
        # Test de création d'une partie déjà existante
        self.assertEqual(str(Quoridor(partie_existante_etat['joueurs'],
                                      partie_existante_etat['murs'])),
                                      partie_existante_tableau)
        # TODO: ajouter des tests qui doivent soulever des erreurs et vérifier qu'ils soulèvent bel et bien ces erreurs
        # NOTE: Il faut tester tous les cas de figures qu'on peut imaginer. Toutes les exceptions qu'on s'attends à voir être levés doivent être testées

    #def test__str__(self):
    
    def test_déplacer_jeton(self):

        etatdepartie = {
                        "joueurs": [
                            {"nom": "1", "murs": 0, "pos": [5, 2]},
                         ],
                        "murs": {
                             "horizontaux": [],
                            "verticaux": []
                         }
                     }
        jeu = Quoridor(etatdepartie)
        self.assertRaisesRegex(QuoridorError, "joueur invalide!", jeu.déplacer_jeton, 5, (5, 2))
        self.assertRaisesRegex(QuoridorError, "position invalide!", jeu.déplacer_jeton, 1, (10, 10))
        #NOTE: n'oubliez pas de tester TOUTEs les situations possibles. Il faut bien entendu tester celles où la fonction fonctionne bien.
    
    #def test_état_partie(self):
        #self.assertEqual(Quoridor(partie_existante_etat)),partie_existante_tableau)
 
    def test_jouer_coup(self):
        
        etatdepartie2 = {
                        "joueurs": [
                            {"nom": "1", "murs": 0, "pos": [9, 1]},
                         ],
                        "murs": {
                             "horizontaux": [],
                            "verticaux": []
                         }
                     }
        jeu2 = Quoridor(etatdepartie2)
        self.assertRaisesRegex(QuoridorError, "joueur invalide!", Quoridor(jouer_coup(5)))
        self.assertRaisesRegex(QuoridorError, " La partie est déjà terminée!", jeu2.état_partie())        

    def test_partie_terminée(self):
        self.assertEqual(Quoridor(déplacer_jeton(1, (9,1)), 1)
""" 
    def test_placer_mur(self):
        etatdepartie3 = {
                        "joueurs": [
                            {"nom": "1", "murs": 1, "pos": []},
                         ],
                       "murs": {
                             "horizontaux": [],
                            "verticaux": [5, 2]
                         }
                     }

        self.assertEqual(Quoridor(placer_mur(1, (5,2), "vertical")), etatdepartie3)
"""
#Lancer la batterie de tests unitaires l'orsque ce module est lancé en tant que main (pas importé)
if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)