# Game Jam 2024

## Somaire : 

<ul>

<li><a href="#arborescence">Arborescence</a></li>
<li><a href="#classes">Classes</a></li>

</ul>

## Comment setup mon jeu sous python

### Arborescence

```
.
├── assets
├── networking
├── docs
├── README.md
├── requirements.txt
└── src
...
    ├── classes
    └── main.py
    ...
```

### Environnement virtuel

```sh
# Creation du dossier d'env virtuel
python3 -m venv .venv
# Activation de l'environnement
source .venv/bin/activate
```

### Installation des dépendances du projet

```sh
pip install -r requirements.txt 
```
## Attribution des tâches

Nacer Berkane : Lead Project

Mohammed Ben Aicha : Lead Developer

Axelle Broyer : Networking

Marie Dos Santos : Developer

Angel Gioanni : Graphic Designer, Developer



# Classes

`src/main.py`


## Player

<a href="./src/classes/player.py">`src/classes/player.py`</a>

Déclaration d'un joueur avec le Screen (Surface) en paramètre.

Déclaration des animations, animation actuelle, position et dernière direction enregistrée.


<br>

Charge les frames d'une animation à partir d'un fichier.

```python
load_frames(file_path : str)
```
<br>


Update la frame actuelle de l'animation.


```python
update()
```

<br>
Change l'animation en fonction de la direction et du statut de déplacement du joueur.

```python
change_animation(direction : str, is_moving : bool)
```

<br>

Execute le movement en fonction des inputs du joueurs, les mouvements diagonaux du joueurs sont normalisés afin d'éviter les usebugs de vitesse.

_Rq : Un ScanCodeWrapper est un style de tableau/buffer contenant les différentes préssées._

```python
player_movement(keys : ScanCodeWrapper, delta : float)
```

## Camera 
`src/classes/camera.py`

Jsp sah


## Prop
`src/classes/prop.py`

Déclaration d'un Prop avec son ID, nom ainsi que hitbox

```python
Prop(id : str, name : str, rect : Rect )
```
<br>
Affichage du texte indiquant au joueur d'intéragir avec l'objet.

```python
draw_text(screen : Surface)
```
<br>
Check la collision entre le joueur et l'objet.

Retourne :
- Prop si collision avec joueur 
- None sinon

```python
draw_text(player_rect : Rect)
```

<br>
        Fonction attachée a un objet executant l'intéraction voulue.

```python
interact_with()
```