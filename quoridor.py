""" Quoridor.py
Module qui enferme les classes d'encapsulation
de la structure du jeu
contient les classes:
    - Quoridor
    - QuoridorError(Exception)
"""

import networkx as nx


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
    print("quoridorerror")


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
        """
        # définir les attribut de classes que nous allons utiliser
        self.joueurs = []
        self.murh = []
        self.murv = []
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
                self.murh += mur
            # itérer sur chaque mur vertical
            for mur in murs['verticaux']:
                if 2 < mur[0] > 9 and 1 < mur[1] > 8:
                    raise QuoridorError("position du mur non-valide!")
                self.murv += mur
        # Vérifier que le total des murs donne 20
        if (len(self.murh) + len(self.murv) + joueurs[0]['murs'] + joueurs[1]['murs']) != 20:
            raise QuoridorError("mauvaise quantité totale de murs!")
        # vérifier que joueurs est itérable et de longueur 2
        if len(joueurs) != 2:
            raise QuoridorError("Il n'y a pas exactement 2 joueurs!")
        # itérer sur chaque joueur
        for numero, joueur in enumerate(joueurs):
            # Vérifier s'il s'agit d'un string
            # Si le joueur est un string
            if isinstance(joueur, str):
                # créer un dictionnaire vide
                nouveaujoueur = {}
                # ajouter le nom au dictionnaire
                nouveaujoueur['nom'] = joueur
                # ajouter 10 murs à placer au joueur
                nouveaujoueur['murs'] = 10
                # placer le joueur au bon endroit sur le jeu
                if numero == 0:
                    nouveaujoueur['pos'] = (5, 1)
                else:
                    nouveaujoueur['pos'] = (5, 9)
                # créer le joueur dans l'objet de classe
                self.joueurs[numero] = nouveaujoueur #TODO: remplacer nouveaujoueur par juste self.player
            # Si le joueur fourni est un dictionnaire
            else:
                # vérifier que les murs sont legit
                if  0 < joueur['murs'] > 10:
                    raise QuoridorError("mauvais nombre de murs!")
                # Vérifier que la position du joueur est valide
                if 1 < joueur['pos'] > 9:
                    raise QuoridorError("position du joueur invalide!")
                # updater la valeur de joueur
                self.joueurs[numero] = joueur
        

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
        # place holder où ajouter tous les joueurs (pour permettre plus de 2 joueurs)
        légende = "légende: "
        board = [légende]
        # game board
        for i in reversed(range((board_positions * 2) - 1)):
            if (i % 2) == 0:
                # check if more than 10 positions for better formatting
                if (((i + 1) // 2) + 1) < 10:
                    board += ["{} |".format(((i + 1) // 2) + 1)]
                else:
                    board += ["{}|".format(((i + 1) // 2) + 1)]
                    board += [' ', '.']
                    board += ([' ', ' ', ' ', '.'] * (board_positions - 1))
                    board += [' ', '|\n']
            else:
                board += ["  |"]
                board += ([' '] * spacing_horizontal)
                board += ['|\n']
        # bottom board line
        board += "--|" + ('-' * spacing_horizontal) + '\n'
        # bottom number line
        board += (' ' * 2) + '| '
        for i in range(1, board_positions):
            board += str(i) + (' ' * 3)
        board += "{}\n".format(board_positions)
        # insertion des joueurs dans board
        for num, joueur in enumerate(self.joueurs):
            # ajout du joueur à la légende du tableau
            légende += "{}={} ".format((num + 1), joueur['nom'])
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
        # complétion de la légende du tableau
        board[0] = légende + '\n' + (' ' * 3) + ('-' * spacing_horizontal) + '\n'
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
        """
        déplacer_jeton
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée
        """
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # Vérifier que la position du joueur est valide
        if 1 < position[0] > 9 or 1 < position[1] > 9:
            raise QuoridorError("position invalide!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # vérifier si le mouvement est valide
        if not(position in list(graphe.successors(self.joueurs[(joueur - 1)]))):
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
        """
        jouer_coup        
        Pour le joueur spécifié, jouer automatiquement son meilleur
        coup pour l'état actuel de la partie. Ce coup est soir le déplacement de son jeton,
        soit le placement d'un mur horizontal ou vertical.
        Arguments:
            joueur {int} -- un entier spécifiant le numéro du joueur (1 ou 2)
        NOTE: version temporaire et stupide! à optimiser!
        """
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # vérifier si la partie est déjà terminée
        # TODO: compléter
        coup_a_jouer = nx.shortest_path(graphe, self.joueurs[(joueur - 1)]['pos'], 'B1')[0]
        # jouer le coup
        # TODO: compléter


    def partie_terminée(self):
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
        """
        placer_mur        
        pour le joueur spécifié, placer un mur à la position spécifiée
        Arguments:
            joueur {int} -- Le numéro du joueur (1 ou 2)
            position {tuple} -- le tuple (x, y) de la position du mur
            orientation {str} -- l'orientation du mur: 'horizontal' ou 'vertical'
        """
        # Vérifier que le joueur est valide
        if joueur != 1 and joueur != 2:
            raise QuoridorError("joueur invalide!")
        # Vérifier si le joueur ne peut plus placer de murs
        if self.joueurs[(joueur - 1)]['murs'] <= 0:
            raise QuoridorError("le joueur ne peut plus placer de murs!")
        # créer un graphe des mouvements possible à jouer
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murh,
            self.murv
        )
        # Si le mur est horizontal
        if orientation == 'horizontal':
            # vérifier si les positions sont dans les limites du jeu
            if 1 > position[0] >8 or 2 > position[1] > 9:
                raise QuoridorError("position du mur invalide!")
            # vérifier si l'emplacement est déjà occupé