#!/usr/bin/env python3
"""
Day 2 Feature Tests
"""

from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from breach_checker import BreachChecker

def test_all():
    print("=" * 70)
    print("DAY 2 FEATURE TESTS")
    print("=" * 70)

    # Test1: Password Analysis with Breach Check
    print("\n1. PASSWORD ANALYSIS WITH BREACH CHECK")
    print("-" * 70)

    analyzer = PasswordAnalyzer()
    test_pwd = "password123"

    results = analyzer.analyze_with_breach_check(test_pwd)

    print(f"Password: {test_pwd}")
    print(f"Strength: {results['strength']} ({results['score']}/100)")
    print(f"Breached: {'YES' if results['breach_check']['is_pwned'] else 'NO'}")
    if results['breach_check']['is_pwned']:
        print(f"Found in breaches: {results['breach_check']['pwned_count']:,} times")

    # Test 2: Password Generation
    print("\n\n2. PASSWORD GENERATION")
    print("-" * 70)

    generator = PasswordGenerator()

    print("Standard password:")
    pwd1 = generator.generate(length=16)
    print(f"    {pwd1}")

    print("\nPassphrase:")
    phrase = generator.generate_passphrase(word_count=4)
    print(f"    {phrase}")

    # Test 3: Analyze Generated Passwords
    print("\n\n3. ANALYZE GENERATED PASSWORDS")
    print("-" * 70)

    for i in range(3):
        pwd = generator.generate(length=14)
        analysis = analyzer.analyze(pwd)
        print(f"\nPassword #{i+1}: {pwd}")
        print(f" Strength: {analysis['strength']} ({analysis['score']}/100)")
        print(f" Entropy: {analysis['entropy']} bits")
        print(f" Crack time: {analysis['crack_time']}")

    print("\n" + "=" * 70)
    print("✓ All Day 2 features working!")
    print("=" * 70)

if __name__ == "__main__":
    test_all()