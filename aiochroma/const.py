"""Constants module"""

import re

from .dataclass import Color, Key

CREDENTIALS = '{"title":"AIOChroma","description":"Async Python library for remote control of Razer Chroma","author":{"name":"Yevhenii Vaskivskyi","contact":"https://github.com/Vaskivskyi/aiochroma"},"device_supported":["keyboard","mouse","headset","mousepad","keypad","chromalink"],"category":"application"}'

DEFAULT_SLEEP = 0.5
DEFAULT_SPACING = 0.5
DEFAULT_BRIGHTNESS = 255
DEFAULT_COLOR = Color(255, 255, 0)

HEADERS = {
    "Host": "chromasdk.io",
    "content-type": "application/json",
}

### CHROMA PARAMETERS -->

KEY_HEADSET = "headset"
KEY_KEYBOARD = "keyboard"
KEY_KEYPAD = "keypad"
KEY_LINK = "chromalink"
KEY_MOUSE = "mouse"
KEY_MOUSEPAD = "mousepad"

CHROMA_TARGETS = [
    KEY_HEADSET,
    KEY_KEYBOARD,
    KEY_KEYPAD,
    KEY_LINK,
    KEY_MOUSE,
    KEY_MOUSEPAD,
]

EFFECT_CUSTOM = "CHROMA_CUSTOM"
EFFECT_NONE = "CHROMA_NONE"
EFFECT_STATIC = "CHROMA_STATIC"

CHROMA_EFFECT = "effect"
CHROMA_PARAM = "param"

CHROMA_KEYBOARD_HEIGHT = 6
CHROMA_KEYBOARD_WIDTH = 22

### <-- CHROMA PARAMETERS

### CHROMA EFFECTS -->

# Keyboard sequence
KEYBOARD_SEQUENCE: dict[str, str] = {
    "arrow_left": "lkjhgf6tv ",
    "arrow_right": "sdfghj6yn ",
}
KEYBOARD_SEQUENCE_LOAD = "{Num8}{Num9}{Num6}{Num3}{Num2}{Num1}{Num4}{Num7}"
KEYBOARD_SEQUENCE_LOAD_CCW = "{Num8}{Num7}{Num4}{Num1}{Num2}{Num3}{Num6}{Num9}"
KEYBOARD_SEQUENCE_LOAD_LARGE = (
    "{NumLock}{Num/}{Num*}{Num-}{Num+}{NumEnter}{Num.}{Num0}{Num1}{Num4}{Num7}"
)
KEYBOARD_SEQUENCE_LOAD_ALPHA = "1234567890-=]'/.,mnbvcxzaq"
KEYBOARD_SEQUENCE_LOAD_ALPHA_CCW = "1qazxcvbnm,./']=-098765432"

### <-- CHROMA EFFECTS

KEYREG = re.compile("\{[A-Za-z0-9./*\-\+]+\}")

DEFAULT_PORT = 54236

URL = "https://{}:{}/{}"
URL_MAIN = "razer/chromasdk"

### KEY POSITIONS -->

