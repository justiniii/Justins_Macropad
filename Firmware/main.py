import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.macros import Macros, Macro, Press, Release, Tap
from kmk.modules.layers import Layers
from kmk.extensions.RGB import RGB
from kmk.extensions.oled import Oled, OledData, OledDisplayMode

keyboard = KMKKeyboard()

# ── Direct pin wiring (each switch has its own GPIO) ──────────────────────────
# SW1=D10=GP4, SW2=D9=GP3, SW3=D8=GP2, SW4=D7=GP1, SW5=D2=GP28
keyboard.modules.append(Macros())
keyboard.modules.append(Layers())

keyboard.matrix = KeysScanner(
    pins=[
        board.GP4,   # SW1
        board.GP3,   # SW2
        board.GP2,   # SW3
        board.GP1,   # SW4
        board.GP28,  # SW5
    ]
)

# ── RGB (6x SK6812MINI on GP27) ───────────────────────────────────────────────
rgb = RGB(
    pixel_pin=board.GP27,
    num_pixels=6,
    val_limit=150,       # cap brightness (SK6812MINI get hot at full power)
    hue_default=0,
    sat_default=255,
    val_default=80,
)
keyboard.extensions.append(rgb)

# ── OLED (SSD1306 on SDA=GP6, SCL=GP7) ───────────────────────────────────────
oled = Oled(
    OledData(
        corner_one={0: OledDisplayMode.TXT, 1: ["MACROPAD"]},
        corner_two={0: OledDisplayMode.TXT, 1: ["Layer:"]},
        corner_three={0: OledDisplayMode.TXT, 1: ["SW1-SW5"]},
        corner_four={0: OledDisplayMode.TXT, 1: ["KMK Ready"]},
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled)

# ── Layers ────────────────────────────────────────────────────────────────────
# Layer 0 = Base
# Layer 1 = Fn (hold SW5)

SW5_FN = KC.MO(1)   # hold SW5 to access Fn layer

keyboard.keymap = [
    # Layer 0 — Base
    # Change KC.A / KC.B etc. to whatever you want!
    [
        KC.A,     # SW1
        KC.B,     # SW2
        KC.C,     # SW3
        KC.D,     # SW4
        SW5_FN,   # SW5 — hold for Fn
    ],
    # Layer 1 — Fn (hold SW5)
    [
        KC.RGB_TOG,  # SW1 — toggle RGB on/off
        KC.RGB_MOD,  # SW2 — cycle RGB animation
        KC.RGB_HUI,  # SW3 — hue up
        KC.RGB_SAI,  # SW4 — saturation up
        KC.TRNS,     # SW5 — (held)
    ],
]

if __name__ == "__main__":
    keyboard.go()
