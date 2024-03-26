from io import BufferedIOBase
from threading import Condition
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Thread

class StreamingOutput(BufferedIOBase):
	def __init__(self):
		self.frame = None
		self.condition = Condition()

	def write(self, buf):
		with self.condition:
			self.frame = buf
			self.condition.notify_all()

class Camera:
	
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"size": (640, 480)}))
        self.encoder = JpegEncoder()
        self.output3 = StreamingOutput()
        self.output2 = FileOutput(self.output3)
        self.encoder.output = [self.output2]

    def start(self):
        self.camera.start_encoder(self.encoder) 
        self.camera.start()
        self.daemon = Thread(target=self.update_frame, daemon=True, name='update_frame')
        self.daemon.start()
		
    def update_frame(self):
        while True:
            with self.output3.condition:
                self.output3.condition.wait()
                frame = self.output3.frame
                self.frame = (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
    def get_frame_contents(self):
          while True:
                yield self.frame
