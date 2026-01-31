#!/usr/bin/env python3
"""
Password Checker CLI
Author: Olaoluwa Aminu Taiwo
Description: Command-line interface for password analysis and generation
"""

import argparse
import sys
import json
import csv
from typing import List, Dict
from datetime import datetime
from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from breach_checker import BreachChecker

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def colorize(text: str, color: str) -> str:
    """Add color to text"""
    return f"{color}{text}{Colors.END}"

def print_banner():
    """Print CLI banner"""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════╗
║                                               ║
║     🔐  PASSWORD STRENGTH CHECKER CLI  🔐     ║
║                                               ║
║          By: Olaoluwa Aminu Taiwo            ║
║                                               ║
╚═══════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def analyze_single_password(password: str, args) -> Dict:
    """Analyze a single password"""
    analyzer = PasswordAnalyzer()
    results = analyzer.analyze(password)
    
    # Add breach check if requested
    if args.check_breach:
        breach_checker = BreachChecker()
        is_pwned, count = breach_checker.check_password(password)
        results['breach_check'] = {
            'is_pwned': is_pwned,
            'pwned_count': count
        }
        
        if is_pwned and count > 0:
            results['suggestions'].insert(0, 
                f"🚨 CRITICAL: Found in {count:,} data breaches!")
            results['score'] = max(0, results['score'] - 40)
            results['strength'] = analyzer._determine_strength(results['score'])
    
    return results

