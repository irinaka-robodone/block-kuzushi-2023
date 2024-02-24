from typing import Self
import pyxel


class App:
    def __init__(self):
        self.SCREEN_SIZE = (175, 120)
        self.FPS = 60
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="ブロック崩し", fps=self.FPS)
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        
        self.reset()
        self.bar_disappeared_count = 0
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
        self.balls.append({"x": ball_x, "y": ball_y, "dx": ball_dx, "dy": ball_dy, "radius": ball_radius, "speed": speed})
    
    def create_rects(self):
        rect_count = 22
        rect_width = 20
        space_between_rects = 1
        # ブロック全体の幅を計算し、初期位置を設定
        total_width = (rect_count - 1) * space_between_rects + rect_count * rect_width
        initial_x = (self.SCREEN_SIZE[0] - total_width)
        
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
        if pyxel.frame_count % (60 * 60) == 0 and pyxel.frame_count % (60 * 60)>0:
            self.create_ball()
        
    def update_bar(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1.5
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1.5
        
    def update_ball(self):
        for ball in self.balls:
            ball["x"] += ball["dx"] * ball["speed"]
            ball["y"] += ball["dy"] * ball["speed"]
            if (ball["y"] + ball["radius"] > self.y
                and ball["x"] + ball["radius"] > self.x
                and ball["x"] - ball["radius"] < self.x + self.width
                and ball["y"] - ball["radius"] < self.y + self.height):
                ball["dy"] = -ball["dy"]
            # ボールが壁に当たった場合、反転
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > pyxel.width:
                ball["dx"] = -ball["dx"]
            # ボール壁に当たった場合、反転
            if ball["y"] - ball["radius"] < 0:
                ball["dy"] = -ball["dy"]  
        # update_gameover メソッドを呼び出す
    def update_gameover(self):
        for ball in self.balls:
            if all(ball["y"] + ball["radius"] > self.SCREEN_SIZE[1] - 10 for ball in self.balls):
                pyxel.quit()       
        # update_rects(self) メソッドを呼び出す
    def update_rects(self):      
        for ball in self.balls:
            for rect in self.rectangles:
                if (rect["x"] <= ball["x"] <= rect["x"] + rect["width"] and rect["y"] <= ball["y"] <= rect["y"] + rect["height"]):
                    self.rectangles.remove(rect)
                    ball["dy"] = -ball["dy"]
                    self.bar_disappeared_count += 1
        # 描画する処理
    def draw(self):
        pyxel.cls(0)
        self.draw_bar()
        self.draw_ball()
        self.draw_rects()
        pyxel.text(10,10, f"Points: {self.bar_disappeared_count}",7)
        # 長方形を描画する処理
    def draw_bar(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 5)
        # ボールを描画する処理
    def draw_ball(self):
        for ball in self.balls:
            pyxel.circ(ball["x"], ball["y"], ball["radius"], 3)   
        # ブロックを描画する処理
    def draw_rects(self):
        for rect in self.rectangles:
            if 0 <= rect["x"] <= self.SCREEN_SIZE[0] and 0 <= rect["y"] <= self.SCREEN_SIZE[1]:
                pyxel.rect(rect["x"], rect["y"], rect["width"], rect["height"],12)

App()
