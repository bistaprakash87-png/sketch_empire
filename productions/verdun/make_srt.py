import json,sys,io,contextlib
sys.path.insert(0,'.')
with contextlib.redirect_stdout(io.StringIO()):
    from shots import SHOTS
T=json.load(open('timeline.json')); SP=json.load(open('speech.json'))
nar={f"S{i:03d}":s[3] for i,s in enumerate(SHOTS,1)}
nar['S001']='In February 1916 more than twelve hundred German guns opened fire on a quiet French fortress town.'
def ts(ms):
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
def split(words):
    # break into chunks of <=7 words, max 42 chars, prefer punctuation
    out=[];cur=[]
    for w in words:
        if cur and (len(cur)>=7 or len(' '.join(cur+[w]))>42):
            out.append(cur);cur=[]
        cur.append(w)
        if w[-1] in ',:;' and len(cur)>=3: out.append(cur);cur=[]
    if cur:
        if out and len(cur)<=2 and len(' '.join(out[-1]+cur))<=42: out[-1]+=cur
        else: out.append(cur)
    return out
lines=[];k=1
for sid,st,du in T:
    on,off=SP[sid]; a=st+int(on*1000); b=st+min(int(off*1000)+150,du-40)
    parts=split(nar[sid].split()); tot=sum(len(' '.join(p)) for p in parts); t=a
    for p in parts:
        d=int((b-a)*len(' '.join(p))/tot)
        lines.append(f"{k}\n{ts(t)} --> {ts(t+d)}\n{' '.join(p)}\n"); k+=1; t+=d
open('verdun-subtitles-en.srt','w').write('\n'.join(lines))
print(k-1)
