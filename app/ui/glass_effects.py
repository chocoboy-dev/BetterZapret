import ctypes
from ctypes import wintypes

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_SYSTEMBACKDROP_TYPE = 38
DWMWA_BORDER_COLOR = 34
DWMWA_CAPTION_COLOR = 35
DWMWA_TEXT_COLOR = 36
DWMWA_MICA_EFFECT = 1029
DWMWA_WINDOW_CORNER_PREFERENCE = 33

DWMSBT_AUTO = 0
DWMSBT_NONE = 1
DWMSBT_MAINWINDOW = 2
DWMSBT_TRANSIENTWINDOW = 3
DWMSBT_TABBEDWINDOW = 4

DWMWCP_DEFAULT = 0
DWMWCP_DONOTROUND = 1
DWMWCP_ROUND = 2
DWMWCP_ROUNDSMALL = 3


def enable_acrylic(hwnd: int):
    dwm = ctypes.windll.dwmapi
    hwnd = wintypes.HWND(hwnd)

    value = ctypes.c_int(DWMSBT_TRANSIENTWINDOW)
    result = dwm.DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(value), ctypes.sizeof(value))

    if result != 0:
        value = ctypes.c_int(DWMSBT_MAINWINDOW)
        dwm.DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(value), ctypes.sizeof(value))

    dark = ctypes.c_int(1)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(dark), ctypes.sizeof(dark))

    border = ctypes.c_int(0x00000000)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_BORDER_COLOR, ctypes.byref(border), ctypes.sizeof(border))

    caption = ctypes.c_int(0x00000000)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(caption), ctypes.sizeof(caption))

    text = ctypes.c_int(0x00FFFFFF)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_TEXT_COLOR, ctypes.byref(text), ctypes.sizeof(text))


def enable_rounded_corners(hwnd: int):
    dwm = ctypes.windll.dwmapi
    hwnd = wintypes.HWND(hwnd)
    value = ctypes.c_int(DWMWCP_ROUND)
    dwm.DwmSetWindowAttribute(hwnd, DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(value), ctypes.sizeof(value))
