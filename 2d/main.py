import pygame
import random
import time

# Constants
GRID_SIZE = 20  # Size of each grid cell in pixels
GRID_WIDTH = 40
GRID_HEIGHT = 30
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

class GameObject:
    """Base class for all game objects"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self, surface):
        pass
    
    def update(self):
        pass

class Player(GameObject):
    """Player character"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = "UP"  # UP, DOWN, LEFT, RIGHT
        self.photos_taken = 0
        
    def draw(self, surface):
        # Draw player as a triangle pointing in direction
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        
        if self.direction == "UP":
            points = [(center_x, center_y - 10), (center_x - 7, center_y + 5), (center_x + 7, center_y + 5)]
        elif self.direction == "DOWN":
            points = [(center_x, center_y + 10), (center_x - 7, center_y - 5), (center_x + 7, center_y - 5)]
        elif self.direction == "LEFT":
            points = [(center_x - 10, center_y), (center_x + 5, center_y - 7), (center_x + 5, center_y + 7)]
        else:  # RIGHT
            points = [(center_x + 10, center_y), (center_x - 5, center_y - 7), (center_x - 5, center_y + 7)]
            
        pygame.draw.polygon(surface, BLUE, points)
        
    def move(self, dx, dy, game_map):
        """Try to move in the specified direction"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if new position is valid
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def take_photo(self, game_map, deer_list):
        """Take a photo in the direction the player is facing"""
        x, y = self.x, self.y
        
        # Direction vectors
        if self.direction == "UP":
            dx, dy = 0, -1
        elif self.direction == "DOWN":
            dx, dy = 0, 1
        elif self.direction == "LEFT":
            dx, dy = -1, 0
        else:  # RIGHT
            dx, dy = 1, 0
        
        # Track how far the photo "travels"
        photo_range = 10  # How far the photo can see
        
        # Check each cell in the photo's path
        deer_photographed = []
        for i in range(1, photo_range + 1):
            check_x = x + dx * i
            check_y = y + dy * i
            
            # Stop if we hit a boundary
            if not (0 <= check_x < GRID_WIDTH and 0 <= check_y < GRID_HEIGHT):
                break
                
            # Stop if we hit a solid obstacle
            if game_map.get_cell(check_x, check_y) in ["TREE", "ROCK"]:
                break
                
            # Check if we see a deer
            for deer in deer_list:
                if deer.x == check_x and deer.y == check_y:
                    deer_photographed.append(deer)
                    
            # In bushes, reduce visibility (50% chance to continue)
            if game_map.get_cell(check_x, check_y) == "BUSH" and random.random() < 0.5:
                break
                
        # Return any deer we photographed
        return deer_photographed

class Deer(GameObject):
    """Deer that player photographs"""
    def __init__(self, x, y, deer_type="NORMAL"):
        super().__init__(x, y)
        self.deer_type = deer_type
        self.photographed = False
        self.alert_level = 0  # 0-10, higher means more likely to flee
        
    def draw(self, surface):
        # Draw deer as brown circle
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(surface, BROWN, (center_x, center_y), GRID_SIZE // 2)
        
    def update(self, player, game_map):
        """Update deer behavior based on player position"""
        # Calculate distance to player
        distance = abs(self.x - player.x) + abs(self.y - player.y)  # Manhattan distance
        
        # If player is close, become more alert
        if distance < 5:
            self.alert_level += 2
        else:
            self.alert_level = max(0, self.alert_level - 1)  # Calm down over time
            
        # If very alert, try to move away from player
        if self.alert_level > 5:
            self.flee(player, game_map)
        else:
            # Random movement (25% chance)
            if random.random() < 0.25:
                self.random_move(game_map)
    
    def flee(self, player, game_map):
        """Move away from player"""
        # Determine direction away from player
        dx = 1 if self.x < player.x else -1
        dy = 1 if self.y < player.y else -1
        
        # Try to move in that direction
        possible_moves = [
            (-dx, 0),  # Horizontal away
            (0, -dy),  # Vertical away
            (-dx, -dy),  # Diagonal away
            (0, 0)  # Stay put
        ]
        
        # Shuffle to avoid predictable patterns
        random.shuffle(possible_moves)
        
        # Try each move until we find a valid one
        for move_dx, move_dy in possible_moves:
            new_x = self.x + move_dx
            new_y = self.y + move_dy
            
            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                    game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
                self.x = new_x
                self.y = new_y
                break
    
    def random_move(self, game_map):
        """Move in a random direction"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                    game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
                self.x = new_x
                self.y = new_y
                break

