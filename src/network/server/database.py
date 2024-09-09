import sqlite3
import json

class Database:
    def __init__(self):
        self.connection = None
        self.create()

    def create(self):
        self.connection = sqlite3.connect("game.db")