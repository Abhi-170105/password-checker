from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

common_passwords = [
    "password", "123456", "123456789", "qwerty", "abc123", "111111",
    "123123", "password1", "12345678", "iloveyou", "admin", "incorrectpassword", "abcdefgh", "12344321"
]

def password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Password should include at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Password should include at least one lowercase letter.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Password should include at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Password should include at least one special character (!@#$%^&* etc.).")

    if re.search(r"\s", password):
        feedback.append("Password should not contain spaces.")

    if password.lower() in common_passwords:
        feedback.append("Password is too common — choose something more unique.")

    strength_levels = {
        0: "Very Weak",
        1: "Weak",
        2: "Weak",
        3: "Medium",
        4: "Strong",
        5: "Very Strong"
    }

    strength = strength_levels.get(score, "Very Weak")

    return strength, feedback

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_password():
    password = request.form.get('password', '')
    strength, feedback = password_strength(password)
    return jsonify({'strength': strength, 'feedback': feedback})

if __name__ == '__main__':
    app.run(debug=True)
