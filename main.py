from pynput import keyboard

import time
import os
import json
from helicopter import Helicopter
from clouds import Clouds
from map import Map



TICK_SLEEP = 0.1
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 60
MAP_W, MAP_H = 20, 10

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = Helicopter(MAP_W, MAP_H)

MOVES = {'w': (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}

def process_key(key):
    global helico, tick, clouds, field
    c = key.char.lower()

    # Обработка движений верталета
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    # Сохранение игры
    elif c == 'f':
        data = {"helicopter": helico.export_data(),
                "clouds": clouds.export_data(),
                "field": field.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    # Загрузка игры
    elif c == "g":
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            tick = data["tick"] or 1
            helico.import_data(data["helicopter"])
            field.import_data(data["field"])
            clouds.import_data(data["clouds"])





listener = keyboard.Listener(
    on_press=None,
    on_release=process_key,)
listener.start()

tick = 1

while True:
    os.system('cls')
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if tick % TREE_UPDATE == 0:
        field.generate_tree()
    if tick % FIRE_UPDATE == 0:
        field.update_fire(helico)
    if tick % CLOUDS_UPDATE == 0:
        clouds.update()