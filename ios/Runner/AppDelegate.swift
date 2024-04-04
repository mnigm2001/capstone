import UIKit
import Flutter
import AVFoundation

class CameraHandler: NSObject, AVCapturePhotoCaptureDelegate {
    var captureSession: AVCaptureSession?
    var previewLayer: AVCaptureVideoPreviewLayer?
    var photoOutput: AVCapturePhotoOutput?
    var photoCaptureCompletion: ((String?, Error?) -> Void)?
    var cameraPreviewView: UIView?

func startCamera(withView view: UIView) {
    captureSession = AVCaptureSession()
    captureSession?.sessionPreset = .high

    guard let captureDevice = AVCaptureDevice.default(for: .video),
          let input = try? AVCaptureDeviceInput(device: captureDevice) else {
        print("Failed to get the camera device")
        return
    }

    if captureSession?.canAddInput(input) ?? false {
        captureSession?.addInput(input)
    }

    photoOutput = AVCapturePhotoOutput()
    if captureSession?.canAddOutput(photoOutput!) ?? false {
        captureSession?.addOutput(photoOutput!)
    }

    // Adjust the top offset for the cameraPreviewView to leave space for the navigation bar (back arrow)
    let topOffset: CGFloat = 110 // Adjust this value based on your navigation bar's height
    let buttonSpace: CGFloat = 100 // Space for buttons at the bottom
    cameraPreviewView = UIView(frame: CGRect(x: 0, y: topOffset, width: view.bounds.width, height: view.bounds.height - topOffset - buttonSpace))
    if let cameraPreviewView = cameraPreviewView {
        previewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
        previewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
        previewLayer?.frame = cameraPreviewView.bounds

        cameraPreviewView.layer.addSublayer(previewLayer!)
        view.addSubview(cameraPreviewView)

        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(focusAndExposeTap(_:)))
        cameraPreviewView.addGestureRecognizer(tapGesture)
    }

    captureSession?.startRunning()
}


    @objc private func focusAndExposeTap(_ gestureRecognizer: UITapGestureRecognizer) {
        let location = gestureRecognizer.location(in: gestureRecognizer.view)
        guard let previewLayer = self.previewLayer else { return }

        let devicePoint = previewLayer.captureDevicePointConverted(fromLayerPoint: location)
        guard let device = captureSession?.inputs.first(where: { $0 is AVCaptureDeviceInput }) as? AVCaptureDeviceInput else { return }
        focus(with: device.device, focusMode: .autoFocus, exposureMode: .autoExpose, at: devicePoint, monitorSubjectAreaChange: true)
    }

    private func focus(with device: AVCaptureDevice, focusMode: AVCaptureDevice.FocusMode, exposureMode: AVCaptureDevice.ExposureMode, at devicePoint: CGPoint, monitorSubjectAreaChange: Bool) {
        do {
            try device.lockForConfiguration()
            if device.isFocusPointOfInterestSupported && device.isFocusModeSupported(focusMode) {
                device.focusPointOfInterest = devicePoint
                device.focusMode = focusMode
            }
            if device.isExposurePointOfInterestSupported && device.isExposureModeSupported(exposureMode) {
                device.exposurePointOfInterest = devicePoint
                device.exposureMode = exposureMode
            }
            device.isSubjectAreaChangeMonitoringEnabled = monitorSubjectAreaChange
            device.unlockForConfiguration()
        } catch {
            print("Could not lock device for configuration: \(error)")
        }
    }

    func stopCamera() {
        captureSession?.stopRunning()
        previewLayer?.removeFromSuperlayer()
        cameraPreviewView?.removeFromSuperview()
    }

    func captureImage(completion: @escaping (String?, Error?) -> Void) {
        self.photoCaptureCompletion = completion

        guard let photoOutput = self.photoOutput else {
            completion(nil, NSError(domain: "com.meddetect.capstone", code: -1, userInfo: [NSLocalizedDescriptionKey: "Photo output is nil"]))
            return
        }

        let settings = AVCapturePhotoSettings()
        photoOutput.capturePhoto(with: settings, delegate: self)
    }

    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        if let error = error {
            photoCaptureCompletion?(nil, error)
            return
        }

        guard let imageData = photo.fileDataRepresentation() else {
            photoCaptureCompletion?(nil, NSError(domain: "com.meddetect.capstone", code: -2, userInfo: [NSLocalizedDescriptionKey: "Unable to get image data"]))
            return
        }

        let tempDir = NSTemporaryDirectory()
        let tempFile = tempDir + "/capturedPhoto.jpg"
        let tempUrl = URL(fileURLWithPath: tempFile)

        do {
            try imageData.write(to: tempUrl)
            photoCaptureCompletion?(tempUrl.path, nil)
        } catch {
            photoCaptureCompletion?(nil, error)
        }
    }
}

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    private var cameraHandler = CameraHandler()

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        GeneratedPluginRegistrant.register(with: self)

        let controller = window?.rootViewController as! FlutterViewController
        let cameraChannel = FlutterMethodChannel(name: "com.meddetect.capstone/camera", binaryMessenger: controller.binaryMessenger)

        cameraChannel.setMethodCallHandler({
            [weak self, weak controller] (call: FlutterMethodCall, result: @escaping FlutterResult) -> Void in
            guard let self = self, let controller = controller else {
                result(FlutterError(code: "ERROR", message: "Failed to get self or controller", details: nil))
                return
            }

            switch call.method {
            case "openNativeCamera":
                self.cameraHandler.startCamera(withView: controller.view)
                result(nil)
            case "stopNativeCamera":
                self.cameraHandler.stopCamera()
                result(nil)
            case "captureImage":
                self.cameraHandler.captureImage { imagePath, error in
                    if let error = error {
                        result(FlutterError(code: "CAPTURE_ERROR", message: error.localizedDescription, details: nil))
                    } else if let imagePath = imagePath {
                        result(imagePath)
                    } else {
                        result(FlutterError(code: "CAPTURE_ERROR", message: "Failed to capture image", details: nil))
                    }
                }
            default:
                result(FlutterMethodNotImplemented)
            }
        })

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
