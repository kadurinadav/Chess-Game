import pygame
import sys
from src.game import Game
from src.square import Square
from src.move import Move
from src.piece import *
from src.const import *

class Main:  
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Queen\'s Gambit Project')
        self.game = Game() 

    def mainloop(self):
        dragger = self.game.dragger
        screen = self.screen
        game = self.game
        board = self.game.board

        # while not quit
        while True:
            game.show(screen)

            for event in pygame.event.get():  
                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # save mouse cursor position
                    dragger.update_mouse(pygame.mouse.get_pos())
                    # calculate clicked row and clicked col
                    dragger.save_initial_pos()
                    clicked_row = dragger.clicked_row
                    clicked_col = dragger.clicked_col
                    # check if we need to choose between pawn selection options
                    if board.pawn_promotion:
                        board.choose_pawn_promotion_piece(clicked_row, clicked_col)
                    # check if clicked square has a piece
                    elif board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # check if it is the right color turn
                        if piece.color == board.next_player:
                            # find all valid moves for current piece
                            board.calc_moves(piece, clicked_row, clicked_col, check_flag = True)
                            # drag the piece
                            dragger.drag_piece(piece)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:   
                    if dragger.dragging:
                        dragger.update_mouse(pygame.mouse.get_pos())

                # mouse click release  
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        # save mouse cursor position
                        dragger.update_mouse(pygame.mouse.get_pos())
                        # calculate released row and released col
                        dragger.save_final_pos()
                        released_row = dragger.released_row
                        released_col = dragger.released_col
                        # create possible move
                        initial_sq = Square(dragger.clicked_row, dragger.clicked_col)
                        final_sq = Square(released_row, released_col, dragger.piece)
                        move = Move(initial_sq, final_sq)
                        # check if move is valid
                        if board.valid_move(dragger.piece, move):
                            # check if this is capture move
                            captured = board.squares[released_row][released_col].has_piece()
                            # move
                            board.move(dragger.piece, move, simulating = False)
                            if captured:
                                board.clear_board_history()
                            # play move sound
                            game.play_sound(captured)
                            # check if pawn promotion move
                            if isinstance(dragger.piece, Pawn):
                                board.pawn_promotion = board.check_if_pawn_promotion_move(final_sq)
                            # set en passant property to false to all pawn other than last move piece
                            board.set_false_en_passant()
                            # update next turn
                            board.next_turn()
                            # update board_history
                            board.add_board_to_history()
                            # check if checkmate or stalemate
                            ans = board.is_stalemate_or_checkmate(board.next_player)
                            if ans:
                                # checkmate
                                if ans == 1:
                                    game.checkmate = True
                                # stalemate
                                elif ans == 2:
                                    game.stalemate = True
                                board.next_player = None
                            # check threefold repetition
                            if board.check_threefold_repetition():
                                game.threefold_repetition = True
                                board.next_player = None
                            # check insufficiant material
                            if board.insufficient_material():
                                game.insufficient_material = True
                                board.next_player = None
                        # undrag the piece
                        dragger.undrag_piece()

                # keyboard click
                elif event.type == pygame.KEYDOWN:
                    # if the playes pressed the R key on the keyboard then restart the game 
                    if event.key == pygame.K_r:
                        game.restart()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()