import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/create_account_screen.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart'; // This is assuming firebase_options.dart is in the root of the lib directory

void main() async {
  WidgetsFlutterBinding
      .ensureInitialized(); // Required for async main to work correctly before runApp
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions
        .currentPlatform, // This uses the options from your firebase_options.dart
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Page',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        primaryColor: Color(0xFF0A84FF), // Set your primary color here
        visualDensity: VisualDensity.adaptivePlatformDensity,
        textSelectionTheme: TextSelectionThemeData(
          selectionHandleColor:
              Color(0xFF0A84FF), // Set your desired color here
        ),
      ),
      // Define the initial route
      initialRoute: '/',
      // Define the routes table
      routes: {
        '/': (context) => LoginScreen(),
        '/createAccount': (context) => CreateAccountScreen(),
      },
    );
  }
}
