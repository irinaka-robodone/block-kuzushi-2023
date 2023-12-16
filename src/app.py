import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="ブロック崩し")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 40, "ブロック崩し", pyxel.frame_count % 16)
        pyxel.rect(0, 0, 20, 5, 6)
        pyxel.circ(80,80,5,10)
        
    
App()
