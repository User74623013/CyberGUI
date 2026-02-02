import pygame
import os

# --------------------------------------------------
# INIT
# --------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Platformer – Green Zone")
clock = pygame.time.Clock()

# --------------------------------------------------
# PATH
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset_path(*parts):
    return os.path.join(BASE_DIR, *parts)

# --------------------------------------------------
# CONSTANTS
# --------------------------------------------------
FPS = 60
GRAVITY = 0.8
MOVE_SPEED = 5
JUMP_POWER = -15

TILE_SIZE = 32
SOLID_TILES = {0, 1, 2, 3, 5, }

# --------------------------------------------------
# PLAYER
# --------------------------------------------------
player_x = 200
player_y = 100
player_w = 48
player_h = 48

player_vel_x = 0
player_vel_y = 0
player_on_ground = False
player_facing = "right"

# --------------------------------------------------
# TILE MAP
# --------------------------------------------------
level_map = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [ 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47],
    [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63],
    [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
    [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# --------------------------------------------------
# LOAD TILE IMAGES (AUTOMATIC)
# --------------------------------------------------
def load_tiles(folder):
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    tiles = []
    for file in files:
        img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
        tiles.append(img)
    return tiles

tiles_folder = asset_path("Tileset", "1 Tiles")
tiles = load_tiles(tiles_folder)

# --------------------------------------------------
# BUILD SOLID TILE RECTANGLES
# --------------------------------------------------
def get_solid_tiles():
    rects = []
    for y, row in enumerate(level_map):
        for x, tile_id in enumerate(row):
            if tile_id in SOLID_TILES:
                obj =  pygame.Rect(
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                pygame.draw.rect(screen, (255, 0, 0), obj, 2)
                rects.append(
                    obj
                )
    return rects

solid_tiles = get_solid_tiles()

# --------------------------------------------------
# PLAYER SPRITES
# --------------------------------------------------
def slice_strip(path, frames):
    image = pygame.image.load(path).convert_alpha()
    w = image.get_width() // frames
    h = image.get_height()
    return [
        image.subsurface((i * w, 0, w, h)).copy()
        for i in range(frames)
    ]

idle_path = asset_path(
    "Player Character",
    "Original Player",
    "1 Biker",
    "Biker_idle.png"
)

player_frames = slice_strip(idle_path, 4)
player_frame = 0
anim_timer = 0
ANIM_SPEED = 10

# --------------------------------------------------
# INPUT
# --------------------------------------------------
def handle_input():
    global player_vel_x, player_vel_y, player_on_ground, player_facing

    keys = pygame.key.get_pressed()
    player_vel_x = 0

    if keys[pygame.K_a]:
        player_vel_x = -MOVE_SPEED
        player_facing = "left"

    if keys[pygame.K_d]:
        player_vel_x = MOVE_SPEED
        player_facing = "right"

    if keys[pygame.K_SPACE] and player_on_ground:
        player_vel_y = JUMP_POWER
        player_on_ground = False

# --------------------------------------------------
# PHYSICS
# --------------------------------------------------
def apply_physics():
    global player_x, player_y, player_vel_y
    player_x += player_vel_x
    player_vel_y += GRAVITY
    player_y += player_vel_y

def check_collisions():
    global player_y, player_vel_y, player_on_ground

    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    player_on_ground = False

    for tile in solid_tiles:
        if player_rect.colliderect(tile):
            if player_vel_y > 0:
                player_y = tile.top - player_h
                player_vel_y = 0
                player_on_ground = True

# --------------------------------------------------
# ANIMATION
# --------------------------------------------------
def update_animation():
    global player_frame, anim_timer
    anim_timer += 1
    if anim_timer >= ANIM_SPEED:
        player_frame = (player_frame + 1) % len(player_frames)
        anim_timer = 0

# --------------------------------------------------
# DRAW
# --------------------------------------------------
def draw():
    screen.fill((135, 206, 235))

    for y, row in enumerate(level_map):
        for x, tile_id in enumerate(row):
            if tile_id != -1:
                screen.blit(
                    tiles[tile_id],
                    (x * TILE_SIZE, y * TILE_SIZE)
                )

    frame = player_frames[player_frame]
    if player_facing == "left":
        frame = pygame.transform.flip(frame, True, False)

    screen.blit(frame, (player_x, player_y))
    pygame.display.flip()

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_input()
    apply_physics()
    check_collisions()
    update_animation()
    draw()

pygame.quit()
