import numpy as np
from flask import send_from_directory, Flask, request, jsonify, render_template, redirect, url_for
import pickle

app = Flask(__name__, static_url_path='')
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('fill.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        return redirect(url_for('fill'))
    return render_template('room.html')

@app.route('/fill', methods=['GET', 'POST'])
def fill():
    if request.method == 'POST':
        return redirect(url_for('room'))
    return render_template('fill.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        return redirect(url_for('room'))
    return render_template('book.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = request.form.to_dict() 
    features = list(features.values()) 
    features = list(map(int, features))
    final_features = np.array(features).reshape(1,6)
    prediction = model.predict(final_features)
    #select = request.form.get('category')
    output = round(prediction[0], 2)
    return render_template('fill.html', prediction_text='家具價格為(Furniture prediction price is): $ {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls through request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
    
