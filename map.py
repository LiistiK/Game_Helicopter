from utils import randbool, randcell, randcell2

CELL_TYPES = '🟩🌲🌊🏥🔥🔧'
TREE_BONUS = 100
UPGRADE_COST = 2500
LIFE_COST = 5000


class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(5, 10)
        self.generate_rivers(10)
        self.generate_rivers(10)
        self.generate_rivers(10)

        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        if x < 0 or y < 0 or x > self.h or y > self.w:
            return False
        return True

    def print_map(self, helico, clouds):
        print("⬛️" * (self.w + 2))
        for ri in range(self.h):
            print("⬛️", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if clouds.cells[ri][ci] == 1:
                    print('⚪', end='')#11111111111111111111111111111111111111111111111
                elif clouds.cells[ri][ci] == 2:
                    print('⚡', end='')#11111111111111111111111111111111111111111111111
                elif helico.x == ri and helico.y == ci:
                    print('🚁', end='')
                elif 0 <= cell < len(CELL_TYPES):
                    print(CELL_TYPES[cell], end="")
            print("⬛️")
        print("⬛️" * (self.w + 2))

    def generate_rivers(self, l):
        rc = randcell(self.w, self.h)
        rx = rc[0]
        ry = rc[1]
        self.cells[rx][ry] = 2
        for _ in range(l):
            rc2 = randcell2(rx, ry)
            print(rc2)
            rx2, ry2 = rc2[0], rc2[1]
            if self.check_bounds(rx2, ry2):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1

    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 5

    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 3

    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 4

    def update_fire(self, helico):
        for ri in range(self.h):
            for ci in range(self.w):
                if self.cells[ri][ci] == 4:
                    self.cells[ri][ci] = 0
                    if helico.score > 0:
                        helico.score -= 50
        for i in range(10):
            self.add_fire()

    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if c == 2:
            helico.tank = helico.mxtank
        if c == 4 and helico.tank > 0:
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if c == 5 and helico.score >= UPGRADE_COST:
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if c == 3 and helico.score >= LIFE_COST:
            helico.lives += 1
            helico.score -= LIFE_COST
        if (d == 2):
            helico.lives -= 1
            if helico.lives == 0:
                helico.game_over()

    def export_data(self):
        return {"cells": self.cells}

    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]