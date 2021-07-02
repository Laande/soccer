'''
--------------------------------------------------
'''

ID = "886731978"  # global id of the furni

# Header :

WALK = 3320
TALK = 1314
RESET = 2312
USE_FURNI = 99
FURNI_UPDATE = 3776

ADD_FURNI = "1534"
REMOVE_FURNI = "2703"
TALK_IN = "1446"

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
    "title": "Soccer | Leet",
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
            ext.send_to_client('{l}{h:'+ADD_FURNI+'}{i:10000'+str(idd)+'}{i:'+ID+'}{i:0}{i:0}{i:0}{s:"100.0"}{s:"0.47"}{i:0}{i:0}{s:"0"}{i:-1}{i:1}{i:4296487}{s:"Lande"}')
        spawn = True


def reset_furni():
    global spawn

    if spawn:
        for idd in range(8):
            ext.send_to_client('{l}{h:'+REMOVE_FURNI+'}{s:"10000'+str(idd)+'"}{b:false}{i:4296487}{i:0}')
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
                ext.send_to_client('{l}{h:'+str(FURNI_UPDATE)+'}{i:10000'+str(i)+'}{i:11139}{i:'+str(x+r[i][0])+'}{i:'+str(y+r[i][1])+'}{i:0}{s:"'+z+'"}{s:"0.47"}{i:0}{i:0}{s:"0"}{i:-1}{i:1}{i:25297484}')


def talk(txt):
    ext.send_to_client('{l}{h:'+TALK_IN+'}{i:50000}{s:"'+txt+'"}{i:0}{i:1}{i:0}{i:0}')


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


ext.intercept(Direction.TO_SERVER, walk, WALK)
ext.intercept(Direction.TO_SERVER, speech, TALK)
ext.intercept(Direction.TO_SERVER, reset, RESET)
ext.intercept(Direction.TO_SERVER, set_furni, USE_FURNI)
ext.intercept(Direction.TO_CLIENT, update_furni, FURNI_UPDATE)
