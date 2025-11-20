import pygame
import sys
import numpy as np
import math
import time

pygame.init()

WIDTH, HEIGHT = 600, 700
LINE_WIDTH, PANEL_HEIGHT = 8, 90
BG_COLOR, LINE_COLOR = (28, 170, 156), (23, 145, 135)
CROSS_COLOR, CIRCLE_COLOR = (66, 66, 66), (239, 231, 200)
PANEL_COLOR, TEXT_COLOR = (20, 120, 110), (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Level Tic-Tac-Toe")
font = pygame.font.SysFont("Arial", 20, bold=True)
big_font = pygame.font.SysFont("Arial", 32, bold=True)

stats = {
    "games": 0, "wins": 0, "losses": 0, "draws": 0,
    "human_move_times": [], "ai_move_times": [],
    "level_summaries": [], "human_moves": 0, "ai_moves": 0
}

help_remaining = 5       
help_position = None      


def draw_panel_text(lines):
    pygame.draw.rect(screen, PANEL_COLOR, (0, HEIGHT - PANEL_HEIGHT, WIDTH, PANEL_HEIGHT))
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, TEXT_COLOR), (20, HEIGHT - PANEL_HEIGHT + 10 + i * 24))

def draw_message_center(text, y):
    label = big_font.render(text, True, TEXT_COLOR)
    rect = label.get_rect(center=(WIDTH // 2, y))
    screen.blit(label, rect)

#Board
class Board:
    def __init__(self, size):
        self.size = size
        self.squares = np.zeros((size, size), dtype=int)
        self.marked = 0

    def mark(self, r, c, player):
        if self.squares[r, c] == 0:
            self.squares[r, c] = player
            self.marked += 1
            return True
        return False

    def empty_sqr(self, r, c):
        return self.squares[r, c] == 0

    def empty_squares(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.empty_sqr(r, c)]

    def full(self):
        return self.marked == self.size * self.size

    def check_winner(self, win_len):
        S, n, w = self.squares, self.size, win_len
        for r in range(n):
            for c in range(n - w + 1):
                seg = S[r, c:c + w]
                if seg[0] != 0 and np.all(seg == seg[0]):
                    return int(seg[0])
        for c in range(n):
            for r in range(n - w + 1):
                seg = S[r:r + w, c]
                if seg[0] != 0 and np.all(seg == seg[0]):
                    return int(seg[0])
        for r in range(n - w + 1):
            for c in range(n - w + 1):
                d1 = [S[r + i, c + i] for i in range(w)]
                d2 = [S[r + w - 1 - i, c + i] for i in range(w)]
                if d1[0] != 0 and all(x == d1[0] for x in d1):
                    return int(d1[0])
                if d2[0] != 0 and all(x == d2[0] for x in d2):
                    return int(d2[0])
        return 0

# Minimax + Alpha-Beta Pruning
class AI:
    def __init__(self, player=2, depth_limit=None):
        self.player = player
        self.depth_limit = depth_limit

    def best_move(self, board, win_len):
        best_score, best = math.inf, None
        alpha, beta = -math.inf, math.inf
        for (r, c) in board.empty_squares():
            nb = Board(board.size)
            nb.squares = board.squares.copy()
            nb.marked = board.marked
            nb.mark(r, c, self.player)
            score = self.minimax(nb, win_len, 1, True, alpha, beta)
            if score < best_score:
                best_score, best = score, (r, c)
        return best

    def minimax(self, board, win_len, depth, maximizing, alpha, beta):
        winner = board.check_winner(win_len)
        if winner == 1:
            return 1
        if winner == 2:
            return -1
        if board.full():
            return 0
        if self.depth_limit and depth >= self.depth_limit:
            return 0

        if maximizing:
            value = -math.inf
            for (r, c) in board.empty_squares():
                nb = Board(board.size)
                nb.squares = board.squares.copy()
                nb.marked = board.marked
                nb.mark(r, c, 1)
                value = max(value, self.minimax(nb, win_len, depth + 1, False, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for (r, c) in board.empty_squares():
                nb = Board(board.size)
                nb.squares = board.squares.copy()
                nb.marked = board.marked
                nb.mark(r, c, self.player)
                value = min(value, self.minimax(nb, win_len, depth + 1, True, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

def draw_board(board):
    global help_position
    screen.fill(BG_COLOR)
    n, sq = board.size, WIDTH // board.size

    for i in range(1, n):
        pygame.draw.line(screen, LINE_COLOR, (0, i * sq), (WIDTH, i * sq), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * sq, 0), (i * sq, WIDTH), LINE_WIDTH)

    for r in range(n):
        for c in range(n):
            x, y = c * sq + sq // 2, r * sq + sq // 2
            if board.squares[r, c] == 1:
                off = sq // 3
                pygame.draw.line(screen, CROSS_COLOR, (x - off, y - off), (x + off, y + off), LINE_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (x - off, y + off), (x + off, y - off), LINE_WIDTH)
            elif board.squares[r, c] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), sq // 3, LINE_WIDTH)

    if help_position:
        r, c = help_position
        x, y = c * sq + sq // 2, r * sq + sq // 2
        pygame.draw.circle(screen, (255, 0, 255), (x, y), sq // 6, 4)

def draw_winning_line(board, win_len, winner):
    n, sq = board.size, WIDTH // board.size
    S, w = board.squares, win_len
    for r in range(n):
        for c in range(n - w + 1):
            seg = S[r, c:c + w]
            if seg[0] == winner and np.all(seg == seg[0]):
                pygame.draw.line(screen, (255, 0, 0),
                                 (c * sq, r * sq + sq // 2),
                                 ((c + w - 1) * sq + sq, r * sq + sq // 2),
                                 LINE_WIDTH + 4)
                return

def main_menu():
    while True:
        screen.fill(BG_COLOR)
        draw_message_center("Multi-Level Tic-Tac-Toe", HEIGHT // 2 - 80)
        draw_message_center("Press ENTER to Start", HEIGHT // 2)
        draw_message_center("Press Q to Quit", HEIGHT // 2 + 60)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# Levels 
levels = [
    {"label": "Level 1 - Easy (3x3)", "size": 3, "win": 3, "ai_depth": None},
    {"label": "Level 2 - Medium (4x4)", "size": 4, "win": 4, "ai_depth": 4},
    {"label": "Level 3 - Hard (5x5)", "size": 5, "win": 5, "ai_depth": 3}
]

def run_levels():
    main_menu()
    lvl_index = 0
    while lvl_index < len(levels):
        lvl = levels[lvl_index]
        result = play_level(lvl)
        if result == "HUMAN_WIN":
            lvl_index += 1
        else:
            replay_screen = lvl_replay_screen(lvl["label"])
            if replay_screen == "Y":
                continue
            elif replay_screen == "Q":
                print_final_summary()
                pygame.quit(); sys.exit()
    print_final_summary()
    show_completion_screen()

def lvl_replay_screen(level_name):
    while True:
        screen.fill(BG_COLOR)
        draw_message_center(f"You lost or drew {level_name}!", HEIGHT // 2 - 60)
        draw_message_center("Press Y to play again", HEIGHT // 2)
        draw_message_center("Press Q to quit", HEIGHT // 2 + 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return "Y"
                elif event.key == pygame.K_q:
                    return "Q"

def play_level(lvl):
    global help_remaining, help_position
    board = Board(lvl["size"])
    ai = AI(2, lvl["ai_depth"])
    human_turn, running = True, True
    human_times, ai_times = [], []
    human_moves, ai_moves = 0, 0
    human_start_time = time.time()

    while running:
        draw_board(board)
        draw_panel_text([
            lvl["label"],
            f"Wins:{stats['wins']}  Losses:{stats['losses']}  Draws:{stats['draws']}",
            f"Helps left: {help_remaining}"
        ])
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

           
            if e.type == pygame.KEYDOWN and e.key == pygame.K_h and human_turn:
                if help_remaining > 0:
                    mv = ai.best_move(board, lvl["win"])
                    help_position = mv
                    help_remaining -= 1
                    print(f"[HELP] Suggested move: {mv} | Remaining helps: {help_remaining}")
                else:
                    print("[HELP] No helps remaining!")

            
            if e.type == pygame.MOUSEBUTTONDOWN and running and human_turn:
                x, y = e.pos
                sq = WIDTH // board.size
                r, c = y // sq, x // sq
                if 0 <= r < board.size and 0 <= c < board.size and board.empty_sqr(r, c):
                    end = time.time()
                    human_times.append((end - human_start_time) * 1000)
                    board.mark(r, c, 1)
                    human_moves += 1
                    human_turn = False
                    help_position = None

        if running and not human_turn:
            pygame.time.delay(200)
            start_ai = time.time()
            mv = ai.best_move(board, lvl["win"])
            end_ai = time.time()
            if mv:
                board.mark(mv[0], mv[1], 2)
                ai_moves += 1
            ai_times.append((end_ai - start_ai) * 1000)
            human_turn = True
            human_start_time = time.time()

        winner = board.check_winner(lvl["win"])
        if winner or board.full():
            running = False

    stats["games"] += 1
    if winner == 1:
        stats["wins"] += 1; result = "HUMAN_WIN"
    elif winner == 2:
        stats["losses"] += 1; result = "AI_WIN"
    else:
        stats["draws"] += 1; result = "DRAW"

    stats["human_move_times"].extend(human_times)
    stats["ai_move_times"].extend(ai_times)
    stats["human_moves"] += human_moves
    stats["ai_moves"] += ai_moves

    draw_board(board)
    if winner:
        draw_winning_line(board, lvl["win"], winner)
    msg = "You WIN!" if winner == 1 else "AI WINS!" if winner == 2 else "Draw!"
    draw_panel_text([lvl["label"], msg])
    pygame.display.update()
    pygame.time.delay(1500)

    print_level_summary(lvl, human_times, ai_times, human_moves, ai_moves, result)
    return result

def print_level_summary(lvl, human_times, ai_times, human_moves, ai_moves, result):
    print(f"\n--- {lvl['label']} Summary ---")
    print(f"Human Avg: {np.mean(human_times):.2f} ms | Total: {np.sum(human_times):.2f} ms")
    print(f"AI Avg: {np.mean(ai_times):.2f} ms | Total: {np.sum(ai_times):.2f} ms")
    print(f"Human Moves: {human_moves} | AI Moves: {ai_moves}")
    print(f"Winner: {result}")

def print_final_summary():
    total_games = stats["games"]
    accuracy_human = (stats["wins"] / total_games * 100) if total_games > 0 else 0
    accuracy_ai = (stats["losses"] / total_games * 100) if total_games > 0 else 0

    print("\n===== OVERALL PERFORMANCE =====")
    print(f"Games Played: {total_games}")
    print(f"Wins: {stats['wins']} | Losses: {stats['losses']} | Draws: {stats['draws']}")
    print(f"Total Human Moves: {stats['human_moves']} | Total AI Moves: {stats['ai_moves']}")
    print(f"Accuracy (Human): {accuracy_human:.2f}% | Accuracy (AI): {accuracy_ai:.2f}%")
    print("================================")

def show_completion_screen():
    while True:
        screen.fill(BG_COLOR)
        draw_message_center("🎉 You completed all levels!", HEIGHT // 2 - 60)
        draw_message_center(f"Wins: {stats['wins']}  Losses: {stats['losses']}  Draws: {stats['draws']}", HEIGHT // 2)
        draw_message_center("Press Q to quit", HEIGHT // 2 + 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit(); sys.exit()

if __name__ == "__main__":
    run_levels()
