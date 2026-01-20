import turtle

class Button:
    def __init__(self, label, x, y, w, h, color_theme, action_code):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.theme = color_theme
        self.action_code = action_code
        
        self.palettes = {
            "green":  {"bg": "#1b5e20", "border": "#00e676", "text": "white"},
            "orange": {"bg": "#e65100", "border": "#ffea00", "text": "white"},
            "red":    {"bg": "#b71c1c", "border": "#ff1744", "text": "white"},
            "blue":   {"bg": "#01579b", "border": "#00e5ff", "text": "white"},
            "purple": {"bg": "#4a148c", "border": "#d500f9", "text": "white"},
            "gray":   {"bg": "#263238", "border": "#90a4ae", "text": "#cfd8dc"}
        }

    def draw(self, pen):
        p = self.palettes.get(self.theme, self.palettes["gray"])
        
        # 1. Bordure de commande
        pen.penup(); pen.pensize(2); pen.color(p["border"])
        pen.goto(self.x - 2, self.y - 2); pen.pendown()
        self._rect(pen, self.w + 4, self.h + 4, fill=False)
        
        # 2. Fond du bouton
        pen.penup(); pen.goto(self.x, self.y)
        pen.begin_fill(); pen.color(p["bg"])
        self._rect(pen, self.w, self.h, fill=True)
        pen.end_fill()
        
        # 3. Label
        pen.penup(); pen.color(p["text"])
        pen.goto(self.x + self.w/2, self.y + self.h/2 - 7)
        pen.write(self.label, align="center", font=("Consolas", 10, "bold"))
        pen.pensize(1)

    def _rect(self, pen, w, h, fill=True):
        if not fill: pen.pendown()
        for _ in range(2):
            pen.forward(w); pen.left(90)
            pen.forward(h); self.pen_dummy = None # Eviter erreur de scope
            pen.left(90)
        pen.penup()

    def is_clicked(self, x, y):
        return (self.x <= x <= self.x + self.w) and (self.y <= y <= self.y + self.h)

class InterfaceManager:
    def __init__(self):
        self.buttons = []
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()
        
        y_top = 280
        y_bot = -300
        
        # Top Controls (Centered)
        self.buttons.append(Button("[ RUN ]",   -185, y_top, 85, 30, "green", "PLAY"))
        self.buttons.append(Button("[ PAUSE ]", -90,  y_top, 85, 30, "orange", "PAUSE"))
        self.buttons.append(Button("[ ABORT ]",  5,   y_top, 85, 30, "red", "STOP"))
        self.buttons.append(Button("[ RESET ]",  100, y_top, 85, 30, "blue", "RESET"))

        # Bottom Controls
        self.buttons.append(Button("> SYNC_NORM", -360, y_bot, 105, 25, "gray", "SCENARIO_1"))
        self.buttons.append(Button("> RUSH_HOUR", -245, y_bot, 105, 25, "gray", "SCENARIO_2"))
        self.buttons.append(Button("> NIGHT_CMD", -130, y_bot, 105, 25, "gray", "SCENARIO_3"))
        self.buttons.append(Button("> MNL_OVERIDE", -15, y_bot, 115, 25, "gray", "SCENARIO_4"))
        self.buttons.append(Button("|| SIGNAL_FLIP ||", 110, y_bot, 145, 25, "purple", "MANUAL_CLICK"))

    def draw_controls(self):
        self.pen.clear()
        self.pen.color("#0d0f12")
        # Top Panel
        self._panel(-200, 275, 415, 45)
        # Bottom Panel
        self._panel(-375, -310, 645, 40)
        for btn in self.buttons:
            btn.draw(self.pen)

    def _panel(self, x, y, w, h):
        self.pen.penup(); self.pen.goto(x, y); self.pen.begin_fill()
        for _ in range(2):
            self.pen.forward(w); self.pen.left(90)
            self.pen.forward(h); self.pen.left(90)
        self.pen.end_fill()

    def handle_click(self, x, y):
        for btn in self.buttons:
            if btn.is_clicked(x, y):
                return btn.action_code
        return None