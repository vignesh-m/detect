from flask import Flask, request
from flask import render_template
import os
import glob
from subprocess import call
import shutil

app = Flask(__name__, static_folder='storage')

@app.route('/')
def main():
    return render_template('template.html')

@app.route('/submit', methods=['POST'])
def submit():
    video = request.files['video']
    filename = 'storage/{}'.format(video.filename)
    video.save(filename)
    img_dir = os.path.splitext(filename)[0]
    print(img_dir)
    try:
        os.mkdir(img_dir)
    except OSError:
        pass
    
    files = glob.glob('darknet/Data/*.jpg')
    for file in files:
        os.remove(file)
    call(['ffmpeg', '-i', filename, '-vf', 'fps=3', 'darknet/Data/out%d.jpg'])
    n_files = len(os.listdir('darknet/Data'))
    print(n_files)
    shutil.copyfile('darknet/predictions.png', 'storage/predictions.png')
    
    return render_template('result.html', filename=filename)

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
