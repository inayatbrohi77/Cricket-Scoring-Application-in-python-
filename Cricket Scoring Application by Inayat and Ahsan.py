"""
Cricket Scorer - Terminal-based Cricket Scoring Application
Run: python cricket_scorer.py
"""

import os
import sys
import copy

# â”€â”€ ANSI color helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    RED     = "\033[91m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BG_GREEN  = "\033[42m"
    BG_BLUE   = "\033[44m"
    BG_RED    = "\033[41m"
    BG_YELLOW = "\033[43m"
    BG_GRAY   = "\033[100m"

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def col(text, *codes):
    return "".join(codes) + str(text) + C.RESET

def box(text, width=60):
    pad = max(0, width - len(text) - 2)
    left = pad // 2
    right = pad - left
    return f"â”‚ {' '*left}{text}{' '*right} â”‚"

def hline(width=60, char="â”€"):
    return "â”œ" + char * (width - 2) + "â”¤"

def tline(width=60):
    return "â”Œ" + "â”€" * (width - 2) + "â”"

def bline(width=60):
    return "â””" + "â”€" * (width - 2) + "â”˜"

# â”€â”€ Data structures â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def new_batter(name):
    return {"name": name, "runs": 0, "balls": 0, "fours": 0, "sixes": 0,
            "out": False, "dismissal": ""}

def new_bowler(name):
    return {"name": name, "runs": 0, "wickets": 0, "balls": 0,
            "overs_done": 0, "this_over": []}

def new_state(team1, team2, overs, batters, bowler_name):
    return {
        "team1": team1, "team2": team2,
        "overs": overs,
        "runs": 0, "wickets": 0, "balls": 0,
        "extras": {"wide": 0, "nb": 0, "lb": 0},
        "batters": batters,
        "striker": 0,
        "bowler": new_bowler(bowler_name),
        "all_bowlers": [],
        "dismissed": [],
        "over_log": [],
        "history": []
    }

# â”€â”€ Display helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def over_str(balls):
    return f"{balls // 6}.{balls % 6}"

def crr(state):
    b = state["balls"]
    if b == 0:
        return "0.00"
    return f"{(state['runs'] / b * 6):.2f}"

def ball_display(b):
    if b == "W":   return col(f" W ", C.BOLD, C.BG_RED, C.WHITE)
    if b == "Wd":  return col("Wd ", C.BOLD, C.BG_YELLOW, C.WHITE)
    if b == "NB":  return col("NB ", C.BOLD, C.BG_YELLOW, C.WHITE)
    if b == "lb":  return col("lb ", C.DIM)
    if b == "4":   return col(" 4 ", C.BOLD, C.BG_GREEN, C.WHITE)
    if b == "6":   return col(" 6 ", C.BOLD, C.BG_BLUE, C.WHITE)
    if b == "0":   return col(" Â· ", C.DIM)
    return col(f" {b} ", C.WHITE)

def sr(runs, balls):
    if balls == 0: return "0.00"
    return f"{runs / balls * 100:.1f}"

