from __future__ import annotations
import argparse
import tkinter as tk
import numpy as np

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conway のライフゲーム")
    parser.add_argument("--width", type=int, default=400, help="盤面の横幅")
    parser.add_argument("--height", type=int, default=200, help="盤面の高さ")
    parser.add_argument(
        "--density",
        type=float,
        default=0.25,
        help="初期状態で生きている確率 (0〜1)",
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
        help="端をトーラス状に接続する（ラップあり）",
    )
    parser.add_argument(
        "--cell-size",
        type=int,
        default=12,
        help="1 マスのピクセルサイズ",
    )
    return parser.parse_args()


def create_grid(width: int, height: int, density: float) -> np.ndarray:
    """ランダムな初期盤面を生成する。"""
    density = max(0.0, min(1.0, density))
    return (np.random.random((height, width)) < density).astype(np.uint8)


def neighbor_counts(grid: np.ndarray, wrap: bool) -> np.ndarray:
    """周囲 8 マスの生存数をまとめて計算する。"""
    if wrap:
        # 周囲をトーラス接続したままロールで集計
        return sum(
            np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )
    # ラップなし: 0 埋めパディングしてスライスで集計
    padded = np.pad(grid, 1, mode="constant")
    return (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] +                     padded[1:-1, 2:] +
        padded[2:, :-2] +  padded[2:, 1:-1] +   padded[2:, 2:]
    )


def step(grid: np.ndarray, wrap: bool) -> np.ndarray:
    """次世代へ進めた盤面を返す（numpy でベクトル化）。"""
    neighbors = neighbor_counts(grid, wrap)
    survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
    birth = (grid == 0) & (neighbors == 3)
    return (survive | birth).astype(np.uint8)


class LifeGameApp:
    def __init__(self, grid: np.ndarray, wrap: bool, interval: float, steps: int, cell_size: int):
        self.grid = grid
        self.wrap = wrap
        self.interval_ms = max(1, int(interval * 1000))
        self.steps_remaining = steps
        self.cell_size = max(2, cell_size)
        self.generation = 0

        height, width = grid.shape

        self.root = tk.Tk()
        self.root.title("Life Game")

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
        # 生存セルのみを抽出して描画するので負荷が低い
        live_cells = np.argwhere(self.grid == 1)
        for y, x in live_cells:
            x0, y0 = x * cs, y * cs
            x1, y1 = x0 + cs, y0 + cs
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="")
        self.root.title(f"Life Game - Generation {self.generation}")

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
    grid = create_grid(args.width, args.height, args.density)
    app = LifeGameApp(
        grid=grid,
        wrap=args.wrap,
        interval=args.interval,
        steps=args.steps,
        cell_size=args.cell_size,
    )
    app.run()


if __name__ == "__main__":
    run()
