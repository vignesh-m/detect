from flask import Flask, request
from flask import render_template
import os
import glob
from subprocess import call

app = Flask(__name__, static_folder='storage')

@app.route('/')
def main():
    return render_template('template.html')

@app.route('/submit', methods=['POST'])
def submit():
    video = request.files['video']
    filename = 'storage/{}'.format(video.filename)
    video.save(filename)
    
    files = glob.glob('darknet/Data/*.jpg')
    for file in files:
        os.remove(file)
    call(['ffmpeg', '-i', filename, '-vf', 'fps=3', 'darknet/Data/out%d.jpg'])

    n_files = len(os.listdir('darknet/Data'))
    os.chdir("darknet")
    call(('./darknet detect cfg/yolo.cfg yolo.weights ' + str(n_files) + ' 0 ').split())
    os.chdir("..")

    return render_template('result.html', filename=filename)

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
