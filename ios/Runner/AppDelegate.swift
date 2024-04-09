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
            if call.method == "openNativeCamera" {
                self?.openCamera(rootViewController: controller)
            } else {
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
            flutterResult?("Camera not available")
        }
    }

    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        if let image = info[.originalImage] as? UIImage {
            saveImageTemporarily(image: image) { fileURL in
                self.sendImageToServer(imageURL: fileURL) {
                    DispatchQueue.main.async {
                        picker.dismiss(animated: true) {
                            // The response handling will be in sendImageToServer
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
        guard let url = URL(string: "http://172.20.10.2:8000/pill_vault/api/scan-image/") else {
            print("Invalid URL")
            DispatchQueue.main.async {
                self.flutterResult?("Invalid URL")
            }
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
            body.append("Content-Disposition: form-data; name=\"image1\"; filename=\"\(filename)\"\r\n")
            body.append("Content-Type: image/jpeg\r\n\r\n")
            body.append(imageData)
            body.append("\r\n")
        }

        body.append("--\(boundary)--\r\n")
        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self else {
                completion()
                return
            }

            if let error = error {
                print("Network error: \(error)")
                DispatchQueue.main.async {
                    self.flutterResult?("Network error: \(error)")
                }
                completion()
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                print("HTTP Response Code: \(httpResponse.statusCode)")
                if httpResponse.statusCode != 200 {
                    DispatchQueue.main.async {
                        self.flutterResult?("HTTP Error: \(httpResponse.statusCode)")
                    }
                    completion()
                    return
                }
            }

if let data = data {
    let responseString = String(data: data, encoding: .utf8) ?? "Invalid response data"
    print("Raw Response String: \(responseString)")

    // Debug: Print the data as bytes to inspect any hidden characters
    print("Data bytes: \(data as NSData)")

    do {
        // Using .allowFragments to handle cases where the JSON might not start with an array or object
        if let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as? [String: Any] {
            print("JSON Response: \(json)")
            DispatchQueue.main.async {
                self.flutterResult?(json)
            }
        } else {
            print("Invalid JSON format")
            DispatchQueue.main.async {
                self.flutterResult?("Invalid JSON format")
            }
        }
    } catch {
        print("JSON parsing error: \(error)")
        DispatchQueue.main.async {
            self.flutterResult?("JSON parsing error: \(error)")
        }
    }
} else {
    print("No data received")
    DispatchQueue.main.async {
        self.flutterResult?("No data received")
    }
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
