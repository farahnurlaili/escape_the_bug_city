"""
victory.py – Victory and Game Over screens
"""
import pygame
import sys


def _draw_button(screen, rect, label, font, color, hover_color):
    mp = pygame.mouse.get_pos()
    c = hover_color if rect.collidepoint(mp) else color
    pygame.draw.rect(screen, c, rect, border_radius=14)
    pygame.draw.rect(screen, (220, 220, 220), rect, 2, border_radius=14)
    t = font.render(label, True, (255, 255, 255))
    screen.blit(t, t.get_rect(center=rect.center))


def run_victory(screen, clock, game_state) -> str:
    font_big = pygame.font.SysFont("impact", 70)
    font_med = pygame.font.SysFont("arialblack", 30)
    font_sm = pygame.font.SysFont("arialblack", 22)

    btn_menu = pygame.Rect(200, 420, 180, 55)
    btn_quit = pygame.Rect(420, 420, 180, 55)

    t = 0
    while True:
        t += 1
        screen.fill((10, 10, 30))

        # Starfield
        import math, random
        random.seed(42)
        for _ in range(60):
            sx = random.randint(0, 800)
            sy = random.randint(0, 600)
            alpha = abs(math.sin(t * 0.03 + random.random() * 6))
            pygame.draw.circle(screen, (int(200 * alpha), int(200 * alpha), 255), (sx, sy), 2)

        # Title
        title = font_big.render("🎉 VICTORY! 🎉", True, (255, 220, 50))
        screen.blit(title, title.get_rect(center=(400, 140)))

        # Stats
        screen.blit(font_med.render(f"Final Score:  {game_state.score}", True, (180, 255, 180)),
                    (240, 230))
        screen.blit(font_med.render(f"Lives Remaining:  {game_state.lives}", True, (255, 150, 150)),
                    (240, 280))
        screen.blit(font_med.render(f"Time Left:  {game_state.get_remaining()}s", True, (150, 200, 255)),
                    (240, 330))

        # Grade
        grade = "A+" if game_state.score >= 100 else "A" if game_state.score >= 75 else "B"
        screen.blit(font_sm.render(f"Grade: {grade}", True, (255, 255, 100)), (340, 380))

        _draw_button(screen, btn_menu, "Main Menu", font_sm, (50, 100, 180), (80, 150, 255))
        _draw_button(screen, btn_quit, "Quit", font_sm, (140, 40, 40), (200, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_menu.collidepoint(event.pos):
                    game_state.reset()
                    return "MENU"
                if btn_quit.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(60)


def run_game_over(screen, clock, game_state) -> str:
    font_big = pygame.font.SysFont("impact", 70)
    font_med = pygame.font.SysFont("arialblack", 28)
    font_sm = pygame.font.SysFont("arialblack", 22)

    btn_retry = pygame.Rect(200, 400, 180, 55)
    btn_menu = pygame.Rect(420, 400, 180, 55)

    while True:
        screen.fill((20, 0, 0))

        title = font_big.render("GAME OVER", True, (220, 40, 40))
        screen.blit(title, title.get_rect(center=(400, 150)))

        reason = "Time ran out!" if game_state.get_remaining() == 0 else "No lives left!"
        screen.blit(font_med.render(reason, True, (255, 150, 150)),
                    font_med.render(reason, True, (255, 150, 150)).get_rect(center=(400, 250)))
        screen.blit(font_med.render(f"Score: {game_state.score}", True, (220, 220, 220)),
                    font_med.render(f"Score: {game_state.score}", True, (220, 220, 220)).get_rect(center=(400, 310)))

        _draw_button(screen, btn_retry, "Try Again", font_sm, (60, 120, 60), (80, 180, 80))
        _draw_button(screen, btn_menu, "Main Menu", font_sm, (60, 60, 120), (80, 80, 180))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos):
                    game_state.reset()
                    return "PLAY_ROOM1"
                if btn_menu.collidepoint(event.pos):
                    game_state.reset()
                    return "MENU"

        pygame.display.update()
        clock.tick(60)
