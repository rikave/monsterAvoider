import pygame, sys, random, time
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BACKGROUND = (0, 0, 0)
TEXTCOLOR = (255, 255, 255)
FPS = 60
MONSTERSIZE = 20
#MONSTERSPEED in menu loop
PLAYERSIZE = 40
LTBLUE = (0, 128, 255)
FIRSTLINEX = 200

def terminate():
   pygame.quit()
   sys.exit()

def waitForPlayerToPressKey():
   while True:
      for event in pygame.event.get():
         if event.type == QUIT:
            terminate()
         if event.type == KEYUP:
            if event.key == ord("e"):
               terminate()
            if event.key == ord("q"):
               return 0    #should set gotomenu = 0 and start a game

def collisionDetection(playerOne, playerTwo, monsters):
   for m in monsters[0]:
      if playerRect1.colliderect(m['rect']):
         return True
   for m in monsters[1]:
      if playerRect2.colliderect(m['rect']):
         return True
   return False

def drawText(text, font, surface, x, y):
   textObj = font.render(text, 1, TEXTCOLOR)
   textrect = textObj.get_rect()
   textrect.topleft = (x, y)
   windowSurface.blit(textObj, textrect)

def drawLines():
   pygame.draw.line(windowSurface, LTBLUE, (FIRSTLINEX, 0), (FIRSTLINEX, WINDOWHEIGHT), 3)
   pygame.draw.line(windowSurface, LTBLUE, (FIRSTLINEX + 50, 0), (FIRSTLINEX + 50, WINDOWHEIGHT), 1)
   pygame.draw.line(windowSurface, LTBLUE, (FIRSTLINEX + 100, 0), (FIRSTLINEX + 100, WINDOWHEIGHT), 3)
   pygame.draw.line(windowSurface, LTBLUE, (FIRSTLINEX + 150, 0), (FIRSTLINEX + 150, WINDOWHEIGHT), 1)
   pygame.draw.line(windowSurface, LTBLUE, (FIRSTLINEX + 200, 0), (FIRSTLINEX + 200, WINDOWHEIGHT), 3)

#for player creation ((WINDOWWIDTH / 2) - (PLAYERSIZE / 2), WINDOWHEIGHT - PLAYERSIZE - 20)

#set up pygame, window
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("Monster avoider")
pygame.display.set_icon(windowSurface)
pygame.mouse.set_visible(False)

#set up font
font = pygame.font.SysFont(None, 36)
smallerfont = pygame.font.SysFont(None, 28)

#set up images
playerImage = pygame.image.load("images/player.png")
playerRect1 = playerImage.get_rect()
playerRect2 = playerImage.get_rect()
monsterImage = pygame.image.load("images/baddie.png")
monsterStretchedImage = pygame.transform.scale(monsterImage, (MONSTERSIZE, MONSTERSIZE))

topScore = 0
score = 0