KEY_CODES = {
    "Esc": Key(0, 1),
    "F1": Key(0, 3),
    "F2": Key(0, 4),
    "F3": Key(0, 5),
    "F4": Key(0, 6),
    "F5": Key(0, 7),
    "F6": Key(0, 8),
    "F7": Key(0, 9),
    "F8": Key(0, 10),
    "F9": Key(0, 11),
    "F10": Key(0, 12),
    "F11": Key(0, 13),
    "F12": Key(0, 14),
    "PrtSc": Key(0, 15),
    "ScrLk": Key(0, 16),
    "Pause": Key(0, 17),
    "Multi": Key(0, 18),
    "Volume": Key(0, 21),
    "`": Key(1, 1),
    "1": Key(1, 2),
    "2": Key(1, 3),
    "3": Key(1, 4),
    "4": Key(1, 5),
    "5": Key(1, 6),
    "6": Key(1, 7),
    "7": Key(1, 8),
    "8": Key(1, 9),
    "9": Key(1, 10),
    "0": Key(1, 11),
    "-": Key(1, 12),
    "=": Key(1, 13),
    "Backspace": Key(1, 14),
    "Ins": Key(1, 15),
    "Home": Key(1, 16),
    "PgUp": Key(1, 17),
    "NumLock": Key(1, 18),
    "Num/": Key(1, 19),
    "Num*": Key(1, 20),
    "Num-": Key(1, 21),
    "Tab": Key(2, 1),
    "q": Key(2, 2),
    "w": Key(2, 3),
    "e": Key(2, 4),
    "r": Key(2, 5),
    "t": Key(2, 6),
    "y": Key(2, 7),
    "u": Key(2, 8),
    "i": Key(2, 9),
    "o": Key(2, 10),
    "p": Key(2, 11),
    "[": Key(2, 12),
    "]": Key(2, 13),
    "\\": Key(2, 14),
    "Del": Key(2, 15),
    "End": Key(2, 16),
    "PgDn": Key(2, 17),
    "Num7": Key(2, 18),
    "Num8": Key(2, 19),
    "Num9": Key(2, 20),
    "Num+": Key(2, 21),
    "CapsLock": Key(3, 1),
    "a": Key(3, 2),
    "s": Key(3, 3),
    "d": Key(3, 4),
    "f": Key(3, 5),
    "g": Key(3, 6),
    "h": Key(3, 7),
    "j": Key(3, 8),
    "k": Key(3, 9),
    "l": Key(3, 10),
    ";": Key(3, 11),
    "'": Key(3, 12),
    "Enter": Key(3, 14),
    "Num4": Key(3, 18),
    "Num5": Key(3, 19),
    "Num6": Key(3, 20),
    "Shift": Key(4, 1),
    "z": Key(4, 3),
    "x": Key(4, 4),
    "c": Key(4, 5),
    "v": Key(4, 6),
    "b": Key(4, 7),
    "n": Key(4, 8),
    "m": Key(4, 9),
    ",": Key(4, 10),
    ".": Key(4, 11),
    "/": Key(4, 12),
    "RShift": Key(4, 14),
    "Up": Key(4, 16),
    "Num1": Key(4, 18),
    "Num2": Key(4, 19),
    "Num3": Key(4, 20),
    "NumEnter": Key(4, 21),
    "Ctrl": Key(5, 1),
    "Win": Key(5, 2),
    "Alt": Key(5, 3),
    "Space": Key(5, 7),
    "RAlt": Key(5, 11),
    "Fn": Key(5, 12),
    "Menu": Key(5, 13),
    "RCtrl": Key(5, 14),
    "Left": Key(5, 15),
    "Down": Key(5, 16),
    "Right": Key(5, 17),
    "Num0": Key(5, 19),
    "Num.": Key(5, 20),
}

### <-- KEY POSITIONS

### LAYOUTS -->

LAYOUT = dict()

