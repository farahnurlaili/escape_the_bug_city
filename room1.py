"""
room1.py – The Witchy Room
Collect the key → solve puzzle at the door → exit LEFT side.
"""
import pygame
from game_data import BaseRoom, Player, Door, Collectible, Puzzle, GameState


class Room1(BaseRoom):
    """Witchy-themed escape room. Door on the RIGHT. Correct answer: CENTER option."""

    def setup(self):
        self.bg = pygame.transform.scale(
            pygame.image.load("assets/backgrounds/room1_witchy.png"), (800, 600)
        )

        walk_sprites = [
            pygame.transform.scale(
                pygame.image.load(f"assets/characters/Walk ({i}).png"), (90, 100)
            )
            for i in range(1, 8)
        ]
        # Player starts LEFT side
        self.player = Player(60, self.FLOOR_Y, walk_sprites)

        # Door on the RIGHT side
        door_img = pygame.transform.scale(
            pygame.image.load("assets/objects/door.png"), (120, 180)
        )
        self.door = Door(670, self.FLOOR_Y - 80, door_img)

        # Key placed in the middle of the room
        key_img = pygame.transform.scale(
            pygame.image.load("assets/objects/key.png"), (50, 50)
        )
        self.key = Collectible(350, self.FLOOR_Y + 50, key_img, "Key")
        self.collectibles = [self.key]

        # Intermediate puzzle – correct answer is the CENTER option (index 1)
        self.puzzle = Puzzle(
            question="What does len([1, 2, 3]) return?",
            options=["2", "3", "4"],        # correct = "3" (middle)
            correct="3",
            bg_color=(50, 30, 70),
        )

    def extra_update(self):
        if self.key.check_pickup(self.player):
            self.gs.add_score(10)

        if self.key.collected and self.door.locked:
            if self.door.is_player_at_door(self.player) and not self.puzzle.active:
                self.puzzle.activate()
                self.gs.pause_timer()

        if self.puzzle.solved and self.door.locked:
            self.door.unlock()
            self.gs.resume_timer()

    def extra_draw(self):
        if not self.key.collected:
            hint = self.font_sm.render("🗝  Collect the key first!", True, (255, 230, 80))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))
        elif self.key.collected and self.door.locked and not self.puzzle.active:
            hint = self.font_sm.render("🚪  Reach the door on the right!", True, (180, 255, 180))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))
        elif not self.door.locked:
            hint = self.font_sm.render("✅  Puzzle solved! Step into the door!", True, (100, 255, 100))
            self.screen.blit(hint, hint.get_rect(center=(400, 80)))

        label = self.font_sm.render("Room 1 – The Witchy Chamber", True, (220, 180, 255))
        self.screen.blit(label, (250, 570))


def run_room1(screen, clock, game_state: GameState) -> str:
    room = Room1(screen, clock, game_state, next_state="PLAY_ROOM2")
    return room.run()
