import pygame
import sys
import os.path
import math
pygame.init()


#some rgb values
black = (0, 0, 0)
white = (255, 255, 255)

window=pygame.display.set_mode((1000,750))

def distance(x1,y1,x2,y2):
    return ((x1-x2)** 2 + (y1-y2) ** 2) ** 0.5
#GameBoard Class
class GameBoard(object):
    
    #initialzes board data
    def __init__(self,path=[],size=15):
        self.path= path #takes list of tuples same as path number
        self.width= 1000
        self.height = 750
        self.rows=15
        self.cols=15
        self.screen = window
        pygame.display.set_caption('GPA Defense')
        self.clock = pygame.time.Clock()
        self.cellSize= 50
        self.board = [ [None]*self.cols for row in range(self.rows) ]
        
        #images
        self.grass= pygame.image.load("images" + os.sep + "grass.jpg").convert()
        self.roadBend = pygame.image.load("images" + os.sep + "roadbend.png").convert()
        self.roadStraight = pygame.image.load("images" + os.sep + "roadstraight.png").convert()
        self.roadBendRotated = pygame.transform.rotate(self.roadBend, 180)
        self.roadStraightRotated = pygame.transform.rotate(self.roadStraight, 90)
        
        #path stuffs
        self.pathLocations =[] #List of Tuples of where paths are drawn
        self.pathImg = None
    
    #sets path data on to board data
    def initPath(self):
        currRow=0
        currCol=0 
        for index in range(len(self.path)):
            self.board[currRow][currCol]=self.path[index]
            self.pathLocations.append((currCol,currRow))
            currCol+=self.path[index][0]
            currRow+=self.path[index][1]
    #returns list of direction tuples for Ken's part
    def getDirection(self):
        return self.path

GPA=4.00
isHolding = False
selectedTower = None
dinex = 20000
cellSize = 50

redOut = pygame.image.load("outlines" + os.sep + "redoutline.png").convert_alpha()
redOut = pygame.transform.scale(redOut, (cellSize, cellSize))
redOut.set_colorkey(black)
blueOut = pygame.image.load("outlines" + os.sep + "blueoutline.png").convert_alpha()
blueOut = pygame.transform.scale(blueOut, (cellSize, cellSize))
blueOut.set_colorkey(black)
redSurface = pygame.Surface((cellSize, cellSize), pygame.SRCALPHA, 32)
redSurface.convert_alpha(redSurface)
redSurface.blit(redOut, (0,0))
blueSurface = pygame.Surface((cellSize, cellSize), pygame.SRCALPHA, 32)
blueSurface.blit(blueOut, (0,0))

#helper functions
def getNewTower(x, y, towerType):
    cellSize = 50
    if towerType == "wean":
        newTower = TowerWean(x, y, cellSize)
    elif towerType == "gates":
        newTower = TowerGates(x, y, cellSize)
    elif towerType == "tent":
        newTower = TowerTent(x, y, cellSize)
    elif towerType == "cfa":
        newTower = TowerCFA(x, y, cellSize)
    return newTower

def drawOutline(cellSize):
    mouseX, mouseY = pygame.mouse.get_pos()
    col, row = mouseX // cellSize, mouseY // cellSize
    x, y = col * cellSize, row * cellSize
    if board2DList[row][col] == None:
        board.screen.blit(blueSurface, (x, y))
    else:
        board.screen.blit(redSurface, (x, y))

# classes
class Tower(pygame.sprite.Sprite):
    price = None
    damage = None
    fireRate = None
    def __init__(self, x, y, cellSize):
        pygame.sprite.Sprite.__init__(self)

        self.col, self.row = x // cellSize, y // cellSize
        self.x, self.y = self.col * cellSize, self.row * cellSize
        self.cx, self.cy = x + cellSize / 2, y + cellSize / 2

        self.cellSize = cellSize
        self.range = 2 * cellSize
        self.hitbox = pygame.Rect((self.x - self.range), (self.y - self.range),
                                  2 * self.range, 2 * self.range)
        self.tSurface = pygame.Surface((cellSize, cellSize))

        self.lockedEnemy = None

    def findEnemy(self, enemyLst):
        if self.lockedEnemy == None:
            for enemy in enemyLst[::-1]:
                if abs(enemy.cx - self.cx) <= self.range \
                        and abs(enemy.cy - self.cy) <= self.range:
                    self.lockedEnemy = enemy
                    break
        elif self.lockedEnemy not in enemyLst:
            self.lockedEnemy = None
            
    def draw(self):
        window.blit(self.tSurface, (self.x, self.y))
    
    def fire(self):
        if self.lockedEnemy != None:
            angle = math.atan(self.lockedEnemy.y/self.lockedEnemy.x)
            newBullet = Bullet(self.cx, self.cy, angle)

