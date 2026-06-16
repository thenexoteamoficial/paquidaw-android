from kivy.app import App
 fr om kivy.uix.widget import Widget
 fr om kivy.graphics import Color, Ellipse, Rectangle
 fr om kivy.clock import Clock
 fr om kivy.core.window import Window
 fr om kivy.uix.label import Label
 fr om kivy.uix.button import Button
 fr om kivy.uix.boxlayout import BoxLayout
 fr om random import randint, choice

Window.size = (400, 700)

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        
        # Fondo
        with self.canvas:
            Color(0.05, 0.05, 0.15)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        
        # Jugador (nave)
        with self.canvas:
            Color(0, 0.8, 1)
            self.player = Ellipse(pos=(180, 50), size=(40, 40))
        
        # Puntaje
        self.score_label = Label(text="Puntuación: 0", font_size=24, pos=(200, 650))
        self.add_widget(self.score_label)
        
        # Iniciar juego
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.5)
        
        # Controles táctiles
        self.bind(on_touch_down=self.on_touch_down)
    
    def on_touch_down(self, instance, touch):
        if self.game_over:
            self.restart_game()
            return
        
        # Disparar
        with self.canvas:
            Color(1, 1, 0)
            bullet = Ellipse(pos=(self.player.pos[0] + 15, self.player.pos[1] + 40), size=(10, 20))
            self.bullets.append(bullet)
    
    def update(self, dt):
        if self.game_over:
            return
        
        # Mover jugador con toque
        # (simplificado: el jugador sigue el toque)
        
        # Mover balas
        for bullet in self.bullets[: ]:
            bullet.pos = (bullet.pos[0], bullet.pos[1] + 15)
            if bullet.pos[1] > 700:
                self.canvas.remove(bullet)
                self.bullets.remove(bullet)
        
        # Mover enemigos
        for enemy in self.enemies[:]:
            enemy.pos = (enemy.pos[0], enemy.pos[1] - 3)
            if enemy.pos[1] < 0:
                self.canvas.remove(enemy)
                self.enemies.remove(enemy)
        
        # Colisiones
        self.check_collisions()
        
        # Actualizar puntaje
        self.score_label.text = f"Puntuación: {self.score}"
    
    def spawn_enemy(self, dt):
        if self.game_over:
            return
        x = randint(20, 360)
        with self.canvas:
            Color(1, 0.3, 0.3)
            enemy = Ellipse(pos=(x, 650), size=(35, 35))
            self.enemies.append(enemy)
    
    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self.collide(bullet, enemy):
                    self.canvas.remove(bullet)
                    self.canvas.remove(enemy)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
    
    def collide(self, obj1, obj2):
        x1, y1 = obj1.pos
        w1, h1 = obj1.size
        x2, y2 = obj2.pos
        w2, h2 = obj2.size
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def restart_game(self):
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