
import os

print("Listing files:")
print(os.listdir('.'))

try:
    with open('calculator.py', 'r') as f:
        content = f.read()
        print("\nContent of calculator.py:")
        print(content)
except FileNotFoundError:
    print("\nError: calculator.py not found")
except Exception as e:
    print(f"\nAn error occurred: {e}")