class TowerTent(Tower):
    price = 250
    damage = 2
    fireRate = 1

    def __init__(self, x, y, cellSize):
        super().__init__(x, y, cellSize)
        self.tSurface = pygame.Surface((cellSize, cellSize))
        self.tImage = pygame.image.load("images" + os.sep + "tent.png")
        self.tSurface.blit(self.tImage, (0, 0))
    
    def findEnemy(self, enemyLst):
        if self.lockedEnemy == None:
            for enemy in enemyLst[::-1]:
                if abs(enemy.cx - self.cx <= self.range) \
                        and abs(enemy.cy - self.cy <= self.range):
                    self.lockedEnemy=enemy
        elif self.lockedEnemy not in enemyLst:
            self.lockedEnemy = None
    #
    # def fire(self):
    #     if self.lockedEnemy != None:
    #         angle = math.atan(self.lockedEnemy.y/self.lockedEnemy.x)
    #         newBullet = Bullet(self.cx, self.cy, angle)


class TowerCFA(Tower):
    price = 1000
    damage = 1
    fireRate = 1

    def __init__(self, x, y, cellSize):
        super().__init__(x, y, cellSize)
        self.tSurface = pygame.Surface((cellSize, cellSize))
        self.tImage = pygame.image.load("images" + os.sep + "cfa.png")
        self.tSurface.blit(self.tImage, (0, 0))

        self.lockedEnemy = None

    def findEnemy(self, enemyLst):
        if self.lockedEnemy == None:
            for enemy in enemyLst[::-1]:
                if abs(enemy.cx - self.cx <= self.range) \
                        and abs(enemy.cy - self.cy <= self.range):
                    self.lockedEnemy=enemy
        elif self.lockedEnemy not in enemyLst:
            self.lockedEnemy = None

    def AOEfire(self):
        for enemy in self.lockedEnemy:
            enemy.health -= self.damage

class TowerGates(Tower):
    price = 1500
    damage = 20
    fireRate = 5
    def __init__(self, x, y, cellSize):
        super().__init__(x, y, cellSize)
        self.tSurface = pygame.Surface((cellSize, cellSize))
        self.tImage = pygame.image.load("images" + os.sep + "gates.png")
        self.tSurface.blit(self.tImage, (0, 0))
    
    def findEnemy(self, enemyLst):
        if self.lockedEnemy == None:
            for enemy in enemyLst[::-1]:
                if abs(enemy.cx - self.cx <= self.range) \
                        and abs(enemy.cy - self.cy <= self.range):
                    self.lockedEnemy=enemy
        elif self.lockedEnemy not in enemyLst:
            self.lockedEnemy = None
    # def fire(self):
    #     if self.lockedEnemy != None:
    #         angle = math.atan(self.lockedEnemy.y/self.lockedEnemy.x)
    #         newBullet = BulletGates(self.cx, self.cy, angle)


class TowerWean(Tower):
    price = 500
    damage = 5
    fireRate = 1

    def __init__(self, x, y, cellSize):
        super().__init__(x, y, cellSize)
        self.tSurface = pygame.Surface((cellSize, cellSize))
        self.tImage = pygame.image.load("images" + os.sep + "wean.png")
        self.tSurface.blit(self.tImage, (0, 0))
    
    def findEnemy(self, enemyLst):
        if self.lockedEnemy == None:
            for enemy in enemyLst[::-1]:
                if abs(enemy.cx - self.cx <= self.range) \
                        and abs(enemy.cy - self.cy <= self.range):
                    self.lockedEnemy=enemy
        elif self.lockedEnemy not in enemyLst:
            self.lockedEnemy = None
