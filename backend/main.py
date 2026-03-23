from flask import Flask, request, jsonify
from flask_cors import CORS
from salary_calculation import calcola_netto_2025

app = Flask(__name__)
CORS(app, origins=["https://salary-calculator-five-ecru.vercel.app/"])

@app.route('/calculate', methods=['POST'])
def calculate_salary():
    data = request.get_json()
    base_salary = float(data.get('base_salary', 0))
    bonus = float(data.get('bonus', 0))
    deductions = float(data.get('deductions', 0))

    # Include bonus/deductions in the gross annual salary before tax calc
    gross_salary = max(0.0, base_salary + bonus - deductions)

    result = calcola_netto_2025(gross_salary)

    result.update({
        'input_gross_salary': gross_salary,
        'input_base_salary': base_salary,
        'input_bonus': bonus,
        'input_deductions': deductions
    })

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)