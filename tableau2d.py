"""
Module : tableau2d.py
Description : Module de tri et de recherche dans un tableau à deux dimensions.
              Les algorithmes travaillent sur une version aplatie du tableau 2D,
              puis reconstituent la structure 2D après traitement.
Utilisation  : import tableau2d
"""

import random


# ============================================================
#  UTILITAIRES
# ============================================================

def generer_tableau(lignes=3, colonnes=4, min_val=0, max_val=99):
    """
    Génère un tableau 2D rempli de valeurs entières aléatoires.
    Exemple de résultat :
        [[42, 7, 18, 55],
         [3,  91, 26, 14],
         [60, 33, 8,  77]]
    """
    return [[random.randint(min_val, max_val) for _ in range(colonnes)]
            for _ in range(lignes)]


def aplatir(tableau):
    """
    Transforme un tableau 2D en liste 1D.
    [[1, 2], [3, 4]] → [1, 2, 3, 4]
    Nécessaire pour appliquer les algorithmes de tri classiques.
    """
    return [element for ligne in tableau for element in ligne]


def reconstruire(liste_1d, nb_colonnes):
    """
    Reconstruit un tableau 2D à partir d'une liste 1D et d'un nombre de colonnes.
    [1, 2, 3, 4], nb_colonnes=2 → [[1, 2], [3, 4]]
    """
    return [liste_1d[i:i + nb_colonnes] for i in range(0, len(liste_1d), nb_colonnes)]


def afficher(tableau, titre="Tableau"):
    """Affiche le tableau 2D de façon lisible dans la console."""
    print(f"\n=== {titre} ===")
    for ligne in tableau:
        print(ligne)


# ============================================================
#  ALGORITHMES DE TRI
# ============================================================

def tri_bulle(tableau):
    """
    TRI À BULLE (Bubble Sort)
    ─────────────────────────
    Principe : On parcourt la liste plusieurs fois.
    À chaque passage, on compare chaque élément avec son voisin de droite.
    Si l'élément gauche est plus grand, on les échange (ils "remontent" comme
    des bulles). On répète jusqu'à ce qu'aucun échange ne soit nécessaire.

    Complexité : O(n²) dans le pire cas.
    """
    nb_colonnes = len(tableau[0])
    # Étape 1 : aplatir le tableau 2D en liste 1D
    liste = aplatir(tableau)
    n = len(liste)

    for i in range(n):
        # À chaque passage i, le plus grand élément "remonte" à la fin
        # On peut donc ignorer les derniers i éléments déjà triés
        for j in range(0, n - i - 1):
            # Comparaison de deux voisins
            if liste[j] > liste[j + 1]:
                # Échange si le gauche est plus grand que le droit
                liste[j], liste[j + 1] = liste[j + 1], liste[j]

    # Étape finale : reconstruire le tableau 2D avec la liste triée
    return reconstruire(liste, nb_colonnes)


def tri_rapide(tableau):
    """
    TRI RAPIDE (Quick Sort)
    ────────────────────────
    Principe : On choisit un élément "pivot" (ici le dernier de la liste).
    On divise la liste en deux parties :
      - Les éléments plus petits que le pivot (à gauche)
      - Les éléments plus grands que le pivot (à droite)
    On trie récursivement chaque partie, puis on les réassemble.

    Complexité : O(n log n) en moyenne, O(n²) dans le pire cas.
    """
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau)

    def quicksort(lst):
        # Cas de base : une liste vide ou d'un seul élément est déjà triée
        if len(lst) <= 1:
            return lst

        # On choisit le dernier élément comme pivot
        pivot = lst[-1]

        # Partition : tous les éléments < pivot vont à gauche
        gauche = [x for x in lst[:-1] if x <= pivot]
        # Tous les éléments >= pivot vont à droite
        droite = [x for x in lst[:-1] if x > pivot]

        # Appel récursif sur chaque partition, puis assemblage
        return quicksort(gauche) + [pivot] + quicksort(droite)

    return reconstruire(quicksort(liste), nb_colonnes)


def tri_selection(tableau):
    """
    TRI PAR SÉLECTION (Selection Sort)
    ────────────────────────────────────
    Principe : On divise la liste en deux zones : triée (à gauche) et non triée (à droite).
    À chaque étape, on cherche le MINIMUM de la zone non triée,
    et on le place à la fin de la zone triée (en l'échangeant avec le 1er élément non trié).

    Complexité : O(n²) toujours (même si la liste est déjà triée).
    """
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau)
    n = len(liste)

    for i in range(n):
        # On suppose que le premier élément non trié est le minimum
        idx_min = i

        # On cherche le vrai minimum dans le reste de la liste
        for j in range(i + 1, n):
            if liste[j] < liste[idx_min]:
                idx_min = j  # On a trouvé un nouveau minimum

        # On échange le minimum trouvé avec le premier élément non trié
        liste[i], liste[idx_min] = liste[idx_min], liste[i]

    return reconstruire(liste, nb_colonnes)


def tri_insertion(tableau):
    """
    TRI PAR INSERTION (Insertion Sort)
    ────────────────────────────────────
    Principe : Comme quand on trie des cartes dans sa main.
    On prend chaque élément un par un et on l'insère à la bonne
    position dans la partie gauche déjà triée, en décalant les
    éléments plus grands vers la droite.

    Complexité : O(n²) dans le pire cas, O(n) si déjà trié.
    """
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau)
    n = len(liste)

    # On commence au 2e élément (le 1er est considéré comme déjà "trié")
    for i in range(1, n):
        # On mémorise l'élément courant à insérer
        cle = liste[i]
        j = i - 1

        # On décale vers la droite tous les éléments plus grands que la clé
        while j >= 0 and liste[j] > cle:
            liste[j + 1] = liste[j]
            j -= 1

        # On insère la clé à sa position correcte
        liste[j + 1] = cle

    return reconstruire(liste, nb_colonnes)