class GameMap:
    """Represents the game environment"""
    def __init__(self):
        self.grid = [["EMPTY" for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        
    def generate_map(self):
        """Generate a random map with trees, rocks, bushes"""
        # Add trees (20% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.2)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.grid[x][y] = "TREE"
            
        # Add rocks (10% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.1)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == "EMPTY":
                self.grid[x][y] = "ROCK"
                
        # Add bushes (15% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.15)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == "EMPTY":
                self.grid[x][y] = "BUSH"
    
    def get_cell(self, x, y):
        """Get the type of cell at the given coordinates"""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.grid[x][y]
        return None
    
    def draw(self, surface):
        """Draw the map"""
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                
                if self.grid[x][y] == "TREE":
                    pygame.draw.rect(surface, GREEN, rect)
                elif self.grid[x][y] == "ROCK":
                    pygame.draw.rect(surface, (100, 100, 100), rect)
                elif self.grid[x][y] == "BUSH":
                    pygame.draw.rect(surface, (144, 238, 144), rect)  # Light green
                else:
                    pygame.draw.rect(surface, (200, 255, 200), rect)  # Light grass color
                
                # Draw grid lines
                pygame.draw.rect(surface, (220, 220, 220), rect, 1)

class Game:
    """Main game class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Deer Picture Hunting")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        self.map = GameMap()
        self.map.generate_map()
        
        # Place player in an empty cell
        self.player = self.place_in_empty_cell(Player)
        
        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self.place_in_empty_cell(Deer))
            
        # Game state
        self.score = 0
        self.time_left = 60  # 60 seconds
        self.last_time = time.time()
        
    def place_in_empty_cell(self, object_class):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if self.map.get_cell(x, y) == "EMPTY":
                return object_class(x, y)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.direction = "UP"
                    self.player.move(0, -1, self.map)
                elif event.key == pygame.K_DOWN:
                    self.player.direction = "DOWN"
                    self.player.move(0, 1, self.map)
                elif event.key == pygame.K_LEFT:
                    self.player.direction = "LEFT"
                    self.player.move(-1, 0, self.map)
                elif event.key == pygame.K_RIGHT:
                    self.player.direction = "RIGHT"
                    self.player.move(1, 0, self.map)
                elif event.key == pygame.K_SPACE:
                    self.take_photo()
    
    def take_photo(self):
        """Player takes a photo"""
        photographed_deer = self.player.take_photo(self.map, self.deer)
        for deer in photographed_deer:
            if not deer.photographed:
                deer.photographed = True
                self.score += 1
    
    def update(self):
        """Update game state"""
        # Update timer
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        
        self.time_left -= elapsed
        if self.time_left <= 0:
            self.running = False
            
        # Update deer
        for deer in self.deer:
            deer.update(self.player, self.map)
    
    def draw(self):
        """Draw everything to the screen"""
        # Clear screen
        self.screen.fill(WHITE)
        
        # Draw map
        self.map.draw(self.screen)
        
        # Draw deer
        for deer in self.deer:
            deer.draw(self.screen)
            
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        time_text = font.render(f"Time: {int(self.time_left)}s", True, BLACK)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(time_text, (WINDOW_WIDTH - 150, 10))
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)  # 30 FPS
            
        # Game over
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, BLACK)
        final_score = font.render(f"Final Score: {self.score}", True, BLACK)
        
        self.screen.fill(WHITE)
        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(final_score, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 20))
        pygame.display.flip()
        
        # Wait a bit before exiting
        pygame.time.wait(3000)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
