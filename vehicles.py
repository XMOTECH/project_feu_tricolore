import turtle
import random
import os

# Chemin vers les assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Images de voitures disponibles
CAR_IMAGES = ["car_red.gif", "car_blue.gif", "car_green.gif", "car_yellow.gif"]

# Directions possibles (Nomenclature : Direction du flux)
DIRECTIONS = {
    "EST": {"spawn_x": -600, "spawn_y": -35, "heading": 0, "target_x": 600},   # Va vers l'Est (+X), voie sud
    "OUEST": {"spawn_x": 600, "spawn_y": 35, "heading": 180, "target_x": -600}, # Va vers l'Ouest (-X), voie nord
    "NORD": {"spawn_x": 35, "spawn_y": -600, "heading": 90, "target_y": 600},   # Va vers le Nord (+Y), voie est
    "SUD": {"spawn_x": -35, "spawn_y": 600, "heading": 270, "target_y": -600}   # Va vers le Sud (-Y), voie ouest
}

def register_car_shapes(screen):
    """Enregistre une forme de voiture vectorielle propre (Nez vers +Y)."""
    car_shape = turtle.Shape("compound")
    
    # Corps (Nez à y=22, arrière à y=-18)
    body = ((-10, -18), (10, -18), (10, 14), (6, 22), (-6, 22), (-10, 14))
    car_shape.addcomponent(body, "gray", "black")
    
    # Toit / Vitres
    roof = ((-7, -10), (7, -10), (7, 8), (4, 12), (-4, 12), (-7, 8))
    car_shape.addcomponent(roof, "#b3e5fc", "black")
    
    # Phares (à l'avant, y=18 à 22)
    l_light = ((-9, 18), (-5, 18), (-5, 22), (-9, 22))
    r_light = ((5, 18), (9, 18), (9, 22), (5, 22))
    car_shape.addcomponent(l_light, "white", "black")
    car_shape.addcomponent(r_light, "white", "black")
    
    screen.register_shape("vector_car", car_shape)

