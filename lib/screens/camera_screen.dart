import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:async';
import 'package:flutter/services.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({Key? key}) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  static const platform = MethodChannel('com.meddetect.capstone/camera');

  @override
  void initState() {
    super.initState();
    _openNativeCamera();  // Open the camera preview immediately
  }

  Future<void> _openNativeCamera() async {
    try {
      await platform.invokeMethod('openNativeCamera');
    } catch (e) {
      print('Failed to open native camera: $e');
    }
  }

  Future<void> _captureImage() async {
    try {
      final result = await platform.invokeMethod('captureImage');
      print('Image captured: $result');
    } catch (e) {
      print('Failed to capture image: $e');
    }
  }

  Future<void> _pickImageFromGallery() async {
    try {
      final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);
      if (pickedFile != null) {
        print('Picked image path: ${pickedFile.path}');
      }
    } catch (e) {
      print('Failed to pick image from gallery: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(color: Color(0xFF0A84FF)),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () async {
            await platform.invokeMethod('stopNativeCamera');
            Navigator.of(context).pop();
          },
        ),
      ),
      body: Stack(
        children: [
          Positioned.fill(
            child: Container(
              color: Colors.white, // Placeholder for native camera preview
            ),
          ),
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              color: Colors.white,
              padding: const EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 30.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  FloatingActionButton(
                    heroTag: "captureButton",
                    onPressed: _captureImage,
                    child: Icon(Icons.camera),
                    backgroundColor: Color(0xFF0A84FF),
                  ),
                  FloatingActionButton(
                    heroTag: "galleryButton",
                    onPressed: _pickImageFromGallery,
                    child: Icon(Icons.photo_library),
                    backgroundColor: Color(0xFF0A84FF),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
