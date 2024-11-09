from flask import Flask
from text_engine import Engine
import neopixel
import board
import os
app = Flask(__name__)

DATA_PIN = board.D18
NUM_PIXELS = 256
ORDER = neopixel.RGB

p = neopixel.NeoPixel(DATA_PIN, NUM_PIXELS ,brightness=.1, auto_write=False, pixel_order=ORDER)
E = Engine(p, DATA_PIN, NUM_PIXELS, ORDER) 

@app.route('/')
def hello_world():
   return 'sup pussy' 

@app.route('/play/<file>')
def play(file):
    try: 
        E.run_function(E._play_gif, file=f'../gifs/{file}', loop=True)
        return f'playing {file}' 
    except Exception as e:
        return f'{e} \n {os.listdir(path="../gifs")}'

@app.route('/stop')
def stop():
    E.stop()
    return('stopped')
