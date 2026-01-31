#!/usr/bin/env python3
"""
Example: Password policy compliance checking
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_analyzer import PasswordAnalyzer
import json

# Define password policy
policy = {
    "min_length": 12,
    "min_score": 60,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digits": True,
    "require_symbols": True,
    "reject_common": True
}

def check_policy(password: str, policy: dict) -> tuple:
    """Check if password meets policy"""
    analyzer = PasswordAnalyzer()
    results = analyzer.analyze(password)
    
    failures = []
    
    if results['length'] < policy['min_length']:
        failures.append(f"Length must be at least {policy['min_length']}")
    
    if results['score'] < policy['min_score']:
        failures.append(f"Score must be at least {policy['min_score']}")
    
    if policy['require_uppercase'] and not results['character_types']['uppercase']:
        failures.append("Must contain uppercase letters")
    
    if policy['require_lowercase'] and not results['character_types']['lowercase']:
        failures.append("Must contain lowercase letters")
    
    if policy['require_digits'] and not results['character_types']['digits']:
        failures.append("Must contain numbers")
    
    if policy['require_symbols'] and not results['character_types']['symbols']:
        failures.append("Must contain symbols")
    
    if policy['reject_common'] and results['has_common_password']:
        failures.append("Common passwords not allowed")
    
    return len(failures) == 0, failures

# Test passwords
test_passwords = {
    "weak": "password",
    "short": "P@ss1",
    "no_symbols": "Password123",
    "compliant": "MyS3cur3P@ss!"
}

print("=" * 70)
print("PASSWORD POLICY COMPLIANCE CHECK")
print("=" * 70)
print(f"\nPolicy Requirements:")
print(f"  - Minimum length: {policy['min_length']}")
print(f"  - Minimum score: {policy['min_score']}")
print(f"  - Requires: uppercase, lowercase, digits, symbols")
print(f"  - Rejects: common passwords")
print("=" * 70)

for name, password in test_passwords.items():
    meets_policy, failures = check_policy(password, policy)
    
    print(f"\nPassword: {name}")
    print(f"  {'✓ PASS' if meets_policy else '✗ FAIL'}")
    
    if failures:
        print("  Violations:")
        for failure in failures:
            print(f"    - {failure}")

print("\n" + "=" * 70)
