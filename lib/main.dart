/* import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/create_account_screen.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:timezone/data/latest.dart' as tz;
import 'package:timezone/timezone.dart' as tz;
import 'package:flutter_native_timezone_updated_gradle/flutter_native_timezone.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await _configureLocalTimeZone();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(MyApp());
}

Future<void> _configureLocalTimeZone() async {
  tz.initializeTimeZones(); // Initialize timezone data
  final String timeZoneName = await FlutterNativeTimezone.getLocalTimezone();
  tz.setLocalLocation(tz.getLocation(timeZoneName));
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Page',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        primaryColor: Color(0xFF0A84FF),
        visualDensity: VisualDensity.adaptivePlatformDensity,
        textSelectionTheme: TextSelectionThemeData(
          selectionHandleColor: Color(0xFF0A84FF),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/createAccount': (context) => CreateAccountScreen(),
      },
    );
  }
}
 */

import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/create_account_screen.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:awesome_notifications/awesome_notifications.dart'; // Ensure this is correctly imported

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  // Initialize awesome_notifications
  AwesomeNotifications().initialize(
      // Ensure you have added a proper app icon in your Android and iOS project
      'resource://mipmap/ic_launcher', // null was replaced with a valid resource
      [
        NotificationChannel(
          channelKey: 'basic_channel', // Same as used in your notification code
          channelName: 'Basic notifications',
          channelDescription: 'Notification channel for basic tests',
          defaultColor: Color(0xFF9D50DD),
          ledColor: Colors.white,
          playSound: true,
          enableVibration: true,
        )
      ],
      // Set to true if you want to debug notifications
      debug: true);

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Login Page',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        primaryColor: Color(0xFF0A84FF),
        visualDensity: VisualDensity.adaptivePlatformDensity,
        textSelectionTheme: TextSelectionThemeData(
          selectionHandleColor: Color(0xFF0A84FF),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/createAccount': (context) => CreateAccountScreen(),
      },
    );
  }
}