# â”€â”€ Render scoreboard â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def render_scoreboard(state):
    W = 62
    s = state
    team = col(s["team1"].upper(), C.BOLD, C.CYAN)
    score = col(f"{s['runs']}/{s['wickets']}", C.BOLD, C.WHITE)
    overs_disp = f"{over_str(s['balls'])} / {s['overs']}.0 ov"
    run_rate = crr(s)
    ext = s["extras"]
    total_extras = ext["wide"] + ext["nb"] + ext["lb"]

    print()
    print(col(tline(W), C.DIM))
    print(col(box(f"  {s['team1'].upper()} vs {s['team2'].upper()}  ", W), C.DIM))
    print(col(hline(W), C.DIM))

    # Score line
    score_line = f"{s['runs']}/{s['wickets']}   {overs_disp}   CRR: {run_rate}"
    print(col("â”‚ ", C.DIM) + col(f"{score_line:<{W-4}}", C.BOLD, C.WHITE) + col(" â”‚", C.DIM))

    extras_line = f"Extras: {total_extras}  (Wd:{ext['wide']} NB:{ext['nb']} LB:{ext['lb']})"
    print(col("â”‚ ", C.DIM) + col(f"{extras_line:<{W-4}}", C.DIM) + col(" â”‚", C.DIM))

    print(col(hline(W), C.DIM))

    # Batters
    header = f"  {'BATTER':<18} {'R':>4} {'B':>4} {'4s':>4} {'6s':>4}  {'SR':>6}"
    print(col("â”‚ ", C.DIM) + col(f"{header:<{W-4}}", C.DIM, C.BOLD) + col(" â”‚", C.DIM))
    for i, bt in enumerate(s["batters"]):
        if bt["out"]:
            continue
        strike_mark = col("*", C.GREEN, C.BOLD) if i == s["striker"] else " "
        name_str = f"{strike_mark} {bt['name']:<17}"
        bat_line = f"{name_str} {bt['runs']:>4} {bt['balls']:>4} {bt['fours']:>4} {bt['sixes']:>4}  {sr(bt['runs'], bt['balls']):>6}"
        color = C.GREEN if i == s["striker"] else C.WHITE
        print(col("â”‚ ", C.DIM) + col(f"{bat_line:<{W-4}}", color) + col(" â”‚", C.DIM))

    print(col(hline(W), C.DIM))

    # Bowler
    bwl = s["bowler"]
    bwl_line = f"  Bowling: {bwl['name']}   {over_str(bwl['balls'])} ov   {bwl['runs']} runs   {bwl['wickets']}W"
    print(col("â”‚ ", C.DIM) + col(f"{bwl_line:<{W-4}}", C.YELLOW) + col(" â”‚", C.DIM))

    # This over
    over_balls = "  This over: " + " ".join(ball_display(b) for b in bwl["this_over"]) if bwl["this_over"] else "  This over: â€”"
    # strip ANSI for width calc
    raw_over = "  This over: " + " ".join(bwl["this_over"])
    padding = max(0, W - 4 - len(raw_over))
    print(col("â”‚ ", C.DIM) + over_balls + " " * padding + col(" â”‚", C.DIM))

    print(col(bline(W), C.DIM))

# â”€â”€ Render dismissed scorecard â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def render_scorecard(state):
    if not state["dismissed"]:
        return
    W = 62
    print()
    print(col("  SCORECARD", C.BOLD, C.DIM))
    print(col("  " + "â”€" * 58, C.DIM))
    for d in state["dismissed"]:
        line = f"  {d['name']:<18} {d['runs']:>3} ({d['balls']}b)  {d['dismissal']}"
        print(col(line, C.DIM))
    print()

# â”€â”€ Render over log â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def render_over_log(state):
    if not state["over_log"]:
        return
    recent = state["over_log"][-3:]
    print(col("  RECENT OVERS", C.BOLD, C.DIM))
    for o in recent:
        balls_str = "  ".join(o["balls"])
        print(col(f"  Over {o['over']+1}: {balls_str}  â€” {o['bowler']}", C.DIM))
    print()

# â”€â”€ Input helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def prompt(text, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(col(f"  {text}{suffix}: ", C.CYAN)).strip()
    return val if val else default

def setup_match():
    clr()
    W = 62
    print()
    print(col(tline(W), C.DIM))
    print(col(box("  CRICKET SCORER", W), C.BOLD, C.WHITE))
    print(col(bline(W), C.DIM))
    print()

    team1   = prompt("Team 1 (batting first)", "Team A")
    team2   = prompt("Team 2", "Team B")
    overs   = int(prompt("Overs per innings", "20") or 20)
    b1      = prompt("Opener 1 name", "Batter 1")
    b2      = prompt("Opener 2 name", "Batter 2")
    bowler  = prompt("Opening bowler name", "Bowler 1")

    batters = [new_batter(b1), new_batter(b2)]
    return new_state(team1, team2, overs, batters, bowler)

