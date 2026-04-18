import sys
print(f"Python executable: {sys.executable}")
print(f"Version:           {sys.version}")
print(f"Search path:")
for p in sys.path:
  print(f"                   {p}") 