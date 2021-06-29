'''
--------------------------------------------------
'''

# Commands :

SET_TILE = "/ball"
START = "/ball on"
STOP = "/ball off"

'''
--------------------------------------------------
'''

import sys

from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "Soccer",
    "description": "Indicator for the ball",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


spawn = False
wait = False
on = False
id_furni = ""
r = [[0, 4], [4, 0], [4, 4], [0, -4], [-4, 0], [-4, -4], [4, -4], [-4, 4]]


def spawn_furni():
    global spawn

    if not spawn:
        for idd in range(8):
            ext.send_to_client('{in:ObjectAdd}{i:10000'+str(idd)+'}{i:3895}{i:0}{i:0}{i:0}{s:"100.0"}{s:"0.47"}{i:0}{i:0}{s:"0"}{i:-1}{i:1}{i:25297484}{s:"Lande"}')
        spawn = True


def reset_furni():
    global spawn

    if spawn:
        for idd in range(8):
            ext.send_to_client('{in:ObjectRemove}{s:"10000'+str(idd)+'"}{b:false}{i:25297484}{i:0}')
        spawn = False


def speech(msg):
    global wait, on

    text, _, _ = msg.packet.read('sii')

    if text == SET_TILE:
        msg.is_blocked = True
        wait = True
        talk('Double click on the furni')

    if text == START:
        msg.is_blocked = True
        on = True
        talk("Indicator on")

    if text == STOP:
        msg.is_blocked = True
        on = False
        reset_furni()
        talk('Indicator off')


def update_furni(msg):
    idd, _, x, y, _, z, _, _, _, _, _, _, _ = msg.packet.read('iiiiissiisiii')

    if on:
        if idd == id_furni:
            for i in range(8):
                ext.send_to_client('{in:ObjectUpdate}{i:10000'+str(i)+'}{i:11139}{i:'+str(x+r[i][0])+'}{i:'+str(y+r[i][1])+'}{i:0}{s:"'+z+'"}{s:"0.47"}{i:0}{i:0}{s:"0"}{i:-1}{i:1}{i:25297484}')


def talk(txt):
    ext.send_to_client('{in:Whisper}{i:9999999}{s:"@red@'+txt+'"}{i:0}{i:30}{i:0}{i:0}')


def reset(msg):
    global wait, on, spawn, id_furni

    wait, on, spawn = False, False, False
    id_furni = ""


def set_furni(msg):
    global id_furni, wait

    if wait:
        msg.is_blocked = True
        id_furni, _ = msg.packet.read('ii')
        talk(f"Id set to : {id_furni}")
        wait = False
        spawn_furni()


def walk(msg):
    if wait:
        msg.is_blocked = True


ext.intercept(Direction.TO_SERVER, walk, 'MoveAvatar')
ext.intercept(Direction.TO_SERVER, speech, 'Chat')
ext.intercept(Direction.TO_SERVER, reset, 'GetGuestRoom')
ext.intercept(Direction.TO_SERVER, set_furni, 'UseFurniture')
ext.intercept(Direction.TO_CLIENT, update_furni, 'ObjectUpdate')