# â”€â”€ State mutation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def save_snapshot(state):
    snap = copy.deepcopy(state)
    snap.pop("history", None)
    state["history"].append(snap)
    if len(state["history"]) > 50:
        state["history"].pop(0)

def undo(state):
    if not state["history"]:
        print(col("  Nothing to undo.", C.RED))
        return state
    prev = state["history"].pop()
    prev["history"] = state["history"]
    print(col("  â†© Undone.", C.YELLOW))
    return prev

def check_over_end(state):
    bwl = state["bowler"]
    if bwl["balls"] == 6:
        state["over_log"].append({
            "over": state["balls"] // 6 - 1,
            "balls": list(bwl["this_over"]),
            "bowler": bwl["name"]
        })
        state["all_bowlers"].append(copy.copy(bwl))
        # rotate strike
        state["striker"] = 1 - state["striker"]
        # reset bowler for next over
        name = bwl["name"]
        new_name = prompt(f"  New bowler (Enter to keep {name})", name)
        state["bowler"] = new_bowler(new_name)

def add_runs(state, runs, extra=None):
    save_snapshot(state)
    state["runs"] += runs
    bwl = state["bowler"]
    bt = state["batters"][state["striker"]]

    if extra is None:
        bt["runs"] += runs
        bt["balls"] += 1
        if runs == 4: bt["fours"] += 1
        if runs == 6: bt["sixes"] += 1
        bwl["runs"] += runs
        bwl["balls"] += 1
        state["balls"] += 1
        bwl["this_over"].append(str(runs) if runs > 0 else "0")
        if runs % 2 != 0:
            state["striker"] = 1 - state["striker"]
    elif extra in ("wide", "nb"):
        state["extras"][extra] += 1
        bwl["runs"] += 1
        bwl["this_over"].append("Wd" if extra == "wide" else "NB")
    elif extra == "lb":
        state["extras"]["lb"] += 1
        bwl["balls"] += 1
        state["balls"] += 1
        bwl["this_over"].append("lb")

    check_over_end(state)

def add_wicket(state):
    save_snapshot(state)
    dismissals = ["Bowled", "Caught", "LBW", "Run Out", "Stumped", "Hit Wicket", "Obstructing"]
    print()
    for i, d in enumerate(dismissals, 1):
        print(col(f"    {i}. {d}", C.WHITE))
    choice = input(col("  Dismissal type (1-7): ", C.CYAN)).strip()
    try:
        dismissal = dismissals[int(choice) - 1]
    except Exception:
        dismissal = "Bowled"

    bwl = state["bowler"]
    bt = state["batters"][state["striker"]]
    bt["out"] = True
    bt["dismissal"] = dismissal
    state["dismissed"].append(copy.copy(bt))

    state["wickets"] += 1
    bwl["wickets"] += 1
    bwl["balls"] += 1
    state["balls"] += 1
    bwl["this_over"].append("W")

    check_over_end(state)

    if state["wickets"] >= 10:
        return  # All out

    new_name = prompt("  New batter name", f"Batter {state['wickets'] + 2}")
    state["batters"][state["striker"]] = new_batter(new_name)

def change_bowler(state):
    name = prompt("  New bowler name", state["bowler"]["name"])
    state["bowler"]["name"] = name

# â”€â”€ Main game loop â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

MENU = """
  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
  â”‚  0  Dot ball     1  1 run    2  2 runs  â”‚
  â”‚  3  3 runs       4  FOUR     5  5 runs  â”‚
  â”‚  6  SIX          W  Wicket             â”‚
  â”‚  wd Wide         nb No Ball  lb Leg Bye â”‚
  â”‚  u  Undo         b  Change bowler       â”‚
  â”‚  q  Quit                                â”‚
  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
"""

