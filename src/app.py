import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="ブロック崩し")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        
        
        self.create_bar()
        self.create_ball()
        pyxel.run(self.update, self.draw)
        
    def create_bar(self):
        self.x = 75
        self.y = 80
        self.width = 25
        self.height = 3
    def create_ball(self):
        self.ball_x = 10
        self.ball_y = 10
        self.ball_radius = 3
        
        self.speed = 2
        self.ball_dx = 1
        self.ball_dy = 1
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # update_circ メソッドを呼び出す
        self.update_bar()
    def update_bar(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        # update_ball メソッドを呼び出す
        self.update_ball()    
    def update_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

    
    def draw(self):
        
        pyxel.cls(0)
        self.draw_bar()
        self.draw_ball()
    def draw_bar(self):
        # 長方形を描画する処理
        pyxel.rect(self.x, self.y, self.width, self.height, 9)
    def draw_ball(self):
        pyxel.circ(self.ball_x, self.ball_y, self.ball_radius, 9)   
    
App()
