#!/usr/bin/python

import commands
import serial, sys
import threading, time

import xbmc
import xbmcaddon

import json
import urllib2


__addon__ = xbmcaddon.Addon()
__setting__ = __addon__.getSetting
__addon_id__ = __addon__.getAddonInfo('id')
__localize__ = __addon__.getLocalizedString


class MyMonitor( xbmc.Monitor ):
    def __init__( self, *args, **kwargs ):
        xbmc.Monitor.__init__( self )

    def onSettingsChanged( self ):
        load_addon_settings()


def load_addon_settings():
    global p0_bright, p0_fade, p0_color, p1_bright, p1_fade, p1_color
    global r0_bright, r0_fade, r0_color, r1_bright, r1_fade, r1_color
    global sleep_time, kodi_ssl, kodi_server, kodi_username, kodi_password

    ############################################################################
    # Sleep time between status polls:
    ############################################################################
    try:
        sleep_time = int(__setting__('sleep_time'))
    except ValueError:
        sleep_time = 5

    if (sleep_time < 0):
        sleep_time = 0

    ############################################################################
    # Kodi IP address and credentials:
    ############################################################################
    try:
        kodi_ssl = __setting__('kodi_ssl')
    except ValueError:
        kodi_ssl = 'false'

    try:
        kodi_server = __setting__('kodi_server')
    except ValueError:
        kodi_server = "localhost"

    try:
        kodi_username = __setting__('kodi_username')
    except ValueError:
        kodi_username = ""

    try:
        kodi_password = __setting__('kodi_password')
    except ValueError:
        kodi_password = ""

    ############################################################################
    # Normal state
    ############################################################################
    # Power LED Brightness
    try:
        p0_bright = int(__setting__('p0_bright'))
    except ValueError:
        p0_bright = 100

    if (p0_bright < 0):
        p0_bright = 0
    if (p0_bright > 100):
        p0_bright = 100

    ### Power LED Fade/Blink
    try:
        p0_fade = int(__setting__('p0_fade'))
    except ValueError:
        p0_fade = 0;

    if (p0_fade == 1):
        p0_fade = "blink_fast"
    elif (p0_fade == 2):
        p0_fade = "blink_medium"
    elif (p0_fade == 3):
        p0_fade = "blink_slow"
    elif (p0_fade == 4):
        p0_fade = "fade_fast"
    elif (p0_fade == 5):
        p0_fade = "fade_medium"
    elif (p0_fade == 6):
        p0_fade = "fade_slow"
    else:
        p0_fade = "off"

    ### Power LED Color
    try:
        p0_color = int(__setting__('p0_color'))
    except ValueError:
        p0_color = 0;

    if (p0_color == 1):
        p0_color = "amber"
    elif (p0_color == 2):
        p0_color = "blue"
    else:
        p0_color = "off"

    ############################################################################
    # Recording state
    ############################################################################
    ### Power LED Brightness
    try:
        p1_bright = int(__setting__('p1_bright'))
    except ValueError:
        p1_bright = 100
        
    if (p1_bright < 0):
        p1_bright = 0
    if (p1_bright > 100):
        p1_bright = 100

    ### Power LED Fade/Blink
    try:
        p1_fade = int(__setting__('p1_fade'))
    except ValueError:
        p1_fade = 0;

    if (p1_fade == 1):
        p1_fade = "blink_fast"
    elif (p1_fade == 2):
        p1_fade = "blink_medium"
    elif (p1_fade == 3):
        p1_fade = "blink_slow"
    elif (p1_fade == 4):
        p1_fade = "fade_fast"
    elif (p1_fade == 5):
        p1_fade = "fade_medium"
    elif (p1_fade == 6):
        p1_fade = "fade_slow"
    else:
        p1_fade = "off"

    ### Power LED Color
    try:
        p1_color = int(__setting__('p1_color'))
    except ValueError:
        p1_color = 0;

    if (p1_color == 1):
        p1_color = "amber"
    elif (p1_color == 2):
        p1_color = "blue"
    else:
        p1_color = "off"

    ############################################################################
    # Normal state
    ############################################################################
    ### Ring LED Brightness
    try:
        r0_bright = int(__setting__('r0_bright'))
    except ValueError:
        r0_bright = 100

    if (r0_bright < 0):
        r0_bright = 0
    if (r0_bright > 100):
        r0_bright = 100

    ### Ring LED Fade/Blink
    try:
        r0_fade = int(__setting__('r0_fade'))
    except ValueError:
        r0_fade = 0;

    if (r0_fade == 1):
        r0_fade = "blink_fast"
    elif (r0_fade == 2):
        r0_fade = "blink_medium"
    elif (r0_fade == 3):
        r0_fade = "blink_slow"
    elif (r0_fade == 4):
        r0_fade = "fade_fast"
    elif (r0_fade == 5):
        r0_fade = "fade_medium"
    elif (r0_fade == 6):
        r0_fade = "fade_slow"
    else:
        r0_fade = "off"

    ### Ring LED Color
    try:
        r0_color = int(__setting__('r0_color'))
    except ValueError:
        r0_color = 0;

    if (r0_color == 1):
        r0_color = "cyan"
    elif (r0_color == 2):
        r0_color = "blue"
    elif (r0_color == 3):
        r0_color = "green"
    elif (r0_color == 4):
        r0_color = "pink"
    elif (r0_color == 5):
        r0_color = "red"
    elif (r0_color == 6):
        r0_color = "white"
    elif (r0_color == 7):
        r0_color = "yellow"
    else:
        r0_color = "off"

    ############################################################################
    # Recording state
    ############################################################################
    ### Ring LED Brightness
    try:
        r1_bright = int(__setting__('r1_bright'))
    except ValueError:
        r1_bright = 100

    if (r1_bright < 0):
        r1_bright = 0
    if (r1_bright > 100):
        r1_bright = 100

    ### Ring LED Fade/Blink
    try:
        r1_fade = int(__setting__('r1_fade'))
    except ValueError:
        r1_fade = 0;

    if (r1_fade == 1):
        r1_fade = "blink_fast"
    elif (r1_fade == 2):
        r1_fade = "blink_medium"
    elif (r1_fade == 3):
        r1_fade = "blink_slow"
    elif (r1_fade == 4):
        r1_fade = "fade_fast"
    elif (r1_fade == 5):
        r1_fade = "fade_medium"
    elif (r1_fade == 6):
        r1_fade = "fade_slow"
    else:
        r1_fade = "off"

    ### Ring LED Color
    try:
        r1_color = int(__setting__('r1_color'))
    except ValueError:
        r1_color = 0;

    if (r1_color == 1):
        r1_color = "cyan"
    elif (r1_color == 2):
        r1_color = "blue"
    elif (r1_color == 3):
        r1_color = "green"
    elif (r1_color == 4):
        r1_color = "pink"
    elif (r1_color == 5):
        r1_color = "red"
    elif (r1_color == 6):
        r1_color = "white"
    elif (r1_color == 7):
        r1_color = "yellow"
    else:
        r1_color = "off"

    return


