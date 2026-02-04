from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_salary():
    data = request.get_json()
    base_salary = data.get('base_salary', 0)
    bonus = data.get('bonus', 0)
    deductions = data.get('deductions', 0)

    total_salary = base_salary + bonus - deductions

    return jsonify({'total_salary': total_salary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)