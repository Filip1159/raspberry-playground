from flask import Flask, Response, render_template
from Camera import Camera

app = Flask(__name__)

camera = Camera()
camera.start()

@app.route('/greet/<text>')
def greet(text):
    f = open("greetings.txt", "a")
    f.write(text + '\n')
    f.close()
    return ''

@app.route('/')
def index():
    return render_template('greet.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera.get_frame_contents(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True, host='0.0.0.0')
