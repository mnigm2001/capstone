import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    var imagePicker: UIImagePickerController?
    var flutterResult: FlutterResult?

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        GeneratedPluginRegistrant.register(with: self)
        
        let controller = window?.rootViewController as! FlutterViewController
        let cameraChannel = FlutterMethodChannel(name: "com.meddetect.capstone/camera", binaryMessenger: controller.binaryMessenger)

        cameraChannel.setMethodCallHandler { [weak self] (call, result) in
            self?.flutterResult = result
            switch call.method {
            case "openNativeCamera":
                self?.openCamera(rootViewController: controller)
            default:
                result(FlutterMethodNotImplemented)
            }
        }

        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    private func openCamera(rootViewController: UIViewController) {
        if UIImagePickerController.isSourceTypeAvailable(.camera) {
            imagePicker = UIImagePickerController()
            imagePicker?.delegate = self
            imagePicker?.sourceType = .camera
            rootViewController.present(imagePicker!, animated: true, completion: nil)
        } else {
            print("Camera not available")
            flutterResult?("Camera not available")
        }
    }

    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        if let image = info[.originalImage] as? UIImage {
            saveImageTemporarily(image: image)
        }
        picker.dismiss(animated: true) {
            self.flutterResult?(nil)
        }
    }

    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true) {
            self.flutterResult?(nil)
        }
    }

    private func saveImageTemporarily(image: UIImage) {
        let fileManager = FileManager.default
        if let data = image.jpegData(compressionQuality: 1.0) {
            do {
                let tempDirectory = fileManager.temporaryDirectory
                let fileName = UUID().uuidString + ".jpg"
                let fileURL = tempDirectory.appendingPathComponent(fileName)
                try data.write(to: fileURL)
                print("Image saved at \(fileURL.path)")
                // Store this path if needed to access the image later
            } catch {
                print("Error saving image: \(error)")
            }
        }
    }
}
