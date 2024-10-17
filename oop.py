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
        self.rect = pygame.Rect(x, y, width, height) #Associate a Rect object with Ball
        #Default Specifications for Movement Direction, Velocity and Radius
        self.dirX = 1
        self.dirY = 1
        self.velocity = BALL_VEL
        self.radius = BALL_RADIUS

    #Default Movement
    def ball_movement(self):
        self.rect.y += self.velocity * self.dirY
        self.rect.x += self.velocity * self.dirX

    #Check Collision with Paddle or Block
    def check_object_collision(self, collider):
        if self.rect.colliderect(collider):
            self.dirY *= -1

    #Collision with Wall
    def wall_collision(self):
        if self.rect.x + (self.radius*2) > WIDTH or self.rect.x < 0:
            self.dirX *= -1
        if self.rect.y < 0:
            self.dirY *= -1


class Paddle():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = PLAYER_VEL

    # Move the paddle left
    def move_left(self):
        self.rect.x -= self.velocity
    
    # Move the paddle right
    def move_right(self):
        self.rect.x += self.velocity

class Block():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = 1
        self.type = 1

    def check_collision(self, collider, score: int):
        if self.rect.colliderect(collider):
            score += 1
            self.health -= 1

class SturdyBlock(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.health = 2
        self.type = 2

class TimedBlock(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.health = 1
        self.type = 3
        self.timer = 8
    
    def time_block_timer(self, blocks: list):
        if self.timer > 0:
            self.timer -= 1200
        else:
            blocks.remove(self)

    def check_collision(self, collider, score):
        if self.rect.colliderect(collider):
            score += 1

#Draw on Display
def draw(player: Paddle, elapsedTime, ball: Ball, blocks: list, stage: int, score: int):
    WIN.fill("sky blue")

    timeText = FONT.render(f"Time: {round(elapsedTime)}s", 1, "black")
    WIN.blit(timeText, (10, 10))

    stageText = FONT.render(f"Stage: {stage}", 1, "black")
    WIN.blit(stageText, (WIDTH - stageText.get_width() - 10, 10))

    scoreText = FONT.render(f"Score: {score}", 1, "black")
    WIN.blit(scoreText, (WIDTH - scoreText.get_width() - 10, stageText.get_height() + 10))

    pygame.draw.rect(WIN, "blue", player.rect)

    pygame.draw.rect(WIN, "red", ball.rect)

    for block in blocks:
        if block.type == 1:
            pygame.draw.rect(WIN, "brown", block)
        if block.type == 2:
            pygame.draw.rect(WIN, "yellow", block)
        if block.type == 3:
            pygame.draw.rect(WIN, "green", block)

    pygame.display.update()

def controls(paddle: Paddle):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.rect.x - paddle.velocity >= 0:
        paddle.move_left()
    if keys[pygame.K_RIGHT] and paddle.rect.x + paddle.rect.width + paddle.velocity <= WIDTH:
        paddle.move_right()

def lose(msg):
    lostText = FONT.render("You lost! Due to: " + msg, 1, "black")
    WIN.blit(lostText, (WIDTH/2 - lostText.get_width()/2, HEIGHT/2 - lostText.get_width()/2))
    pygame.display.update()
    pygame.time.delay(4000)

#Main Game
def main():
    run = True

    #Create Player
    paddle = Paddle(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball = Ball(0, 0, BALL_RADIUS*2, BALL_RADIUS*2)

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
                if stage <= 3:
                    block = Block(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                elif stage <= 4:
                    chances = random.randint(1, 100)
                    if chances < 75:
                        block = Block(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                    elif chances >= 25:
                        block = SturdyBlock(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                elif stage >= 5:
                    chances = random.randint(1, 100)
                    if chances < 60:
                        block = Block(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                    elif chances <= 85:
                        block = SturdyBlock(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                    elif chances >= 85:
                        block = TimedBlock(blockX, blockY, BLOCK_SIZE, BLOCK_SIZE)
                blocks.append(block)

        #Adding a New Stage
        if currentTime - lastStageTime >= stageIncrementTime * stage:
            stage += 1
            lastStageTime = currentTime
            #Adding More Blocks in New Stage
            if stageBlocks < 15:
                stageBlocks += 2

        ball.wall_collision()
        ball.check_object_collision(paddle)
        for block in blocks:
            if block.type == 3:
                block.time_block_timer(blocks)
            ball.check_object_collision(block)
            block.check_collision(ball, score)
            if block.health <= 0:
                blocks.remove(block)

        ball.ball_movement()
        controls(paddle)

        #Lose Game when Ball Reaches Bottom
        if ball.rect.y > HEIGHT:
            lose('Ball hit the bottom')
            break

        draw(paddle, elapsedTime, ball, blocks, stage, score)

    pygame.quit()

if __name__ == "__main__":
    main()
