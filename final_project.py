#Name(s): Aarush, Pranav, Luke#Final Project - Build Something Worth Showing Off'''This is the big one. At the end of camp you will demo this project at theSHOWCASE, and it should be good enough to put on a resume or mention in acollege application. That means it is not just "code that works." It is aproject you designed, built, polished, and can explain.
"""
WHAT MAKES IT SHOWCASE-WORTHY (the autograder checks for these):

ORGANIZED: your code is split into clear, purposeful segments (functions optional), not onegiant blob. (Aim for at least 3-4 functions with real jobs.)

SUBSTANTIAL: this is a multi-day build, bigger than the mini-project.

REAL LOGIC: decisions (if/elif/else) and repetition (loops) working together.

DOCUMENTED: fill out PROJECT.md so a stranger (or a college admissionsreader!) can understand what you built and how to run it.

Whether it is impressive, creative, and demo-ready is judged by humans atshowcase, not by the autograder.

============================= PICK YOUR TRACK =================================

TRACK A: IMAGE PROCESSING PROGRAMBuild a program that opens an image and transforms it with a specialfunction you write yourself: brightness adjustment, a color filter overlay,grayscale, mirror, pixelate, or invent your own effect.The Pillow library is preinstalled. The core moves:

  from PIL import Image
  img = Image.open("photo.png")
  width, height = img.size
  pixel = img.getpixel((x, y))          # (red, green, blue), each 0-255
  img.putpixel((x, y), (r, g, b))       # set a pixel
  img.save("output.png")                # then click it in VS Code to view!

Brightness is a for loop over every pixel that multiplies r, g, b by afactor the user chooses (careful: values must stay between 0 and 255).A filter overlay nudges every pixel toward a color (add red, drop blue...).Level up: ask the user which effect to apply with input(), show a menu,process any image file they name, draw the result with turtle or pygame.

TRACK B: ADVENTURE GAMEBuild a text adventure where the player explores, makes choices, and winsor loses based on decisions and luck. Use random for surprises: treasure,traps, enemy encounters, dice rolls, critical hits.The shape of it: one function per location or scene, input() for choices,an inventory list, health or gold as numbers, and random.randint() forthe unexpected. Level up: turn-based combat, a map, multiple endings,ASCII art title screens, a save-your-score high score.

TRACK C: YOUR OWN IDEAA bigger game (pygame or turtle), a quiz app, a tool that solves a realproblem you have, a simulation, generative turtle art... Pitch it to yourinstructor FIRST, then build it. The four requirements above still apply.

=============================== PLAN FIRST ====================================Before you write code, fill this in (it will keep you honest all week):

MY PROJECT: We are building a chess game.THE PIECES I NEED TO BUILD: The board, the pieces, and establishing how they move.WHAT I WILL DEMO AT SHOWCASE: Play a sample scholar's mate game.

==============================================================================Build your project below (and split it into more .py files if it gets big;the grader reads all of them). Delete this line and start!'''import pygameimport sysimport turtle
"""
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
                text_surface = FONT.render(symbol, True, textColor)
                text_rect = text_surface.get_rect()
                text_rect.center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                screen.blit(text_surface, text_rect)


def is_clear_path(startC, startR, targetC, targetR):
    """Returns True when every square between the starting square
    and target square is empty."""

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
    """Checks whether a selected move is legal.
    Returns True or False."""

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
        if col_change == 0 and row_change == direction and targetPiece == "--":
            return True

        # Move forward two squares from the starting row.
        if (col_change == 0 and row_change == 2 * direction
                and startR == starting_row and targetPiece == "--"):
            middle_row = startR + direction
            if BOARD[middle_row][startC] == "--":
                return True

        # Capture one square diagonally.
        if (abs(col_change) == 1 and row_change == direction
                and targetPiece != "--" and targetPiece[0] != piece_color):
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
        if abs(row_change) == 2 and abs(col_change) == 1:
            return True
        if abs(row_change) == 1 and abs(col_change) == 2:
            return True
        return False

    # ---------------- BISHOP ----------------
    if piece_type == "B":
        # Bishops move diagonally.
        if abs(row_change) == abs(col_change):
            return is_clear_path(startC, startR, targetC, targetR)
        return False

    # ---------------- QUEEN ----------------
    if piece_type == "Q":
        # A queen can move like a rook.
        moving_straight = (startR == targetR or startC == targetC)
        # A queen can also move like a bishop.
        moving_diagonally = (abs(row_change) == abs(col_change))

        if moving_straight or moving_diagonally:
            return is_clear_path(startC, startR, targetC, targetR)
        return False

    # ---------------- KING ----------------
    if piece_type == "K":
        # The king moves one square in any direction.
        if abs(row_change) <= 1 and abs(col_change) <= 1:
            return True
        return False

    # Reject any move that did not match a piece's rules.
    return False


count = 0
startX = -1
startY = -1
targetX = -1
targetY = -1


def highlight_moves(white_move, startC, startR, SQUARE_SIZE):
    startPiece = BOARD[startR][startC]
    piece_color = startPiece[0]
    piece_type = startPiece[1]

    for r in range(8):
        for c in range(8):
            if is_legal_move(white_move, startC, startR, c, r):
                x = c * SQUARE_SIZE
                y = r * SQUARE_SIZE
                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))



def find_king(color):
    for row in range(8):
        for col in range(8):
            if BOARD[row][col] == color + "K":
                return col, row

    return None


