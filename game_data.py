"""
game_data.py – Core OOP classes for Escape Powered by Python
"""
import pygame


# ─────────────────────────────────────────────
# Entity base class
# ─────────────────────────────────────────────
class Entity:
    """Base class for every visible game object."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    def draw(self, surface: pygame.Surface):
        raise NotImplementedError

    def get_rect(self) -> pygame.Rect:
        return self.rect


# ─────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────
class Player(Entity):
    """Animated, physics-enabled player character."""

    SPEED = 5
    JUMP_POWER = -16
    GRAVITY = 0.7
    FLOOR_Y = 450          # pixel y where player rests

    def __init__(self, x: int, y: int, sprites: list):
        super().__init__(x, y, 90, 100)
        self.sprites = sprites
        self.frame_index = 0.0
        self.velocity_y = 0
        self.is_jumping = False
        self.facing_right = True

    def handle_movement(self, keys):
        """Process keyboard input and apply physics."""
        moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.SPEED
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.SPEED
            self.facing_right = True
            moving = True

        # Boundary clamp
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))

        # Jump
        if not self.is_jumping and keys[pygame.K_UP]:
            self.is_jumping = True
            self.velocity_y = self.JUMP_POWER

        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.GRAVITY
            if self.rect.y >= self.FLOOR_Y:
                self.rect.y = self.FLOOR_Y
                self.is_jumping = False
                self.velocity_y = 0

        # Animation
        if moving:
            self.frame_index = (self.frame_index + 0.2) % len(self.sprites)
        else:
            self.frame_index = 0.0

    def draw(self, surface: pygame.Surface):
        frame = self.sprites[int(self.frame_index)]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, self.rect)


# ─────────────────────────────────────────────
# Collectible (Key, etc.)
# ─────────────────────────────────────────────
class Collectible(Entity):
    """An item that can be picked up by the player."""

    def __init__(self, x: int, y: int, image: pygame.Surface, label: str = ""):
        super().__init__(x, y, image.get_width(), image.get_height())
        self.image = image
        self.label = label
        self.collected = False

    def draw(self, surface: pygame.Surface):
        if self.visible and not self.collected:
            surface.blit(self.image, self.rect)

    def check_pickup(self, player: Player) -> bool:
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            return True
        return False


# ─────────────────────────────────────────────
# Door
# ─────────────────────────────────────────────
class Door(Entity):
    """Exit door – can be locked or unlocked."""

    def __init__(self, x: int, y: int, image: pygame.Surface):
        super().__init__(x, y, image.get_width(), image.get_height())
        self.image = image
        self.locked = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def unlock(self):
        self.locked = False

    def is_player_at_door(self, player: Player) -> bool:
        return self.rect.colliderect(player.rect)


# ─────────────────────────────────────────────
# Puzzle
# ─────────────────────────────────────────────
class Puzzle:
    """A multiple-choice Python question shown as an overlay."""

    def __init__(self, question: str, options: list[str], correct: str, bg_color=(50, 50, 80)):
        self.question = question
        self.options = options
        self.correct = correct
        self.bg_color = bg_color
        self.active = False
        self.solved = False
        self.feedback = ""
        self.feedback_timer = 0

    def activate(self):
        self.active = True

    def handle_click(self, pos, game_state) -> bool:
        """Returns True if answer was correct."""
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(220, 240 + i * 65, 360, 50)
            if rect.collidepoint(pos):
                if opt == self.correct:
                    self.solved = True
                    self.active = False
                    game_state.add_score(25)
                    return True
                else:
                    game_state.lose_life()
                    self.feedback = "Wrong! -1 Life"
                    self.feedback_timer = 90
        return False

    def draw(self, surface: pygame.Surface, font_sm, font_lg):
        if not self.active:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # Card
        card = pygame.Rect(160, 140, 480, 320)
        pygame.draw.rect(surface, self.bg_color, card, border_radius=24)
        pygame.draw.rect(surface, (200, 200, 255), card, 3, border_radius=24)

        # Question header
        pygame.draw.rect(surface, (30, 30, 60), (160, 140, 480, 60), border_radius=24)
        q_surf = font_sm.render("🐍  Python Puzzle", True, (180, 255, 180))
        surface.blit(q_surf, q_surf.get_rect(center=(400, 165)))

        # Question text (word-wrap naive)
        q_text = font_lg.render(self.question, True, (255, 255, 180))
        surface.blit(q_text, q_text.get_rect(center=(400, 215)))

        mouse_pos = pygame.mouse.get_pos()
        for i, opt in enumerate(self.options):
            rect = pygame.Rect(220, 240 + i * 65, 360, 50)
            hover = rect.collidepoint(mouse_pos)
            color = (255, 220, 80) if hover else (90, 90, 130)
            pygame.draw.rect(surface, color, rect, border_radius=12)
            pygame.draw.rect(surface, (200, 200, 255), rect, 2, border_radius=12)
            txt = font_sm.render(opt, True, (20, 20, 40) if hover else (240, 240, 240))
            surface.blit(txt, txt.get_rect(center=rect.center))

        # Feedback flash
        if self.feedback_timer > 0:
            fb = font_sm.render(self.feedback, True, (255, 80, 80))
            surface.blit(fb, fb.get_rect(center=(400, 420)))
            self.feedback_timer -= 1


# ─────────────────────────────────────────────
# GameState (session data)
# ─────────────────────────────────────────────
class GameState:
    """Holds persistent data across all rooms."""

    TIMER_LIMIT = 15    # seconds per room

    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.current_room = 1
        self.game_over = False
        self._start_ticks = pygame.time.get_ticks()
        self._paused_ticks = 0
        self._is_running = True

    def reset_room_timer(self):
        """Call when entering a new room."""
        self._start_ticks = pygame.time.get_ticks()
        self._paused_ticks = 0
        self._is_running = True

    def pause_timer(self):
        if self._is_running:
            self._paused_ticks = pygame.time.get_ticks() - self._start_ticks
            self._is_running = False

    def resume_timer(self):
        if not self._is_running:
            self._start_ticks = pygame.time.get_ticks() - self._paused_ticks
            self._is_running = True

    def get_remaining(self) -> int:
        if self._is_running:
            elapsed = (pygame.time.get_ticks() - self._start_ticks) // 1000
        else:
            elapsed = self._paused_ticks // 1000
        remaining = self.TIMER_LIMIT - elapsed
        if remaining <= 0:
            self.game_over = True
            return 0
        return remaining

    # Alias for backward compat
    def update_timer(self) -> int:
        return self.get_remaining()

    def add_score(self, points: int):
        self.score += points

    def lose_life(self):
        self.lives = max(0, self.lives - 1)
        if self.lives == 0:
            self.game_over = True


# ─────────────────────────────────────────────
# Room base class
# ─────────────────────────────────────────────
class BaseRoom:
    """Common room lifecycle – subclass and implement setup() + extra_draw()."""

    BG_SIZE = (800, 600)
    FLOOR_Y = 450

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 game_state: GameState, next_state: str):
        self.screen = screen
        self.clock = clock
        self.gs = game_state
        self.next_state = next_state
        self.paused = False
        self.font_sm = pygame.font.SysFont("arialblack", 22)
        self.font_lg = pygame.font.SysFont("arialblack", 28)

        # Populated by subclass
        self.bg: pygame.Surface | None = None
        self.player: Player | None = None
        self.door: Door | None = None
        self.puzzle: Puzzle | None = None
        self.collectibles: list[Collectible] = []

    # ── Subclasses override these ──────────────
    def setup(self):
        raise NotImplementedError

    def extra_update(self):
        """Per-room logic called each frame (before drawing)."""
        pass

    def extra_draw(self):
        """Per-room drawing called after main draw but before UI."""
        pass

    # ── Main loop ─────────────────────────────
    def run(self) -> str:
        self.setup()
        self.gs.reset_room_timer()

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            self.gs.pause_timer()
                        else:
                            self.gs.resume_timer()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Back button
                    if pygame.Rect(10, 560, 90, 34).collidepoint(event.pos):
                        return "MENU"

                    if self.paused:
                        # Resume / Quit buttons in pause screen
                        if pygame.Rect(300, 260, 200, 50).collidepoint(event.pos):
                            self.paused = False
                            self.gs.resume_timer()
                        if pygame.Rect(300, 330, 200, 50).collidepoint(event.pos):
                            return "MENU"
                    elif self.puzzle and self.puzzle.active:
                        self.puzzle.handle_click(event.pos, self.gs)

            # ── Game update ───────────────────────
            if not self.paused:
                # Timer
                remaining = self.gs.get_remaining()
                if self.gs.game_over:
                    return "GAME_OVER"

                # Movement (only when puzzle not active)
                if self.puzzle and not self.puzzle.active and self.player:
                    keys = pygame.key.get_pressed()
                    self.player.handle_movement(keys)

                self.extra_update()

                # Check door transition
                if self.door and not self.door.locked and self.player:
                    if self.door.is_player_at_door(self.player):
                        return self.next_state

                if self.gs.lives <= 0:
                    return "GAME_OVER"

            # ── Draw ──────────────────────────────
            if self.bg:
                self.screen.blit(self.bg, (0, 0))

            if self.door:
                self.door.draw(self.screen)

            for c in self.collectibles:
                c.draw(self.screen)

            if self.player:
                self.player.draw(self.screen)

            if self.puzzle:
                self.puzzle.draw(self.screen, self.font_sm, self.font_lg)

            self.extra_draw()
            self._draw_ui()

            if self.paused:
                self._draw_pause()

            pygame.display.update()
            self.clock.tick(60)

        return "MENU"

    # ── UI helpers ────────────────────────────
    def _draw_ui(self):
        # Hearts
        for i in range(3):
            color = (220, 50, 50) if i < self.gs.lives else (60, 60, 60)
            pygame.draw.circle(self.screen, color, (30 + i * 38, 25), 14)
            pygame.draw.circle(self.screen, (255, 255, 255), (30 + i * 38, 25), 14, 2)

        # Score & Timer
        remaining = self.gs.get_remaining()
        timer_color = (255, 80, 80) if remaining <= 20 else (255, 255, 255)
        score_surf = self.font_sm.render(f"Score: {self.gs.score}", True, (255, 255, 180))
        time_surf = self.font_sm.render(f"⏱ {remaining}s", True, timer_color)
        self.screen.blit(score_surf, (620, 8))
        self.screen.blit(time_surf, (650, 36))

        # Pause hint
        hint = self.font_sm.render("ESC = Pause", True, (180, 180, 180))
        self.screen.blit(hint, (320, 8))

        # Back button
        back_rect = pygame.Rect(10, 560, 90, 34)
        pygame.draw.rect(self.screen, (80, 80, 80), back_rect, border_radius=8)
        pygame.draw.rect(self.screen, (160, 160, 160), back_rect, 2, border_radius=8)
        b = self.font_sm.render("Menu", True, (255, 255, 255))
        self.screen.blit(b, b.get_rect(center=back_rect.center))

    def _draw_pause(self):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        card = pygame.Rect(250, 190, 300, 220)
        pygame.draw.rect(self.screen, (30, 30, 60), card, border_radius=20)
        pygame.draw.rect(self.screen, (150, 150, 255), card, 3, border_radius=20)

        title = self.font_lg.render("PAUSED", True, (255, 255, 100))
        self.screen.blit(title, title.get_rect(center=(400, 225)))

        for y, label, color in [
            (260, "Resume", (60, 160, 60)),
            (330, "Quit to Menu", (160, 60, 60)),
        ]:
            btn = pygame.Rect(300, y, 200, 50)
            pygame.draw.rect(self.screen, color, btn, border_radius=12)
            t = self.font_sm.render(label, True, (255, 255, 255))
            self.screen.blit(t, t.get_rect(center=btn.center))
