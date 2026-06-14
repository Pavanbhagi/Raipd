# 30 Days of Python - Master Script (Days 1-8)
# pavanbhagi code series

import math
import random

def day_8_modules():
    print("Day 8: Modules & Libraries")
    print(f"Math: Square root of 16 is {math.sqrt(16)}")
    print(f"Random: Number between 1-100: {random.randint(1, 100)}")

class PavanSeries:
    def __init__(self, day):
        self.day = day
    def show(self):
        print(f"Currently on Day {self.day}")

if __name__ == "__main__":
    # Previous days logic
    print("Running 30 Days of Python...")
    
    # Day 7 Logic (OOP)
    p = PavanSeries(8)
    p.show()
    
    # Day 8 Logic (Modules)
    day_8_modules()