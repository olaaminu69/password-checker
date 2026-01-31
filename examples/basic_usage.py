#!/usr/bin/env python3
"""
Basic usage examples for Password Checker
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from breach_checker import BreachChecker

print("=" * 60)
print("PASSWORD CHECKER - BASIC USAGE EXAMPLES")
print("=" * 60)

# Example 1: Analyze a password
print("\n1. ANALYZE PASSWORD")
print("-" * 60)

analyzer = PasswordAnalyzer()
password = "MyS3cur3P@ssw0rd!"

results = analyzer.analyze(password)
print(f"Password: {'*' * len(password)}")
print(f"Strength: {results['strength']}")
print(f"Score: {results['score']}/100")
print(f"Entropy: {results['entropy']} bits")
print(f"Crack time: {results['crack_time']}")

# Example 2: Generate password
print("\n2. GENERATE PASSWORD")
print("-" * 60)

generator = PasswordGenerator()
new_password = generator.generate(length=16)
print(f"Generated: {new_password}")

analysis = analyzer.analyze(new_password)
print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")

# Example 3: Generate passphrase
print("\n3. GENERATE PASSPHRASE")
print("-" * 60)

passphrase = generator.generate_passphrase(word_count=4)
print(f"Passphrase: {passphrase}")

analysis = analyzer.analyze(passphrase)
print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")

# Example 4: Check breach database
print("\n4. CHECK BREACH DATABASE")
print("-" * 60)

checker = BreachChecker()
test_password = "password123"

is_pwned, count = checker.check_password(test_password)
print(f"Password: {test_password}")
if is_pwned:
    print(f"⚠️  BREACHED: Found in {count:,} data breaches!")
else:
    print("✓ Not found in breach databases")

# Example 5: Multiple passwords
print("\n5. BATCH ANALYSIS")
print("-" * 60)

test_passwords = [
    "weak",
    "Moderate123",
    "Str0ng!P@ssw0rd",
    "aB3$xY9#mK2!pL7@vN5&"
]

for pwd in test_passwords:
    result = analyzer.analyze(pwd)
    print(f"{result['strength']:15} | Score: {result['score']:3}/100 | {'*' * len(pwd)}")

print("\n" + "=" * 60)