####### MENU LOOP
while True:
   monsters = [[], []]     #two sublists of monsters for playerOne and playerTwo
   monsterOneAddCounter = 0
   monsterTwoAddCounter = 0
   MONSTERSPEED = 5
   MONSTERADDRATEMIN = 30 - MONSTERSPEED  #original value = 70
   MONSTERADDRATEMAX = 60 - MONSTERSPEED  #original value = 95
   MONSTERONEADDRATE = random.randint(MONSTERADDRATEMIN, MONSTERADDRATEMAX)
   MONSTERTWOADDRATE = random.randint(MONSTERADDRATEMIN, MONSTERADDRATEMAX)

   playerRect1.topleft = (FIRSTLINEX + 6, WINDOWHEIGHT - PLAYERSIZE - 20)
   playerRect2.topleft = (FIRSTLINEX + 156, WINDOWHEIGHT - PLAYERSIZE - 20)
   playerOnePos = "left"
   playerTwoPos = "right"
   canSpeedUp = False

   for event in pygame.event.get():
      if event.type == QUIT:
         terminate()


   windowSurface.fill(BACKGROUND)
   drawText("Last score: %s" % score, font, windowSurface, 100, 100)
   drawText("Top score: %s" % topScore, font, windowSurface, 100, 140)
   drawText("Q - Play", font, windowSurface, 100, 220)
   drawText("E - Exit", font, windowSurface, 100, 260)
   drawText("Controls:", font, windowSurface, 100, 360)
   drawText("Z - left player", font, windowSurface, 100, 400)
   drawText("LEFT ARROW - right player", font, windowSurface, 100, 440)
   drawText("Your goal is to avoid monsters.", smallerfont, windowSurface, 100, 510)
   drawText("Switch lanes by using controls", smallerfont, windowSurface, 100, 540)
   pygame.display.update()
   gotomenu = waitForPlayerToPressKey()

   score = 0
   ########### Game loop
   while not gotomenu:
      monsterOneAddCounter += 1
      monsterTwoAddCounter += 1
      if score % 20 == 0 and score != 0:
         canSpeedUp = True

      for event in pygame.event.get():
         if event.type == QUIT:
            terminate()
         if event.type == KEYUP:
            if event.key == K_ESCAPE:
               gotomenu = 1
         if event.type == KEYDOWN:
            if event.key == ord("z"):
               if playerOnePos == "left":
                  playerOnePos = "right"
                  playerRect1.move_ip(50, 0)
               elif playerOnePos == "right":
                  playerOnePos = "left"
                  playerRect1.move_ip(-50, 0)
            if event.key == K_LEFT:
               if playerTwoPos == "left":
                  playerTwoPos = "right"
                  playerRect2.move_ip(50, 0)
               elif playerTwoPos == "right":
                  playerTwoPos = "left"
                  playerRect2.move_ip(-50, 0)

      if monsterOneAddCounter == MONSTERONEADDRATE:
         monsterOneAddCounter = 0
         MONSTERONEADDRATE = random.randint(MONSTERADDRATEMIN, MONSTERADDRATEMAX)
         newMonster = { "rect": pygame.Rect(random.choice((FIRSTLINEX + 16, FIRSTLINEX + 66)), 0, MONSTERSIZE, MONSTERSIZE)
                      }
         monsters[0].append(newMonster)

      if monsterTwoAddCounter == MONSTERTWOADDRATE:
         monsterTwoAddCounter = 0
         MONSTERTWOADDRATE = random.randint(MONSTERADDRATEMIN, MONSTERADDRATEMAX)
         newMonster = { "rect": pygame.Rect(random.choice((FIRSTLINEX + 116, FIRSTLINEX + 166)), 0, MONSTERSIZE, MONSTERSIZE)
                      }
         monsters[1].append(newMonster)


      for m in monsters[0]:
         m["rect"].move_ip(0, MONSTERSPEED)

      for m in monsters[1]:
         m["rect"].move_ip(0, MONSTERSPEED)

      for m in monsters[0][:]:
         if m["rect"].top > WINDOWHEIGHT:
            monsters[0].remove(m)
            score += 1
            if canSpeedUp:
               MONSTERSPEED += 1
               canSpeedUp = False
               if MONSTERADDRATEMIN >= 40:
                  MONSTERADDRATEMIN -= MONSTERSPEED
                  MONSTERADDRATEMAX -= MONSTERSPEED

      for m in monsters[1][:]:
         if m["rect"].top > WINDOWHEIGHT:
            monsters[1].remove(m)
            score += 1
            if canSpeedUp:
               MONSTERSPEED += 1
               canSpeedUp = False
               if MONSTERADDRATEMIN >= 40:
                  MONSTERADDRATEMIN -= MONSTERSPEED
                  MONSTERADDRATEMAX -= MONSTERSPEED


      #draw background
      windowSurface.fill(BACKGROUND)

      #draw players
      windowSurface.blit(playerImage, playerRect1)
      windowSurface.blit(playerImage, playerRect2)

      #draw monsters
      for monster in monsters[0]:
         windowSurface.blit(monsterImage, monster["rect"])
      for monster in monsters[1]:
         windowSurface.blit(monsterImage, monster["rect"])

      drawLines()
      drawText("Score:", font, windowSurface, FIRSTLINEX + 280, 20)
      drawText("%s" % score, font, windowSurface, FIRSTLINEX + 280, 60)
      #drawText("%s / %s" % (monsterOneAddCounter ,MONSTERONEADDRATE), font, windowSurface, FIRSTLINEX + 280, 60)
      #drawText("%s / %s" % (monsterTwoAddCounter, MONSTERTWOADDRATE), font, windowSurface, FIRSTLINEX + 280, 100)
      #drawText("%s" % MONSTERSPEED, font, windowSurface, FIRSTLINEX + 280, 140)
      #drawText("%s" % MONSTERADDRATEMIN, font, windowSurface, FIRSTLINEX + 280, 180)
      #drawText("%s" % MONSTERADDRATEMAX, font, windowSurface, FIRSTLINEX + 280, 220)

      pygame.display.update()

      if collisionDetection(playerRect1, playerRect2, monsters):
         if score > topScore:
            topScore = score
         break
      mainClock.tick(FPS)
