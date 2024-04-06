import 'package:flutter/material.dart';
import 'guest_options_screen.dart';
import 'home_screen.dart';
import 'package:firebase_auth/firebase_auth.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final FirebaseAuth _auth = FirebaseAuth.instance; // Firebase Auth instance

  void _login() async {
    try {
      UserCredential userCredential = await _auth.signInWithEmailAndPassword(
        email: _emailController.text.trim(),
        password: _passwordController.text.trim(),
      );

      if (userCredential.user != null) {
        String firstName =
            userCredential.user!.displayName?.split(' ')?.first ?? 'User';
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
              builder: (context) => HomePage(firstName: firstName)),
        );
      }
    } on FirebaseAuthException catch (e) {
      // Handle errors
      final snackBar =
          SnackBar(content: Text(e.message ?? 'An error occurred'));
      ScaffoldMessenger.of(context).showSnackBar(snackBar);
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:
          Colors.white, // Matching the background color of the logo
      body: GestureDetector(
        onTap: () {
          // Dismiss the keyboard when the user taps outside of the text fields
          FocusScope.of(context).requestFocus(FocusNode());
        },
        child: SafeArea(
          child: LayoutBuilder(
            builder:
                (BuildContext context, BoxConstraints viewportConstraints) {
              return SingleChildScrollView(
                child: ConstrainedBox(
                  constraints: BoxConstraints(
                    minHeight: viewportConstraints.maxHeight,
                  ),
                  child: IntrinsicHeight(
                    child: Column(
                      children: <Widget>[
                        Padding(
                          padding: EdgeInsets.only(top: 75),
                          child: Image.asset(
                            'assets/images/blue_and_white.png',
                            width: 200,
                            height: 200,
                          ),
                        ),
                        SizedBox(height: 30),
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 10),
                          child: TextField(
                            controller: _emailController,
                            keyboardType: TextInputType.emailAddress,
                            decoration: InputDecoration(
                              labelText: 'Email',
                              labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                              border: OutlineInputBorder(),
                              enabledBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(color: Color(0xFF0A84FF)),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(color: Color(0xFF0A84FF)),
                              ),
                            ),
                            style: TextStyle(color: Color(0xFF0A84FF)),
                            cursorColor:
                                Color(0xFF0A84FF), // Set the cursor color here
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 10),
                          child: TextField(
                            controller: _passwordController,
                            obscureText: true,
                            decoration: InputDecoration(
                              labelText: 'Password',
                              labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                              border: OutlineInputBorder(),
                              enabledBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(color: Color(0xFF0A84FF)),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(color: Color(0xFF0A84FF)),
                              ),
                            ),
                            style: TextStyle(color: Color(0xFF0A84FF)),
                            cursorColor:
                                Color(0xFF0A84FF), // Set the cursor color here
                          ),
                        ),
                        ElevatedButton(
                          onPressed: _login,
                          child: Text('Login'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Color(0xFF0A84FF),
                            foregroundColor: Colors.white,
                          ),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/createAccount');
                          },
                          child: Text(
                            'Create an Account',
                            style: TextStyle(color: Color(0xFF0A84FF)),
                          ),
                        ),
                        Spacer(),
                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => GuestOptionsScreen()),
                            );
                          },
                          child: Text(
                            'Continue as Guest',
                            style: TextStyle(color: Color(0xFF0A84FF)),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}








 

/* 

second pop up version, before loading into guest user page

import 'package:flutter/material.dart';
import 'guest_options_screen.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Function to show the pop-up dialog
    void _showGuestWarning(BuildContext context) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text("Disclaimer!"),
            content: Text(
                "Results may not be perfect, contact your physician for serious concerns."),
            actions: <Widget>[
              TextButton(
                child: Text('Cancel'),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
              TextButton(
                child: Text('Continue'),
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => GuestOptionsScreen()),
                  );
                },
              ),
            ],
          );
        },
      );
    }

    return Scaffold(
      backgroundColor:
          Colors.black, // Matching the black background of the logo
      body: GestureDetector(
        onTap: () {
          // Dismiss the keyboard when the user taps outside of the text fields
          FocusScope.of(context).requestFocus(FocusNode());
        },
        child: SafeArea(
          child: LayoutBuilder(
            builder:
                (BuildContext context, BoxConstraints viewportConstraints) {
              return SingleChildScrollView(
                child: ConstrainedBox(
                  constraints: BoxConstraints(
                    minHeight: viewportConstraints
                        .maxHeight, // Min height equal to the viewport height
                  ),
                  child: IntrinsicHeight(
                    child: Column(
                      children: <Widget>[
                        Padding(
                          padding: EdgeInsets.only(top: 110), // Top padding
                          child: Image.asset(
                            'assets/images/capstone_logo.png',
                            width: 200,
                            height: 200,
                          ),
                        ),
                        SizedBox(
                            height: 50), // Space between logo and input fields

                        // Email Input Field
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 10),
                          child: TextField(
                            keyboardType: TextInputType.emailAddress,
                            decoration: InputDecoration(
                              labelText: 'Email',
                              labelStyle: TextStyle(
                                  color: Colors.amber), // Gold color for text
                              border: OutlineInputBorder(),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color:
                                        Colors.amber), // Gold color for border
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: Colors
                                        .amber), // Gold color when focused
                              ),
                            ),
                            style: TextStyle(
                                color: Colors
                                    .white), // Text color inside the field
                          ),
                        ),

                        // Password Input Field
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 10),
                          child: TextField(
                            obscureText: true,
                            decoration: InputDecoration(
                              labelText: 'Password',
                              labelStyle: TextStyle(
                                  color: Colors.amber), // Gold color for text
                              border: OutlineInputBorder(),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color:
                                        Colors.amber), // Gold color for border
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: Colors
                                        .amber), // Gold color when focused
                              ),
                            ),
                            style: TextStyle(
                                color: Colors
                                    .white), // Text color inside the field
                          ),
                        ),

                        // Button to Create an Account
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/createAccount');
                          },
                          child: Text('Create an Account',
                              style: TextStyle(
                                  color: Colors.amber)), // Gold color for text
                        ),

                        Spacer(), // Use Spacer to push the next widget to the bottom

                        // Button to Continue as Guest
                        TextButton(
                          onPressed: () {
                            _showGuestWarning(context);
                          },
                          child: Text('Continue as Guest',
                              style: TextStyle(
                                  color: Colors.amber)), // Gold color for text
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
 */