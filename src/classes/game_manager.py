import pygame
from network import Network

class GameManager:
    def __init__(self):
        self.network = Network()
        self.player_id = self.network.connect()
        self.game_state = {}
        self.valve_activated = False
        self.props = []
        self.potentiometer_values = {}

    def update(self):
        data = self.network.send("get")
        if data is None:
            print("Aucune donnée reçue du serveur")
            return
        
        if isinstance(data, dict) and "action" in data:
            self.handle_server_action(data)
        else:
            self.game_state = data

        # Appliquer les effets de la valve si elle est activée
        if self.valve_activated:
            for prop in self.props:
                if prop.type == "valve":
                    prop.apply_valve_effect(self)
            self.valve_activated = False  # Réinitialiser après application

        # La mise à jour des potentiomètres a été supprimée d'ici

    def send_prop_interaction(self, prop_id, action, value=None):
        data = {"action": "prop_interaction", "prop_id": prop_id, "specific_action": action}
        if value is not None:
            data["value"] = value
        self.network.send(data)

    def handle_server_action(self, action):
        if action["action"] == "prop_interaction":
            prop_id = action["prop_id"]
            specific_action = action["specific_action"]
            self.game_state[prop_id] = specific_action
            
            if specific_action == "valve_activated":
                self.valve_activated = True
                print(f"Valve {prop_id} a été activée sur tous les clients!")
            elif specific_action == "potentiometer_updated":
                self.potentiometer_values[prop_id] = action["value"]
                print(f"Potentiomètre {prop_id} mis à jour avec la valeur {action['value']}")

    def add_prop(self, prop):
        self.props.append(prop)

    def get_potentiometer_value(self, prop_id):
        return self.potentiometer_values.get(prop_id, 0)

