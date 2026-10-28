import json, csv, re, sys
sys.path.insert(0, '.')
from shots import SHOTS

PREFIX = ("Layered 2.5D paper-cutout diorama style, handcrafted cardboard and matte paper layers with bevelled cut edges "
          "and soft drop shadows between layers, subtle paper grain texture, muted historical palette of olive green, "
          "slate blue, khaki, charcoal grey and warm brown with selective deep red accents, soft warm key light from "
          "upper left, 16:9 cinematic composition.")
PEOPLE = (" All people are stylised angular paper-doll figures with faceted geometric face planes, thick dark outlines "
          "and simplified hands, in period-accurate clothing.")
DESC = {
 "Falkenhayn": "Erich von Falkenhayn: tall upright Prussian general, close-cropped grey-white hair, neat grey moustache, field-grey general's tunic with red collar patches and high collar.",
 "Pétain": "Philippe Pétain: stern sixty-year-old French general, balding with white hair and a full white moustache, pale blue eyes, horizon-blue general's tunic and kepi with gold oak-leaf embroidery.",
 "Nivelle": "Robert Nivelle: slim French general with a neat dark grey moustache, horizon-blue general's tunic and kepi with gold oak-leaf embroidery.",
 "Raynal": "Major Raynal: middle-aged French major with a dark moustache and tired eyes, horizon-blue uniform and kepi.",
 "French soldier": "French soldiers of 1916: horizon-blue greatcoats, horizon-blue Adrian helmets with a crest, puttees, Lebel rifles.",
 "German soldier": "German soldiers of 1916: field-grey tunics, steel Stahlhelm helmets, leather belts and pouches, Gewehr 98 rifles.",
 "Verdun map": "Set: a carved wooden and cardboard relief map on a dark wooden table, raised hills, the winding River Meuse in slate blue, top-down three-quarter angle, warm desk-lamp light.",
 "Falkenhayn's office": "Set: a dark-panelled German staff office, large war table with a map in the centre, tall window on the left, desk lamp on the right.",
 "Pétain's headquarters": "Set: a plain French headquarters room in a requisitioned town hall, wooden table with a map of Verdun, telephones, window on the right.",
 "Fort Douaumont": "Fort Douaumont: a huge low concrete fortress set into a grassy hilltop with armoured round gun turrets and a dry moat.",
 "Fort Vaux": "Fort Vaux: a smaller low concrete fort on a cratered hill with a battered concrete facade.",
 "Fort Vaux corridor": "Set: a narrow arched concrete corridor inside a fort, damp walls, oil lamps, sandbags.",
}
out, rows, script = [], [], []
lastch = None
for i, (ch, yr, typ, nar, vis, mot, r1, r2) in enumerate(SHOTS, 1):
    sid = f"S{i:03d}"
    if sid in {"S006","S009","S011","S083"}:
        r2 = ""; vis = vis + ", carved wooden and cardboard relief map on a dark wooden table, top-down three-quarter angle, warm desk-lamp light"
    m = re.search(r'reading \\?"([^"]+)\\?"', vis)
    txt = m.group(1) if m else ""
    desc = " ".join(DESC[r] for r in (r1, r2) if r)
    img = f"{PREFIX}{PEOPLE} {desc} {yr}: {vis}." + ("" if txt else " No text.")
    img = re.sub(r"\s+", " ", img)
    motion = (f"{mot[0].upper()}{mot[1:]}. Initially the paper diorama shows {vis}; then one small natural motion plays out "
              "with gentle parallax between the paper layers, drifting smoke or a small gesture; finally the camera settles "
              "on the main subject. The layout and paper-cutout style stay fixed.")
    out.append(dict(id=sid, chapter=ch, ref1=r1, ref2=r2, image=img, motion=motion, narration=nar))
    rows.append([sid, ch, yr, nar, typ, vis, r2, txt, mot, r1, r2, "", "", ""])
    if ch != lastch:
        script.append(f"\n## {ch}\n"); lastch = ch
    script.append(f"{i}. {nar}")

json.dump(out, open("prompts.json", "w"), indent=1, ensure_ascii=False)
with open("shots.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow("shot_id,chapter,year,narration_line,shot_type,subjects_and_counts,set_or_map,on_screen_text,camera_move,ref_photo_1,ref_photo_2,image_status,job_id,duration_s".split(","))
    w.writerows(rows)
words = sum(len(s[3].split()) for s in SHOTS)
open("script.md", "w").write(f"# Script: Verdun: The Battle Designed to Bleed France White\n\n16:9 · {len(SHOTS)} lines · {words} words\n" + "\n".join(script) + "\n")

# checks
types = [s[2] for s in SHOTS]
for i in range(len(types) - 2):
    if types[i] == types[i+1] == types[i+2]:
        print("3 in a row:", i+1, types[i])
for i, s in enumerate(SHOTS, 1):
    n = len(s[3].split()); c = len(s[3])
    if c > 120 or n < 8 or n > 19:
        print(f"S{i:03d} words={n} chars={c}: {s[3]}")
    if i > 1 and s[3].split()[0] == SHOTS[i-2][3].split()[0]:
        print("same opener", i, s[3].split()[0])
print(len(SHOTS), "shots,", words, "words")
from collections import Counter
print(Counter(r for s in SHOTS for r in (s[6], s[7]) if r))
