from kivy.app import App
 fr om kivy.uix.widget import Widget
 fr om kivy.graphics import Color, Ellipse, Rectangle
 fr om kivy.clock import Clock
 fr om kivy.core.window import Window
 fr om kivy.uix.label import Label
 fr om random import randint

Window.size = (400, 700)

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_x = 180
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        self.touch_x = None
        
        with self.canvas:
            Color(0.05, 0.05, 0.2)
            self.bg = Rectangle(pos=(0, 0), size=(400, 700))
        
        # Jugador (nave azul)
        with self.canvas:
            Color(0, 0.7, 1)
            self.player = Ellipse(pos=(self.player_x, 60), size=(45, 45))
        
        self.score_label = Label(text="Puntuación: 0", font_size=26, bold=True, pos=(200, 660))
        self.add_widget(self.score_label)
        
        Clock.schedule_interval(self.update, 1.0/60)
        Clock.schedule_interval(self.spawn_enemy, 1.2)
        
        self.bind(on_touch_down=self.on_touch_down)
        self.bind(on_touch_move=self.on_touch_move)
    
    def on_touch_down(self, instance, touch):
        if self.game_over:
            self.restart()
            return True
        self.touch_x = touch.x
        self.shoot()
        return True
    
    def on_touch_move(self, instance, touch):
        if not self.game_over:
            self.player_x = max(20, min(355, touch.x - 22))
            self.player.pos = (self.player_x, 60)
        return True
    
    def shoot(self):
        with self.canvas:
            Color(1, 1, 0)
            bullet = Ellipse(pos=(self.player_x + 17, 105), size=(10, 25))
            self.bullets.append(bullet)
    
    def update(self, dt):
        if self.game_over:
            return
        
        # Mover balas
        for b in self.bullets[:]:
            b.pos = (b.pos[0], b.pos[1] + 18)
            if b.pos[1] > 720:
                self.canvas.remove(b)
                self.bullets.remove(b)
        
        # Mover enemigos
        for e in self.enemies[:]:
            e.pos = (e.pos[0], e.pos[1] - 4)
            if e.pos[1] < 0:
                self.canvas.remove(e)
                self.enemies.remove(e)
        
        self.check_collisions()
        self.score_label.text = f"Puntuación: {self.score}"
    
    def spawn_enemy(self, dt):
        if self.game_over: return
        x = randint(30, 350)
        with self.canvas:
            Color(1, 0.2, 0.2)
            enemy = Ellipse(pos=(x, 680), size=(38, 38))
            self.enemies.append(enemy)
    
    def check_collisions(self):
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if self.collide(b, e):
                    self.canvas.remove(b)
                    self.canvas.remove(e)
                    self.bullets.remove(b)
                    self.enemies.remove(e)
                    self.score += 15
                    break
    
    def collide(self, a, b):
        ax, ay = a.pos
        aw, ah = a.size
        bx, by = b.pos
        bw, bh = b.size
        return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)
    
    def restart(self):
        self.game_over = False
        self.score = 0
        for obj in self.enemies + self.bullets:
            self.canvas.remove(obj)
        self.enemies.clear()
        self.bullets.clear()
        self.score_label.text = "Puntuación: 0"

class PaquidawAndroidApp(App):
    def build(self):
        return GameWidget()

if __name__ == "__main__":
    PaquidawAndroidApp().run()