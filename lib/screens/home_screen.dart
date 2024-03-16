import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'pills_screen.dart';
import 'guest_options_screen.dart';
import 'account_screen.dart'; // Import the AccountScreen

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
    double buttonWidth =
        200.0; // Arbitrary width to fit the "Reminders" text and icon

    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Welcome, ${widget.firstName}',
              style: TextStyle(
                  fontSize: 50,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF0A84FF)),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 30),
            SizedBox(
              width: buttonWidth,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) =>
                            GuestOptionsScreen(showDisclaimer: false)),
                  );
                },
                icon: Icon(Icons.camera_alt, color: Color(0xFF0A84FF)),
                label:
                    Text('Detect', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  backgroundColor:
                      Colors.white, // Set the background color to white
                  onPrimary: Color(0xFF0A84FF), // Text color
                ),
              ),
            ),
            SizedBox(height: 10),
            SizedBox(
              width: buttonWidth,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => PillsPage()));
                },
                icon: Icon(Icons.medical_services, color: Color(0xFF0A84FF)),
                label:
                    Text('Pills', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  onPrimary: Color(0xFF0A84FF),
                ),
              ),
            ),
            SizedBox(height: 10),
            SizedBox(
              width: buttonWidth,
              child: ElevatedButton.icon(
                onPressed: () {
                  // Navigator.push(
                  //   context,
                  //   MaterialPageRoute(builder: (context) => RemindersPage()),
                  // );
                },
                icon: Icon(Icons.list, color: Color(0xFF0A84FF)),
                label: Text('Reminders',
                    style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  onPrimary: Color(0xFF0A84FF),
                ),
              ),
            ),
            SizedBox(height: 10),
            SizedBox(
              width: buttonWidth,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => AccountScreen()),
                  );
                },
                icon: Icon(Icons.account_circle, color: Color(0xFF0A84FF)),
                label:
                    Text('Account', style: TextStyle(color: Color(0xFF0A84FF))),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  onPrimary: Color(0xFF0A84FF),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
