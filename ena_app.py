from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    # return "<h1 style='color:blue'>Hello World!!</h1>"

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
