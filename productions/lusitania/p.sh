#!/bin/sh
python3 -c "
import json,sys;P={p['id']:p for p in json.load(open('prompts.json'))}
for s in sys.argv[1:]:
  p=P[s]; print('==',s,p['ref1'],'|',p['ref2']); print('IMG:',p['image']); print('MOT:',p['motion']); print('NAR:',p['narration'])
" "$@"
