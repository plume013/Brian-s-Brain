from __future__ import annotations
import argparse
import tkinter as tk
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Brian's Brain")
    parser.add_argument("--width", type=int, default=100, help="盤面の横幅")
    parser.add_argument("--height", type=int, default=100, help="盤面の高さ")
    parser.add_argument(
        "--pattern",
        type=str,
        default=None,
        help="有名なパターンを使用 (2x2_block, oscillator_p3, cross, line)。指定しない場合はランダム",
    )
    parser.add_argument(
        "--fire-density",
        type=float,
        default=0.25,
        help="初期状態で発火セル(1)にする確率 (0〜1)",
    )
    parser.add_argument(
        "--refractory-density",
        type=float,
        default=0.00,
        help="初期状態で不応期セル(2)にする確率 (0〜1)。fire と合計が1以下になるように自動調整されます",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=200,
        help="実行ステップ数。-1 で無限",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.1,
        help="各ステップ間の秒数（描画間隔）",
    )
    parser.add_argument(
        "--wrap",
        action="store_true",
    )
    parser.add_argument(
        "--cell-size",
        type=int,
        default=12,
        help="1 マスのピクセルサイズ",
    )
    return parser.parse_args()


def create_grid(width: int, height: int, fire_density: float, refractory_density: float) -> np.ndarray:
    """0/1/2 を指定割合で混在させたランダム初期盤面を生成する。"""
    p_fire = max(0.0, min(1.0, fire_density))
    p_refractory = max(0.0, min(1.0, refractory_density))

    # 合計が1を超えないようにスケール調整
    total = p_fire + p_refractory
    if total > 1.0:
        p_fire /= total
        p_refractory /= total

    rnd = np.random.random((height, width))
    grid = np.zeros((height, width), dtype=np.uint8)
    grid[rnd < p_fire] = 1
    grid[(rnd >= p_fire) & (rnd < p_fire + p_refractory)] = 2
    return grid


def create_famous_pattern(width: int, height: int, pattern_name: str = "2x2_block") -> np.ndarray:
    """Brian's Brain の有名な初期パターンを生成する。

    Args:
        width: 盤面の幅
        height: 盤面の高さ
        pattern_name: パターンの名前
            - "2x2_block": 2×2ブロック（永遠に拡大するダイヤモンド）
            - "oscillator_p3": 周期3の振動子
            - "cross": 十字型パターン

    Returns:
        初期化された盤面
    """
    grid = np.zeros((height, width), dtype=np.uint8)
    center_y, center_x = height // 2, width // 2

    if pattern_name == "2x2_block":
        # 最も有名な2×2ブロック - 永遠に拡大するダイヤモンドパターン
        grid[center_y:center_y+2, center_x:center_x+2] = 1

    elif pattern_name == "oscillator_p3":
        # 周期3の振動子パターン
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

    elif pattern_name == "cross":
        # 十字型の発火パターン
        for i in range(-2, 3):
            grid[center_y+i, center_x] = 1
            grid[center_y, center_x+i] = 1

    elif pattern_name == "line":
        # 水平線パターン
        for i in range(-5, 6):
            grid[center_y, center_x+i] = 1

    return grid


def neighbor_counts(grid: np.ndarray, wrap: bool) -> np.ndarray:
    """周囲8マスに存在する「発火セル(=1)」の数をまとめて計算する。"""
    firing = (grid == 1).astype(np.uint8)  # 0/1 に正規化して数えやすくする

    if wrap:
        # 周囲をトーラス接続したままロールで集計
        return sum(
            np.roll(np.roll(firing, dy, axis=0), dx, axis=1)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )

    # ラップなし: 0 埋めパディングしてスライスで集計
    padded = np.pad(firing, 1, mode="constant")

    return (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] +                     padded[1:-1, 2:] +
        padded[2:, :-2] +  padded[2:, 1:-1] +   padded[2:, 2:]
    )


def step(grid: np.ndarray, wrap: bool) -> np.ndarray:
    """次世代へ進めた盤面を返す（numpy でベクトル化）。"""
    neighbor = neighbor_counts(grid, wrap)
    firing_next = (grid == 0) & (neighbor == 2)
    refractory_next = (grid == 1)
    ready_next = (grid == 2)

    next_grid = np.zeros_like(grid, dtype=np.uint8)
    next_grid[firing_next] = 1
    next_grid[refractory_next] = 2
    next_grid[ready_next] = 0

    return next_grid


class BriansBrainApp:
    def __init__(self, grid: np.ndarray, wrap: bool, interval: float, steps: int, cell_size: int):
        self.grid = grid
        self.wrap = wrap
        self.interval_ms = max(1, int(interval * 1000))
        self.steps_remaining = steps
        self.cell_size = max(2, cell_size)
        self.generation = 0

        height, width = grid.shape

        self.root = tk.Tk()
        self.root.title("Brian's Brain")

        canvas_width = width * self.cell_size
        canvas_height = height * self.cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.pack()

        # キーボードで終了しやすいようにエスケープキーをバインド
        self.root.bind("<Escape>", lambda _: self.root.destroy())

    def draw(self) -> None:
        """現在の盤面をキャンバスに描画する。"""
        self.canvas.delete("all")
        cs = self.cell_size
        # 発火セル(1)を白、不応期セル(2)を赤で描画
        firing_cells = np.argwhere(self.grid == 1)
        for y, x in firing_cells:
            x0, y0 = x * cs, y * cs
            x1, y1 = x0 + cs, y0 + cs
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="")

        refractory_cells = np.argwhere(self.grid == 2)
        for y, x in refractory_cells:
            x0, y0 = x * cs, y * cs
            x1, y1 = x0 + cs, y0 + cs
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline="")
        self.root.title(f"Brian's Brain - Generation {self.generation}")

    def tick(self) -> None:
        """1 ステップ進めて再描画し、次の tick を予約する。"""
        if self.steps_remaining == 0:
            return

        self.draw()
        self.grid = step(self.grid, self.wrap)
        self.generation += 1
        if self.steps_remaining > 0:
            self.steps_remaining -= 1

        # 次のフレームを予約
        self.root.after(self.interval_ms, self.tick)

    def run(self) -> None:
        self.tick()
        self.root.mainloop()


def run() -> None:
    args = parse_args()

    if args.pattern:
        # 有名なパターンを使用
        grid = create_famous_pattern(args.width, args.height, args.pattern)
    else:
        # ランダム初期化
        grid = create_grid(args.width, args.height, args.fire_density, args.refractory_density)

    app = BriansBrainApp(
        grid=grid,
        wrap=args.wrap,
        interval=args.interval,
        steps=args.steps,
        cell_size=args.cell_size,
    )
    app.run()


if __name__ == "__main__":
    run()
