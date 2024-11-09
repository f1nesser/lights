#!/usr/bin/python3
import sys
import board
import neopixel
import time
from PIL import Image, GifImagePlugin

#GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS
DATA_PIN = board.D18
NUM_PIXELS=256
ORDER=neopixel.RGB

def cycle_test():
    for i in range(NUM_PIXELS):
        pixels[i] = (255,0,0)
        pixels.show()
        print(i)
        time.sleep(.3)

def cycle_test():
    for i in range(NUM_PIXELS):
        pixels[i] = (255,0,0)
        pixels.show()
        print(i)
        time.sleep(.3)

def render_pixel(frame, strip, x, y): #this modifying tuple stuff is dumb
        return frame.convert('RGB').getpixel((x,y))


def render_frame(frame, strip):
    pixel_index = 0
    for x in range(frame.width-1, -1, -1):
        if x % 2 != 0:
            for y in range(frame.height-1, -1, -1):
                strip[pixel_index] = render_pixel(frame, strip, x, y)
                pixel_index+=1
        else:
            for y in range(frame.height):
                strip[pixel_index] = render_pixel(frame, strip, x, y)
                pixel_index+=1

    strip.show()

def loop(im, pixels):
    frame_num = 0
    while True:
        try:
            im.seek(frame_num)
            render_frame(im,pixels)
            time.sleep(.3)
            frame_num+=1
        except EOFError:
            frame_num = 0

pixels = neopixel.NeoPixel(DATA_PIN, NUM_PIXELS ,brightness=.1,auto_write=False, pixel_order=ORDER )
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print('give a file')
        exit(-1)
    pixels = neopixel.NeoPixel(DATA_PIN, NUM_PIXELS ,brightness=.1,auto_write=False, pixel_order=ORDER )
    im = Image.open(sys.argv[1])
    #cycle_test()
    loop(im, pixels)
    while True:
        choice = input('what frame?')
        try:
            im.seek(int(choice))
            render_frame(im, pixels)
        except:
            print('whoops')
            exit -1
