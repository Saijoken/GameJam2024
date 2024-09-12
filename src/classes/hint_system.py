from typing import Dict, List

class HintSystem:
    def __init__(self):
        self.hints: Dict[str, Dict[str, List[str]]] = {
            "past": {},
            "future": {}
        }
        self.current_hints: Dict[str, Dict[str, int]] = {
            "past": {},
            "future": {}
        }

    def add_hint(self, temporality: str, puzzle_id: str, hint: str):
        if puzzle_id not in self.hints[temporality]:
            self.hints[temporality][puzzle_id] = []
            self.current_hints[temporality][puzzle_id] = 0
        self.hints[temporality][puzzle_id].append(hint)

    def get_current_hint(self, temporality: str, puzzle_id: str) -> str:
        if puzzle_id in self.hints[temporality]:
            hint_index = self.current_hints[temporality][puzzle_id]
            return self.hints[temporality][puzzle_id][hint_index]
        return "Aucun indice disponible pour cette énigme."

    def next_hint(self, temporality: str, puzzle_id: str) -> bool:
        if puzzle_id in self.current_hints[temporality]:
            max_hints = len(self.hints[temporality][puzzle_id])
            if self.current_hints[temporality][puzzle_id] < max_hints - 1:
                self.current_hints[temporality][puzzle_id] += 1
                return True
        return False

    def reset_hints(self, temporality: str, puzzle_id: str):
        if puzzle_id in self.current_hints[temporality]:
            self.current_hints[temporality][puzzle_id] = 0

hint_system = HintSystem()

# Initialisation du système d'indices
hint_system.add_hint("past", "valve_puzzle", "Cherchez une valve près de l'entrée.")
hint_system.add_hint("past", "valve_puzzle", "La valve est de couleur rouge.")
hint_system.add_hint("past", "nuit", "La nuit est tombée.")
hint_system.add_hint("future", "symbol_lock", "Les symboles sont liés aux constellations.")

# Dans le code du jeu:
def display_hint(player):
    hint = hint_system.get_current_hint(player.temporality, "current_puzzle_id")
    # Afficher l'indice avec ModalMenu ou une autre méthode

def advance_hint(player):
    if hint_system.next_hint(player.temporality, "current_puzzle_id"):
        display_hint(player)
    else:
        print("Pas d'autre indice disponible.")