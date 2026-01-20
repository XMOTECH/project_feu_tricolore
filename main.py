import turtle
import time
from turtle_scene import SceneBuilder
from intersection_controller import IntersectionController
from vehicles import VehicleManager
from gui import InterfaceManager
from scenarios import NormalScenario, RushHourScenario, NightScenario, ManualScenario
from logger import Logger

class SimulationController:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Simulation Carrefour - Projet L3 (Version Améliorée)")
        self.screen.setup(width=900, height=700)
        self.screen.tracer(0)

        # Construction de la scène
        self.scene = SceneBuilder()
        self.scene.draw_background()
        self.scene.draw_roads()
        self.scene.draw_decorations()
        
        # Interface utilisateur
        self.gui = InterfaceManager()
        self.gui.draw_controls()
        
        # Contrôleur d'intersection (4 feux synchronisés)
        self.intersection = IntersectionController()
        
        # Gestionnaire de véhicules (avec référence à l'écran pour les images)
        self.veh_manager = VehicleManager(self.screen)
        
        # Logger
        self.logger = Logger()
        
        # État de la simulation
        self.is_running = True
        self.is_paused = False

        # Scénarios disponibles
        self.scenarios = {
            "SCENARIO_1": NormalScenario(),
            "SCENARIO_2": RushHourScenario(),
            "SCENARIO_3": NightScenario(),
            "SCENARIO_4": ManualScenario()
        }
        self.current_scenario = self.scenarios["SCENARIO_1"]
        
        # HUD pour affichage informations
        self.hud = turtle.Turtle()
        self.hud.hideturtle()
        self.hud.penup()
        self.hud.color("white")
        
        # Log du démarrage
        self.logger.log_event("SYSTEM", "Démarrage Application (Mode Amélioré)", 
                              self.intersection, self.current_scenario.name)

        self.screen.onclick(self.handle_mouse_click)

    def handle_mouse_click(self, x, y):
        action = self.gui.handle_click(x, y)
        
        if not action: 
            return

        # Log de l'interaction utilisateur
        self.logger.log_event("USER_INPUT", f"Clic sur {action}", 
                              self.intersection, self.current_scenario.name)

        if action == "PAUSE":
            self.is_paused = True
        elif action == "PLAY":
            self.is_paused = False
        elif action == "STOP":
            self.is_running = False
            self.logger.log_event("SYSTEM", "Arrêt Application", 
                                  self.intersection, self.current_scenario.name)
        elif action == "RESET":
            self._reset_simulation()

        elif action in self.scenarios:
            self.current_scenario = self.scenarios[action]
            self.logger.log_event("SCENARIO", f"Changement vers {self.current_scenario.name}", 
                                  self.intersection, self.current_scenario.name)

        elif action == "MANUAL_CLICK":
            if isinstance(self.current_scenario, ManualScenario):
                self.intersection.manual_change()
                self.logger.log_event("TRAFFIC_LIGHT", 
                                      f"Changement Manuel vers {self.intersection.current_phase}", 
                                      self.intersection, self.current_scenario.name)

    def _reset_simulation(self):
        """Réinitialise la simulation."""
        # Supprimer tous les véhicules
        for v in self.veh_manager.vehicles:
            v.shape.hideturtle()
        self.veh_manager.vehicles.clear()
        self.veh_manager.next_id = 1
        
        # Réinitialiser l'intersection
        self.intersection.phase_index = 0
        self.intersection.current_phase = "A"
        self.intersection.timer = 0
        self.intersection._apply_phase()
        
        self.is_paused = True
        self.logger.log_event("SYSTEM", "Réinitialisation", 
                              self.intersection, self.current_scenario.name)

    def update_hud(self):
        """Affiche les données télémétriques de la console opérateur."""
        self.hud.clear()
        
        # En-tête Console
        self.hud.color("#00e5ff")
        self.hud.goto(250, 315)
        self.hud.write("□ TELEMETRY_DASHBOARD", font=("Consolas", 11, "bold"))
        
        # Données Système
        self.hud.color("#cfd8dc")
        y_pos = 280
        data = [
            f"ID_SCNR  :: {self.current_scenario.name}",
            f"ID_PHASE :: {self.intersection.current_phase}",
            f"ID_VTF   :: {self.veh_manager.get_vehicle_count():02d} UNITS"
        ]
        
        for line in data:
            self.hud.goto(250, y_pos)
            self.hud.write(line, font=("Consolas", 10, "normal"))
            y_pos -= 20
            
        # État Système
        status_text = ">> STATUS: PAUSED" if self.is_paused else ">> STATUS: OPERATIONAL"
        status_color = "#ffab00" if self.is_paused else "#00e676"
        
        self.hud.color(status_color)
        self.hud.goto(250, y_pos)
        self.hud.write(status_text, font=("Consolas", 10, "bold"))

    def run(self):
        previous_phase = self.intersection.current_phase

        while self.is_running:
            if not self.is_paused:
                # Mise à jour de l'intersection
                self.intersection.update(self.current_scenario)
                
                # Mise à jour des véhicules
                self.veh_manager.update_vehicles(self.intersection)

                # Détection changement de phase
                if self.intersection.current_phase != previous_phase:
                    self.logger.log_event("TRAFFIC_LIGHT", 
                                          f"Phase passée à {self.intersection.current_phase}", 
                                          self.intersection, self.current_scenario.name)
                    previous_phase = self.intersection.current_phase
            
            # Mise à jour HUD
            self.update_hud()
            
            self.screen.update()
            time.sleep(0.02)

if __name__ == "__main__":
    app = SimulationController()
    app.run()