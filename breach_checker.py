#!/usr/bin/env python3
"""
Password Breach Checker using HaveIBeenPwned API
Author: Olaoluwa Aminu-Taiwo
Description: Check if passwords have been leaked in data breaches
"""

import hashlib
import requests
from typing import Tuple

class BreachChecker:
    """Check passwords against HaveIBeenPwned database"""

    API_URL = "https://api.pwnedpasswords.com/range/"

    def check_password(self, password: str) -> Tuple[bool, int]:
        """
        Check if password has been pwned
        Uses k-anonymity model: only sends first 5 chars of SHA-1 hash

        Args:
            password (str): Password to check

        Returns:
            Tuple[bool, int]: (is_pwned, occurrence_count)
        """
        # Hash the password
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

        # Split into prefix (first 5 chars) and suffix
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]

        try:
            # Query API with prefix only (k-anonymity)
            response = requests.get(f"{self.API_URL}{prefix}", timeout=5)
            response.raise_for_status()

            # Check if our suffix appears in results
            hashes = response.text.splitlines()
            for hash_line in hashes:
                hash_suffix, count = hash_line.split(':')
                if hash_suffix == suffix:
                    return True, int(count)

            return False, 0

        except requests.RequestException as e:
            # If API call fails, return unknown status
            print(f"Warning: Could not check breach database: {e}")
            return False, -1   # -1 indicates API error

    def check_multiple(self, passwords: list) -> dict:
        """Check multiple passwords"""
        results = {}
        for password in passwords:
            is_pwned, count = self.check_password(password)
            results[password] = {'pwned': is_pwned, 'count': count}
        return results


def main():
    """Test the breach checker"""
    checker = BreachChecker()

    print("=" * 70)
    print("PASSWORD BREACH CHECKER TEST")
    print("=" * 70)

    # Test passwords (some known to be breached)
    test_passwords = [
        "password123",   # Very common
        "MyS3cur3P@ssw0rd!",    # Probably not breached
        "qwerty",   # Very common
        "Tr0ub4dor&3"   # From XKCD, likely breached
    ]

    for pwd in test_passwords:
        is_pwned, count = checker.check_password(pwd)

        print(f"\nPassword: {'*' * len(pwd)}")
        if count == -1:
            print("   Status: Could not check (API error)")
        elif is_pwned:
            print(f"   Status: ⚠️  BREACHED - Found {count:,} times in data breaches!")
        else:
            print("   Status: ✓ Not found in breach databases")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()