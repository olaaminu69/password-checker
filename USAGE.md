# Usage Guide

## Web Interface

### Starting the Server
```bash
python app.py
```

Open browser to `http://localhost:5000`

### Features

#### Password Strength Checker
1. Enter password in input field
2. Watch real-time strength meter update
3. Toggle password visibility with 👁️ icon
4. Enable breach checking for security validation
5. Review suggestions for improvement

#### Password Generator
1. Adjust length slider (8-32 characters)
2. Select character types (lowercase, uppercase, digits, symbols)
3. Enable/disable ambiguous character exclusion
4. Click "Generate Password"
5. Copy to clipboard with 📋 button

#### Passphrase Generator
1. Switch to "Passphrase" tab
2. Adjust word count (3-8 words)
3. Select separator (-, _, ., space)
4. Click "Generate Passphrase"
5. Copy generated passphrase

---

## Command Line Interface

### Basic Commands
```bash
# Analyze single password
python cli.py analyze -p "MyPassword123"

# Analyze with verbose output
python cli.py analyze -p "MyPassword123" -v

# Check against breach database
python cli.py analyze -p "password123" --check-breach

# Batch analyze from file
python cli.py analyze -f passwords.txt

# Export results to JSON
python cli.py analyze -f passwords.txt -o results.json

# Export to CSV
python cli.py analyze -f passwords.txt --format csv -o results.csv

# Check against password policy
python cli.py analyze -p "P@ssw0rd" --policy policy.json

# Generate passwords
python cli.py generate -c 5 -l 16

# Generate with analysis
python cli.py generate -c 3 -a

# Generate passphrase
python cli.py generate --passphrase -w 4

# Save generated passwords to file
python cli.py generate -c 10 -o passwords.txt
```

### Advanced Options
```bash
# Exclude specific character types
python cli.py generate --no-symbols -l 12

# Custom passphrase separator
python cli.py generate --passphrase -w 5 -s "_"

# Quiet mode (minimal output)
python cli.py analyze -f passwords.txt -q

# Exclude ambiguous characters
python cli.py generate --exclude-ambiguous -l 20
```

---

## Password Policy

Create a `policy.json` file:
```json
{
  "min_length": 12,
  "min_score": 60,
  "require_uppercase": true,
  "require_lowercase": true,
  "require_digits": true,
  "require_symbols": true,
  "reject_common": true,
  "description": "Corporate password policy"
}
```

Check compliance:
```bash
python cli.py analyze -p "YourPassword" --policy policy.json
```

---

## Python API

### Basic Usage
```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
results = analyzer.analyze("MyP@ssw0rd2024")

print(f"Strength: {results['strength']}")
print(f"Score: {results['score']}/100")
print(f"Entropy: {results['entropy']} bits")
```

### Password Generation
```python
from password_generator import PasswordGenerator

generator = PasswordGenerator()

# Generate standard password
password = generator.generate(
    length=16,
    use_lowercase=True,
    use_uppercase=True,
    use_digits=True,
    use_symbols=True
)

# Generate passphrase
passphrase = generator.generate_passphrase(
    word_count=4,
    separator="-"
)
```

### Breach Checking
```python
from breach_checker import BreachChecker

checker = BreachChecker()
is_pwned, count = checker.check_password("password123")

if is_pwned:
    print(f"⚠️  Found in {count:,} breaches!")
```

---

## Tips for Strong Passwords

### What Makes a Strong Password?

1. **Length**: Minimum 12 characters (16+ recommended)
2. **Variety**: Mix of uppercase, lowercase, digits, symbols
3. **Randomness**: Avoid patterns, sequences, personal info
4. **Uniqueness**: Don't reuse passwords across sites
5. **Unpredictability**: Avoid dictionary words, common substitutions

### Good Examples

- `K7@mP2#xR9$vN4&q` - Very Strong (95/100)
- `Correct-Horse-Battery-Staple42` - Strong passphrase
- `MyS3cur3P@ssw0rd!2024` - Strong (78/100)

### Bad Examples

- `password123` - Very Weak, common, breached
- `qwerty` - Very Weak, keyboard pattern
- `admin` - Very Weak, common

---

## Troubleshooting

### Web Interface

**Page not loading?**
- Check Flask is running (`python app.py`)
- Verify port 5000 is not in use
- Try `http://127.0.0.1:5000` or `http://localhost:5000`

**Styles not loading?**
- Check `static/css/style.css` exists
- Clear browser cache (Ctrl+Shift+R)
- Check browser console (F12) for errors

**JavaScript errors?**
- Check `static/js/main.js` exists
- Verify all HTML element IDs match
- Check browser console for specific errors

### CLI

**Command not found?**
```bash
python cli.py --help
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**File not found?**
- Ensure file paths are correct
- Use absolute paths if needed

---

## Security Notes

- Never share passwords through unsecured channels
- This tool analyzes passwords locally (web version)
- Breach checking uses k-anonymity (only hash prefix sent)
- Generated passwords are cryptographically secure
- No passwords are stored or logged

---

## Performance

- Web interface: Real-time analysis (<100ms)
- Batch processing: ~100-200 passwords/second
- Breach checking: ~1-3 seconds per password (API dependent)
- Password generation: Instant

---

## Getting Help

- GitHub Issues: [Report bugs or request features](https://github.com/olaaminu69/password-checker/issues)
- Documentation: See README.md for detailed info
- Examples: Check `examples/` directory

---

**Need more help? Open an issue on GitHub!**
