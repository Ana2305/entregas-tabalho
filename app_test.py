from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "API Rodando!"

if __name__ == '__main__':
    print("Testando Flask...")
    app.run(debug=True)
