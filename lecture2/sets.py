# Create an empty set
s = set()

s.add(1)
s.add(2)
s.add(3)
s.add(4)

print(s)

s.add(3)
s.add(2)

print(s)

s.remove(2)

print(s)
print(f"The set has {len(s)} elements now.")