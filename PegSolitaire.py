import pygame
import game
import solver 
import time

pygame.init()
screen = pygame.display.set_mode((650, 500))
pygame.display.set_caption("Peg Solitaire")
done = False

game.FONT = pygame.font.Font('freesansbold.ttf', 24) 

board =     game.Board()
inst =      game.Instruction()
score =     game.ScoreBoard()
undo =      game.UndoButton()
reset =     game.ResetButton()
auto =      game.Automode()
mhandler =  game.MouseHandler()

driver = game.Driver(board, score, undo, reset, auto)

for i in range(7):
    for j in range(7):
        if board.cells[i][j]:
            board.cells[i][j].driver = driver
            mhandler.add(board.cells[i][j])

undo.driver = driver
mhandler.add(undo)

reset.driver = driver
mhandler.add(reset)

auto.driver = driver
mhandler.add(auto)


while not driver.done and not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:               done = True
                elif event.type == pygame.MOUSEMOTION:      mhandler.handle_motion()
                elif event.type == pygame.MOUSEBUTTONDOWN:  mhandler.handle_click()

        if game.onAutoMod == True: 
            listAction = solver.ans
            for iter in listAction: 
                print(iter)
                mhandler.auto_click(iter[0], iter[1], iter[2])
                screen.fill(game.BLACK)
                board.draw(screen)
                inst.draw(screen)
                score.draw(screen)
                undo.draw(screen)
                reset.draw(screen)
                auto.draw(screen)
                pygame.display.flip()
                time.sleep(1)
            break


        screen.fill(game.BLACK)
        board.draw(screen)
        inst.draw(screen)
        score.draw(screen)
        undo.draw(screen)
        reset.draw(screen)
        auto.draw(screen)
        pygame.display.flip()

text = game.FONT.render("You Win!", True, game.WHITE)
text_rect = text.get_rect()
text_rect.center = 500, 400
        

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        screen.fill(game.BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()