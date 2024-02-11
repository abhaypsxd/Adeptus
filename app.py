from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index.html')

def index():
    # Your Python code here
    account = 0
    balance = 0
    selected_contact = "Laudo"
    action = "Paid"
    amount = 69420

    # Render an HTML template with the Python output
    return render_template('index.html', output1=balance, output2 = account, output3=action, output4= amount, output5 = selected_contact)
@app.route('/pay.html')
def pay():

    return render_template('pay.html')

if __name__ == '__main__':
    app.run(debug=True)