import pygame
import time
import random
pygame.font.init()

#Set Game Display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paddle Ball Game")

#Main Font
FONT = pygame.font.SysFont("comicsansms", 20) 

#Player Parameters
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 15
PLAYER_VEL = 7

#Ball Parameters
BALL_MAX_VEL = 10
BALL_RADIUS = 10
BALL_VEL = 5

#Block Parameters
BLOCK_SIZE = 25
MAX_BLOCKS = 10

class Ball():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dirX = 1
        self.dirY = 1
        self.velocity = BALL_VEL
        self.radius = BALL_RADIUS

    def ball_movement(self):
        self.rect.y += self.velocity * self.dirY
        self.rect.x += self.velocity * self.dirX
    
    def check_collision(self, collider):
        if self.rect.colliderect(collider):
            self.onCollison();

    def on_collision(self, paddle):
        padCollision = pygame.Rect.colliderect(self.rect, paddle.rect)
        if self.rect.x + (self.radius*2) > WIDTH or self.rect.x < 0:
            self.dirX *= -1
        if self.y < 0:
            self.dirY *= -1
        if padCollision:
            self.dirY *= -1


class Paddle():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = PLAYER_VEL

     # Move the paddle up
    def move_left(self):
        self.rect.x -= self.velocity
    
    # Move the paddle down
    def move_right(self):
        self.rect.x += self.velocity

class Block():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def check_collision(self, collider):
        if self.rect.colliderect(collider):
            self.block_collision()

    def block_collision(self, blocks, score):
        score += 1
        blocks.remove(self)

#Draw on Display
def draw(player, elapsedTime, ball, blocks, stage, score):
    WIN.fill("sky blue")

    timeText = FONT.render(f"Time: {round(elapsedTime)}s", 1, "black")
    WIN.blit(timeText, (10, 10))

    stageText = FONT.render(f"Stage: {stage}", 1, "black")
    WIN.blit(stageText, (WIDTH - stageText.get_width() - 10, 10))

    scoreText = FONT.render(f"Score: {score}", 1, "black")
    WIN.blit(scoreText, (WIDTH - scoreText.get_width() - 10, stageText.get_height() + 10))

    pygame.draw.rect(WIN, "blue", player)

    pygame.draw.rect(WIN, "red", ball)

    for block in blocks:
        pygame.draw.rect(WIN, "brown", block)

    pygame.display.update()

def controls(paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.x - paddle.velocity >= 0:
        paddle.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.velocity <= WIDTH:
        paddle.x += PLAYER_VEL

#Main Game
def main():
    run = True

    #Create Player
    paddle = Paddle(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball = Ball(0, 0, BALL_RADIUS*2, BALL_RADIUS*2)
    ballVelocity = BALL_VEL

    #Initial Direction of Ball Movement
    ballDirX = 1
    ballDirY = 1

    #Time Parameters
    clock = pygame.time.Clock()
    startTime = time.time()
    elapsedTime = 0
    lastStageTime = startTime
    stageIncrementTime = 10

    timeIncrement = 0
    stage = 1

    #Block Init
    blocks = []
    stageBlocks = 0

    #Init Score
    score = 0

    #Main Loop
    while run:
        #For Framerate set to 60
        clock.tick(60)

        elapsedTime = time.time() - startTime
        currentTime = time.time()
        
        #Increase Time Between Stages
        timeMultiplier = timeIncrement * stage
        timeIncrement = elapsedTime - timeMultiplier

        #For quitting game on pressing cross button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        #Add Blocks
        if len(blocks) < stageBlocks:
            #StageBlock is the number of blocks in a stage, Length is total blocks in present
            for _ in range(stageBlocks - len(blocks)):
                blockX = random.randint(5, int(WIDTH - BLOCK_SIZE - 5))
                blockY = random.randint(5, int(3*HEIGHT/5))
                block = Block(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                blocks.append(block)
        
        #Adding a New Stage
        if currentTime - lastStageTime >= stageIncrementTime * stage:
            stage += 1
            lastStageTime = currentTime
            #Adding More Blocks in New Stage
            if stageBlocks < 15:
                stageBlocks += 2
    
        #Ball Collision with Borders and Paddle
        padCollision = pygame.Rect.colliderect(ball, paddle)
        if ball.x + (BALL_RADIUS*2) > WIDTH or ball.x < 0:
            ballDirX *= -1
        if ball.y < 0:
            ballDirY *= -1
        if padCollision:
            ballDirY *= -1

        #Block Collision
        for block in blocks:
            blockCollision = pygame.Rect.colliderect(ball, block)
            if blockCollision:
                score += 1
                ballDirY *= -1
                blocks.remove(block)

        #Ball Movement Absolute
        ball.y += ballVelocity * ballDirY
        ball.x += ballVelocity * ballDirX

        #Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.x - PLAYER_VEL >= 0:
            paddle.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and paddle.x + paddle.width + PLAYER_VEL <= WIDTH:
            paddle.x += PLAYER_VEL

        #Lose Game when Ball Reaches Bottom
        if ball.y > HEIGHT:
            lostText = FONT.render("You lost!", 1, "black")
            WIN.blit(lostText, (WIDTH/2 - lostText.get_width()/2, HEIGHT/2 - lostText.get_width()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(paddle, elapsedTime, ball, blocks, stage, score)

    pygame.quit()

if __name__ == "__main__":
    main()
