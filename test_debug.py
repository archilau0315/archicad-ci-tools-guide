import re
t = open('site/quantities.html', encoding='utf-8').read()

h3_ids = {'s-4-1','s-4-2','s-4-3','s-4-4','s-4-5','s-4-6','s-4-7','s-8-1','s-9-1'}
def _to_id(n): return '#s-' + n.replace('.','-')

# 找原始裸文本那行
orig = None
for l in t.splitlines():
    if 'Sections 4.4, Calculated Measurements' in l and 'href' not in l:
        orig = l
        break

print('原始:', orig)
print()

line = orig

# 4a range
prev = line
line = re.sub(r'(\d+(?:\.\d+)*)\s+to\s+(\d+(?:\.\d+)+)',
              lambda m: f'{m.group(1)} to {m.group(2)}', line, flags=re.I)
print('4a range:', 'changed' if line != prev else '-')

# 4b plural and/or
prev = line
line = re.sub(r'(sections?)\s+(\d+(?:\.\d+)*)\s+(and|or|,|、)\s+(\d+(?:\.\d+)*)',
              lambda m: (f'<a href="{_to_id(m.group(2))}" class="xref">{m.group(1)} {m.group(2)}</a> {m.group(3)} '
                         f'<a href="{_to_id(m.group(4))}" class="xref">{m.group(4)}</a>'),
              line, flags=re.I)
print('4b plural:', 'changed' if line != prev else '-')
if line != prev: print('  ', line[:250])

# 4d section+decimal
prev = line
line = re.sub(r'\b(sections?)\s+(\d+(?:\.\d+)+)',
              lambda m: f'<a href="{_to_id(m.group(2))}" class="xref">{m.group(0)}</a>',
              line, flags=re.I)
print('4d sec+dec:', 'changed' if line != prev else '-')
if line != prev: print('  ', line[:300])

# 4e see+dec / 4f see+plain (skip)

# 4g section+plain  <-- 会命中 "sections 8"！
prev = line
line = re.sub(r'\b(sections?)\s+(\d+)\b',
              lambda m: f'<a href="#s-{m.group(2)}-1" class="xref">{m.group(0)}</a>',
              line, flags=re.I)
print('4g sec+plain:', 'changed' if line != prev else '-')
if line != prev: print('  ', line[:350])

# 4h zh tail - skip (英文)

# 4i bare dec  <-- 会命中 "4.7," 吗？
prev = line
line = re.sub(r'(?<![.\da-zA-Z#"\'>/])(\d+(?:\.\d+){1,3})(?=[\s，,。.;；:：)）\]》])',
              lambda m: f'<a href="{_to_id(m.group(1))}" class="xref">{m.group(1)}</a>',
              line)
print('4i bare dec:', 'changed' if line != prev else '-')
if line != prev: print('  ', line[:450])

print()
print('最终:', line)
