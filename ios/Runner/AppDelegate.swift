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
            saveImageTemporarily(image: image) { fileURL in
                self.sendImageToServer(imageURL: fileURL) {
                    DispatchQueue.main.async {
                        picker.dismiss(animated: true) {
                            self.flutterResult?("Image capturing completed")
                        }
                    }
                }
            }
        }
    }

    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true) {
            self.flutterResult?(nil)
        }
    }

    private func saveImageTemporarily(image: UIImage, completion: @escaping (URL) -> Void) {
        let fileManager = FileManager.default
        if let data = image.jpegData(compressionQuality: 1.0) {
            do {
                let tempDirectory = fileManager.temporaryDirectory
                let fileName = UUID().uuidString + ".jpg"
                let fileURL = tempDirectory.appendingPathComponent(fileName)
                try data.write(to: fileURL)
                print("Image saved at \(fileURL.path)")
                completion(fileURL)
            } catch {
                print("Error saving image: \(error)")
            }
        }
    }

    private func sendImageToServer(imageURL: URL, completion: @escaping () -> Void) {
        guard let url = URL(string: "http://10.0.0.242:8000/pill_vault/api/scan-image/") else {
            print("Invalid URL")
            completion()
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()
        let filename = imageURL.lastPathComponent
        if let imageData = try? Data(contentsOf: imageURL) {
            body.append("--\(boundary)\r\n")
            body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n")
            body.append("Content-Type: image/jpeg\r\n\r\n")
            body.append(imageData)
            body.append("\r\n")
        }

        body.append("--\(boundary)--\r\n")
        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending image: \(error)")
            } else if let response = response as? HTTPURLResponse, response.statusCode == 200 {
                print("Image sent successfully")
            } else {
                print("Error sending image. Response: \(String(describing: response))")
            }
            completion()
        }

        task.resume()
    }
}

extension Data {
    mutating func append(_ string: String) {
        if let data = string.data(using: .utf8) {
            append(data)
        }
    }
}
