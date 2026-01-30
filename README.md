# 🔐 Password Strength Checker

A comprehensive password security tool with real-time strength analysis, breach detection, and secure password generation. Built with Python and Flask.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📸 Screenshots

### Password Strength Analysis
*Real-time password strength checking with detailed feedback*

### Password Generator
*Generate secure passwords and memorable passphrases*

### Breach Detection
*Check if passwords have been exposed in data breaches*

---

## ✨ Features

### Password Analysis
- ✅ **Real-time strength calculation** - Instant feedback as you type
- ✅ **Entropy calculation** - Measures password randomness in bits
- ✅ **Crack time estimation** - Estimates time to break using modern hardware
- ✅ **Character variety detection** - Checks for uppercase, lowercase, numbers, symbols
- ✅ **Pattern detection** - Identifies keyboard patterns, sequences, and repetition
- ✅ **Common password detection** - Checks against top 1000 most common passwords
- ✅ **Breach database integration** - Uses HaveIBeenPwned API (330+ million pwned passwords)

### Password Generation
- ✅ **Customizable length** (8-32 characters)
- ✅ **Character type selection** - Choose which character types to include
- ✅ **Ambiguous character exclusion** - Avoid confusing characters (i, l, 1, L, o, 0, O)
- ✅ **Passphrase generator** - Create memorable multi-word passwords
- ✅ **Cryptographically secure** - Uses Python's `secrets` module
- ✅ **Copy to clipboard** - One-click password copying

### User Interface
- ✅ **Modern dark theme** - Easy on the eyes
- ✅ **Responsive design** - Works on desktop, tablet, and mobile
- ✅ **Color-coded strength meter** - Visual feedback (red → yellow → green)
- ✅ **Real-time updates** - No page refresh needed
- ✅ **Accessibility friendly** - Semantic HTML and proper contrast

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/olaaminu69/password-checker.git
   cd password-checker
```

2. **Create virtual environment**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Run the application**
```bash
   python app.py
```

5. **Open your browser**
```
   http://localhost:5000
```

---

## 📖 Usage

### Web Interface

1. **Check Password Strength:**
   - Enter any password in the input field
   - View real-time strength analysis
   - Optionally enable breach database checking
   - Review suggestions for improvement

2. **Generate Secure Password:**
   - Adjust length slider (8-32 characters)
   - Select character types (lowercase, uppercase, digits, symbols)
   - Click "Generate Password"
   - Copy to clipboard with one click

3. **Generate Passphrase:**
   - Switch to "Passphrase" tab
   - Adjust word count (3-8 words)
   - Choose separator (dash, underscore, period, space)
   - Click "Generate Passphrase"

### Python API
```python
from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from breach_checker import BreachChecker

# Analyze password
analyzer = PasswordAnalyzer()
results = analyzer.analyze("MyP@ssw0rd2024")
print(f"Strength: {results['strength']}")
print(f"Score: {results['score']}/100")
print(f"Entropy: {results['entropy']} bits")
print(f"Crack time: {results['crack_time']}")

# Generate password
generator = PasswordGenerator()
password = generator.generate(length=16, use_symbols=True)
print(f"Generated: {password}")

# Generate passphrase
passphrase = generator.generate_passphrase(word_count=4)
print(f"Passphrase: {passphrase}")

# Check breach database
checker = BreachChecker()
is_pwned, count = checker.check_password("password123")
if is_pwned:
    print(f"⚠️  Found in {count:,} data breaches!")
