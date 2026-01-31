#!/usr/bin/env python3
"""
Example: Batch password checking with statistics
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from password_analyzer import PasswordAnalyzer
from collections import Counter

# Sample passwords to analyze
passwords = [
    "password",
    "Password123",
    "P@ssw0rd2024",
    "MyS3cur3P@ssw0rd!",
    "correct-horse-battery-staple",
    "aB3$xY9#mK2!pL7@",
    "qwerty123",
    "Tr0ub4dor&3",
    "admin",
    "letmein"
]

analyzer = PasswordAnalyzer()
results = []

print("=" * 70)
print("BATCH PASSWORD ANALYSIS")
print("=" * 70)

# Analyze all passwords
for password in passwords:
    result = analyzer.analyze(password)
    results.append(result)
    print(f"{result['strength']:15} | {result['score']:3}/100 | "
          f"{result['entropy']:5.1f} bits | {'*' * len(password)}")

# Statistics
print("\n" + "=" * 70)
print("STATISTICS")
print("=" * 70)

strengths = Counter(r['strength'] for r in results)
print("\nStrength Distribution:")
for strength, count in strengths.most_common():
    percentage = (count / len(results)) * 100
    print(f"  {strength:15} {count:2} ({percentage:5.1f}%)")

avg_score = sum(r['score'] for r in results) / len(results)
avg_entropy = sum(r['entropy'] for r in results) / len(results)
avg_length = sum(r['length'] for r in results) / len(results)

print(f"\nAverages:")
print(f"  Score:   {avg_score:.1f}/100")
print(f"  Entropy: {avg_entropy:.1f} bits")
print(f"  Length:  {avg_length:.1f} characters")

common_count = sum(1 for r in results if r['has_common_password'])
pattern_count = sum(1 for r in results if r['has_pattern'])

print(f"\nIssues Found:")
print(f"  Common passwords: {common_count}")
print(f"  Pattern detected: {pattern_count}")

print("\n" + "=" * 70)
