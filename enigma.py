# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from ast import Num
from base64 import encode
from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:                          # A, B, C 중 하나
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:                    # I, II, III 중 3개 선택
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:                       # A~Z중 3개가 들어감
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A')) # 0~25까지 중 하나가 들어감

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper(): # 두 글자 + 모두 대문자
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    if reverse == False:
        for i in range(2, -1, -1):
            num = ord(input) - ord('A') + SETTINGS["WHEEL_POS"][i]
            if num > 25 :
                num -= 26
            else :
                pass
            input = SETTINGS["WHEELS"][i]["wire"][num] 

        return input

    else :
        for i in range(3):
            num = SETTINGS["WHEELS"][i]["wire"].index(input)
            num += SETTINGS["WHEEL_POS"][i]
            if num > 25 :
                num -= 26
            else :
                pass
            input = SETTINGS["ETW"][num]
        return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    # 한 글자가 입력될 때 마다 right 휠의 position +1
    # right 휠이 한 바퀴를 돌게되면 middle 휠의 position + 1
    # middle 휠도 한 바퀴를 돌게되면 left 휠의 position + 1
    SETTINGS["WHEEL_POS"][2] + 1
    if not count == 0 and count % 26 == 0:
        SETTINGS["WHEEL_POS"][1] = chr(ord(SETTINGS["WHEEL_POS"][1]) + 1)
    elif not count == 0 and count % 676 == 0:
        SETTINGS["WHEEL_POS"][0] = chr(ord(SETTINGS["WHEEL_POS"][0]) + 1)
    else :
        pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")
count = 0

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext: # plaintext의 한 글자씩 가져와 암호화 작업
    count += 1
    rotate_wheels()

    encoded_ch = ch
    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch) # 입력 신호는 오른쪽에서 왼쪽으로
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True) # 반사판에 맞고 돌아온 신호는 왼쪽에서 오른쪽으로
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')