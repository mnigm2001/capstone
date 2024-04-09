import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';

import 'pill.dart';
import 'pills_screen.dart';

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
    print('Native camera result: $result'); // Debugging line
    if (result != null) {
      final pillData = Map<String, dynamic>.from(result as Map);
      print('Pill data: $pillData'); // Debugging line
      if (pillData['Pill Detected'] == true) {
        try {
          // Ensure the 'Pill' data is also a Map<String, dynamic>
          Map<String, dynamic> pillMap = Map<String, dynamic>.from(pillData['Pill'] as Map);
          Pill detectedPill = Pill.fromMap(pillMap);
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => PillsPage(detectedPill: detectedPill),
            ),
          );
        } catch (e) {
          print('Error parsing pill data: $e');
          Navigator.of(context).pop();
        }
      } else {
        Navigator.of(context).pop();
      }
    } else {
      Navigator.of(context).pop();
    }
  } catch (e) {
    print('Failed to open native camera: $e');
    Navigator.of(context).pop();
  }
}


  Future<void> savePillToFile(Pill pill) async {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/user_pills.json');

    List<Pill> existingPills = await _readPillsFromFile();

    existingPills.add(pill);

    String jsonString = jsonEncode(existingPills.map((e) => e.toMap()).toList());

    await file.writeAsString(jsonString);
  }

  Future<List<Pill>> _readPillsFromFile() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final file = File('${directory.path}/user_pills.json');

      if (await file.exists()) {
        String jsonString = await file.readAsString();
        List<dynamic> jsonData = jsonDecode(jsonString);
        return jsonData.map((e) => Pill.fromMap(e)).toList();
      } else {
        return [];
      }
    } catch (e) {
      print('Error reading pills from file: $e');
      return [];
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
      body: Center(child: Text('Opening camera...')),
    );
  }
}
