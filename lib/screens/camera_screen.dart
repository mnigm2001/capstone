import 'package:flutter/material.dart';
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
    _openNativeCamera();
  }

  Future<void> _openNativeCamera() async {
    try {
      final result = await platform.invokeMethod('openNativeCamera');
      if (result == null) {
        // Assuming the method will return null when the camera is closed
        Navigator.of(context).pop();
      }
    } catch (e) {
      print('Failed to open native camera: $e');
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
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: Center(
        child: Text('Opening camera...'),
      ),
    );
  }
}