def is_square_attacked(targetC, targetR, attacking_color):
    for startR in range(8):
        for startC in range(8):
            piece = BOARD[startR][startC]

            if piece == "--" or piece[0] != attacking_color:
                continue

            piece_type = piece[1]
            row_change = targetR - startR
            col_change = targetC - startC

            # Pawn attacks
            if piece_type == "P":
                if attacking_color == "w":
                    direction = -1
                else:
                    direction = 1

                if row_change == direction and abs(col_change) == 1:
                    return True

            # Knight attacks
            elif piece_type == "N":
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

            # Bishop attacks
            elif piece_type == "B":
                if abs(row_change) == abs(col_change):
                    if is_clear_path(
                        startC,
                        startR,
                        targetC,
                        targetR
                    ):
                        return True

            # Rook attacks
            elif piece_type == "R":
                if startR == targetR or startC == targetC:
                    if is_clear_path(
                        startC,
                        startR,
                        targetC,
                        targetR
                    ):
                        return True

            # Queen attacks
            elif piece_type == "Q":
                moving_straight = (
                    startR == targetR
                    or startC == targetC
                )

                moving_diagonally = (
                    abs(row_change) == abs(col_change)
                )

                if moving_straight or moving_diagonally:
                    if is_clear_path(
                        startC,
                        startR,
                        targetC,
                        targetR
                    ):
                        return True

            # King attacks
            elif piece_type == "K":
                if (
                    abs(row_change) <= 1
                    and abs(col_change) <= 1
                ):
                    return True

    return False


def is_in_check(color):
    king_location = find_king(color)

    if king_location is None:
        return False

    kingC, kingR = king_location

    if color == "w":
        enemy_color = "b"
    else:
        enemy_color = "w"

    return is_square_attacked(
        kingC,
        kingR,
        enemy_color
    )


def move_keeps_king_safe(
    white_move,
    startC,
    startR,
    targetC,
    targetR
):
    if not is_legal_move(
        white_move,
        startC,
        startR,
        targetC,
        targetR
    ):
        return False

    moving_piece = BOARD[startR][startC]
    captured_piece = BOARD[targetR][targetC]

    # Temporarily make the move.
    BOARD[targetR][targetC] = moving_piece
    BOARD[startR][startC] = "--"

    moving_color = moving_piece[0]
    safe = not is_in_check(moving_color)

    # Undo the temporary move.
    BOARD[startR][startC] = moving_piece
    BOARD[targetR][targetC] = captured_piece

    return safe


def is_checkmate(color):
    if not is_in_check(color):
        return False

    if color == "w":
        white_turn = True
    else:
        white_turn = False

    for startR in range(8):
        for startC in range(8):
            piece = BOARD[startR][startC]

            if piece == "--" or piece[0] != color:
                continue

            for targetR in range(8):
                for targetC in range(8):
                    if move_keeps_king_safe(
                        white_turn,
                        startC,
                        startR,
                        targetC,
                        targetR
                    ):
                        return False

    return True


def draw_checkmate_screen(winner):
    flash = pygame.time.get_ticks() // 500

    if flash % 2 == 0:
        green = (0, 220, 80)
    else:
        green = (0, 130, 50)

    pygame.draw.rect(
        screen,
        green,
        pygame.Rect(
            0,
            0,
            WINDOW_SIZE,
            WINDOW_SIZE
        )
    )

    checkmate_font = pygame.font.SysFont(
        "arial",
        55,
        bold=True
    )

    winner_font = pygame.font.SysFont(
        "arial",
        32,
        bold=True
    )

    checkmate_text = checkmate_font.render(
        "CHECKMATE!",
        True,
        (255, 255, 255)
    )

    winner_text = winner_font.render(
        winner + " wins!",
        True,
        (255, 255, 255)
    )

    checkmate_rect = checkmate_text.get_rect(
        center=(
            WINDOW_SIZE // 2,
            WINDOW_SIZE // 2 - 30
        )
    )

    winner_rect = winner_text.get_rect(
        center=(
            WINDOW_SIZE // 2,
            WINDOW_SIZE // 2 + 35
        )
    )

    screen.blit(checkmate_text, checkmate_rect)
    screen.blit(winner_text, winner_rect)
game_over = False
winner = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif   event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            count += 1
            print("Click number:", count)

            # First click: choose the piece.
            if count == 1:
                startX = event.pos[0] // SQUARE_SIZE
                startY = event.pos[1] // SQUARE_SIZE

                targetX = -1
                targetY = -1

                print("Selected:", startX, startY)
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(256, 320, SQUARE_SIZE, SQUARE_SIZE))

            # Second click: choose where the piece moves.
            elif count == 2:
                targetX = event.pos[0] // SQUARE_SIZE
                targetY = event.pos[1] // SQUARE_SIZE

                if move_keeps_king_safe(white_move, startX, startY, targetX, targetY):
                    BOARD[targetY][targetX] = BOARD[startY][startX]
                    BOARD[startY][startX] = "--"
                

                    # Switch turns.
                    white_move = not white_move

                    if white_move:
                        current_color = "w"
                    else:
                        current_color = "b"

                    if is_checkmate(current_color):
                        game_over = True

                    if current_color == "w":
                        winner = "Black"
                    else:
                        winner = "White"

                # Reset after the second click.
                count = 0

    if count == 1:
        draw_board()
        highlight_moves(white_move, startX, startY, SQUARE_SIZE)
    else:
        draw_board()

    
    draw_pieces()
    if game_over:
        draw_checkmate_screen(winner)

    pygame.display.flip()