"""
room3.py – The Dreamcore Room
Puzzle piece decoration. Final hardest puzzle. Door centered at top platform.
"""
import pygame
import math
from game_data import BaseRoom, Player, Door, Puzzle, GameState


class Room3(BaseRoom):
    """Investigation-themed escape room. Door centered-top area. Correct answer: TOP option."""

    # Override floor since the door is on a raised area
    FLOOR_Y = 450

    def setup(self):
        self.bg = pygame.transform.scale(
            pygame.image.load("assets/backgrounds/room3_dreamcore.png"), (800, 600)
        )

        walk_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/characters/Walk ({i}).png"), (90, 100)
            )
            for i in range(1, 8)
        ]
        # Player starts centre-left
        self.player = Player(80, self.FLOOR_Y, walk_sprites)

        # Door placed in the CENTER of the screen (player must walk mid-room)
        door_img = pygame.transform.scale(
            pygame.image.load("assets/objects/door2.png"), (120, 180)
        )
        self.door = Door(340, self.FLOOR_Y - 80, door_img)

        # Puzzle piece decoration near door
        pp_img = pygame.transform.scale(
            pygame.image.load("assets/objects/puzzle_piece.png"), (55, 55)
        )
        self.puzzle_piece_img = pp_img
        self.puzzle_piece_rect = pygame.Rect(490, self.FLOOR_Y - 10, 55, 55)

        # Hardest puzzle – correct answer is the TOP option (index 0)
        self.puzzle = Puzzle(
            question="What does range(2,8,2) produce?",
            options=["[2, 4, 6]", "[2, 4, 6, 8]", "[0, 2, 4, 6]"],   # correct = top
            correct="[2, 4, 6]",
            bg_color=(40, 30, 80),
        )

        self.time_elapsed = 0

    def extra_update(self):
        self.time_elapsed += 1

        if self.door.locked and self.door.is_player_at_door(self.player) and not self.puzzle.active:
            self.puzzle.activate()
            self.gs.pause_timer()

        if self.puzzle.solved and self.door.locked:
            self.door.unlock()
            self.gs.add_score(50)
            self.gs.resume_timer()

    def extra_draw(self):
        # Puzzle piece decoration
        self.screen.blit(self.puzzle_piece_img, self.puzzle_piece_rect)

        # Floating particles loop has been removed to simplify the scene

        # UI Hints
        if not self.puzzle.active and self.door.locked:
            hint = self.font_sm.render("✨  Walk to the centre door for the final puzzle!", True, (200, 180, 255))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))
        elif not self.door.locked:
            hint = self.font_sm.render("🌟  You're free! Step through to victory!", True, (255, 255, 100))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))

        label = self.font_sm.render("Room 3 – The Investigation Portal", True, (200, 180, 255))
        self.screen.blit(label, (250, 570))


def run_room3(screen, clock, game_state: GameState) -> str:
    room = Room3(screen, clock, game_state, next_state="VICTORY")
    return room.run()
