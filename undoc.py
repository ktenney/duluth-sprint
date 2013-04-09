"""Find undocumented hooks in Leo"""
import os
import re
from collections import defaultdict

leodir = g.computeLeoDir()

hook_pattern = re.compile(r"""\.doHook\s*\(\s*['"]([^'"]+)['"]""")
call_pattern = re.compile(r"""\.registerHandler\s*\(\s*['"]([^'"]+)['"]""")

hooks = {}
calls = defaultdict(lambda: 0)

# search all .py files for calls to doHook() and registerHandler()
for path, dirs, files in os.walk(leodir):
    for filename in files:

        if not filename.lower().endswith('.py'):
            continue
        filepath = os.path.join(path, filename)
        for n, line in enumerate(open(filepath)):
            matches = hook_pattern.search(line)
            if matches:
                for group in matches.groups():
                    hooks[group] = filepath, n+1
            matches = call_pattern.search(line)
            if matches:
                for group in matches.groups():
                    calls[group] += 1

# now 'read' scripting.txt to see what's in the table,
# somewhat fragile if layout of scripting.txt changes
doced = set()
docs = open(os.path.join(leodir, 'doc', 'scripting.txt'))
for line in docs:  # scan for table column header
    if line.startswith('Event name (tag argument)'):
        break
for line in docs:
    line = line.strip()
    if not line:
        break
    if line.startswith('=='):
        continue
    doced.add(line.split()[0].strip('"\'\\'))
    
print("\nHOOK USAGE")
for hook in sorted(calls):
    print("%3d %s%s" % (
        calls[hook],
        hook,
        " *** NO doHook() ***" if hook not in hooks else ""
    ))
for hook in sorted(hooks):
    if hook not in calls:
        print("%3d %s" % (0, hook))

print("\nUNDOCUMENTED HOOKS")
for hook in sorted(hooks):
    if hook not in doced:
        path, line = hooks[hook]
        path = path.replace(leodir, '').strip('/')
        print("%25s %s:%s" % (hook, path, line))

print("\nDOCUMENTED HOOKS NOT FOUND IN SOURCE")
for hook in sorted(doced):
    if hook not in hooks:
        print(hook)
