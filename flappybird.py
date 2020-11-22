import pygame, sys, random

pygame.init()
activeGame = True
width = 680
height = 724
pygame.display.set_caption("Vagabonding freaking fireball")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
floorColor = ((192, 192, 192))
floor_x_pos = 0

userColor = ((255, 0, 0))
user = pygame.Rect(width / 2 - 175, height / 2 - 15, 30, 30)
userSpeed = 0

gravity = 0.20
score = 0
highScore = 0
gameFont = pygame.font.Font('freesansbold.ttf', 30)


obstacle = pygame.Rect(600, 500, 30, 30)
obstacleList = []
obstacleHeight = [500, 400, 470, 550, 600]
SPAWNOBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWNOBSTACLE, 1000)

def floorMovement():
    pygame.draw.rect(screen, floorColor, pygame.Rect(floor_x_pos, 680, 680, 60))
    pygame.draw.rect(screen, floorColor, pygame.Rect(floor_x_pos + 680, 680, 680, 60))


def createNewObstacle():
    randomPipeHeight = random.choice(obstacleHeight)
    bottomObstacle = pygame.Rect(600, randomPipeHeight, 100, 300)
    topObstacle = pygame.Rect(600, randomPipeHeight - 600, 100, 300)
    return topObstacle, bottomObstacle

def moveObstacles(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 5
    return obstacles

def drawObstacles(obstacles):
    for obstacle in obstacles:
        #if obstacle.bottom >= height:
            pygame.draw.rect(screen, floorColor, obstacle)
        #else:
            #flipObstacle = pygame.transform.flip(obstacle, False, True)
            #pygame.draw.rect(screen, floorColor, flipObstacle)

def collision(obstacles):
    for obstacle in obstacles:
        if user.colliderect(obstacle):
            return False
    if user.top <= -200 or user.bottom >= 680:
            return False
    return True

def displayScore(game_state):
    if game_state == 'main game':
        score_display = gameFont.render(str(int(score - 1)), True, (255, 255, 255))
        score_rect = score_display.get_rect(center = (width/2 - 15, 100))
        screen.blit(score_display, score_rect)
    if game_state == 'game over':
        score_display = gameFont.render(f'Your score is {int(score - 1)}', True, (255, 255, 255))
        score_rect = score_display.get_rect(center = (width/2 - 15, 100))
        screen.blit(score_display, score_rect)

        high_score_display = gameFont.render(f'Your highscore is {int(highScore - 1)}', True, (255, 255, 255))
        high_score_rect = score_display.get_rect(center = (width/2 - 40, 150))
        screen.blit(high_score_display, high_score_rect)

def highscoreUpdate(score, highScore):
    if score > highScore:
        highScore = score
    return highScore

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and activeGame:
                userSpeed = 0
                userSpeed -= 6
            if event.key == pygame.K_UP and activeGame == False:
                activeGame = True
                obstacleList.clear()
                user = pygame.Rect(width / 2 - 175, height / 2 - 15, 30, 30)
                userSpeed = 0
                score = 0

        if event.type == SPAWNOBSTACLE:
            obstacleList.extend(createNewObstacle())
            
    if activeGame:
        floor_x_pos -= 1
        userSpeed += gravity
        user.centery += userSpeed
        activeGame = collision(obstacleList)

        obstacleList = moveObstacles(obstacleList)
        drawObstacles(obstacleList)
        score += 0.01
        displayScore('main game')
    else:
        highScore = highscoreUpdate(score, highScore)
        displayScore('game over')

    floorMovement()
    if floor_x_pos <= 680:
        floor_x_pos = 0

    pygame.draw.ellipse(screen, (255, 0, 0), user)
    #pygame.draw.rect(screen, floorColor, obstacle)
    pygame.display.update()
    clock.tick(100)