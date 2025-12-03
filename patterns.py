import numpy as np

def _pattern_2x2_block(grid: np.ndarray, center_x: int, center_y: int) -> None:
    """最も有名な2×2ブロック - 永遠に拡大するダイヤモンドパターン"""
    grid[center_y:center_y+2, center_x:center_x+2] = 1

def _pattern_oscillator_p3(grid: np.ndarray, center_x: int, center_y: int) -> None:
    """周期3の振動子パターン"""
    positions = [
        (center_y, center_x),
        (center_y, center_x+1),
        (center_y+1, center_x),
        (center_y+1, center_x+1),
    ]
    for y, x in positions:
        grid[y, x] = 1
    grid[center_y-1, center_x] = 2
    grid[center_y-1, center_x+1] = 2
    grid[center_y+2, center_x] = 2
    grid[center_y+2, center_x+1] = 2

def _pattern_cross(grid: np.ndarray, center_x: int, center_y: int) -> None:
    """十字型の発火パターン"""
    for i in range(-2, 3):
        grid[center_y+i, center_x] = 1
        grid[center_y, center_x+i] = 1

def _pattern_line(grid: np.ndarray, center_x: int, center_y: int) -> None:
    """水平線パターン"""
    for i in range(-5, 6):
        grid[center_y, center_x+i] = 1

def create_pattern(width: int, height: int, pattern_name: str) -> np.ndarray:
    """指定された名前のパターンで初期化された盤面を生成する。"""
    grid = np.zeros((height, width), dtype=np.uint8)
    center_y, center_x = height // 2, width // 2

    patterns = {
        "2x2_block": _pattern_2x2_block,
        "oscillator_p3": _pattern_oscillator_p3,
        "cross": _pattern_cross,
        "line": _pattern_line,
    }

    if pattern_name in patterns:
        patterns[pattern_name](grid, center_x, center_y)
    
    return grid
