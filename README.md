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
