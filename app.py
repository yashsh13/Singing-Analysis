from flask import Flask, render_template, request
import os
from moviepy.editor import VideoFileClip
from analyze import analysis
from llm import ai_call


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static','audio')

@app.route('/',methods=['POST','GET'])
def index():

    val=0
    response=0
    if request.method == 'POST':
        video = request.files['video']

        if video :
            video.save(os.path.join(app.config['UPLOAD_FOLDER'],video.filename))
            video = VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'],video.filename))
            audio = video.audio
            audio.write_audiofile(os.path.join(app.config['UPLOAD_FOLDER'],'audio.wav'))

            parameters = analysis(os.path.join(app.config['UPLOAD_FOLDER'],'audio.wav'))

            response = ai_call(parameters)

            val=1

    return render_template('index.html', val=val, response=response)

if __name__ == '__main__':
    app.run(debug=True)