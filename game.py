import pygame
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREEN = 65, 79, 71
GREEN = 89, 153, 78
BROWN = 193, 154, 107

FONT = None

onAutoMod = False
import time
class Instruction:
    rect = pygame.Rect(0, 0, 600, 80)
    text = "Your Goal is to Have One Peg Remaining"
    def draw(self, surf):
        text = FONT.render(self.text, True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surf.blit(text, text_rect)

class ScoreBoard:
    rect = pygame.Rect(460, 80, 140, 60)
    text = "Pegs: "
    npegs = 0
    def draw(self, surf):
        text = FONT.render(self.text + str(self.npegs), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surf.blit(text, text_rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)

class UndoButton:
    rect = pygame.Rect(460, 180, 140, 60)
    text = "Undo"
    mhover = False
    driver = None
    def draw(self, surf):
        if self.mhover:  pygame.draw.rect(surf, WHITE, self.rect)
        color = BLACK if self.mhover else WHITE
        text = FONT.render(self.text, True, color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surf.blit(text, text_rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)
    
    def on_click(self):
        self.driver.on_undo()

class ResetButton:
    rect = pygame.Rect(460, 280, 140, 60)
    text = "Reset"
    mhover = False
    driver = None
    def draw(self, surf):
        if self.mhover:  pygame.draw.rect(surf, WHITE, self.rect)
        color = BLACK if self.mhover else WHITE
        text = FONT.render(self.text, True, color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surf.blit(text, text_rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)

    def on_click(self):
        self.driver.on_reset()
        

class Automode:
    rect = pygame.Rect(460, 380, 140, 60)
    text = "Auto mode"
    mhover = False
    driver = None
    def draw(self, surf):
        if self.mhover:  pygame.draw.rect(surf, WHITE, self.rect)
        color = BLACK if self.mhover else WHITE
        text = FONT.render(self.text, True, color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        surf.blit(text, text_rect)
        pygame.draw.rect(surf, WHITE, self.rect, 2)

    def on_click(self):
        self.driver.on_auto()

class Cell:
    mhover = False
    driver = None
    cid = None
    sel = False
    loc = None
    empty = None
    color = None
    rect = pygame.Rect(0, 0, 50, 50)

    def on_click(self):
        self.driver.on_cell(self)

class Board:
    cells = None
    rect = None

    def __init__(self):

        self.rect = pygame.Rect(20, 80, 600, 600)
        self.cells = [[None for j in range(7)] for i in range(7)]

        cid = 1
        loc = (1, 0)
        while cid < 34:
            if   cid == 4:  loc = (2, 1)
            elif cid == 7:  loc = (0, 2)
            elif cid == 14: loc = (0, 3)
            elif cid == 21: loc = (0, 4)
            elif cid == 28: loc = (2, 5)
            elif cid == 31: loc = (2, 6)
            else:           loc = (loc[0] + 1, loc[1])
            cell = Cell()
            cell.cid = cid
            cell.loc = loc
            cell.empty = False
            cell.color = BLACK
            cell.rect = cell.rect.move(50*loc[0] + self.rect.left + 3, 50*loc[1] + self.rect.top + 3)
            self.cells[loc[0]][loc[1]] = cell
            cid += 1
        
    def draw(self, surf):
        for i in range(7):
            for j in range(7):
                if self.cells[i][j]:
                    rect = self.cells[i][j].rect
                    color = GREEN if self.cells[i][j].mhover else DARK_GREEN
                    color = WHITE if self.cells[i][j].sel else color
                    pygame.draw.rect(surf, color, rect)
                    
                    if not self.cells[i][j].empty:
                        rect = pygame.Rect(rect.left + 10, rect.top + 10, 30, 30)
                        pygame.draw.rect(surf, BROWN, rect)

class MouseHandler:
    pmon = None
    objs = []

    def add(self, obj):
        self.objs.append(obj)

    def handle_motion(self):
        mpos = pygame.mouse.get_pos()
        mon = self.mouse_on(mpos)
        if mon:
            mon.mhover = True
        if self.pmon and self.pmon != mon:
            self.pmon.mhover = False
        self.pmon = mon

    def handle_click(self):
        mpos = pygame.mouse.get_pos()
        mon = self.mouse_on(mpos)
        if mon: mon.on_click()

    def auto_click(self, x, y, nextState): 
        mpos = (50 + (y * 50), 100 + (x * 50))
        mon = self.mouse_on(mpos)
        if mon: 
            mon.on_click()
            mon.mhover = True 
            
        if mon:
            mon.mhover = True
        if self.pmon and self.pmon != mon:
            self.pmon.mhover = False
        self.pmon = mon
 

        if nextState == 1: x, y = x + 2, y 
        if nextState == 2: x, y = x - 2, y 
        if nextState == 3: x, y = x, y + 2
        if nextState == 4: x, y = x, y - 2
 

        mpos = (50 + (y * 50), 100 + (x * 50))
        mon = self.mouse_on(mpos)
        if mon: mon.on_click()


    def mouse_on(self, mpos):
        for obj in self.objs:
            if obj.rect.collidepoint(mpos):
                return obj
        return None

# I CONTROLL ALL THINGS
class Driver:
    board = None
    score = None
    undo = None
    reset = None
    c_sel = None
    done = False
    auto = False
    undo_q = []

    def __init__(self, board, score, undo, reset, auto):
        self.board = board
        self.score = score
        self.undo = undo
        self.reset = reset
        self.auto = auto
       
        self.on_reset()
    
    def recount(self):
        npegs = 0
        for i in range(7):
            for j in range(7):
                if self.board.cells[i][j]:
                    npegs = npegs if self.board.cells[i][j].empty else npegs + 1
        self.score.npegs = npegs
        if npegs == 1:
            self.done = True

    def action(self, c1, c2):
        if not c2.empty: return
        mcell = None
        if  c2.loc == (c1.loc[0] + 2, c1.loc[1]):       mcell = self.board.cells[c1.loc[0] + 1][c1.loc[1]]
        elif c2.loc == (c1.loc[0] - 2, c1.loc[1]):      mcell = self.board.cells[c1.loc[0] - 1][c1.loc[1]]
        elif c2.loc == (c1.loc[0], c1.loc[1] + 2):      mcell = self.board.cells[c1.loc[0]][c1.loc[1] + 1]
        elif c2.loc == (c1.loc[0], c1.loc[1] - 2):      mcell = self.board.cells[c1.loc[0]][c1.loc[1] - 1]
        else:                                           return
        if mcell.empty:                                 return

        mcell.empty = True
        c1.empty = True
        c2.empty = False
        self.undo_q.append((c1, mcell, c2))
        self.recount()
 
    def on_auto(self): 
        global onAutoMod
        onAutoMod = True
        return None 


    def on_cell(self, cell):
        if self.c_sel:
            self.action(self.c_sel, cell)
            self.c_sel.sel = False
            self.c_sel = None
        else:
            if not cell.empty:
                self.c_sel = cell
                self.c_sel.sel = True


    def on_undo(self):
        if self.c_sel:
            self.c_sel.sel = False
            self.c_sel = None
        if self.undo_q:
            c1, mcell, c2 = self.undo_q.pop()
            c1.empty = False
            mcell.empty = False
            c2.empty = True
            self.recount()

    def on_reset(self):
        if self.c_sel:
            self.c_sel.sel = False
            self.c_sel = None
        for i in range(7):
            for j in range(7):
                if self.board.cells[i][j]:
                    self.board.cells[i][j].empty = False
        self.board.cells[3][3].empty = True
        self.recount()
        self.undo_q = []