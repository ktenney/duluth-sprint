"""Find undocumented hooks in Leo"""
import os
import re

loaddir = g.computeLoadDir()
loaddir = os.path.dirname(loaddir)

pattern = re.compile(r"""\.doHook\s*\(\s*['"]([^'"]+)['"]""")

hooks = {}
for path, dirs, files in os.walk(loaddir):
    for filename in files:

        if not filename.lower().endswith('.py'):
            continue
        filepath = os.path.join(path, filename)
        for n, line in enumerate(open(filepath)):
            matches = pattern.search(line)
            if matches:
                for group in matches.groups():
                    hooks[group] = filepath, n+1


doced = set()
docs = open(os.path.join(loaddir, 'doc', 'scripting.txt'))
for line in docs:
    if line.startswith('Event name (tag argument)'):
        break
for line in docs:
    line = line.strip()
    if not line:
        break
    doced.add(line.split()[0].strip('"\'\\'))
for hook in sorted(hooks):
    if hook not in doced:
        print hook, hooks[hook]

    
