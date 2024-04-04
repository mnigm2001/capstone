import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    var window: UIWindow?
    var imagePicker: UIImagePickerController?

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        GeneratedPluginRegistrant.register(with: self)
        
        let controller = window?.rootViewController as! FlutterViewController
        let cameraChannel = FlutterMethodChannel(name: "com.meddetect.capstone/camera", binaryMessenger: controller.binaryMessenger)

        cameraChannel.setMethodCallHandler { [weak self] (call, result) in
            if call.method == "openNativeCamera" {
                self?.openCamera()
                result(nil)
            } else if call.method == "stopNativeCamera" {
                self?.imagePicker?.dismiss(animated: true, completion: nil)
                result(nil)
            }
        }

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    private func openCamera() {
        if UIImagePickerController.isSourceTypeAvailable(.camera) {
            imagePicker = UIImagePickerController()
            imagePicker?.delegate = self
            imagePicker?.sourceType = .camera

            if let picker = imagePicker {
                window?.rootViewController?.present(picker, animated: true, completion: nil)
            }
        } else {
            print("Camera not available")
        }
    }

    // UIImagePickerControllerDelegate methods
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        // Handle the image captured here if needed
        picker.dismiss(animated: true, completion: nil)
    }

    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
    }
}
