# Projet de Python - ISF apprentissage - Automate cellulaire 
## Lou Lacroix et Emma Le Priol

### Entrée 
Ce programme permet de simuler un automate cellulaire probabiliste, permettant de simuler différents phénomènes. 

En entrée, il demande à l'utilisateur de définir : 
- les états souhaités (nombre, couleur et proportion initiale dans la grille de chacun)
- les transitions souhaitées (à partir d'une paire de cellule, on en définit une nouvelle, il n'y a qu'une transition à chaque étape)
- la probabilité d'occurence de chacune des transitions définies 
- la taille de la grille 
- le nombre d'itération 

### Sortie
Le résultat est sous forme de gif et s'enregistre quand on exécute la fonction *game()*.

### Axes d'amélioration
Ayant conscience que notre projet est améliorable, voici les axes principaux d'amélioration auxquels nous avons pensé, et que nous pourrions mettre en place dans un second temps :  
- quand une transition n'est plus possible, mettre sa probabilité à 0
- simuler une nouvelle grille si aucune transition n'est possible dès le début 
- quand plus aucune transition n'est possible, stopper le programme et afficher un message
