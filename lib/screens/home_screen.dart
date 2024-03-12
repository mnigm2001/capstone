import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'pills_screen.dart';
import 'guest_options_screen.dart';
import 'account_screen.dart'; // Import the AccountScreen
import 'pill_details_screen.dart';

class HomePage extends StatefulWidget {
  String firstName;
  final bool isFirstVisit;

  HomePage({Key? key, required this.firstName, this.isFirstVisit = false})
      : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  User? user = FirebaseAuth.instance.currentUser;

  void _updateName(String newName) {
    setState(() {
      widget.firstName = newName; // Update the firstName
    });
  }

  void _navigateToAccountScreen() async {
    final updatedName = await Navigator.of(context).push<String>(
      MaterialPageRoute(builder: (context) => AccountScreen()),
    );

    if (updatedName != null && updatedName.isNotEmpty) {
      setState(() {
        // Update the name displayed on the HomePage
        // Note: Make sure the firstName field in HomePage is not final
        widget.firstName = updatedName;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    if (widget.isFirstVisit) {
      WidgetsBinding.instance
          .addPostFrameCallback((_) => _showDisclaimerDialog(context));
    }
  }

  void _showDisclaimerDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Disclaimer!"),
          content: Text(
              "Results may not be perfect, contact your physician for serious concerns."),
          actions: <Widget>[
            TextButton(
              child: Text("Understood"),
              style: TextButton.styleFrom(
                primary: Color(0xFF0A84FF), // Blue color for text
              ),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // Use the first name passed to the widget
    String firstName =
        widget.firstName; // Modify this line to use the passed first name

    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Padding(
            padding: EdgeInsets.only(
                top: 16.0, left: 16.0, right: 16.0, bottom: 16.0),
            child: Text(
              'Welcome, $firstName', // Display the passed first name
              style: TextStyle(
                  fontSize: 50,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF0A84FF)),
              textAlign: TextAlign.center,
            ),
          ),
          ButtonBar(
            alignment: MainAxisAlignment.center,
            children: <Widget>[
              ElevatedButton.icon(
                onPressed: () async {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => GuestOptionsScreen(showDisclaimer: false)),
                  );
                },
                icon: Icon(Icons.camera_alt,
                    color: Color(0xFF0A84FF)), // Camera icon for Scan button
                // Add icon for Scan button
                label: Text('Detect', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  primary: Colors.white, // Set the background color to white
                  onPrimary: Color(0xFF0A84FF), // Text color
                ),
              ),
              ElevatedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(MaterialPageRoute(builder: (context) => PillsPage()));
                },
                icon: Icon(Icons.medical_services,
                    color: Color(0xFF0A84FF)), // Add icon for Pills button
                label:
                    Text('Pills', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  primary: Colors.white,
                  onPrimary: Color(0xFF0A84FF),
                ),
              ),
              ElevatedButton.icon(
                onPressed: () async {
                  final updatedName = await Navigator.of(context).push(
                    MaterialPageRoute(builder: (context) => AccountScreen()),
                  );

                  if (updatedName != null && updatedName is String) {
                    setState(() {
                      // Update the name displayed in HomePage
                      widget.firstName = updatedName;
                    });
                  }
                },
                icon: Icon(Icons.account_circle,
                    color: Color(0xFF0A84FF)), // Icon for Account button
                label:
                    Text('Account', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  primary: Colors.white,
                  onPrimary: Color(0xFF0A84FF),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
