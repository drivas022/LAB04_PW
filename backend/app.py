from flask import Flask, jsonify

# llamando dependencias e inicializando la app
app = Flask(__file__)

# decorador
@app.route('/')

def home():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)