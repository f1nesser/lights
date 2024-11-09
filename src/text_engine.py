#!/usr/bin/python3
import sys
import board
import neopixel
import time
from multiprocessing import Process
from itertools import count
from PIL import Image, GifImagePlugin

class Engine():
    
    animation_process = Process()

    def __init__(self, pixel, data_pin, num_pixels, color_order):
        self._DATA_PIN = data_pin
        self._NUM_PIXELS = num_pixels # 256
        self._ORDER = color_order #neopixel.RGB
        self._pixel = pixel #neopixel.NeoPixel(DATA_PIN, NUM_PIXELS ,brightness=.1,auto_write=False, pixel_order=ORDER )
        
    
    @staticmethod
    def _render_pixel(frame, x, y): 
            return frame.convert('RGB').getpixel((x,y)) # no hard code rgb

    def _render_frame(self, frame):
        pixel_index = 0
        for x in range(frame.width-1, -1, -1):
            if x % 2 != 0:
                for y in range(frame.height-1, -1, -1): # refactor?
                    self._pixel[pixel_index] = self._render_pixel(frame, x, y)
                    pixel_index+=1
            else:
                for y in range(frame.height):
                    self._pixel[pixel_index] = self._render_pixel(frame, x, y)
                    pixel_index+=1

        self._pixel.show()
        #print(self._pixel.pin, self._pixel._power)

    def _cycle_test(self, delay=.3):
        for i in range(self._NUM_PIXELS):
            self._pixel[i] = (5,5,20)
            self._pixel.show()
            print(i)
            time.sleep(delay)

    def _clear_pixel(self):
        for i in range(self._NUM_PIXELS):
            self._pixel[i] = (0,0,0)
        self._pixel.show()

    
    def _play_gif(self, file=None, frame_delay=.3, frame_start=0, loop=False):
        with Image.open(file) as im:
            frame_num = 0
            while True:
                try:
                    im.seek(frame_num)
                    self._render_frame(im)
                    time.sleep(frame_delay)
                    frame_num+=1
                except EOFError:
                    if not loop: # pull conditional out of loop somehow?
                        return
                    frame_num = 0

    def stop(self):
        self.animation_process.terminate()
        self._clear_pixel()

    def run_function(self, function, **kwargs):
        if self.animation_process.is_alive(): #its gonna throw
            self.animation_process.terminate()
        self.animation_process = Process(target=function, name=function, kwargs=kwargs, daemon=True)
        self.animation_process.start()



if __name__ == "__main__":
    DATA_PIN = board.D18
    NUM_PIXELS = 256
    ORDER = neopixel.RGB
    with neopixel.NeoPixel(DATA_PIN, NUM_PIXELS ,brightness=.1, auto_write=False, pixel_order=ORDER) as p:
        print(p.pin.value)
        e = Engine(p, DATA_PIN, NUM_PIXELS, ORDER) 
        #e.cycle_test(delay=0)
        e.play_gif('../gifs/idk0.gif', loop=True)
