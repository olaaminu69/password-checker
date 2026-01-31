# Contributing to Password Checker

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Open a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Error messages/screenshots

### Suggesting Features

1. Open an issue with tag `enhancement`
2. Describe the feature and use case
3. Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

### Testing

Test your changes:
```bash
# Test analyzer
python password_analyzer.py

# Test generator  
python password_generator.py

# Test CLI
python cli.py analyze -p "test"
python cli.py generate -c 3

# Test web app
python app.py
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issues when applicable

Examples:
```
Add passphrase generation feature
Fix entropy calculation for special characters
Update README with usage examples
```

## Development Setup
```bash
git clone https://github.com/YOUR_USERNAME/password-checker.git
cd password-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Questions?

Open an issue or reach out to the maintainer.

**Thank you for contributing!** 🎉
