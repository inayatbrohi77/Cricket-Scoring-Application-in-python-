**Assigned And Developed**

Inayatullah Brohi Roll No TCS 27
Ahsan Umrani Roll No TCS 10

# 🏏 Cricket Scorer

A lightweight, terminal-based cricket scoring application written in Python. Score live matches directly from your command line — no internet, no GUI, no dependencies.

---

## ✨ Features

- **Live scoreboard** — runs, wickets, overs, CRR updated after every ball
- **Ball-by-ball input** — dot balls, runs (1–6), fours, sixes, wides, no balls, leg byes
- **Wicket tracking** — choose dismissal type (Bowled, Caught, LBW, Run Out, Stumped, etc.)
- **Batting scorecard** — runs, balls, 4s, 6s, strike rate per batter
- **Bowling figures** — overs, runs, wickets per bowler; supports multiple bowlers
- **Over log** — last 3 overs displayed ball-by-ball
- **Undo** — step back up to 50 actions
- **Extras tracking** — Wides, No Balls, Leg Byes tracked separately
- **Final innings summary** — full batting & bowling scorecard at end of innings
- **ANSI color output** — color-coded display for quick reading

---

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Works on **Linux**, **macOS**, and **Windows** (with ANSI-compatible terminal)

### Installation

```bash
git clone https://github.com/yourusername/cricket-scorer.git
cd cricket-scorer
```

No external dependencies — uses only Python standard library.

### Run

```bash
python cricket_scorer.py
```

---

## 🎮 Usage

On launch, you'll be prompted to enter match details:

```
Team 1 (batting first) [Team A]: Pakistan
Team 2 [Team B]: India
Overs per innings [20]: 20
Opener 1 name [Batter 1]: Babar
Opener 2 name [Batter 2]: Rizwan
Opening bowler name [Bowler 1]: Bumrah
```

### Controls

| Key | Action         |
|-----|----------------|
| `0` | Dot ball       |
| `1` | 1 run          |
| `2` | 2 runs         |
| `3` | 3 runs         |
| `4` | Four (boundary)|
| `5` | 5 runs         |
| `6` | Six            |
| `w` | Wicket         |
| `wd`| Wide           |
| `nb`| No Ball        |
| `lb`| Leg Bye        |
| `u` | Undo last ball |
| `b` | Change bowler  |
| `q` | Quit           |

At the end of an over, you'll be prompted to enter the next bowler's name (press Enter to keep the same bowler).

---

## 📸 Screenshot

```
┌────────────────────────────────────────────────────────────┐
│              PAKISTAN vs INDIA                             │
├────────────────────────────────────────────────────────────┤
│ 47/2   7.3 / 20.0 ov   CRR: 6.27                          │
│ Extras: 3  (Wd:2 NB:1 LB:0)                               │
├────────────────────────────────────────────────────────────┤
│   BATTER               R    B   4s   6s      SR            │
│ * Babar               34   28    4    1   121.4            │
│   Iftikhar            10   18    1    0    55.6            │
├────────────────────────────────────────────────────────────┤
│   Bowling: Bumrah   1.3 ov   9 runs   1W                   │
│   This over:  ·   1   W   4                                │
└────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
cricket-scorer/
└── cricket_scorer.py   # Single-file application
```

---

## 🤝 Contributing

Contributions are welcome! Some ideas for improvement:

- Second innings support with target/run-rate chase display
- Save/load match state to JSON
- Partnership tracking
- Export scorecard to text or PDF

Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

> Built with ❤️ for cricket fans who prefer the terminal.
