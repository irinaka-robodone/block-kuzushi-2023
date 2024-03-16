from typing import Self
import pyxel
import math
class App:
    def __init__(self):
        self.SCREEN_SIZE = (200,240)
        self.FPS = 60
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="ブロック崩し", fps=self.FPS)
        pyxel.load("my_resource.pyxres")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        self.reset()
        pyxel.run(self.update, self.draw)
        
    def reset(self):
        self.rectangles = []
        self.balls = []
        self.create_bar()
        self.create_ball()
        self.create_rects()
        self.bar_disappeared_count = 0
        self.score = 0
        self.game_started = False
        
    def create_bar(self):
        self.x = 75
        self.y = 200
        self.width = 40
        self.height = 3
            
    def create_ball(self):
        ball_x = 15
        ball_y = 60
        ball_radius = 4
        speed = 0.8
        ball_dx = 1
        ball_dy = 1
        self.balls.append({"x": ball_x, "y": ball_y, "dx": ball_dx, "dy": ball_dy, "radius": ball_radius, "speed": speed})
    
    def create_rects(self):
            
        row_count = 7  # 行数を増やす
        rect_count_per_row = 8
        rect_width = 24
        rect_height = 5
        space_between_rects = 1.0

        # ブロック全体の幅を計算し、初期位置を設定
        total_width = rect_count_per_row * (rect_width + space_between_rects) - space_between_rects
        initial_x = (self.SCREEN_SIZE[0] - total_width) // 2

    # 既存のブロックがあれば、それらの座標を更新
        if len(self.rectangles) > 0:
            for rect in self.rectangles:
                rect["y"] += rect_height + space_between_rects  # 現在の行数と間隔分だけY座標を調整

    # 新しいブロックを生成し、リストに追加
        for row in range(row_count):
            color = self.get_color_by_row(row)  # 行数から色を取得
            for i in range(rect_count_per_row):
                rect_x = initial_x + i * (rect_width + space_between_rects)
                rect_y = 3 + row * (rect_height + space_between_rects)  # 行ごとにY座標を増やす
                self.rectangles.append({"x": rect_x, "y": rect_y, "width": rect_width, "height": rect_height, "color": color})
    def get_color_by_row(self, row):
        # 行数に応じて色を変更するロジックをここに実装
        colors = [8, 9, 10, 11, 12, 13, 7]  # 行ごとに異なる色を割り当てる
        return colors[row % len(colors)]  # 行数が増えるごとに色をサイクリックに変更

    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if not self.game_started:
            if pyxel.btnp(ord("\r")):
                self.game_started = True
            
        else:
            self.update_bar()
            self.update_ball()
            self.update_gameover()
            self.update_rects()
        
            if pyxel.frame_count % (60 * 20) == 0:
                self.create_rects()
            if pyxel.frame_count % (60 * 30) == 0:
                self.create_ball()
        
        
    def update_bar(self):
        min_x = 0
        max_x = self.SCREEN_SIZE[0] - self.width  # バーが画面外に出ないように調整
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(max_x, self.x + 2.0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(min_x, self.x - 2.0)

        
    def update_ball(self):
        for ball in self.balls:
            
            ball["x"] += ball["dx"] * ball["speed"]
            ball["y"] += ball["dy"] * ball["speed"]
            
            # ボールがバーと衝突した場合の処理
            if (ball["y"] + ball["radius"] > self.y 
                and ball["x"] + ball["radius"] > self.x - 1
                and ball["x"] - ball["radius"] < self.x + self.width + 1
                and ball["y"] - ball["radius"]  < self.y + self.height):
                
                relative_position = (ball["x"] - (self.x + self.width / 2)) / (self.width / 2)
                
                # 反射角度を計算
                reflection_angle = relative_position * math.pi / 4  # 最大角度は60度
                
                # ボールの速度ベクトルを更新
                ball_speed = math.sqrt(ball["dx"] ** 2 + ball["dy"] ** 2)
                ball["dx"] = ball_speed * math.sin(reflection_angle)
                ball["dy"] = -ball_speed * math.cos(reflection_angle)
                
            
            
            # ボールが壁に当たった場合の処理
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > self.SCREEN_SIZE[0]:
                ball["dx"] = -ball["dx"]
                ball["dy"] *= 1.1 
            
            if ball["y"] - ball["radius"] < 0:
                ball["dy"] = -ball["dy"] 
                ball["dx"] *= 1.1
                ball["y"] = ball["radius"]
            # update_gameover メソッドを呼び出す
            max_speed = 2.0  # ボールの最大速度
            current_speed = math.sqrt(ball["dx"] ** 2 + ball["dy"] ** 2)
            if current_speed > max_speed:
                ball["dx"] *= max_speed / current_speed
                ball["dy"] *= max_speed / current_speed
    
    
    
    def update_gameover(self):
        for ball in self.balls:
            if all(ball["y"] + ball["radius"] > self.SCREEN_SIZE[1]  for ball in self.balls):
                self.game_started = False
                self.reset()

        # update_rects(self) メソッドを呼び出す
    #短形ブロック
    def update_rects(self):      
        for ball in self.balls:
            for rect in self.rectangles:
                if (rect["x"] <= ball["x"] <= rect["x"] + rect["width"] and rect["y"] <= ball["y"] <= rect["y"] + rect["height"]):
                    self.rectangles.remove(rect)
                    ball["dy"] = -ball["dy"]
                    
                    self.bar_disappeared_count += 1
                    self.score += 1
        if self.bar_disappeared_count % 5 == 0 and self.bar_disappeared_count >0:
            
            self.bar_disappeared_count = 0            

        
        # 描画する処理
    def draw(self):
        pyxel.cls(1)
        
        if not self.game_started:
            self.draw_start_screen()
        elif not self.game_started and self.is_gameover():
            self.draw_gameover_screen()
        else: 
            self.draw_bar()
            self.draw_ball()
            self.draw_rects()
            self.update_gameover()
            pyxel.text(10,10, f"Points: {self.score}",7)
        
        
        # 長方形を描画する処理
    def draw_bar(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 5)
        # ボールを描画する処理
    def draw_ball(self):
        for ball in self.balls:
            pyxel.circ(ball["x"], ball["y"], ball["radius"], 7)   
        # ブロックを描画する処理
    def draw_rects(self):
        for rect in self.rectangles:
            if 0 <= rect["x"] <= self.SCREEN_SIZE[0] and 0 <= rect["y"] <= self.SCREEN_SIZE[1]:
                pyxel.rect(rect["x"], rect["y"], rect["width"], rect["height"], rect["color"])
    
    def draw_start_screen(self):
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 30, self.SCREEN_SIZE[1] // 2, "block breaker", 11)
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 47, self.SCREEN_SIZE[1] // 2 + 10, "Press 'Enter' to start", 11)
    
    
    
App()