def display_analysis(results: Dict, verbose: bool = False):
    """Display password analysis results"""
    # Strength color coding
    strength_colors = {
        'Very Weak': Colors.RED,
        'Weak': Colors.RED,
        'Moderate': Colors.YELLOW,
        'Strong': Colors.GREEN,
        'Very Strong': Colors.GREEN
    }
    
    color = strength_colors.get(results['strength'], Colors.YELLOW)
    
    print(f"\n{Colors.BOLD}Password Analysis{Colors.END}")
    print("=" * 60)
    print(f"Strength:    {colorize(results['strength'], color)} ({results['score']}/100)")
    print(f"Length:      {results['length']} characters")
    print(f"Entropy:     {results['entropy']} bits")
    print(f"Crack Time:  {results['crack_time']}")
    
    # Character types
    char_types = results['character_types']
    types_present = sum(char_types.values())
    print(f"Char Types:  {types_present}/4 ", end="")
    
    if char_types['lowercase']:
        print(colorize("✓ a-z", Colors.GREEN), end=" ")
    else:
        print(colorize("✗ a-z", Colors.RED), end=" ")
    
    if char_types['uppercase']:
        print(colorize("✓ A-Z", Colors.GREEN), end=" ")
    else:
        print(colorize("✗ A-Z", Colors.RED), end=" ")
    
    if char_types['digits']:
        print(colorize("✓ 0-9", Colors.GREEN), end=" ")
    else:
        print(colorize("✗ 0-9", Colors.RED), end=" ")
    
    if char_types['symbols']:
        print(colorize("✓ !@#$", Colors.GREEN))
    else:
        print(colorize("✗ !@#$", Colors.RED))
    
    # Warnings
    if results['has_common_password']:
        print(f"\n{colorize('⚠️  WARNING: Common password detected!', Colors.RED)}")
    
    if results['has_pattern']:
        print(f"{colorize('⚠️  WARNING: Pattern detected!', Colors.YELLOW)}")
    
    # Breach check
    if 'breach_check' in results:
        if results['breach_check']['is_pwned']:
            count = results['breach_check']['pwned_count']
            print(f"\n{colorize(f'🚨 BREACHED: Found in {count:,} data breaches!', Colors.RED)}")
        else:
            print(f"\n{colorize('✓ Not found in breach databases', Colors.GREEN)}")
    
    # Suggestions
    if results['suggestions'] and verbose:
        print(f"\n{Colors.BOLD}Suggestions:{Colors.END}")
        for i, suggestion in enumerate(results['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    
    # Detailed stats (verbose mode)
    if verbose:
        print(f"\n{Colors.BOLD}Detailed Statistics:{Colors.END}")
        print(f"  Unique characters:   {results['details']['unique_chars']}")
        print(f"  Repeated characters: {results['details']['repeated_chars']}")
        print(f"  Character variety:   {results['details']['char_variety']}")
    
    print("=" * 60)

def batch_analyze(filepath: str, args) -> List[Dict]:
    """Analyze passwords from file"""
    try:
        with open(filepath, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        print(f"\n{Colors.CYAN}Analyzing {len(passwords)} passwords...{Colors.END}\n")
        
        results = []
        for i, password in enumerate(passwords, 1):
            if not args.quiet:
                print(f"[{i}/{len(passwords)}] Analyzing...", end='\r')
            
            analysis = analyze_single_password(password, args)
            analysis['password_index'] = i
            results.append(analysis)
        
        if not args.quiet:
            print()  # New line after progress
        
        return results
        
    except FileNotFoundError:
        print(f"{colorize('Error: File not found:', Colors.RED)} {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"{colorize('Error reading file:', Colors.RED)} {e}")
        sys.exit(1)

def export_results(results: List[Dict], format: str, output_file: str = None):
    """Export results to file"""
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"password_analysis_{timestamp}.{format}"
    
    try:
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
        
        elif format == 'csv':
            with open(output_file, 'w', newline='') as f:
                if isinstance(results, list):
                    # Batch results
                    fieldnames = ['password_index', 'strength', 'score', 'length', 
                                  'entropy', 'crack_time', 'has_common_password', 
                                  'has_pattern']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for result in results:
                        writer.writerow({
                            'password_index': result.get('password_index', 1),
                            'strength': result['strength'],
                            'score': result['score'],
                            'length': result['length'],
                            'entropy': result['entropy'],
                            'crack_time': result['crack_time'],
                            'has_common_password': result['has_common_password'],
                            'has_pattern': result['has_pattern']
                        })
                else:
                    # Single result
                    fieldnames = ['strength', 'score', 'length', 'entropy', 'crack_time']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        'strength': results['strength'],
                        'score': results['score'],
                        'length': results['length'],
                        'entropy': results['entropy'],
                        'crack_time': results['crack_time']
                    })
        
        print(f"\n{colorize('✓ Results exported to:', Colors.GREEN)} {output_file}")
        
    except Exception as e:
        print(f"{colorize('Error exporting results:', Colors.RED)} {e}")
        sys.exit(1)

def generate_passwords(args):
    """Generate passwords based on arguments"""
    generator = PasswordGenerator()
    
    if args.passphrase:
        passwords = [
            generator.generate_passphrase(
                word_count=args.words,
                separator=args.separator
            )
            for _ in range(args.count)
        ]
    else:
        passwords = generator.generate_multiple(
            count=args.count,
            length=args.length,
            use_lowercase=not args.no_lowercase,
            use_uppercase=not args.no_uppercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.exclude_ambiguous
        )
    
    print(f"\n{Colors.BOLD}Generated Passwords:{Colors.END}")
    print("=" * 60)
    
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}. {colorize(pwd, Colors.GREEN)}")
        
        if args.analyze:
            analyzer = PasswordAnalyzer()
            analysis = analyzer.analyze(pwd)
            print(f"   → {analysis['strength']} ({analysis['score']}/100) | "
                  f"{analysis['entropy']} bits | {analysis['crack_time']}")
    
    print("=" * 60)
    
    return passwords

def check_policy(results: Dict, policy: Dict) -> bool:
    """Check if password meets policy requirements"""
    meets_policy = True
    failures = []
    
    if results['length'] < policy.get('min_length', 8):
        meets_policy = False
        failures.append(f"Minimum length: {policy['min_length']}")
    
    if results['score'] < policy.get('min_score', 50):
        meets_policy = False
        failures.append(f"Minimum score: {policy['min_score']}")
    
    if policy.get('require_uppercase', False) and not results['character_types']['uppercase']:
        meets_policy = False
        failures.append("Must contain uppercase")
    
    if policy.get('require_lowercase', False) and not results['character_types']['lowercase']:
        meets_policy = False
        failures.append("Must contain lowercase")
    
    if policy.get('require_digits', False) and not results['character_types']['digits']:
        meets_policy = False
        failures.append("Must contain digits")
    
    if policy.get('require_symbols', False) and not results['character_types']['symbols']:
        meets_policy = False
        failures.append("Must contain symbols")
    
    if policy.get('reject_common', True) and results['has_common_password']:
        meets_policy = False
        failures.append("Common passwords not allowed")
    
    return meets_policy, failures

def main():
    parser = argparse.ArgumentParser(
        description='Password Strength Checker - Analyze and generate secure passwords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Analyze a single password
  python cli.py analyze -p "MyPassword123"
  
  # Analyze with breach check
  python cli.py analyze -p "password123" --check-breach
  
  # Batch analyze from file
  python cli.py analyze -f passwords.txt -o results.json
  
  # Generate passwords
  python cli.py generate -c 5 -l 16
  
  # Generate passphrases
  python cli.py generate --passphrase -w 4
  
  # Check against policy
  python cli.py analyze -p "MyP@ss123" --policy policy.json
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze password strength')
    analyze_parser.add_argument('-p', '--password', help='Password to analyze')
    analyze_parser.add_argument('-f', '--file', help='File containing passwords (one per line)')
    analyze_parser.add_argument('-o', '--output', help='Output file for results')
    analyze_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                                help='Output format (default: json)')
    analyze_parser.add_argument('--check-breach', action='store_true',
                                help='Check against breach database')
    analyze_parser.add_argument('--policy', help='JSON file with password policy')
    analyze_parser.add_argument('-v', '--verbose', action='store_true',
                                help='Show detailed output')
    analyze_parser.add_argument('-q', '--quiet', action='store_true',
                                help='Minimal output')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate secure passwords')
    generate_parser.add_argument('-c', '--count', type=int, default=1,
                                 help='Number of passwords to generate')
    generate_parser.add_argument('-l', '--length', type=int, default=16,
                                 help='Password length (default: 16)')
    generate_parser.add_argument('--passphrase', action='store_true',
                                 help='Generate passphrase instead')
    generate_parser.add_argument('-w', '--words', type=int, default=4,
                                 help='Number of words for passphrase (default: 4)')
    generate_parser.add_argument('-s', '--separator', default='-',
                                 help='Passphrase separator (default: -)')
    generate_parser.add_argument('--no-lowercase', action='store_true',
                                 help='Exclude lowercase letters')
    generate_parser.add_argument('--no-uppercase', action='store_true',
                                 help='Exclude uppercase letters')
    generate_parser.add_argument('--no-digits', action='store_true',
                                 help='Exclude digits')
    generate_parser.add_argument('--no-symbols', action='store_true',
                                 help='Exclude symbols')
    generate_parser.add_argument('--exclude-ambiguous', action='store_true',
                                 help='Exclude ambiguous characters (il1Lo0O)')
    generate_parser.add_argument('-a', '--analyze', action='store_true',
                                 help='Analyze generated passwords')
    generate_parser.add_argument('-o', '--output', help='Save to file')
    
    args = parser.parse_args()
    
    # Show banner
    if not args.quiet if hasattr(args, 'quiet') else True:
        print_banner()
    
    # Handle commands
    if args.command == 'analyze':
        if args.password:
            # Single password analysis
            results = analyze_single_password(args.password, args)
            
            # Check policy if provided
            if args.policy:
                try:
                    with open(args.policy, 'r') as f:
                        policy = json.load(f)
                    
                    meets_policy, failures = check_policy(results, policy)
                    
                    if meets_policy:
                        print(f"\n{colorize('✓ Password meets policy requirements', Colors.GREEN)}")
                    else:
                        print(f"\n{colorize('✗ Password policy violations:', Colors.RED)}")
                        for failure in failures:
                            print(f"  - {failure}")
                except FileNotFoundError:
                    print(f"{colorize('Error: Policy file not found:', Colors.RED)} {args.policy}")
                except json.JSONDecodeError:
                    print(f"{colorize('Error: Invalid JSON in policy file', Colors.RED)}")
            
            if not args.quiet:
                display_analysis(results, args.verbose)
            
            if args.output:
                export_results(results, args.format, args.output)
        
        elif args.file:
            # Batch analysis
            results = batch_analyze(args.file, args)
            
            if not args.quiet:
                # Summary statistics
                print(f"\n{Colors.BOLD}Batch Analysis Summary{Colors.END}")
                print("=" * 60)
                
                strengths = {}
                for result in results:
                    strength = result['strength']
                    strengths[strength] = strengths.get(strength, 0) + 1
                
                for strength, count in sorted(strengths.items()):
                    percentage = (count / len(results)) * 100
                    print(f"{strength:15} {count:3} ({percentage:5.1f}%)")
                
                avg_score = sum(r['score'] for r in results) / len(results)
                avg_entropy = sum(r['entropy'] for r in results) / len(results)
                
                print(f"\nAverage Score:   {avg_score:.1f}/100")
                print(f"Average Entropy: {avg_entropy:.1f} bits")
                print("=" * 60)
            
            if args.output:
                export_results(results, args.format, args.output)
        
        else:
            print(f"{colorize('Error: Provide either -p or -f', Colors.RED)}")
            analyze_parser.print_help()
            sys.exit(1)
    
    elif args.command == 'generate':
        passwords = generate_passwords(args)
        
        if args.output:
            with open(args.output, 'w') as f:
                for pwd in passwords:
                    f.write(pwd + '\n')
            print(f"\n{colorize('✓ Passwords saved to:', Colors.GREEN)} {args.output}")
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()