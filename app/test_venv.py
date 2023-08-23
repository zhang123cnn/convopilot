import sys

if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("You are inside a virtual environment.")
else:
    print("You are not inside a virtual environment.")
