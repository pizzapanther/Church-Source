package webcam {
	import flash.display.BitmapData;	   
	import flash.display.Bitmap;
	import flash.media.Camera;
	import flash.media.Video;
	import flash.utils.ByteArray;
	import mx.containers.Panel;
	import mx.controls.Text;
	import mx.core.UIComponent;   
	import mx.graphics.codec.JPEGEncoder;
	import mx.utils.Base64Encoder;

	public class Webcam extends Panel {
		private var videoHolder:UIComponent = new UIComponent();
		private var video:Video;
		private var photoBitmap:Bitmap;
		private var photo:BitmapData = new BitmapData(320, 240, true);

		public function Webcam(){
			super();
			insertWebcamVideo();
		}

		private function insertWebcamVideo():void {
			try {
				var camera:Camera = Camera.getCamera();
				camera.setMode(320,240,15);
				video = new Video(camera.width, camera.height);
				video.attachCamera(camera);
				videoHolder.addChild(video);
			}
			catch( error:TypeError ){
				var message:Text = new Text();
				message.text = 'You do not have a webcam.';
				message.width = 320;
				message.height = 240;
				videoHolder.addChild(message);
			}
			addChild(videoHolder);
		}

		public function takePhoto():void {
			// Take snapshot
			try {
				photo.draw(video);
			} catch( error:ArgumentError ) {
				photo.noise(Math.random());
			}

			photoBitmap = new Bitmap(photo);
			try {
				videoHolder.removeChild(video);
			} catch( error:TypeError ) {
				// do nothing
			}

			videoHolder.addChild(photoBitmap);
		}

		public function retakePhoto():void {
			videoHolder.removeChild(photoBitmap);
			try {
				videoHolder.addChild(video);
			} catch( error:TypeError ) {
				// do nothing
			}
		}

		public function getBase64():String {
			var jcdr:JPEGEncoder = new JPEGEncoder(75.0);
			var jpg:ByteArray = jcdr.encode(photo);

			// base64 encode image
			var encoder:Base64Encoder = new Base64Encoder();
			encoder.encodeBytes(jpg);

			return encoder.flush();
		}
	}
}
