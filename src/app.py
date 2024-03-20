from typing import Self
import pyxel
import math
from copy import deepcopy

class App:
    def __init__(self):
        self.SCREEN_SIZE = (200,240)
        self.FPS = 60
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="ブロック崩し", fps=self.FPS)
        pyxel.load("assets/resource.pyxres")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        self.init()
        self.state = "start"
    
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def init(self):
        self.best_score = 0
        self.reset()
        
    def reset(self):
        self.state = "start"
        self.rectangles = []
        self.rectangles_cache = []
        self.balls = []
        self.current_ball_speed = 0.8
        self.points_to_ball_speed_up = 0
        self.block_create_interval = 20 # ブロックを生成する間隔 [sec]
        self.ball_create_interval = 30 # ボールを生成する間隔 [sec]
        self.max_block_create_interval = 4 # ブロックを生成する最小間隔 [sec]
        self.max_ball_create_interval = 10 # ボールを生成する最小間隔 [sec]
        self.max_ball_speed = 4.0
        self.count_created_rows = 0
        self.row_colors = [8, 9, 10, 11, 12, 13, 7]  # 行ごとに異なる色を割り当てる
        self.create_bar()
        self.create_ball()
        self.create_rects(7)
        self.bar_disappeared_count = 0
        self.score = 0
        self.game_started = False
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state = "playing"
            
        elif self.state == "playing":
            self.update_rects()
            
            if pyxel.frame_count % (self.FPS * self.block_create_interval) == 0:
                self.create_rects(1)
                self.block_create_interval -= 1
                self.block_create_interval = max(self.block_create_interval, self.max_block_create_interval)
                return
            if pyxel.frame_count % (self.FPS * self.ball_create_interval) == 0:
                self.create_ball()
                self.ball_create_interval -= 1
                self.ball_create_interval = max(self.ball_create_interval, self.max_ball_create_interval)
                return
            
            self.update_bar()
            self.update_ball()
            self.update_game_over()
        
        elif self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset()
        
    def create_bar(self):
        self.x = 75
        self.y = 200
        self.width = 40
        self.height = 3
            
    def create_ball(self):
        ball_x = 15
        ball_y = 60
        ball_radius = 4
        speed = self.current_ball_speed
        ball_dx = 1
        ball_dy = 1
        self.balls.append({"x": ball_x, "y": ball_y, "dx": ball_dx, "dy": ball_dy, "radius": ball_radius, "speed": speed})
    
    def create_rects(self, row_count: int = 1):
        
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

        self.count_created_rows += row_count
        self.row_colors = self.row_colors[row_count:] + self.row_colors[:row_count]  # 行数に応じて色を変更するためのリストを更新

    def get_color_by_row(self, row):
        # 行数に応じて色を変更するロジックをここに実装
        return self.row_colors[row % len(self.row_colors)]  # 行数が増えるごとに色をサイクリックに変更
        
    def update_bar(self):
        min_x = 0
        max_x = self.SCREEN_SIZE[0] - self.width  # バーが画面外に出ないように調整
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(max_x, self.x + 2.0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(min_x, self.x - 2.0)
        
    def update_ball(self):
        
        if self.points_to_ball_speed_up == 5:
                self.current_ball_speed += 0.15
                self.points_to_ball_speed_up = 0
                self.current_ball_speed = min(self.max_ball_speed, self.current_ball_speed)
                
        for ball in self.balls:
            ball["speed"] = self.current_ball_speed
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
                
                # ボールの単位速度ベクトル（方向）を更新
                ball["dx"] = math.sin(reflection_angle)
                ball["dy"] = -1 * math.cos(reflection_angle)
            
            # ボールが壁に当たった場合の処理
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > self.SCREEN_SIZE[0]:
                ball["dx"] = -ball["dx"]
            
            if ball["y"] - ball["radius"] < 0:
                ball["dy"] = -ball["dy"] 
                ball["y"] = ball["radius"]
    
    def update_game_over(self):
        if all(ball["y"] + ball["radius"] > self.SCREEN_SIZE[1]  for ball in self.balls):
            self.state = "gameover"

            # ベストスコアを更新
            if self.best_score < self.score:
                self.best_score = self.score
            
    def update_rects(self):
        hit = False
        for ball_id, ball in enumerate(self.balls):
            if hit == True:
                break
            for rect_id, rect in enumerate(self.rectangles):
                if hit == True:
                    break
                if (rect["x"] <= ball["x"] <= rect["x"] + rect["width"] and rect["y"] <= ball["y"] <= rect["y"] + rect["height"]):
                    self.rectangles.pop(rect_id)
                    ball["dy"] = -ball["dy"]
                    
                    self.points_to_ball_speed_up += 1
                    self.score += 1
                    print(f"{self.score} Hit: ball[{ball_id}] and rect[{rect_id}]")
                    return
                
        # ブロックのキャッシュを更新
        self.rectangles_cache = deepcopy(self.rectangles)
        
        # 描画する処理
    def draw(self):
        pyxel.cls(1)
        
        if self.state == "start":
            self.draw_start_screen()
            
        elif self.state == "gameover":
            self.draw_result()

        elif self.state == "playing": 
            self.draw_bar()
            self.draw_ball()
            self.draw_rects()
            pyxel.text(10,10, f"Score: {self.score}",7)
        
        # 長方形を描画する処理
    def draw_bar(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 5)
        
        # ボールを描画する処理
    def draw_ball(self):
        for ball in self.balls:
            pyxel.circ(ball["x"], ball["y"], ball["radius"], 7)   
            
        # ブロックを描画する処理
    def draw_rects(self):
        for rect in self.rectangles_cache:
            if 0 <= rect["x"] <= self.SCREEN_SIZE[0] and 0 <= rect["y"] <= self.SCREEN_SIZE[1]:
                pyxel.rect(rect["x"], rect["y"], rect["width"], rect["height"], rect["color"])
    
    def draw_start_screen(self):
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 30, self.SCREEN_SIZE[1] // 2, "Block Breaker", 11)
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 47, self.SCREEN_SIZE[1] // 2 + 10, "Press 'Enter' to start", 11)
    
    def draw_result(self):
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 30, self.SCREEN_SIZE[1] // 2, "Game Over",11)
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 50, self.SCREEN_SIZE[1] // 2 + 10, "Press 'Enter' to restart", 11)
        
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 50, self.SCREEN_SIZE[1] // 2 + 30, f"Score: {self.score}", 11)
        pyxel.text(self.SCREEN_SIZE[0] // 2 - 50, self.SCREEN_SIZE[1] // 2 + 40, f"Best Score: {self.best_score}", 11)
    
    
if __name__ == "__main__":
    app = App()
    app.run()