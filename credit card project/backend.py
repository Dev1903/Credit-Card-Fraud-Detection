from flask import Flask, request, jsonify, render_template
import credit_fraud_decision_tree  # Import your existing fraud detection code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html is in the templates folder

@app.route('/detect-fraud', methods=['POST'])
def detect_fraud():
    data = request.json  # This will be a list (array) of feature values
    # Use your fraud detection code to get the result
    result = credit_fraud_decision_tree.detect_fraud(data)  # Assuming your function accepts a list of features

    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