class Vehicle:
    def __init__(self, id_veh, direction="EST", screen=None):
        self.id = id_veh
        self.direction = direction
        config = DIRECTIONS[direction]
        
        self.x = config["spawn_x"]
        self.y = config["spawn_y"]
        self.heading = config["heading"]
        
        self.max_speed = 4
        self.current_speed = self.max_speed
        self.is_active = True
        
        self.shape = turtle.Turtle()
        self.shape.speed(0)
        self.shape.penup()
        
        if screen:
            try: register_car_shapes(screen)
            except: pass
            
        self.shape.shape("vector_car")
        # Palette étendue de couleurs automobiles
        colors = [
            "#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#e67e22",
            "#1abc9c", "#d35400", "#c0392b", "#27ae60", "#7f8c8d", "#2c3e50",
            "#ff4081", "#7c4dff", "#00bcd4", "#8bc34a", "#ffeb3b", "#ff9800",
            "#607d8b", "#9e9e9e", "#ffffff", "#000000"
        ]
        self.shape.color(random.choice(colors))
        
        self.shape.goto(self.x, self.y)
        self.shape.setheading(self.heading)
    
    def move(self):
        """Avance selon la direction et vitesse actuelle (Limites 600 px)."""
        if not self.is_active:
            return
            
        if self.direction == "EST":
            self.x += self.current_speed
            self.shape.setx(self.x)
            if self.x > 600: self.deactivate()
                
        elif self.direction == "OUEST":
            self.x -= self.current_speed
            self.shape.setx(self.x)
            if self.x < -600: self.deactivate()
                
        elif self.direction == "NORD":
            self.y += self.current_speed
            self.shape.sety(self.y)
            if self.y > 600: self.deactivate()
                
        elif self.direction == "SUD":
            self.y -= self.current_speed
            self.shape.sety(self.y)
            if self.y < -600: self.deactivate()

    def deactivate(self):
        """Désactive le véhicule (sorti de l'écran)."""
        self.is_active = False
        self.shape.hideturtle()

    def check_traffic_light(self, light_state, light_pos):
        """Décision d'arrêt précise basée sur le PARE-CHOC AVANT."""
        if not self.is_active:
            return
            
        should_stop = False
        stop_margin = 15 # Distance de détection très précise
        front_offset = 22 # Distance du centre au pare-choc avant
        
        if self.direction == "EST":
            front_x = self.x + front_offset
            dist = light_pos - front_x
            should_stop = (light_state in ["ROUGE", "ORANGE"]) and (0 < dist < stop_margin)
            
        elif self.direction == "OUEST":
            front_x = self.x - front_offset
            dist = front_x - light_pos
            should_stop = (light_state in ["ROUGE", "ORANGE"]) and (0 < dist < stop_margin)
            
        elif self.direction == "NORD":
            front_y = self.y + front_offset
            dist = light_pos - front_y
            should_stop = (light_state in ["ROUGE", "ORANGE"]) and (0 < dist < stop_margin)
            
        elif self.direction == "SUD":
            front_y = self.y - front_offset
            dist = front_y - light_pos
            should_stop = (light_state in ["ROUGE", "ORANGE"]) and (0 < dist < stop_margin)
        
        if should_stop:
            self.current_speed = 0
        elif light_state == "VERT":
            self.current_speed = self.max_speed
        
        if should_stop:
            self.current_speed = 0
        elif light_state == "VERT":
            self.current_speed = self.max_speed

    def check_vehicle_ahead(self, vehicles):
        """Vérifie si un autre véhicule est devant (anti-collision)."""
        if not self.is_active:
            return
            
        min_distance = 60  # Distance de sécurité (augmentée pour les images)
        
        for v in vehicles:
            if v.id == self.id or not v.is_active or v.direction != self.direction:
                continue
            
            if self.direction == "EST":
                if v.x > self.x and (v.x - self.x) < min_distance:
                    self.current_speed = min(self.current_speed, v.current_speed)
                    
            elif self.direction == "OUEST":
                if v.x < self.x and (self.x - v.x) < min_distance:
                    self.current_speed = min(self.current_speed, v.current_speed)
                    
            elif self.direction == "NORD":
                if v.y > self.y and (v.y - self.y) < min_distance:
                    self.current_speed = min(self.current_speed, v.current_speed)
                    
            elif self.direction == "SUD":
                if v.y < self.y and (self.y - v.y) < min_distance:
                    self.current_speed = min(self.current_speed, v.current_speed)


class VehicleManager:
    def __init__(self, screen=None):
        self.vehicles = []
        self.next_id = 1
        self.spawn_timer = 0
        self.spawn_interval = 80  # Frames entre chaque spawn
        self.screen = screen
        
        # Enregistrer les shapes au démarrage
        if screen:
            register_car_shapes(screen)
        
    def spawn_vehicle(self, direction=None):
        """Génère un nouveau véhicule dans une direction aléatoire ou spécifiée."""
        if direction is None:
            direction = random.choice(list(DIRECTIONS.keys()))
        
        new_vehicle = Vehicle(self.next_id, direction, self.screen)
        self.vehicles.append(new_vehicle)
        self.next_id += 1
        return new_vehicle

    def auto_spawn(self):
        """Spawn automatique basé sur le timer."""
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Spawn dans une direction aléatoire
            self.spawn_vehicle()

    def cleanup_inactive(self):
        """Supprime les véhicules inactifs de la mémoire."""
        self.vehicles = [v for v in self.vehicles if v.is_active]

    def update_vehicles(self, intersection_controller):
        """Met à jour tous les véhicules avec le contrôleur d'intersection."""
        # Auto spawn
        self.auto_spawn()
        
        for v in self.vehicles:
            if not v.is_active:
                continue
                
            # Récupérer l'état du feu pour cette direction
            light_state = intersection_controller.get_light_state(v.direction)
            light_pos = intersection_controller.get_stop_position(v.direction)
            
            # Vérifier le feu
            v.check_traffic_light(light_state, light_pos)
            
            # Vérifier les autres véhicules (anti-collision)
            v.check_vehicle_ahead(self.vehicles)
            
            # Déplacer
            v.move()
        
        # Nettoyer les véhicules sortis
        self.cleanup_inactive()

    def get_vehicle_count(self):
        """Retourne le nombre de véhicules actifs."""
        return len([v for v in self.vehicles if v.is_active])