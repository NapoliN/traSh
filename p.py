import re

r = re.compile(r"[亜-熙]")
m = r.match("宇")
print(m)