def json_request(kodi_request, ssl, host, username, password):
    PORT   =    8080
    if ssl == "true":
        URL = "https://"
    else:
        URL = "http://"
    if username != '' and password != '':
        URL = URL + username + ":" + password + "@"
    URL = URL + host + ':' + str(PORT) + '/jsonrpc'
    HEADER = {'Content-Type': 'application/json'}

    if host == 'localhost':
        response = xbmc.executeJSONRPC(json.dumps(kodi_request))
        if response:
            return json.loads(response.decode('utf-8','mixed'))

    request = urllib2.Request(URL, json.dumps(kodi_request), HEADER)
    with closing(urllib2.urlopen(request)) as response:
        return json.loads(response.read().decode('utf-8', 'mixed'))


def is_recording():
    result = False
    #http://192.168.178.12:8080/jsonrpc?request={ "jsonrpc": "2.0", "method": "PVR.GetProperties", "params": { "properties": [ "recording" ] }, "id": 1 }
    PVR_GET_PROPERTIES = {
        'jsonrpc': '2.0',
        'method': 'PVR.GetProperties',
        'params': {
            'properties': ['recording']
            },
        'id': 1
    }

    try:
        data = json_request(PVR_GET_PROPERTIES, kodi_ssl, kodi_server, kodi_username, kodi_password)
        if data['result']:
            result = data['result']['recording']
    except KeyError:
        pass

    return result


def set_nuc_led(bright, fade, color, led):
    line = led + "," + str(bright) + ',' + fade + "," + color
    try:
        file = open("/proc/acpi/nuc_led", "w")
        file.write(line)
        file.close
    except:
        pass


if __name__ == '__main__':

    monitor = MyMonitor()
    xbmc.log(msg='[{}] Addon started.'.format(__addon_id__), level=xbmc.LOGNOTICE)
    load_addon_settings()

    set_nuc_led(p0_bright, p0_fade, p0_color, "power")
    set_nuc_led(r0_bright, r0_fade, r0_color, "ring")

    while not monitor.abortRequested():
        if is_recording():
            set_nuc_led(p1_bright, p1_fade, p1_color, "power")
            set_nuc_led(r1_bright, r1_fade, r1_color, "ring")
        else:
            set_nuc_led(p0_bright, p0_fade, p0_color, "power")
            set_nuc_led(r0_bright, r0_fade, r0_color, "ring")
        if monitor.waitForAbort(float(sleep_time)):
            break
#else:
#    load_addon_settings()
