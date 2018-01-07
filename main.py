from flask import Flask, request
from flask import render_template
import os
import boto3

app = Flask(__name__)
s3 = boto3.resource('s3')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    print(request.files)
    name = request.form['name']
    image = request.files['image']
    # path = os.path.join(os.path.abspath('storage'), 'temp')
    fileobj = open('temp', 'wb')
    image.save(fileobj)
    s3.Bucket('detect-1').put_object(Key='{}.jpg'.format(name), Body=fileobj)
    return 'hello'
    # return "{}<br/>{}<br/>".format(name, image.filename)

def main():
    app.run(debug=True, host="0.0.0.0")

if __name__ == '__main__':
    main()
