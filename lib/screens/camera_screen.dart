import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'dart:async';

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;

  const CameraScreen({
    Key? key,
    required this.camera,
  }) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  Future<void> _pickImageFromGallery() async {
    try {
      final pickedFile =
          await ImagePicker().pickImage(source: ImageSource.gallery);

      if (pickedFile != null) {
        await Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) =>
                DisplayPictureScreen(imagePath: pickedFile.path),
          ),
        );
      }
    } catch (e) {
      print(e);
    }
  }

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(''),
        backgroundColor: Colors.white, // Assuming you have a white AppBar
        iconTheme: IconThemeData(
          color: Color(0xFF0A84FF), // Set the back arrow color to blue
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: FutureBuilder<void>(
              future: _initializeControllerFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  return CameraPreview(_controller);
                } else {
                  return Center(child: CircularProgressIndicator());
                }
              },
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0), // Adjust the padding as needed
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                FloatingActionButton(
                  heroTag: "cameraButton",
                  onPressed: () async {
                    try {
                      await _initializeControllerFuture;
                      final image = await _controller.takePicture();
                      await Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) =>
                              DisplayPictureScreen(imagePath: image.path),
                        ),
                      );
                    } catch (e) {
                      print(e);
                    }
                  },
                  child: Icon(Icons.camera),
                  backgroundColor: Color(0xFF0A84FF), // Set the color here
                ),
                FloatingActionButton(
                  heroTag: "galleryButton",
                  onPressed: _pickImageFromGallery,
                  child: Icon(Icons.photo_library),
                  backgroundColor: Color(0xFF0A84FF), // Set the color here
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({Key? key, required this.imagePath})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(''),
        backgroundColor: Colors.white, // Assuming you have a white AppBar
        iconTheme: IconThemeData(
          color: Color(0xFF0A84FF), // Set the back arrow color to blue
        ),
      ),
      body: Image.file(File(imagePath)),
    );
  }
}
