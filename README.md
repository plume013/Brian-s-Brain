# Brian's Brain

Brian's Brain は、1990 年代半ばに Brian Silverman によって考案されたセル・オートマトンです。
「ライフゲーム」に似ていますが、セルが 3 つの状態を持つことで、より複雑で有機的な動き（脳のニューロンの発火のような動き）を見せます。

## ルール

各セルは以下の 3 つの状態のいずれかを取ります：

1.  **Ready (Off / 0)**: 待機状態（黒）
2.  **Firing (On / 1)**: 発火状態（白）
3.  **Refractory (Dying / 2)**: 不応期（赤）

遷移ルールは以下の通りです：

- **Ready -> Firing**: 周囲 8 マスのうち、ちょうど **2 つ** が Firing 状態であれば、次のステップで Firing になります。
- **Firing -> Refractory**: Firing 状態のセルは、次のステップで必ず Refractory になります。
- **Refractory -> Ready**: Refractory 状態のセルは、次のステップで必ず Ready になります。

この「不応期」の存在により、信号が一方向に伝播したり、複雑な振動パターンが生まれたりします。

## 必要要件

- Python 3.12 以上
- [uv](https://github.com/astral-sh/uv) (パッケージ管理ツール)

## インストール

```bash
git clone https://github.com/plume013/Brian-s-Brain.git
cd Brian-s-Brain
uv sync
```

## 使い方

基本的な実行方法：

```bash
uv run main.py
```

### オプション

様々なオプションを指定してシミュレーションをカスタマイズできます。

| 引数                   | デフォルト値 | 説明                                                               |
| :--------------------- | :----------- | :----------------------------------------------------------------- |
| `--width`              | 100          | 盤面の横幅（セル数）                                               |
| `--height`             | 100          | 盤面の高さ（セル数）                                               |
| `--cell-size`          | 12           | 1 セルのピクセルサイズ                                             |
| `--interval`           | 0.1          | 更新間隔（秒）                                                     |
| `--steps`              | 200          | 実行ステップ数（-1 で無限）                                        |
| `--wrap`               | False        | 盤面の端をループさせる（トーラス状）                               |
| `--pattern`            | (Random)     | 初期パターンを指定 (`2x2_block`, `oscillator_p3`, `cross`, `line`) |
| `--fire-density`       | 0.25         | ランダム初期化時の発火セルの割合                                   |
| `--refractory-density` | 0.00         | ランダム初期化時の不応期セルの割合                                 |

### 実行例

**有名な「2x2 ブロック」（ダイヤモンド状に広がる）を実行:**

```bash
uv run main.py --pattern 2x2_block
```

**端をループさせて無限に実行:**

```bash
uv run main.py --wrap --steps -1
```

**大きな盤面で高速に実行:**

```bash
uv run main.py --width 200 --height 200 --cell-size 4 --interval 0.01
```

## パターン

`--pattern` で指定できるプリセットパターンです。

- **2x2_block**: 2x2 のブロック。Brian's Brain で最も有名なパターンで、4 方向にダイヤモンド状に信号を放出し続けます。
- **oscillator_p3**: 周期 3 で振動するパターン。
- **cross**: 十字型の配置。
- **line**: 横一列の配置。

## 開発

新しいパターンを追加したい場合は、`patterns.py` に関数を追加し、`create_pattern` 関数内の辞書に登録してください。

---

# Brian's Brain (English)

Brian's Brain is a cellular automaton devised by Brian Silverman in the mid-1990s.
It is similar to Conway's Game of Life, but because cells have three states, it exhibits more complex and organic movements (resembling the firing of neurons in the brain).

## Rules

Each cell takes one of the following three states:

1.  **Ready (Off / 0)**: Waiting state (Black)
2.  **Firing (On / 1)**: Firing state (White)
3.  **Refractory (Dying / 2)**: Refractory period (Red)

The transition rules are as follows:

- **Ready -> Firing**: If exactly **2** of the 8 surrounding neighbors are in the Firing state, the cell becomes Firing in the next step.
- **Firing -> Refractory**: A cell in the Firing state always becomes Refractory in the next step.
- **Refractory -> Ready**: A cell in the Refractory state always becomes Ready in the next step.

The existence of this "refractory period" allows signals to propagate in one direction and creates complex oscillating patterns.

## Requirements

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (Package manager)

## Installation

```bash
git clone https://github.com/plume013/Brian-s-Brain.git
cd Brian-s-Brain
uv sync
```

## Usage

Basic execution:

```bash
uv run main.py
```

### Options

You can customize the simulation by specifying various options.

| Argument               | Default  | Description                                                             |
| :--------------------- | :------- | :---------------------------------------------------------------------- |
| `--width`              | 100      | Width of the grid (number of cells)                                     |
| `--height`             | 100      | Height of the grid (number of cells)                                    |
| `--cell-size`          | 12       | Pixel size of one cell                                                  |
| `--interval`           | 0.1      | Update interval (seconds)                                               |
| `--steps`              | 200      | Number of execution steps (-1 for infinite)                             |
| `--wrap`               | False    | Wrap the edges of the grid (Toroidal)                                   |
| `--pattern`            | (Random) | Specify initial pattern (`2x2_block`, `oscillator_p3`, `cross`, `line`) |
| `--fire-density`       | 0.25     | Probability of firing cells during random initialization                |
| `--refractory-density` | 0.00     | Probability of refractory cells during random initialization            |

### Examples

**Run the famous "2x2 block" (expands like a diamond):**

```bash
uv run main.py --pattern 2x2_block
```

**Run infinitely with wrapped edges:**

```bash
uv run main.py --wrap --steps -1
```

**Run fast on a large grid:**

```bash
uv run main.py --width 200 --height 200 --cell-size 4 --interval 0.01
```

## Patterns

Preset patterns available via `--pattern`.

- **2x2_block**: A 2x2 block. The most famous pattern in Brian's Brain, continuously emitting signals in a diamond shape in 4 directions.
- **oscillator_p3**: A pattern that oscillates with a period of 3.
- **cross**: A cross-shaped configuration.
- **line**: A horizontal line configuration.

## Development

If you want to add a new pattern, add a function to `patterns.py` and register it in the dictionary within the `create_pattern` function.
