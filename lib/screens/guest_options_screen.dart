import 'package:flutter/material.dart';
import 'camera_screen.dart';
import 'package:camera/camera.dart';

class GuestOptionsScreen extends StatefulWidget {
  final bool showDisclaimer;

  GuestOptionsScreen({Key? key, this.showDisclaimer = true}) : super(key: key);

  @override
  _GuestOptionsScreenState createState() => _GuestOptionsScreenState();
}

class _GuestOptionsScreenState extends State<GuestOptionsScreen> {
  final TextEditingController _colorController = TextEditingController();
  final TextEditingController _imprint1Controller = TextEditingController();
  final TextEditingController _imprint2Controller = TextEditingController();
  String? _selectedShape;
  String? _selectedColor;
  final List<String> _colors = [
    'White',
    'Black',
    'Brown',
    'Red',
    'Blue',
    'Green',
    'Purple'
  ];
  final List<String> _shapes = ['Round', 'Oblong', 'Oval'];

  final TextStyle commonTextStyle = TextStyle(color: Color(0xFF0A84FF), fontSize: 20);
  final EdgeInsets commonPadding = EdgeInsets.symmetric(vertical: 15);

  @override
  void initState() {
    super.initState();
    if (widget.showDisclaimer) {
      WidgetsBinding.instance.addPostFrameCallback((_) => _showDisclaimerDialog(context));
    }
  }

  void _showDisclaimerDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      barrierColor: Colors.black.withOpacity(0.75),
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Disclaimer!"),
          content: Text("Results may not be perfect, contact your physician for serious concerns. Do you wish to proceed?"),
          actions: <Widget>[
            TextButton(
              child: Text("Yes"),
              onPressed: () {
                Navigator.of(context).pop(); // Dismiss the dialog
              },
              style: TextButton.styleFrom(
                foregroundColor: Color(0xFF0A84FF), // Blue color for text
              ),
            ),
            TextButton(
              child: Text("No"),
              onPressed: () {
                Navigator.of(context).popUntil((route) => route.isFirst); // Go back to the login page
              },
              style: TextButton.styleFrom(
                foregroundColor: Color(0xFF0A84FF), // Blue color for text
              ),
            ),
          ],
        );
      },
    );
  }

  void _performSearch() {
    if (_selectedShape == null ||
        _selectedColor == null ||
        _imprint1Controller.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please fill in all required fields to search.'),
          backgroundColor: Colors.redAccent,
        ),
      );
    } else {
      print(
          'Searching for shape: $_selectedShape, color: ${_colorController.text}, imprint 1: ${_imprint1Controller.text}, imprint 2: ${_imprint2Controller.text}');
      // Add search logic here
    }
  }

  Widget _buildShapeDropdown() {
    // Define a map of shape names to their image paths
    Map<String, String> shapeImages = {
      'Round': 'assets/images/round.png',
      'Oblong': 'assets/images/oblong.png',
      'Oval': 'assets/images/oval.png',
    };
    return DropdownButtonFormField<String>(
      value: _selectedShape,
      decoration: InputDecoration(
        labelText: 'Shape',
        labelStyle: TextStyle(
          color: Color(0xFF0A84FF),
          fontSize: 20,
        ), // Set the color here
        border: OutlineInputBorder(),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
      ),
      onChanged: (String? newValue) {
        setState(() {
          _selectedShape = newValue;
        });
      },
      items: shapeImages.entries.map<DropdownMenuItem<String>>((entry) {
        return DropdownMenuItem<String>(
          value: entry.key,
          child: Row(
            children: <Widget>[
              Image.asset(
                entry.value,
                width: 30, // Adjust the size as needed
                height: 30,
              ),
              SizedBox(width: 8), // Spacing between image and text
              Text(entry.key, style: TextStyle(color: Color(0xFF0A84FF))),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildColorDropdown() {
    Map<String, String> colorImages = {
      'White': 'assets/images/white.png',
      'Black': 'assets/images/black.png',
      'Brown': 'assets/images/brown.png',
      'Red': 'assets/images/red.png',
      'Blue': 'assets/images/blue.png',
      'Green': 'assets/images/green.png',
      'Purple': 'assets/images/purple.png',
    };
    return DropdownButtonFormField<String>(
      value: _selectedColor,
      decoration: InputDecoration(
        labelText: 'Color',
        labelStyle: TextStyle(
          color: Color(0xFF0A84FF),
          fontSize: 20,
        ),
        border: OutlineInputBorder(),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
      ),
      onChanged: (String? newValue) {
        setState(() {
          _selectedColor = newValue;
        });
      },
      items: colorImages.entries.map<DropdownMenuItem<String>>((entry) {
        return DropdownMenuItem<String>(
          value: entry.key,
          child: Row(
            children: <Widget>[
              Image.asset(
                entry.value,
                width: 30,
                height: 30,
              ),
              SizedBox(width: 8),
              Text(entry.key, style: TextStyle(color: Color(0xFF0A84FF))),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildInputField(String label, TextEditingController controller,
      {bool isOptional = false}) {
    return TextField(
      controller: controller,
      decoration: InputDecoration(
        labelText: isOptional ? '$label (Optional)' : label,
        labelStyle: commonTextStyle,
        border: const OutlineInputBorder(),
        enabledBorder: const OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
        focusedBorder: const OutlineInputBorder(
          borderSide: BorderSide(color: Color(0xFF0A84FF)),
        ),
      ),
      style: const TextStyle(color: Color(0xFF0A84FF), fontSize: 20),
      cursorColor: Color(0xFF0A84FF), // Set the cursor color here
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(''),
        backgroundColor: Colors.white,
        iconTheme: const IconThemeData(color: Color(0xFF0A84FF)),
      ),
      body: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: () {
          FocusScope.of(context).unfocus();
        },
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20.0, 100.0, 20.0, 20.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () async {
                    // Since you're using native camera functionality, you no longer need to pass the camera object
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => CameraScreen(),
                      ),
                    );
                  },
                  child: const Text('Scan'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF0A84FF),
                    foregroundColor: Colors.white,
                    textStyle: commonTextStyle,
                    padding: commonPadding,
                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  children: <Widget>[
                    Expanded(
                      child: Divider(color: Color(0xFF0A84FF), height: 36),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8.0),
                      child: Text("or", style: commonTextStyle),
                    ),
                    Expanded(
                      child: Divider(color: Color(0xFF0A84FF), height: 36),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                _buildShapeDropdown(),
                const SizedBox(height: 10),
                _buildColorDropdown(),
                const SizedBox(height: 10),
                _buildInputField(
                  'Imprint 1',
                  _imprint1Controller,
                ),
                const SizedBox(height: 10),
                _buildInputField('Imprint 2', _imprint2Controller,
                    isOptional: true),
                const SizedBox(height: 20),
                Center(
                  child: SizedBox(
                    width: 125,
                    child: ElevatedButton(
                      onPressed: _performSearch,
                      child: const Text('Search'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF0A84FF),
                        foregroundColor: Colors.white,
                        textStyle: commonTextStyle,
                        padding: commonPadding,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
