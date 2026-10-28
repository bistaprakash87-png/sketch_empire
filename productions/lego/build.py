"""Build prompts.json, shots.csv and script.md for the LEGO production (image-and-audio workflow).
Run from this folder: python3 build.py
"""
import csv, json, re, sys
from collections import Counter
sys.path.insert(0, '.')
from shots import SHOTS

PREFIX = ("Layered 2.5D paper-cutout diorama, handcrafted cardboard and matte paper layers with bevelled cut edges and "
          "soft drop shadows between layers, subtle paper grain texture, muted historical palette of olive green, slate blue, "
          "khaki, charcoal grey and warm brown with selective deep red accents, soft warm key light from upper left, "
          "shallow depth of field, clear foreground, middle ground and background layers, 16:9 cinematic composition.")
PEOPLE = (" All people are stylised angular paper-doll figures with faceted geometric face planes, thick dark outlines "
          "and simplified hands, in period-accurate clothing.")
FRAMING = (" Compose with open space around one clear focal point so a slow camera zoom will not crop it. "
           "No logos, brand marks or watermarks.")

DESC = {
 "Ole Kirk": "Ole Kirk Christiansen: stocky Danish carpenter in his forties, receding short brown hair, round weathered face, rolled-up shirtsleeves, dark waistcoat and a long carpenter's apron with sawdust on the sleeves.",
 "Godtfred": "Godtfred Kirk Christiansen: slim Danish man in his thirties to forties, neat fair hair parted to one side, white shirt with rolled sleeves and a dark tie, 1950s trousers.",
 "Knudstorp": "Jorgen Vig Knudstorp: slim Danish businessman in his mid-thirties, short dark hair, dark suit with an open-collared white shirt, 2004.",
 "Billund workshop": "Set: a wooden Danish carpentry workshop, a central workbench with tools, a tall window on the left, shelves of finished wooden toys on the back wall, wood shavings on the floor, warm lamplight.",
 "Boardroom": "Set: a plain modern Danish meeting room of 2004, a long pale-wood table with stacks of reports, a large window on the right looking over flat green farmland.",
}

# Slow Ken Burns moves applied to the still in the editor, rotated per shot type so no move repeats three times in a row.
MOVES = {
 "FIGURE":    ["slow push-in on the face", "slow push-in on the hands", "slow pull-out from the figure"],
 "ARTIFACT":  ["slow push-in on the object", "slow diagonal drift across the object", "slow push-in on the document"],
 "MAP":       ["slow pan along the route", "slow tilt down onto the map", "slow push-in on the key place"],
 "SCENE":     ["slow pan left across the scene", "slow pan right across the scene", "slow push-in on the main action"],
 "LANDSCAPE": ["slow pull-out", "slow pan right", "slow pan left"],
}

def clean(r):
    return "" if r in (None, "") else r

rows, out, script, counters = [], [], [], Counter()
lastch, lastmove = None, [None, None]
for i, (ch, yr, typ, nar, vis, r1, r2) in enumerate(SHOTS, 1):
    sid = f"S{i:03d}"
    r1, r2 = clean(r1), clean(r2)
    m = re.search(r'(?:reading|reads|word|words|year) ([A-Z0-9][A-Z0-9 ,.\-]{1,24})', vis)
    txt = m.group(1).strip() if m and m.group(1).isupper() else ""
    desc = " ".join(DESC[r] for r in (r1, r2) if r)
    PEOPLE_WORDS = ("person", "paper-doll", "worker", "child", "man ", "men ", "figure", "executive", "villager", "neighbour",
                    "firefighter", "investor", "hobbyist", "employee", "visitor", "crowd", "queue", "couple", "boys", "colleague",
                    "banker", "lender", "clerk", "shopkeeper", "student", "carpenter", "father", "designer", "shopper", "warrior",
                    "pirate", "hands", "hand ")
    no_people = " No people." if not (r1 or any(w in vis for w in PEOPLE_WORDS)) and "no people" not in vis else ""
    mid = re.sub(r"\s+", " ", f"{desc} {yr}: {vis}.{no_people}").strip()
    img = f"{PREFIX}{PEOPLE} {desc} {yr}: {vis}.{no_people}{FRAMING}"
    img = re.sub(r"\s+", " ", img).strip()
    k = counters[typ]; counters[typ] += 1
    move = MOVES[typ][k % 3]
    if move == lastmove[0] == lastmove[1]:
        move = MOVES[typ][(k + 1) % 3]
    lastmove = [lastmove[1], move]
    out.append(dict(id=sid, chapter=ch, year=yr, type=typ, ref1=r1, ref2=r2, mid=mid, image=img, camera=move, narration=nar))
    rows.append([sid, ch, yr, nar, typ, vis, r2 or r1, txt, move, r1, r2, "", "", "", ""])
    if ch != lastch:
        script.append(f"\n## {ch}\n"); lastch = ch
    script.append(f"{i}. {nar}")

json.dump(out, open("prompts.json", "w"), indent=1, ensure_ascii=False)
with open("shots.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow("shot_id,chapter,year,narration_line,shot_type,subjects_and_counts,set_or_map,on_screen_text,camera_move,ref_photo_1,ref_photo_2,image_status,image_id,audio_id,duration_s".split(","))
    w.writerows(rows)

words = sum(len(s[3].split()) for s in SHOTS)
est = words / 155 * 60 + 0.15 * len(SHOTS)
mins = f"{int(est // 60)}:{int(est % 60):02d}"
open("script.md", "w").write(
    f"# Script: LEGO — from a Danish carpenter's workshop to the world's favourite toy\n\n16:9 · {len(SHOTS)} lines · {words} words · est. {mins}\n"
    + "\n".join(script) + "\n")

# ---- checks ----
types = [s[2] for s in SHOTS]
for i in range(len(types) - 2):
    if types[i] == types[i+1] == types[i+2]:
        print("3 in a row:", i + 1, types[i])
for i, s in enumerate(SHOTS, 1):
    n = len(s[3].split())
    if n < 10 or n > 19:
        print(f"S{i:03d} words={n}: {s[3]}")
    if i > 1 and s[3].split()[0] == SHOTS[i-2][3].split()[0]:
        print("same opener", i, s[3].split()[0])
print(len(SHOTS), "shots,", words, "words, est", mins)
print(Counter(t for t in types))
print(Counter(r for s in SHOTS for r in (clean(s[5]), clean(s[6])) if r))
