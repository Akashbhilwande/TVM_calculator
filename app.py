from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    initial_investment = db.Column(db.Float, nullable=False)
    interest = db.Column(db.Float, nullable=False)
    tenure = db.Column(db.Integer, nullable=False)



with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        interest = request.form.get('number2')
        initial_investment = request.form.get('number1')
        tenure = request.form.get('number3')
        
        if interest.isdigit() and initial_investment.isdigit() and tenure.isdigit():
            new_entry = Number(interest=float(interest), initial_investment=float(initial_investment), tenure=int(tenure))
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/calculate_irr')

    return render_template('index.html')


def tvm_monthly_installments(principal, rate, years):
    r = rate / 100 / 12  
    n = years * 12 
    if r == 0:
        monthly_payment = principal / n
    else:
        monthly_payment = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    monthly_values = []
    for month in range(1, n + 1):
        discounted_emi = monthly_payment / ((1 + r) ** month)  
        monthly_values.append((month, round(discounted_emi, 2)))

    return monthly_payment, monthly_values



@app.route('/calculate_irr', methods=['GET'])
def calculate_irr():
    latest_entry = Number.query.order_by(Number.id.desc()).first()
    if latest_entry:
        monthly_payment, monthly_values = tvm_monthly_installments(
            latest_entry.initial_investment, latest_entry.interest, latest_entry.tenure
        )
        # for i in monthly_values():
        #         print(monthly_values[1])
        return render_template('calculate.html', monthly_payment=monthly_payment, monthly_values=monthly_values)
        
    return "No data available."

if __name__ == '__main__':
    app.run(debug=True)