class Bullet(object):
    
    def __init__(self,start,end,speed,bulletSize,damage):
        self.x=start[0]
        self.y=start[1]
        self.start=start
        self.end=end
        self.speed = speed
        self.hitBox=[self.x,self.y,self.x+bulletSize,self.y+bulletSize]
        self.bulletSize=bulletSize
        self.damage=damage
    
    def draw(self, window):
        self.moveBullet()
        pygame.draw.rect(window,(0,255,0),(self.x,self.y,self.bulletSize,self.bulletSize))

    # def moveBullet(self):
    #     gradient=(self.end[1]-self.start[1])/(self.end[0]-self.start[0])
    #     angle=math.atan(gradient)
    #     self.x += math.cos(angle)*self.speed
    #     self.y -= math.sin(angle)*self.speed
    #     self.hitBox=[self.x,self.y,self.x+self.bulletSize,self.y+self.bulletSize]
        
    def moveBullet(self):
        dx=self.start[0]-self.end[0]
        dy=self.start[1]-self.end[1]
        r=distance(self.start[0],self.start[1],self.end[0],self.end[1])
        self.x-=(dx/r)*self.speed
        self.y-=(dy/r)*self.speed
        self.hitBox=[self.x,self.y,self.x+self.bulletSize,self.y+self.bulletSize]
        
    def collidesWithEnemy(self, other):
        if(not isinstance(other, Enemy)): 
            return False
        else:
            if self.hitBox[0]<other.hitBox[2] and self.hitBox[2]>other.hitBox[0] and self.hitBox[1]<other.hitBox[3] and self.hitBox[3]>other.hitBox[1]:
                    return True
            
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self,x,y,cellSize,directionLst,grade,gradeInt,speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self.directions = directionLst
        self.grade = grade
        self.gradeInt = gradeInt
        self.speed = speed
        self.currCell = 0
        self.hitBox = [self.x,self.y,self.x+cellSize,self.y+cellSize]
        self.health=30*gradeInt
        self.cx=self.x+self.cellSize/2
        self.cy=self.y+self.cellSize/2
        self.center=[self.cx,self.cy]
        
    def move(self):
        currDirection = self.directions[self.currCell]
        dcol,drow = currDirection[0],currDirection[1]
        self.x += self.speed*dcol
        self.y += self.speed*drow
        self.cx=self.x+self.cellSize/2
        self.cy=self.y+self.cellSize/2
        self.center=[self.cx,self.cy]
        self.hitBox = [self.x,self.y,self.x+cellSize,self.y+cellSize]
        if self.x%self.cellSize == 0 and self.x != 0 and dcol!=0:
            self.currCell+=1
        elif self.y%self.cellSize == 0 and self.y !=0 and drow!=0:
            self.currCell += 1
    

    def draw(self,window):
        self.move()
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,self.cellSize,self.cellSize))
        window.blit(scaledImage, (self.x, self.y))
    
#initial values
enemies=[]
bullets=[]
towers=[]
board = GameBoard([(1,0)]*3 + [(1,0)]*3 + [(0,1)]*5 + [(1,0)]*3 + [(0,1)]*2 +[(1,0)]*3+[(0,1)]*7+[(0,0)])
board2DList=board.board
board.initPath()
directionLst=board.getDirection()
clock=pygame.time.Clock()
cellSize=50
image=pygame.image.load("images" + os.sep + "test.jpg")
scaledImage=pygame.transform.scale(image,(cellSize,cellSize))
t=True
start=(200,200)


