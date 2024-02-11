from typing import Self
import pyxel


class App:
    def __init__(self):
        self.SCREEN_SIZE = (175, 120)
        self.FPS = 60
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="ブロック崩し", fps=self.FPS)
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        
        self.reset()
        pyxel.run(self.update, self.draw)
        
    def reset(self):
        self.rectangles = []
        self.balls = []
        self.create_bar()
        self.create_ball()
        self.create_rects()

    def create_bar(self):
        self.x = 75
        self.y = 100
        self.width = 50
        self.height = 3
    
    def create_ball(self):
        ball_x = 25
        ball_y = 40
        ball_radius = 2.5 
        speed = 0.5
        ball_dx = 1
        ball_dy = 1
        self.balls.append({"x": ball_x, "y": ball_y, "dx": ball_dx, "dy": ball_dy, "radius": ball_radius})
    
    def create_rects(self):
        rect_count = 22
        rect_width = 20
        space_between_rects = 1
        # ブロック全体の幅を計算し、初期位置を設定
        total_width = (rect_count -1) * space_between_rects + rect_count * rect_width
        initial_x = (self.SCREEN_SIZE[0] -total_width)
        
        #　既存のブロックがあれば、それらの座標を更新
        if 0 < len(self.rectangles):
            for i in range(len(self.rectangles)):
                self.rectangles[i]["y"] += 10
        #　新しいブロックを生成し、リストに追加
        for i in range(rect_count):
            rect_x = initial_x + i * (rect_width + 2)
            rect_y = 3
            rect_height = 5
            self.rectangles.append({"x": rect_x, "y": rect_y, "width": rect_width, "height": rect_height})
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_bar()
        self.update_ball()
        self.update_gameover()
        self.update_rects()
        if pyxel.frame_count % (60 * 20) == 0:
            self.create_rects()
        if pyxel.frame_count % (60 * 40) == 0:
            self.create_ball()
        
    def update_bar(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1.5
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1.5
        
    def update_ball(self):
        self.speed = 0.7
        for ball in self.balls:
            ball["x"] += ball["dx"] * self.speed
            ball["y"] += ball["dy"] * self.speed
            if (ball["y"] + ball["radius"] > self.y
                and ball["x"] + ball["radius"] > self.x
                and ball["x"] - ball["radius"] < self.x + self.width
                and ball["y"] - ball["radius"] < self.y +self.height
            ):
                ball["dx"] = -ball["dy"]
            # ボールが壁に当たった場合、反転
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > pyxel.width:
                ball["dx"] = -ball["dx"]
            # ボール壁に当たった場合、反転
            if ball["y"] - ball["radius"] < 0 or ball["y"] + ball["radius"] > pyxel.width:
                ball["dy"] = -ball["dy"]  
        # update_gameover メソッドを呼び出す
    def update_gameover(self):
        if (self.ball_y - self.ball_radius > self.SCREEN_SIZE[1] - 10):
            pyxel.quit()       
        # update_rects(self) メソッドを呼び出す
    def update_rects(self):      
        for rect in self.rectangles:
            if rect["x"] <= self.ball_x <= rect["x"] + rect["width"] and rect["y"] <= self.ball_y <= rect["y"] + rect["height"]:
                self.rectangles.remove(rect)
                self.ball_dy = -self.ball_dy
            
        # 描画する処理
    def draw(self):
        pyxel.cls(0)
        self.draw_bar()
        self.draw_ball()
        self.draw_rects()   
        # 長方形を描画する処理
    def draw_bar(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 5)
        # ボールを描画する処理
    def draw_ball(self):
        pyxel.circ(self.ball_x, self.ball_y, self.ball_radius, 3)   
        # ブロックを描画する処理
    def draw_rects(self):
        for rect in self.rectangles:
            if 0 <= rect["x"] <= self.SCREEN_SIZE[0] and 0 <= rect["y"] <= rect["y"] <= self.SCREEN_SIZE[1]:
                pyxel.rect(rect["x"], rect["y"], rect["width"], rect["height"],12)

App()
