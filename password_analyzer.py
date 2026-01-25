#!/usr/bin/env python3
"""
Password Strength Analyzer
Author: Olaoluwa Aminu-Taiwo
Description: Analyzes password strength and provides security recommendations
"""

import re
import math
import string
from typing import Dict, List, Tuple

class PasswordAnalyzer:
    """Analyzes password strength and security"""

    # Common weak passwords (top 100 most common)
    COMMON_PASSWORDS = {
        'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', '1234567', 'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow', '123123', '654321', 'superman', 'qazwsx', 'michael', 'football', 'password1', 'admin', 'welcome', 'login', 'princess', 'solo', 'starwars', 'password123', 'qwerty123', 'hello', 'freedom'
    }

    # Common patterns to check
    KEYBOARD_PATTERNS = [
        'qwerty', 'asdfgh', 'zxcvbn', '1qaz2wsx', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm', '123qwe', 'qweasd'
    ] 

    def __init__(self):
        self.char_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation
        }

    def analyze(self, password: str) -> Dict:
        """
        Perform comprehensive password analysis
    
        Args:
            password (str): Password to analyze
    
        Returns:
            Dict: Analysis results
        """
        results = {
            'password': password,
            'length': len(password),
            'strength': '',
            'score': 0,
            'entropy': 0,
            'crack_time': '',
            'character_types': {},
            'has_common_password': False,
            'has_pattern': False,
            'suggestions': [],
            'details': {}
        }
    
        # Character type analysis
        results['character_types'] = self._check_character_types(password)
    
        # Calculate entropy
        results['entropy'] = self._calculate_entropy(password)
    
        # Estimate crack time
        results['crack_time'] = self._estimate_crack_time(results['entropy'])
    
        # Check for common passwords
        results['has_common_password'] = self._is_common_password(password)
    
        # Check for patterns
        results['has_pattern'] = self._has_keyboard_pattern(password)
    
        # Calculate score (0-100)
        results['score'] = self._calculate_score(password, results)
    
        # Determine strength level
        results['strength'] = self._determine_strength(results['score'])
    
        # Additional details (MUST come BEFORE suggestions)
        results['details'] = {
            'char_variety': len([v for v in results['character_types'].values() if v]),
            'unique_chars': len(set(password)),
            'repeated_chars': len(password) - len(set(password))
        }
    
        # Generate suggestions (comes AFTER details)
        results['suggestions'] = self._generate_suggestions(password, results)
    
        return results

    def _check_character_types(self, password: str) -> Dict[str, bool]:
        """Check which character types are present"""
        return{
            'lowercase': any(c in self.char_sets['lowercase'] for c in password),
            'uppercase': any(c in self.char_sets['uppercase'] for c in password),
            'digits': any(c in self.char_sets['digits'] for c in password),
            'symbols': any(c in self.char_sets['symbols'] for c in password)
        }

    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate password entropy (bits)

        Entropy = log2(charset_size^password_length)
        """

        charset_size = 0
        char_types = self._check_character_types(password)

        if char_types['lowercase']:
            charset_size += 26
        if char_types['uppercase']:
            charset_size += 26
        if char_types['digits']:
            charset_size += 10
        if char_types['symbols']:
            charset_size += 32

        if charset_size == 0:
            return 0

        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)

    def _estimate_crack_time(self, entropy: float) -> str:
        """
        Estimate time to creack password

        Assumes 1 billion guesses per second (modern GPU)
        """
        if entropy == 0:
            return "Instantly"

        # Possible combinations = 2^entropy
        combinations = 2 ** entropy

        # Guesses per second (1 billion)
        guesses_per_second = 1_000_000_000

        # Seconds to crack (on average, half the keyspace)
        seconds = combinations / (2 * guesses_per_second)

        return self._format_time(seconds)

    def _format_time(self, seconds: float) -> str:
        """Format seconds into human-readable time"""
        if seconds < 1:
            return "Instantly"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 2592000: # 30 days
            return f"{int(seconds / 86400)} days"
        elif seconds < 31536000:  # 365 days
            return f"{int(seconds / 2592000)} months"
        else:
            years = int(seconds / 31536000)
            if years > 1_000_000:
                return f"{years:,} years (practically uncrackable)"
            return f"{years:,} years"

    def _is_common_password(self, password: str) -> bool:
        """Check if password is in common passwords list"""
        return password.lower() in self.COMMON_PASSWORDS

    def _has_keyboard_pattern(self, password: str) -> bool:
        """Check for keyboard patterns"""
        password_lower = password.lower()

        for pattern in self.KEYBOARD_PATTERNS:
            if pattern in password_lower:
                return True

        # Check for sequences (123, abc, etc.)
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            return True
        if re.search(r'(abc|bdc|cde|def|efg|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password_lower):
            return True

        # Check for repeated characters (aaa, 111)
        if re.search(r'(.)\1{2,}', password):
            return True
        
        return False

    def _calculate_score(self, password: str, results: Dict) -> int:
        """Calculate password score (0-100)"""
        score = 0

        # Length scoring (max 30 points)
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 5

        # Character variety (max 30 points)
        char_types = results['character_types']
        variety_count = sum(char_types.values())
        score += variety_count * 7.5

        # Entropy bonus (max 25 points)
        entropy = results['entropy']
        if entropy >= 80:
            score += 25
        elif entropy >= 60:
            score += 20
        elif entropy >= 40:
            score += 15
        elif entropy >= 20:
            score += 10

        # Unique characters (max 15 points)
        unique_ratio = len(set(password)) / len(password) if password else 0
        score += unique_ratio * 15

        # Penalties
        if results['has_common_password']:
            score -= 50
        if results['has_pattern']:
            score -= 20

        # Ensure score is between 0-100
        return max(0, min(100, int(score)))

    def _determine_strength(self, score: int) -> str:
        """Determine strength level from score"""
        if score >= 80:
            return "Very Strong"
        elif score >= 60:
            return "Strong"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Weak"
        else:
            return "Very Weak"

    def _generate_suggestions(self, password: str, results: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        if len(password) < 12:
            suggestions.append(f"Increase length to at least 12 characters (current: {len(password)})")

        char_types = results['character_types']
        if not char_types['lowercase']:
            suggestions.append("Add lowercase letters (a-z)")
        if not char_types['uppercase']:
            suggestions.append("Add uppercase letters (A-Z)")
        if not char_types['digits']:
            suggestions.append("Add numbers (0-9)")
        if not char_types['symbols']:
            suggestions.append("Add special characters (!@#$%^&*)")

        if results['has_common_password']:
            suggestions.append("⚠️ This is a commonly used password - AVOID!")

        if results['has_pattern']:
            suggestions.append("Avoid keyboard patterns and sequences")

        if results['details']['repeated_chars'] > len(password) * 0.3:
            suggestions.append("Reduce repeated characters")

        if not suggestions:
            suggestions.append("✓ Password meets security requirements!")

        return suggestions

def main():
    """Test the password analyzer"""
    analyzer = PasswordAnalyzer()

    # Test passwords
    test_passwords = [
        "password",
        "P@ssw0rd",
        "MyS3cur3P@ssw0rd!",
        "TR0ub4dor&3",
        "correcthorsebatterystaple",
        "aB3$xY9#mk2!pL7@"
    ]

    print("=" * 70)
    print("PASSWORD STRENGTH ANALYZER")
    print("=" * 70)

    for pwd in test_passwords:
        results = analyzer.analyze(pwd)

        print(f"\nPassword: {'*' * len(pwd)}")
        print(f"Strength: {results['strength']} (Score: {results['score']}/100)")
        print(f"Entropy: {results['entropy']} bits")
        print(f"Estimated crack time: {results['crack_time']}")
        print(f"Character types: {sum(results['character_types'].values())}/4")

        if results['suggestions']:
            print("\nSuggestions:")
            for suggestions in results['suggestions']:
                print(f" - {suggestions}")

        print("-" * 70)

if __name__ == "__main__":
    main()
    