import pygame
import json
from datetime import datetime

class Lobby(object):

    def __init__(self):
        self.players = []

    # Pour le lobby mais aussi éventuellement dans le jeu...
    def get_players_name(self):
        players = []
        for player in self.players:
            players.append([player.nickname])
        return players

    # Pour le jeu
    def get_players(self):
        return self.players

    def add(self, player):
        self.players.append(player)

    def remove(self, player):
        if player in self.players:
            self.players.remove(player)

    def count(self):
        return len(self.players)  # Si 2, c'est bon

    # Eventuellement une fonction qui envoie un message quand le jeu se lance
    # ou affiche une barre de chargement pendant l'attente dans le lobby
