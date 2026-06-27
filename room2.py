"""
room2.py – The Horror Room
Candle decoration near door. Solve puzzle → exit through TOP-LEFT door.
"""
import pygame
from game_data import BaseRoom, Player, Door, Puzzle, GameState


class Room2(BaseRoom):
    """Horror-themed escape room. Door on the LEFT side, elevated. Correct answer: BOTTOM option."""

    def setup(self):
        self.bg = pygame.transform.scale(
            pygame.image.load("assets/backgrounds/room2_horror.png"), (800, 600)
        )

        walk_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/characters/Walk ({i}).png"), (90, 100)
            )
            for i in range(1, 8)
        ]
        # Player starts on the RIGHT side this time
        self.player = Player(660, self.FLOOR_Y, walk_sprites)

        # Door on the LEFT side, slightly elevated (on a platform feel)
        door_img = pygame.transform.scale(
            pygame.image.load("assets/objects/door1.png"), (120, 180)
        )
        self.door = Door(20, self.FLOOR_Y - 80, door_img)

        # Candle near the door (decorative)
        candle_img = pygame.transform.scale(
            pygame.image.load("assets/objects/candle.png"), (38, 58)
        )
        self.candle_img = candle_img
        self.candle_rect = pygame.Rect(150, self.FLOOR_Y - 5, 38, 58)

        # Intermediate puzzle – correct answer is the BOTTOM option (index 2)
        self.puzzle = Puzzle(
            question="Which is mutable in Python?",
            options=["tuple", "string", "list"],   # correct = "list" (bottom)
            correct="list",
            bg_color=(70, 20, 20),
        )

        self.symbols = [
            (480, 400, "👁"),
            (560, 420, "💀"),
            (620, 390, "🕷"),
        ]

    def extra_update(self):
        if self.door.locked and self.door.is_player_at_door(self.player) and not self.puzzle.active:
            self.puzzle.activate()
            self.gs.pause_timer()

        if self.puzzle.solved and self.door.locked:
            self.door.unlock()
            self.gs.resume_timer()

    def extra_draw(self):
        # Candle
        self.screen.blit(self.candle_img, self.candle_rect)

        # Spooky symbols (far right side, away from door)
        for sx, sy, sym in self.symbols:
            t = self.font_lg.render(sym, True, (200, 50, 50))
            self.screen.blit(t, (sx, sy))

        if not self.puzzle.active and self.door.locked:
            hint = self.font_sm.render("💀  Approach the door on the LEFT to proceed…", True, (255, 100, 100))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))
        elif not self.door.locked:
            hint = self.font_sm.render("✅  You survived! Step through the door!", True, (100, 255, 100))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))

        label = self.font_sm.render("Room 2 – The Horror Hall", True, (255, 120, 120))
        self.screen.blit(label, (290, 570))


def run_room2(screen, clock, game_state: GameState) -> str:
    room = Room2(screen, clock, game_state, next_state="PLAY_ROOM3")
    return room.run()