LAYOUT["EN_US"] = {
    "Esc": ["Esc"],
    "F1": ["F1"],
    "F2": ["F2"],
    "F3": ["F3"],
    "F4": ["F4"],
    "F5": ["F5"],
    "F6": ["F6"],
    "F7": ["F7"],
    "F8": ["F8"],
    "F9": ["F9"],
    "F10": ["F10"],
    "F11": ["F11"],
    "F12": ["F12"],
    "PrtSc": ["PrtSc"],
    "ScrLk": ["ScrLk"],
    "Pause": ["Pause"],
    "Multi": ["Multi"],
    "Volume": ["Volume"],
    "`": ["`"],
    "~": ["Shift", "`"],
    "1": ["1"],
    "!": ["Shift", "1"],
    "2": ["2"],
    "@": ["Shift", "2"],
    "3": ["3"],
    "#": ["Shift", "3"],
    "4": ["4"],
    "$": ["Shift", "4"],
    "5": ["5"],
    "%": ["Shift", "5"],
    "6": ["6"],
    "^": ["Shift", "6"],
    "7": ["7"],
    "&": ["Shift", "7"],
    "8": ["8"],
    "*": ["Shift", "8"],
    "9": ["9"],
    "(": ["Shift", "9"],
    "0": ["0"],
    ")": ["Shift", "0"],
    "-": ["-"],
    "_": ["Shift", "-"],
    "=": ["="],
    "+": ["Shift", "="],
    "Backspace": ["Backspace"],
    "Ins": ["Ins"],
    "Home": ["Home"],
    "PgUp": ["PgUp"],
    "NumLock": ["NumLock"],
    "Num/": ["Num/"],
    "Num*": ["Num*"],
    "Num-": ["Num-"],
    "Tab": ["Tab"],
    "q": ["q"],
    "Q": ["Shift", "q"],
    "w": ["w"],
    "W": ["Shift", "w"],
    "e": ["e"],
    "E": ["Shift", "e"],
    "r": ["r"],
    "R": ["Shift", "r"],
    "t": ["t"],
    "T": ["Shift", "t"],
    "y": ["y"],
    "Y": ["Shift", "y"],
    "u": ["u"],
    "U": ["Shift", "u"],
    "i": ["i"],
    "I": ["Shift", "i"],
    "o": ["o"],
    "O": ["Shift", "o"],
    "p": ["p"],
    "P": ["Shift", "p"],
    "[": ["["],
    "{": ["Shift", "["],
    "]": ["]"],
    "}": ["Shift", "]"],
    "\\": ["\\"],
    "|": ["Shift", "\\"],
    "Del": ["Del"],
    "End": ["End"],
    "PgDn": ["PgDn"],
    "Num7": ["Num7"],
    "Num8": ["Num8"],
    "Num9": ["Num9"],
    "Num+": ["Num+"],
    "CapsLock": ["CapsLock"],
    "a": ["a"],
    "A": ["Shift", "a"],
    "s": ["s"],
    "S": ["Shift", "s"],
    "d": ["d"],
    "D": ["Shift", "d"],
    "f": ["f"],
    "F": ["Shift", "f"],
    "g": ["g"],
    "G": ["Shift", "g"],
    "h": ["h"],
    "H": ["Shift", "h"],
    "j": ["j"],
    "J": ["Shift", "j"],
    "k": ["k"],
    "K": ["Shift", "k"],
    "l": ["l"],
    "L": ["Shift", "l"],
    ";": [";"],
    ":": ["Shift", ";"],
    "'": ["'"],
    '"': ["Shift", "'"],
    "Enter": ["Enter"],
    "Num4": ["Num4"],
    "Num5": ["Num5"],
    "Num6": ["Num6"],
    "Shift": ["Shift"],
    "z": ["z"],
    "Z": ["Shift", "z"],
    "x": ["x"],
    "X": ["Shift", "x"],
    "c": ["c"],
    "C": ["Shift", "c"],
    "v": ["v"],
    "V": ["Shift", "v"],
    "b": ["b"],
    "B": ["Shift", "b"],
    "n": ["n"],
    "N": ["Shift", "n"],
    "m": ["m"],
    "M": ["Shift", "m"],
    ",": [","],
    "<": ["Shift", ","],
    ".": ["."],
    ">": ["Shift", "."],
    "/": ["/"],
    "?": ["Shift", "/"],
    "RShift": ["RShift"],
    "Up": ["Up"],
    "Num1": ["Num1"],
    "Num2": ["Num2"],
    "Num3": ["Num3"],
    "NumEnter": ["NumEnter"],
    "Ctrl": ["Ctrl"],
    "Win": ["Win"],
    "Alt": ["Alt"],
    "Space": ["Space"],
    " ": ["Space"],
    "RAlt": ["RAlt"],
    "Fn": ["Fn"],
    "Menu": ["Menu"],
    "RCtrl": ["RCtrl"],
    "Left": ["Left"],
    "Down": ["Down"],
    "Right": ["Right"],
    "Num0": ["Num0"],
    "Num.": ["Num."],
}

### <-- LAYOUTS
