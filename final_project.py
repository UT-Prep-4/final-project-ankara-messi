#Name(s): Aarush, Pranav, Luke
#Final Project - Build Something Worth Showing Off
'''
This is the big one. At the end of camp you will demo this project at the
SHOWCASE, and it should be good enough to put on a resume or mention in a
college application. That means it is not just "code that works." It is a
project you designed, built, polished, and can explain.

WHAT MAKES IT SHOWCASE-WORTHY (the autograder checks for these):
  1. ORGANIZED: your code is split into clear, purposeful segments (functions optional), not one
     giant blob. (Aim for at least 3-4 functions with real jobs.)
  2. SUBSTANTIAL: this is a multi-day build, bigger than the mini-project.
  3. REAL LOGIC: decisions (if/elif/else) and repetition (loops) working together.
  4. DOCUMENTED: fill out PROJECT.md so a stranger (or a college admissions
     reader!) can understand what you built and how to run it.

Whether it is impressive, creative, and demo-ready is judged by humans at
showcase, not by the autograder.

============================= PICK YOUR TRACK =================================

TRACK A: IMAGE PROCESSING PROGRAM
  Build a program that opens an image and transforms it with a special
  function you write yourself: brightness adjustment, a color filter overlay,
  grayscale, mirror, pixelate, or invent your own effect.
  The Pillow library is preinstalled. The core moves:

      from PIL import Image
      img = Image.open("photo.png")
      width, height = img.size
      pixel = img.getpixel((x, y))          # (red, green, blue), each 0-255
      img.putpixel((x, y), (r, g, b))       # set a pixel
      img.save("output.png")                # then click it in VS Code to view!

  Brightness is a for loop over every pixel that multiplies r, g, b by a
  factor the user chooses (careful: values must stay between 0 and 255).
  A filter overlay nudges every pixel toward a color (add red, drop blue...).
  Level up: ask the user which effect to apply with input(), show a menu,
  process any image file they name, draw the result with turtle or pygame.

TRACK B: ADVENTURE GAME
  Build a text adventure where the player explores, makes choices, and wins
  or loses based on decisions and luck. Use random for surprises: treasure,
  traps, enemy encounters, dice rolls, critical hits.
  The shape of it: one function per location or scene, input() for choices,
  an inventory list, health or gold as numbers, and random.randint() for
  the unexpected. Level up: turn-based combat, a map, multiple endings,
  ASCII art title screens, a save-your-score high score.

TRACK C: YOUR OWN IDEA
  A bigger game (pygame or turtle), a quiz app, a tool that solves a real
  problem you have, a simulation, generative turtle art... Pitch it to your
  instructor FIRST, then build it. The four requirements above still apply.

=============================== PLAN FIRST ====================================
Before you write code, fill this in (it will keep you honest all week):

  MY PROJECT: We are building a chess game.
  THE PIECES I NEED TO BUILD: The board, the pieces, and establishing how they move.
  WHAT I WILL DEMO AT SHOWCASE: Play a sample scholar's mate game.

==============================================================================
Build your project below (and split it into more .py files if it gets big;
the grader reads all of them). Delete this line and start!
'''
import pygame
import sys


pygame.init()


BOARD_SIZE = 8
SQUARE_SIZE = 64
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE



FONT = pygame.font.SysFont("arial", 64)

LIGHT_COLOR = (240, 217, 181)  
DARK_COLOR = (181, 136, 99)

PIECES = {
    "wK": "♔", "wQ": "♕", "wR": "♖", "wB": "♗", "wN": "♘", "wP": "♙",
    "bK": "♚", "bQ": "♛", "bR": "♜", "bB": "♝", "bN": "♞", "bP": "♟"
}

BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]








screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Board")

