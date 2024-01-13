from typing import Self
import pyxel


class App:
    def __init__(self):
        self.SCREEN_SIZE = (160, 120)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="ブロック崩し")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        
        
        self.create_bar()
        self.create_ball()
        self.create_rect()
        pyxel.run(self.update, self.draw)
        
    def create_bar(self):
        self.x = 75
        self.y = 100
        self.width = 25
        self.height = 3
    def create_ball(self):
        self.ball_x = 10
        self.ball_y = 10
        self.ball_radius = 2.5 
        self.speed = 1.5
        self.ball_dx = 1
        self.ball_dy = 1
    def create_rect(self):
        self.rect_x = 10
        self.rect_y = 3
        self.rect_width = 8
        self.rect_height = 3

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # update_bar メソッドを呼び出す
        self.update_bar()
        # update_ball メソッドを呼び出す
        self.update_ball()
        self.update_gameover()
    def update_bar(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        
    def update_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        if (self.ball_y + self.ball_radius > self.y
            and self.ball_x + self.ball_radius > self.x
            and self.ball_x - self.ball_radius < self.x + self.width
            and self.ball_y - self.ball_radius < self.y +self.height
        ):
            self.ball_dy = -self.ball_dy
        # ボールが壁に当たった場合、反転
        if self.ball_x - self.ball_radius < 0 or self.ball_x + self.ball_radius > pyxel.width:
            self.ball_dx = -self.ball_dx
        # ボール壁に当たった場合、反転
        if self.ball_y - self.ball_radius < 0 or self.ball_y + self.ball_radius > pyxel.width:
            self.ball_dy = -self.ball_dy  

    def update_gameover(self):
        if (self.ball_y - self.ball_radius > self.SCREEN_SIZE[1] - 10):
            pyxel.quit()
            
        
            
        # update_rect メソッドを呼び出す
        self.update_rect()    
    def update_rect(self):      
        pass
    def draw(self):
        pyxel.cls(0)
        self.draw_bar()
        self.draw_ball()
        self.draw_rect()   
    def draw_bar(self):
        # 長方形を描画する処理
        pyxel.rect(self.x, self.y, self.width, self.height, 9)
    def draw_ball(self):
        # ボールを描画する処理
        pyxel.circ(self.ball_x, self.ball_y, self.ball_radius, 9)   
    def draw_rect(self):
        # 長方形を描画する処理
        pyxel.rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height, 9)
App()
