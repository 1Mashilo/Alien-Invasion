import sys
import pygame
from time import sleep
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from shiplives import ShipLives


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)  

        self.lives = 3 
        self.max_aliens = 24
        self.game_active = False

        self.ship_image = pygame.image.load('ship.bmp')
        self.ship_image = pygame.transform.scale(self.ship_image, (40, 30))
        self.ship_rect = self.ship_image.get_rect()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = self._create_stars()
        self.play_button = Button(self, "Play")
        self.ship_lives = ShipLives(self, self.ship_image, self.ship_rect)
    
        self._create_fleet()
        self.game_active = False
      
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)

            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_ships()
            self.sb.prep_level()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_stars()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_stars(self):
        """Create a group of stars."""
        stars = pygame.sprite.Group()
        for _ in range(100):
            star = Star(self.settings.screen_width, self.settings.screen_height)
            stars.add(star)
        return stars

    def _create_fleet(self):
        """Create the fleet of aliens."""
        ship = Ship(self)
        alien = Alien(self) 
        alien_width, alien_height = alien.rect.size
    
       
        available_space_x = self.settings.screen_width - 2 * alien_width
        available_space_y = (self.settings.screen_height -
                         (3 * alien_height) - ship.rect.height) 
        num_aliens_x = available_space_x // (2 * alien_width)
        num_aliens_y = available_space_y // (2 * alien_height)

        num_aliens = num_aliens_x * num_aliens_y
        num_aliens = min(num_aliens, self.max_aliens)

        for row_number in range(2, num_aliens_y + 1):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number)



    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * (row_number -1 )
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
 
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self._check_aliens_bottom()

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):        
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):        
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for star in self.stars.sprites():
            pygame.draw.rect(self.screen, star.color, star)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.ship_lives.draw_lives(self.stats.ships_left)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
          

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
          
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

            self.ship_lives.draw_lives(self.stats.ships_left)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
