from flask import Flask, render_template, request, jsonify
from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from breach_checker import BreachChecker

app = Flask(__name__)

# Initialize tools
analyzer = PasswordAnalyzer()
generator = PasswordGenerator()
breach_checker = BreachChecker()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_password():
    """Analyze password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    
    results = analyzer.analyze(password)
    
    check_breach = data.get('check_breach', False)
    if check_breach:
        is_pwned, count = breach_checker.check_password(password)
        results['breach_check'] = {
            'is_pwned': is_pwned,
            'pwned_count': count
        }
        
        if is_pwned and count > 0:
            results['suggestions'].insert(0, 
                f"🚨 This password appears in {count:,} data breaches!")
    
    return jsonify(results)

@app.route('/generate', methods=['POST'])
def generate_password():
    """Generate new password"""
    data = request.get_json()
    
    length = data.get('length', 16)
    use_lowercase = data.get('use_lowercase', True)
    use_uppercase = data.get('use_uppercase', True)
    use_digits = data.get('use_digits', True)
    use_symbols = data.get('use_symbols', True)
    exclude_ambiguous = data.get('exclude_ambiguous', True)
    
    password_type = data.get('type', 'password')
    
    if password_type == 'passphrase':
        word_count = data.get('word_count', 4)
        separator = data.get('separator', '-')
        password = generator.generate_passphrase(
            word_count=word_count,
            separator=separator
        )
    else:
        password = generator.generate(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
    
    analysis = analyzer.analyze(password)
    
    return jsonify({
        'password': password,
        'analysis': analysis
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
