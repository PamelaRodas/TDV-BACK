import re, json
p=r'c:\\Users\\CESDE\\Desktop\\TDV FRONT\\TVD\\src\\data\\diaryEntries.js'
with open(p, encoding='utf-8') as f:
    txt = f.read()
start = txt.find('[')
end = txt.rfind(']')
arr = txt[start:end+1]
fixed = re.sub(r'([\{\,\s])(\w+)\s*:', r'\1"\2":', arr)
print('--- ORIGINAL START ---')
print(arr[:600])
print('--- FIXED START ---')
print(fixed[:800])
out = r'c:\\Users\\CESDE\\Desktop\\TDV BACK\\TDV-BACK\\scripts\\fixed.json'
with open(out,'w',encoding='utf-8') as f:
    f.write(fixed)
try:
    json.loads(fixed)
    print('\nPARSED OK')
except json.JSONDecodeError as e:
    print('\nPARSE ERROR:', e)
    print('lineno, colno, pos ->', e.lineno, e.colno, e.pos)
    pos = e.pos
    context = fixed[max(0,pos-120):pos+120]
    print('\nContext around error:\n', context)