def tri_fusion(tableau):
    """
    TRI PAR FUSION (Merge Sort)
    ────────────────────────────
    Principe : Diviser pour régner.
    On coupe la liste en deux moitiés, on trie chaque moitié
    récursivement, puis on fusionne les deux moitiés triées
    en une seule liste triée.

    Complexité : O(n log n) toujours (même dans le pire cas).
    """
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau)

    def fusionner(gauche, droite):
        """Fusionne deux listes triées en une seule liste triée."""
        resultat = []
        i = j = 0

        # On compare les éléments des deux listes un par un
        while i < len(gauche) and j < len(droite):
            if gauche[i] <= droite[j]:
                resultat.append(gauche[i])
                i += 1
            else:
                resultat.append(droite[j])
                j += 1

        # On ajoute les éléments restants (l'une des listes est épuisée)
        resultat.extend(gauche[i:])
        resultat.extend(droite[j:])
        return resultat

    def merge_sort(lst):
        # Cas de base : liste vide ou un seul élément → déjà triée
        if len(lst) <= 1:
            return lst

        # On coupe la liste en deux au milieu
        milieu = len(lst) // 2
        gauche = merge_sort(lst[:milieu])   # Tri récursif gauche
        droite = merge_sort(lst[milieu:])   # Tri récursif droite

        # Fusion des deux moitiés triées
        return fusionner(gauche, droite)

    return reconstruire(merge_sort(liste), nb_colonnes)


# ============================================================
#  ALGORITHMES DE RECHERCHE
# ============================================================

def recherche_lineaire(tableau, cible):
    """
    RECHERCHE LINÉAIRE (Linear Search)
    ─────────────────────────────────────
    Principe : On parcourt le tableau élément par élément, de gauche
    à droite (et ligne par ligne), jusqu'à trouver la cible.
    Ne nécessite PAS un tableau trié.

    Retourne : (ligne, colonne) si trouvé, sinon (-1, -1)
    Complexité : O(n) — on peut être obligé de tout parcourir.
    """
    for i, ligne in enumerate(tableau):
        for j, element in enumerate(ligne):
            # Dès qu'on trouve la cible, on retourne sa position
            if element == cible:
                return (i, j)  # Trouvé à la ligne i, colonne j

    # Si on a parcouru tout le tableau sans trouver
    return (-1, -1)


def recherche_binaire(tableau, cible):
    """
    RECHERCHE BINAIRE (Binary Search)
    ───────────────────────────────────
    Principe : On aplatit le tableau 2D en liste 1D triée.
    On maintient deux bornes (gauche et droite) et on regarde
    l'élément du MILIEU :
      - Si milieu == cible → trouvé !
      - Si milieu < cible  → on cherche dans la moitié droite
      - Si milieu > cible  → on cherche dans la moitié gauche
    On répète jusqu'à trouver ou jusqu'à ce que les bornes se croisent.

    ⚠️  NÉCESSITE un tableau trié (on utilise tri_fusion avant).
    Retourne : (ligne, colonne) de la position dans le tableau original.
    Complexité : O(log n) — beaucoup plus rapide que la recherche linéaire.
    """
    # On trie d'abord le tableau (requis pour la recherche binaire)
    tableau_trie = tri_fusion(tableau)
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau_trie)

    gauche = 0
    droite = len(liste) - 1

    while gauche <= droite:
        milieu = (gauche + droite) // 2  # Indice du milieu

        if liste[milieu] == cible:
            # Trouvé ! On reconvertit l'indice 1D en position 2D
            ligne = milieu // nb_colonnes
            colonne = milieu % nb_colonnes
            return (ligne, colonne)
        elif liste[milieu] < cible:
            # La cible est dans la moitié droite
            gauche = milieu + 1
        else:
            # La cible est dans la moitié gauche
            droite = milieu - 1

    return (-1, -1)  # Élément non trouvé


def recherche_dichotomie(tableau, cible):
    """
    RECHERCHE PAR DICHOTOMIE (Dichotomy Search)
    ─────────────────────────────────────────────
    Principe : Même idée que la recherche binaire mais avec une approche
    récursive. On "coupe" la liste en deux à chaque appel récursif et on
    cherche dans la bonne moitié.

    La différence avec recherche_binaire : ici on utilise la récursion
    au lieu d'une boucle while.

    ⚠️  NÉCESSITE un tableau trié.
    Retourne : l'indice dans la liste 1D, ou -1 si non trouvé.
    Complexité : O(log n).
    """
    tableau_trie = tri_fusion(tableau)
    nb_colonnes = len(tableau[0])
    liste = aplatir(tableau_trie)

    def dichotomie(lst, cible, gauche, droite):
        # Cas de base : les bornes se sont croisées → élément absent
        if gauche > droite:
            return -1

        milieu = (gauche + droite) // 2

        if lst[milieu] == cible:
            return milieu  # On retourne l'indice 1D
        elif lst[milieu] < cible:
            # Appel récursif sur la moitié droite
            return dichotomie(lst, cible, milieu + 1, droite)
        else:
            # Appel récursif sur la moitié gauche
            return dichotomie(lst, cible, gauche, milieu - 1)

    indice = dichotomie(liste, cible, 0, len(liste) - 1)

    if indice == -1:
        return (-1, -1)

    # Conversion de l'indice 1D en coordonnées 2D
    ligne = indice // nb_colonnes
    colonne = indice % nb_colonnes
    return (ligne, colonne)
