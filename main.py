"""
main.py – Entry point for Escape Powered by Python
"""
import pygame
import sys
import math
import random

from game_data import GameState
from room1 import run_room1
from room2 import run_room2
from room3 import run_room3
from victory import run_victory, run_game_over

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape Powered by Python 🐍")
clock = pygame.time.Clock()

# ── Fonts ─────────────────────────────────────────────────────────────────────
TITLE_FONT = pygame.font.SysFont("impact", 62)
BTN_FONT   = pygame.font.SysFont("arialblack", 24)
SUB_FONT   = pygame.font.SysFont("arialblack", 18)
INFO_FONT  = pygame.font.SysFont("arial", 20)

# ── BGM ───────────────────────────────────────────────────────────────────────
HAS_MUSIC = False
try:
    pygame.mixer.music.load("assets/sounds/creepy_cartoon.mpeg")
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)
    HAS_MUSIC = True
except Exception:
    pass

sound_on = True   # global toggle

def apply_sound():
    """Mute / unmute based on sound_on flag."""
    if not HAS_MUSIC:
        return
    pygame.mixer.music.set_volume(0.35 if sound_on else 0.0)

# ── Language strings ──────────────────────────────────────────────────────────
STRINGS = {
    "English": {
        "title": "ESCAPE THE BUG CITY",
        "start": "Start Game",
        "instr": "Instructions",
        "lang":  "Language: EN",
        "exit":  "Exit",
        "how":   "HOW TO PLAY",
        "lines": [
            "🎮  Arrow Keys to move  |  ↑ to jump",
            "🗝   Room 1: Collect the key, then reach the door",
            "🕯   Room 2: Door is on the LEFT side",
            "🧩  Room 3: Door is in the CENTRE of the room",
            "🐍  Solve the Python puzzle at each door",
            "❤️   3 lives – wrong answers cost 1 life",
            "⏱   Only 15 seconds per room – be quick!",
            "⏸   Press ESC to pause / resume",
            "",
            "Click anywhere to return to the menu",
        ],
        "back":  "← Back",
    },
    "Bahasa": {
        "title": "ESCAPE THE BUG CITY",
        "start": "Mula Permainan",
        "instr": "Arahan",
        "lang":  "Bahasa: BM",
        "exit":  "Keluar",
        "how":   "CARA BERMAIN",
        "lines": [
            "🎮  Anak Panah untuk bergerak  |  ↑ untuk lompat",
            "🗝   Bilik 1: Ambil kunci, kemudian ke pintu",
            "🕯   Bilik 2: Pintu di sebelah KIRI",
            "🧩  Bilik 3: Pintu di TENGAH bilik",
            "🐍  Selesaikan teka-teki Python di setiap pintu",
            "❤️   3 nyawa – jawapan salah tolak 1 nyawa",
            "⏱   Hanya 15 saat setiap bilik – cepat!",
            "⏸   Tekan ESC untuk jeda / teruskan",
            "",
            "Klik untuk kembali ke menu",
        ],
        "back":  "← Kembali",
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def draw_button(surface, rect, label, font, base_col, hover_col):
    mp = pygame.mouse.get_pos()
    col = hover_col if rect.collidepoint(mp) else base_col
    pygame.draw.rect(surface, col, rect, border_radius=16)
    pygame.draw.rect(surface, (200, 200, 255), rect, 2, border_radius=16)
    t = font.render(label, True, (255, 255, 255))
    surface.blit(t, t.get_rect(center=rect.center))

# ── Menu drawing ──────────────────────────────────────────────────────────────
def draw_menu(t: int, language: str) -> list:
    """Draw animated menu. Returns list of (rect, key) for click detection."""
    mouse_pos = pygame.mouse.get_pos()

    # Gradient bg
    for y in range(HEIGHT):
        r = int(20 + 30 * y / HEIGHT)
        g = int(10 + 20 * y / HEIGHT)
        b = int(60 + 60 * y / HEIGHT)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    # Floating particles
    random.seed(0)
    for i in range(30):
        px = (random.randint(0, 800) + t * (i % 3 + 1) // 2) % 800
        py = (random.randint(0, 600) + t * ((i % 4) + 1) // 3) % 600
        alpha = abs(math.sin(t * 0.04 + i))
        c = (int(100 * alpha), int(80 * alpha), int(200 * alpha))
        pygame.draw.circle(screen, c, (px, py), 2)

    # Snake strip
    sn = SUB_FONT.render("🐍  " * 5, True, (80, 220, 80))
    screen.blit(sn, sn.get_rect(center=(WIDTH // 2, 115)))

    # Title shadow + title
    for ox, oy in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
        sh = TITLE_FONT.render(STRINGS[language]["title"], True, (80, 40, 0))
        screen.blit(sh, sh.get_rect(center=(WIDTH // 2 + ox, 70 + oy)))
    title = TITLE_FONT.render(STRINGS[language]["title"], True, (255, 215, 50))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

    sub = SUB_FONT.render("A Python Escape Room Adventure", True, (180, 180, 255))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 135)))

    # Main buttons (5 rows now: start, instructions, sound, language, exit)
    sound_label = (
        ("🔊  Sound: ON"  if sound_on else "🔇  Sound: OFF")
        if language == "English"
        else ("🔊  Bunyi: ON" if sound_on else "🔇  Bunyi: OFF")
    )

    btn_data = [
        (STRINGS[language]["start"], "START", (50, 130, 50),  (70, 190, 70)),
        (STRINGS[language]["instr"], "INSTR", (50, 80,  160), (70, 120, 220)),
        (sound_label,                "SOUND", (30, 100, 110), (40, 150, 160)),
        (STRINGS[language]["lang"],  "LANG",  (100, 60, 120), (150, 90, 180)),
        (STRINGS[language]["exit"],  "EXIT",  (130, 40,  40), (200, 60,  60)),
    ]

    buttons = []
    for i, (label, key, col, hov) in enumerate(btn_data):
        rect = pygame.Rect(WIDTH // 2 - 150, 165 + i * 68, 300, 54)
        draw_button(screen, rect, label, BTN_FONT, col, hov)
        buttons.append((rect, key))

    # Version stamp
    ver = SUB_FONT.render("SWC3643-0526", True, (100, 100, 140))
    screen.blit(ver, ver.get_rect(bottomright=(WIDTH - 10, HEIGHT - 5)))

    return buttons


def draw_instructions(language: str):
    screen.fill((15, 15, 40))
    heading = TITLE_FONT.render(STRINGS[language]["how"], True, (255, 215, 50))
    screen.blit(heading, heading.get_rect(center=(WIDTH // 2, 55)))
    pygame.draw.line(screen, (80, 80, 180), (80, 100), (720, 100), 2)

    for i, line in enumerate(STRINGS[language]["lines"]):
        col = (220, 255, 220) if line.startswith("🐍") else (255, 255, 200)
        surf = INFO_FONT.render(line, True, col)
        screen.blit(surf, surf.get_rect(midleft=(80, 120 + i * 38)))

    back = BTN_FONT.render(STRINGS[language]["back"], True, (180, 180, 255))
    screen.blit(back, back.get_rect(center=(WIDTH // 2, 555)))


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    global sound_on

    state    = "MENU"
    language = "English"
    game_state = GameState()
    t = 0

    while True:
        t += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    buttons = draw_menu(t, language)
                    for rect, key in buttons:
                        if rect.collidepoint(event.pos):
                            if key == "START":
                                game_state.reset()
                                state = "PLAY_ROOM1"
                            elif key == "INSTR":
                                state = "INSTRUCTIONS"
                            elif key == "SOUND":
                                sound_on = not sound_on
                                apply_sound()
                            elif key == "LANG":
                                language = "Bahasa" if language == "English" else "English"
                            elif key == "EXIT":
                                pygame.quit(); sys.exit()

                elif state == "INSTRUCTIONS":
                    state = "MENU"

        # ── State machine ─────────────────────────
        if state == "MENU":
            draw_menu(t, language)

        elif state == "INSTRUCTIONS":
            draw_instructions(language)

        elif state == "PLAY_ROOM1":
            result = run_room1(screen, clock, game_state)
            state  = result if result else "MENU"
            continue

        elif state == "PLAY_ROOM2":
            result = run_room2(screen, clock, game_state)
            state  = result if result else "MENU"
            continue

        elif state == "PLAY_ROOM3":
            result = run_room3(screen, clock, game_state)
            state  = result if result else "MENU"
            continue

        elif state == "VICTORY":
            result = run_victory(screen, clock, game_state)
            state  = result if result else "MENU"
            continue

        elif state == "GAME_OVER":
            result = run_game_over(screen, clock, game_state)
            state  = result if result else "MENU"
            continue

        elif state == "QUIT":
            pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
