import UIKit
import Flutter
import AVFoundation

class CameraHandler: NSObject {
    var captureSession: AVCaptureSession?
    var previewLayer: AVCaptureVideoPreviewLayer?

    func startCamera(withView view: UIView) {
        captureSession = AVCaptureSession()
        captureSession?.sessionPreset = .high

        guard let captureDevice = AVCaptureDevice.default(for: .video) else {
            print("Failed to get the camera device")
            return
        }

        do {
            let input = try AVCaptureDeviceInput(device: captureDevice)
            captureSession?.addInput(input)

            previewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            previewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill

            let appBarHeight: CGFloat = 56
            let buttonSpace: CGFloat = 100
            let yOffset: CGFloat = appBarHeight * 2
            let adjustedHeight = view.layer.bounds.height - yOffset - buttonSpace

            previewLayer?.frame = CGRect(x: 0, y: yOffset, width: view.layer.bounds.width, height: adjustedHeight)
            view.layer.addSublayer(previewLayer!)

            captureSession?.startRunning()
        } catch {
            print("Error starting camera: \(error)")
        }
    }

    func stopCamera() {
        captureSession?.stopRunning()
        previewLayer?.removeFromSuperlayer()
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
        let cameraChannel = FlutterMethodChannel(name: "com.meddetect.capstone/camera",
                                                 binaryMessenger: controller.binaryMessenger)

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
            default:
                result(FlutterMethodNotImplemented)
            }
        })

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
