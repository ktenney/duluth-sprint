"""Find undocumented hooks in Leo"""
import os
import re

loaddir = g.computeLeoDir()

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
    
print("\nUNDOCUMENTED HOOKS")
for hook in sorted(hooks):
    if hook not in doced:
        path, line = hooks[hook]
        path = path.replace(loaddir, '').strip('/')
        print("%s %s:%s" % (hook, path, line))

print("\nDOCUMENTED HOOKS NOT FOUND IN SOURCE")
for hook in sorted(doced):
    if hook not in hooks:
        print(hook)

