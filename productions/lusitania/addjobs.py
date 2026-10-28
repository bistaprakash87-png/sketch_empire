import json,sys
j=json.load(open('jobs.json'))
for a in sys.argv[1:]:
    s,v=a.split('=',1); j[s]={'video':v}
json.dump(j,open('jobs.json','w'),indent=0); print(len(j),'jobs')