def redrawAll():
    window.fill((255,255,255))
    global GPA
    global dinex
    font = pygame.font.SysFont("Arial", 20)
    text1 = font.render("INSTRUCTIONS: ", 1, (0, 0, 0))
    text1pos = (755, 5)
    text2 = font.render("Press w,t,c,g for different towers", 1, (0, 0, 0))
    text2pos = (755, 25)
    text3 = font.render("Click with mouse to place tower", 1, (0, 0, 0))
    text3pos = (755, 45)
    text4 = font.render("w = Wean(500), t = Tent(250)", 1, (0, 0, 0))
    text4pos = (755, 85)
    text5 = font.render("c = CFA(1000), g = Gates(150)", 1, (0, 0, 0))
    text5pos = (755, 105)
    text6 = font.render("Press Esc to unselect", 1, (0, 0, 0))
    text6pos = (755, 125)
    text7 = font.render("GPA: %0.2f "%(GPA), 1, (0, 0, 0))
    text7pos = (755, 165)
    text8 = font.render("DineX: %d "%(dinex), 1, (0, 0, 0))
    text8pos = (755, 185)
    window.blit(text1, text1pos)
    window.blit(text2, text2pos)
    window.blit(text3, text3pos)
    window.blit(text4, text4pos)
    window.blit(text5, text5pos)
    window.blit(text6, text6pos)
    window.blit(text7, text7pos)
    window.blit(text8, text8pos)
    
    board.screen.blit((pygame.transform.scale(board.grass, (750,750))), (0,0)) 
    
    for path in range(len(board.path) - 1):
        if path!=0 and board.path[path-1] == (1,0) and board.path[path] == (0,1):
            board.pathImg = pygame.transform.scale(board.roadBend, (board.cellSize, board.cellSize))
            
        elif path!=0 and board.path[path-1] == (0,1) and board.path[path] == (1,0):
            board.pathImg = pygame.transform.scale(board.roadBendRotated, (board.cellSize, board.cellSize))
        
        elif board.path[path] == (1, 0):
            board.pathImg = pygame.transform.scale(board.roadStraight, (board.cellSize, board.cellSize))
            
        elif board.path[path] == (0, 1):
            board.pathImg = pygame.transform.scale(board.roadStraightRotated, (board.cellSize, board.cellSize))
            
        board.screen.blit(board.pathImg, (board.pathLocations[path][0]*board.cellSize, board.pathLocations[path
][1]*board.cellSize))
        
        
    board.screen.blit(board.pathImg, (board.pathLocations[-1][0]*board.cellSize, board.pathLocations[-1][1]*board.cellSize))

    for tow in towers:
        tow.draw()
        tow.findEnemy(enemies)
        if tow.lockedEnemy!=None:
            b=Bullet((tow.cx,tow.cy),tow.lockedEnemy.center,50,6,12)
            bullets.append(b)
    
    for enem in enemies:
        
        if enem.directions[enem.currCell]==(0,0):
            GPA-=0.01
            if enem in enemies:
                enemies.remove(enem)
        if enem.health<=0:
            dinex+=100
            if enem in enemies:
                enemies.remove(enem)
        
        enem.draw(window)
    
    for bul in bullets:
        bul.draw(window)
        if bul.x<0 or bul.x>750 or bul.y<0 or bul.y>750:
            if bul in bullets:
                bullets.remove(bul)
        for enem in enemies:
            if bul.collidesWithEnemy(enem):
                enem.health-=bul.damage
                if bul in bullets:
                    bullets.remove(bul)
    if isHolding:
        drawOutline(cellSize)
                
    #updates the display, NEED TO CHANGE THIS TO UPDATE SPECIFIC SURFACES NOT THE WHOLE DISPLAY
    pygame.display.update()
    

while t:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
            
        if isHolding:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                col, row = mouseX // cellSize, mouseY // cellSize
                if mouseX < 750 and board2DList[row][col] == None:  # click within board screen
                    newTower = getNewTower(mouseX, mouseY, selectedTower)
                    towers.append(newTower)
                    board2DList[row][col] = "tower"
                    dinex -= newTower.price
                    selectedTower = None
                    isHolding = None     
            
        
    keys=pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        e=Enemy(0,0,cellSize,directionLst,"R",4,5)
        enemies.insert(0,e)
    if isHolding:
        #drawOutline(cellSize)
        if keys[pygame.K_ESCAPE]:
            isHolding = False
            selectedTower = None
    if keys[pygame.K_t]:
        if dinex >= TowerTent.price:
            isHolding = True
            selectedTower = "tent"
    elif keys[pygame.K_g]:
        if dinex >= TowerGates.price:
            isHolding = True
            selectedTower = "gates"
    elif keys[pygame.K_w]:
        if dinex >= TowerWean.price:
            isHolding = True
            selectedTower = "wean"
    elif keys[pygame.K_c]:
        if dinex >= TowerCFA.price:
            isHolding = True
            selectedTower = "cfa"
        
    redrawAll()

pygame.quit()
        
    
    
    