def is_over(state):
    complete_overs = state["balls"] // 6
    if complete_overs >= state["overs"]:
        return True
    if state["wickets"] >= 10:
        return True
    return False

def final_summary(state):
    clr()
    W = 62
    print()
    print(col(tline(W), C.DIM))
    print(col(box("  INNINGS COMPLETE", W), C.BOLD, C.GREEN))
    print(col(hline(W), C.DIM))
    summary = f"  {state['team1']}: {state['runs']}/{state['wickets']}  ({over_str(state['balls'])} overs)  CRR: {crr(state)}"
    print(col("â”‚ ", C.DIM) + col(f"{summary:<{W-4}}", C.BOLD, C.WHITE) + col(" â”‚", C.DIM))
    print(col(bline(W), C.DIM))
    print()

    if state["dismissed"]:
        print(col("  BATTING SCORECARD", C.BOLD))
        print(col("  " + "â”€" * 55, C.DIM))
        header = f"  {'BATTER':<18} {'R':>4} {'B':>4} {'4s':>3} {'6s':>3}  {'SR':>6}  DISMISSAL"
        print(col(header, C.DIM))
        for d in state["dismissed"]:
            line = f"  {d['name']:<18} {d['runs']:>4} {d['balls']:>4} {d['fours']:>3} {d['sixes']:>3}  {sr(d['runs'], d['balls']):>6}  {d['dismissal']}"
            print(line)
        for bt in state["batters"]:
            if not bt["out"]:
                line = f"  {bt['name']:<18} {bt['runs']:>4} {bt['balls']:>4} {bt['fours']:>3} {bt['sixes']:>3}  {sr(bt['runs'], bt['balls']):>6}  not out"
                print(col(line, C.GREEN))
        print()

    if state["all_bowlers"] or state["bowler"]["balls"] > 0:
        print(col("  BOWLING FIGURES", C.BOLD))
        print(col("  " + "â”€" * 40, C.DIM))
        header = f"  {'BOWLER':<18} {'O':>5} {'R':>5} {'W':>4}"
        print(col(header, C.DIM))
        for bwl in state["all_bowlers"]:
            print(f"  {bwl['name']:<18} {over_str(bwl['balls']):>5} {bwl['runs']:>5} {bwl['wickets']:>4}")
        bwl = state["bowler"]
        if bwl["balls"] > 0:
            print(f"  {bwl['name']:<18} {over_str(bwl['balls']):>5} {bwl['runs']:>5} {bwl['wickets']:>4}")
    print()

def main():
    state = setup_match()

    while True:
        clr()
        render_scoreboard(state)
        render_scorecard(state)
        render_over_log(state)

        if is_over(state):
            break

        print(col(MENU, C.DIM))
        cmd = input(col("  Enter action: ", C.CYAN)).strip().lower()

        if cmd == "q":
            print(col("\n  Goodbye!\n", C.DIM))
            sys.exit(0)
        elif cmd == "0":  add_runs(state, 0)
        elif cmd == "1":  add_runs(state, 1)
        elif cmd == "2":  add_runs(state, 2)
        elif cmd == "3":  add_runs(state, 3)
        elif cmd == "4":  add_runs(state, 4)
        elif cmd == "5":  add_runs(state, 5)
        elif cmd == "6":  add_runs(state, 6)
        elif cmd == "w":  add_wicket(state)
        elif cmd == "wd": add_runs(state, 1, extra="wide")
        elif cmd == "nb": add_runs(state, 1, extra="nb")
        elif cmd == "lb": add_runs(state, 1, extra="lb")
        elif cmd == "u":  state = undo(state)
        elif cmd == "b":  change_bowler(state)
        else:
            print(col("  Unknown command. Try again.", C.RED))
            input(col("  Press Enter to continue...", C.DIM))

    final_summary(state)
    input(col("  Press Enter to exit.", C.DIM))

if __name__ == "__main__":
    main()