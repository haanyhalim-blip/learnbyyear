import re, json, sys
L = open(sys.argv[1], encoding='utf-8').read().split('\n')
B = ''
def section(a, b):
    """Statutory requirements between lines a..b → [(strand, [items])]"""
    out = []; strand = None; i = a; mode = None; cur = None; items = None
    while i < b:
        t = L[i].rstrip(); s = t.strip()
        if s.startswith('<<PAGE') or s in ('Mathematics', 'English') or re.fullmatch(r'\d+', s): i += 1; continue
        if s == 'Statutory requirements':
            # strand = nearest non-empty heading above
            j = i - 1
            while j > a and (not L[j].strip() or L[j].strip().startswith('<<PAGE') or L[j].strip() in ('Mathematics','English') or re.fullmatch(r'\d+', L[j].strip())): j -= 1
            h = L[j].strip()
            if not h.startswith(B) and len(h) < 70 and not h.endswith('.') and h[:1].isupper():
                if out and out[-1][0] == h and h.startswith('Writing – transcription'): h = 'Writing – handwriting'
                strand = h
            elif out and out[-1][1]:
                out[-1][1][-1][0] += ' ' + h
            if out and out[-1][0] == strand: items = out[-1][1]
            else: items = []; out.append((strand, items))
            mode = 'stat'; cur = None; i += 1; continue
        if s.startswith('Notes and guidance') or s.startswith('Year ') and 'programme of study' in s: mode = None; cur = None; i += 1; continue
        if mode == 'stat':
            if s.startswith('Pupils should be taught to') or not s: i += 1; continue
            if s.startswith(B):
                cur = [s[1:].strip()]; items.append(cur)
            elif cur is not None:
                cur[0] = (cur[0] + ' ' + s).strip()
            elif items is not None and not items:
                # heading-like line inside statutory block (e.g. "Spelling (see English Appendix 1)")
                pass
        i += 1
    # nest sub-items under a parent ending with ':'
    res = []
    for strand, its in out:
        flat = [fix(re.sub(r'\s+', ' ', x[0]).replace(' ,', ',')) for x in its]
        nested = []
        for x in flat:
            fw = x.split(' ')[0].lower()
            par = nested[-1] if nested else None
            if par and par['t'].endswith(':') and (fw.endswith('ing') or fw in ('a','an','the','their','angles','other') ) or (par and par.get('sub') and fw.endswith('ing') or (par and par['t'] == 'identify:' and fw in ('angles','other'))):
                nested[-1].setdefault('sub', []).append(x)
            else:
                nested.append({'t': x})
        res.append({'strand': strand, 'items': nested})
    return res
FIX = [("non- unit","non-unit"),("non- prime","non-prime"),("5 + 7 1 = 7 6","5/7 + 1/7 = 6/7"),("0.71 = 100 71","0.71 = 71/100"),
 ("2 1, 4 1, 1, 5 2, 5 4","1/2, 1/4, 1/5, 2/5, 4/5"),("squared (2) and cubed (3)","squared (²) and cubed (³)"),("2 1 a turn","½ a turn"),
 ("360o","360°"),("180o","180°"),("90o","90°"),("degrees (o)","degrees (°)"),("(cm2)","(cm²)"),("(m2)","(m²)"),("1 cm3","1 cm³"),("(mm2)","(mm²)"),("(km2)","(km²)")]
def fix(x):
    for a, b in FIX: x = x.replace(a, b)
    return x
def find(text, start=0):
    for k in range(start, len(L)):
        if L[k].strip() == text: return k
    raise Exception(text)
secs = {}
m3 = find('Year 3 programme of study', 5000); m4 = find('Year 4 programme of study', m3)
m5 = find('Year 5 programme of study', 5600); m6 = find('Year 6 programme of study', m5)
e34 = find('Years 3 and 4 programme of study', 1000); e56 = find('Years 5 and 6 programme of study', e34)
eend = find('English Appendix 1: Spelling', e56)
secs['maths-y3'] = section(m3, m4); secs['maths-y5'] = section(m5, m6)
secs['english-y34'] = section(e34, e56); secs['english-y56'] = section(e56, eend)
json.dump(secs, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for k, v in secs.items():
    print('=====', k)
    for s in v:
        print('##', s['strand'])
        for it in s['items']:
            print(' -', it['t'][:150]); [print('     ·', x[:120]) for x in it.get('sub', [])]