def draw_board():
    """Draws the 8x8 chess board with alternating colors."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            
            if (row + col) % 2 == 0:
                color = LIGHT_COLOR
            else:
                color = DARK_COLOR
            
            
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for r in range(8):
        for c in range(8):
            piece = BOARD[r][c]
            if piece != "--":
                if piece[0] == "w":
                    textColor = (255, 255, 255)
                else:
                    textColor = (0, 0, 0)

                symbol = PIECES[piece] 
                #print(symbol)   
                text_surface = FONT.render(symbol, True, textColor)
                text_rect = text_surface.get_rect()
                text_rect.center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                screen.blit(text_surface, text_rect)




def is_clear_path(startC, startR, targetC, targetR):
    """
    Returns True when every square between the starting square
    and target square is empty.
    """

    row_change = targetR - startR
    col_change = targetC - startC

    # Decide which direction to travel.
    if row_change > 0:
        row_step = 1
    elif row_change < 0:
        row_step = -1
    else:
        row_step = 0

    if col_change > 0:
        col_step = 1
    elif col_change < 0:
        col_step = -1
    else:
        col_step = 0

    currentR = startR + row_step
    currentC = startC + col_step

    # Check every square before the target square.
    while currentR != targetR or currentC != targetC:
        if BOARD[currentR][currentC] != "--":
            return False

        currentR += row_step
        currentC += col_step

    return True



white_move = True



def is_legal_move(white_move, startC, startR, targetC, targetR):
    """
    Checks whether a selected move is legal.
    Returns True or False.
    """

    # Make sure both squares are inside the board.
    if not (0 <= startR < 8 and 0 <= startC < 8):
        return False

    if not (0 <= targetR < 8 and 0 <= targetC < 8):
        return False

    startPiece = BOARD[startR][startC]
    targetPiece = BOARD[targetR][targetC]

    # The player clicked an empty starting square.
    if startPiece == "--":
        return False

    piece_color = startPiece[0]

    # Only allow the correct player to move.
    if white_move and piece_color != "w":
        return False

    if not white_move and piece_color != "b":
        return False

    # Cannot capture your own piece.
    if targetPiece != "--" and targetPiece[0] == piece_color:
        return False

    # Cannot move onto the same square.
    if startR == targetR and startC == targetC:
        return False

    piece_type = startPiece[1]

    row_change = targetR - startR
    col_change = targetC - startC

    # ---------------- PAWN ----------------

    if piece_type == "P":
        # White moves upward, toward smaller row numbers.
        if piece_color == "w":
            direction = -1
            starting_row = 6

        # Black moves downward, toward larger row numbers.
        else:
            direction = 1
            starting_row = 1

        # Move forward one square.
        if (
            col_change == 0
            and row_change == direction
            and targetPiece == "--"
        ):
            return True

        # Move forward two squares from the starting row.
        if (
            col_change == 0
            and row_change == 2 * direction
            and startR == starting_row
            and targetPiece == "--"
        ):
            middle_row = startR + direction

            if BOARD[middle_row][startC] == "--":
                return True

        # Capture one square diagonally.
        if (
            abs(col_change) == 1
            and row_change == direction
            and targetPiece != "--"
            and targetPiece[0] != piece_color
        ):
            return True

        return False

    # ---------------- ROOK ----------------

    if piece_type == "R":
        # A rook moves horizontally or vertically.
        if startR == targetR or startC == targetC:
            return is_clear_path(startC, startR, targetC, targetR)

        return False
        # ---------------- KNIGHT ----------------

    if piece_type == "N":
        # Knights move two squares in one direction
        # and one square in the other direction.
        if (
            abs(row_change) == 2
            and abs(col_change) == 1
        ):
            return True

        if (
            abs(row_change) == 1
            and abs(col_change) == 2
        ):
            return True

        return False

    # ---------------- BISHOP ----------------

    if piece_type == "B":
        # Bishops move diagonally.
        if abs(row_change) == abs(col_change):
            return is_clear_path(
                startC,
                startR,
                targetC,
                targetR
            )

        return False

    # ---------------- QUEEN ----------------

    if piece_type == "Q":
        # A queen can move like a rook.
        moving_straight = (
            startR == targetR
            or startC == targetC
        )

        # A queen can also move like a bishop.
        moving_diagonally = (
            abs(row_change) == abs(col_change)
        )

        if moving_straight or moving_diagonally:
            return is_clear_path(
                startC,
                startR,
                targetC,
                targetR
            )

        return False

    # ---------------- KING ----------------

    if piece_type == "K":
        # The king moves one square in any direction.
        if (
            abs(row_change) <= 1
            and abs(col_change) <= 1
        ):
            return True

        return False

            # ---------------- KNIGHT ----------------

    if piece_type == "N":
        # Knights move two squares in one direction
        # and one square in the other direction.
        if (
            abs(row_change) == 2
            and abs(col_change) == 1
        ):
            return True

        if (
            abs(row_change) == 1
            and abs(col_change) == 2
        ):
            return True

        return False

    # ---------------- BISHOP ----------------

    if piece_type == "B":
        # Bishops move diagonally.
        if abs(row_change) == abs(col_change):
            return is_clear_path(
                startC,
                startR,
                targetC,
                targetR
            )

        return False

    # ---------------- QUEEN ----------------

    if piece_type == "Q":
        # A queen can move like a rook.
        moving_straight = (
            startR == targetR
            or startC == targetC
        )

        # A queen can also move like a bishop.
        moving_diagonally = (
            abs(row_change) == abs(col_change)
        )

        if moving_straight or moving_diagonally:
            return is_clear_path(
                startC,
                startR,
                targetC,
                targetR
            )

        return False

    # ---------------- KING ----------------

    if piece_type == "K":
        # The king moves one square in any direction.
        if (
            abs(row_change) <= 1
            and abs(col_change) <= 1
        ):
            return True

        return False

    # Reject any move that did not match a piece's rules.
    return False

count = 0
startX = -1
startY = -1
targetX = -1
targetY = -1

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            count += 1
            print("Click number:", count)

            # First click: choose the piece.
            if count == 1:
                startX = event.pos[0] // SQUARE_SIZE
                startY = event.pos[1] // SQUARE_SIZE

                targetX = -1
                targetY = -1

                print("Selected:", startX, startY)

            # Second click: choose where the piece moves.
            elif count == 2:
                targetX = event.pos[0] // SQUARE_SIZE
                targetY = event.pos[1] // SQUARE_SIZE

                if is_legal_move(
                    white_move,
                    startX,
                    startY,
                    targetX,
                    targetY
                ):
                    BOARD[targetY][targetX] = BOARD[startY][startX]
                    BOARD[startY][startX] = "--"

                    # Switch turns.
                    white_move = not white_move

                    if white_move:
                        print("White's turn")
                    else:
                        print("Black's turn")

                else:
                    print("Illegal move")

                # Reset after the second click.
                count = 0

    draw_board()
    draw_pieces()
    pygame.display.flip()