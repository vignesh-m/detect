from flask import Flask, request
from flask import render_template
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    print(request.files)
    name = request.form['name']
    image = request.files['image']

    image.save('storage/{}.jpg'.format(name))
    return 'hello'

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