```

---

## 🛠️ Technical Details

### Project Structure
```
password-checker/
│
├── app.py                    # Flask web application
├── password_analyzer.py      # Core password analysis logic
├── password_generator.py     # Secure password generation
├── breach_checker.py         # HaveIBeenPwned API integration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── templates/
│   └── index.html           # Main web interface
│
├── static/
│   ├── css/
│   │   └── style.css        # Styling and animations
│   └── js/
│       └── main.js          # Client-side interactivity
│
└── screenshots/             # Project screenshots
```

### How It Works

#### Password Strength Calculation

The analyzer uses multiple factors to calculate a 0-100 score:

1. **Length** (max 30 points)
   - 6-7 chars: 5 points
   - 8-11 chars: 15 points
   - 12-15 chars: 25 points
   - 16+ chars: 30 points

2. **Character Variety** (max 30 points)
   - Lowercase: 7.5 points
   - Uppercase: 7.5 points
   - Digits: 7.5 points
   - Symbols: 7.5 points

3. **Entropy** (max 25 points)
   - Based on Shannon entropy calculation
   - Higher randomness = higher score

4. **Uniqueness** (max 15 points)
   - Ratio of unique to total characters
   - Penalizes repetition

5. **Penalties**
   - Common password: -50 points
   - Keyboard patterns: -20 points
   - Data breach: -40 points

#### Entropy Calculation
```
Entropy = log₂(charset_size^password_length)
```

Where:
- `charset_size` = number of possible characters (26 for lowercase, 52 for mixed case, etc.)
- Higher entropy = more secure password

#### Crack Time Estimation

Assumes:
- 1 billion guesses per second (modern GPU)
- Average time = 50% of keyspace
```
Time = 2^entropy / (2 × 10^9 guesses/sec)
```

---

## 🔒 Security Features

### Password Generation
- Uses Python's `secrets` module (cryptographically secure)
- True randomness from OS entropy sources
- No predictable patterns

### Breach Detection
- K-anonymity model (only first 5 chars of hash sent to API)
- No plaintext passwords transmitted
- Privacy-preserving design

### Best Practices
- No password storage (all analysis is client-side or session-only)
- No logging of passwords
- Secure defaults (symbols enabled, ambiguous chars excluded)

---

## 📊 Password Strength Levels

| Score | Strength | Color | Crack Time (Estimate) |
|-------|----------|-------|----------------------|
| 0-20 | Very Weak | 🔴 Red | Seconds to minutes |
| 21-40 | Weak | 🟠 Orange | Minutes to hours |
| 41-60 | Moderate | 🟡 Yellow | Days to weeks |
| 61-80 | Strong | 🟢 Green | Months to years |
| 81-100 | Very Strong | 🟢 Dark Green | Centuries+ |

---

## 🌐 API Reference

### `/analyze` (POST)

Analyze password strength

**Request:**
```json
{
  "password": "MyP@ssw0rd2024",
  "check_breach": true
}
```

**Response:**
```json
{
  "password": "MyP@ssw0rd2024",
  "length": 14,
  "strength": "Strong",
  "score": 72,
  "entropy": 82.5,
  "crack_time": "3 years",
  "character_types": {
    "lowercase": true,
    "uppercase": true,
    "digits": true,
    "symbols": true
  },
  "has_common_password": false,
  "has_pattern": false,
  "suggestions": [],
  "breach_check": {
    "is_pwned": false,
    "pwned_count": 0
  }
}
```

### `/generate` (POST)

Generate secure password

**Request:**
```json
{
  "type": "password",
  "length": 16,
  "use_lowercase": true,
  "use_uppercase": true,
  "use_digits": true,
  "use_symbols": true,
  "exclude_ambiguous": true
}
```

**Response:**
```json
{
  "password": "K7@mP2#xR9$vN4&q",
  "analysis": {
    "strength": "Very Strong",
    "score": 95,
    "entropy": 95.3,
    "crack_time": "3,247 years"
  }
}
```

---

## 🧪 Testing

### Manual Testing
```bash
# Test password analyzer
python password_analyzer.py

# Test password generator
python password_generator.py

# Test breach checker
python breach_checker.py
```

### Web Interface Testing

1. Start the server: `python app.py`
2. Open browser to `http://localhost:5000`
3. Test various password scenarios:
   - Very weak: `password`
   - Weak: `Password123`
   - Moderate: `P@ssw0rd2024`
   - Strong: `MyS3cur3P@ssw0rd!`
   - Very strong: `aB3$xY9#mK2!pL7@vN5&`

---

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css`:
```css
:root {
    --primary: #667eea;      /* Primary accent color */
    --success: #48bb78;      /* Success/strong color */
    --warning: #ed8936;      /* Warning/moderate color */
    --danger: #f56565;       /* Danger/weak color */
    --bg-primary: #0f172a;   /* Background color */
}
```

### Adjust Strength Thresholds

Edit `password_analyzer.py`:
```python
def _determine_strength(self, score: int) -> str:
    if score >= 80:      # Change these thresholds
        return "Very Strong"
    elif score >= 60:
        return "Strong"
    # ... etc
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/password-checker.git

# Install dev dependencies
pip install -r requirements.txt

# Make changes and test
python app.py
```

---

## 📝 Future Enhancements

- [ ] Command-line interface (CLI)
- [ ] Batch password checking from file
- [ ] Export results to CSV/JSON
- [ ] Password policy compliance checker
- [ ] Multi-language support
- [ ] Dark/light theme toggle
- [ ] Password strength history tracking
- [ ] Mobile app version

---

## 🐛 Known Issues

- Breach database API calls may be slow on first request
- Copy to clipboard requires HTTPS in production
- Some older browsers may not support all features

---

## 📄 License

This project is licensed under the MIT License - see below for details:
```
MIT License

Copyright (c) 2026 Olaoluwa Aminu Taiwo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Olaoluwa Aminu Taiwo**

- GitHub: [@olaaminu69](https://github.com/olaaminu69)
- LinkedIn: [Olaoluwa Aminu Taiwo](https://linkedin.com/in/olaoluwa-aminu-taiwo-b6963a154/)
- Portfolio: [View Projects](https://github.com/olaaminu69)

---

## 🙏 Acknowledgments

- [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3) by Troy Hunt
- Password strength algorithms inspired by zxcvbn
- Word list for passphrases from EFF Dice-Generated Passphrases
- Flask framework by Pallets Projects
- UI design inspired by modern cybersecurity tools

---

## 📚 References

- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Password Hashing Competition](https://password-hashing.net/)
- [Shannon Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory))

---

## ⭐ Star This Project

If you found this project helpful, please give it a star! It helps others discover the project and motivates continued development.

---

**Built with ❤️ for cybersecurity education and awareness**
