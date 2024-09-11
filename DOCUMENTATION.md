# Documentation du Projet Game Jam 2024 

## Sommaire

- [Configuration et lancement du projet](#configuration-et-lancement-du-projet)
- [Classes principales](#classes-principales)
- [Fichier principal](#fichier-principal-srcmainpy)
- [Structure du projet](#structure-du-projet)
- [Attribution des tâches](#attribution-des-tâches)


## Configuration et lancement du projet

1. Créer un environnement virtuel :
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Installer les dépendances :
   ```sh
   pip install -r requirements.txt
   ```

3. Lancer le jeu :
   ```sh
   python src/main.py
   ```


## Classes principales

### Player (`src/classes/player.py`)

La classe `Player` représente le joueur dans le jeu.

Principales méthodes :
- `load_frames(file_path: str)` : Charge les images d'animation à partir d'un fichier.
- `update()` : Met à jour l'image actuelle de l'animation.
- `change_animation(direction: str, is_moving: bool)` : Change l'animation en fonction de la direction et de l'état de mouvement.
- `player_movement(keys: ScanCodeWrapper, delta: float)` : Gère le mouvement du joueur en fonction des touches pressées.

### Prop (`src/classes/prop.py`)

La classe `Prop` représente un objet interactif dans le jeu.

Principales méthodes :
- `draw(screen: Surface, camera: Camera)` : Dessine l'objet sur l'écran.
- `draw_text(screen: Surface)` : Affiche le texte d'interaction.
- `check_collision(player_rect: Rect)` : Vérifie la collision avec le joueur.
- `interact_with(screen: Surface)` : Exécute l'interaction spécifique à l'objet.

### TileMap (`src/classes/tilemap.py`)

La classe `TileMap` gère la carte du jeu composée de tuiles.

Principales méthodes :
- `draw(screen: Surface, camera: Camera)` : Dessine la carte sur l'écran.
- `collides_with_walls(rect: Rect)` : Vérifie les collisions avec les murs.

### Raycast (`src/classes/raycast.py`)

La classe `Raycast` gère la détection de collision par lancer de rayons.

Principales méthodes :
- `update(new_start_pos: Vector2, new_direction: float, camera: Camera)` : Met à jour la position et la direction du rayon.
- `draw(screen: Surface)` : Dessine le rayon sur l'écran.

### Timer (`src/classes/timer.py`)

La classe `Timer` gère le compte à rebours dans le jeu.

Principales méthodes :
- `update()` : Met à jour le temps restant.
- `is_time_up()` : Vérifie si le temps est écoulé.
- `draw(screen: Surface, font: Font)` : Affiche le temps restant sur l'écran.

### Camera (`src/classes/camera.py`)

La classe `Camera` gère la vue du jeu et suit le joueur.

Principales méthodes :
- `apply(target: Union[Rect, tuple, Vector2])` : Applique la transformation de la caméra à un objet.
- `update()` : Met à jour la position de la caméra en fonction du joueur.

### ModalMenu (`src/classes/modal_menu.py`)

La classe `ModalMenu` gère l'affichage des menus modaux dans le jeu.

Principales méthodes :
- `draw()` : Dessine le menu modal sur l'écran.
- `handle_event(event: Event)` : Gère les événements liés au menu modal.

## Fichier principal (`src/main.py`)

Le fichier `main.py` contient la boucle principale du jeu et initialise les différentes classes.

## Structure du projet

