import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:capstone_application/globals.dart';
import 'home_screen.dart';

class CreateAccountScreen extends StatefulWidget {
  @override
  _CreateAccountScreenState createState() => _CreateAccountScreenState();
}

class _CreateAccountScreenState extends State<CreateAccountScreen> {
  final _formKey = GlobalKey<FormState>(); // Add this line
  final TextEditingController _firstNameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController =
      TextEditingController();
  final TextEditingController _ageController = TextEditingController();
  bool _isMale = false;
  bool _isFemale = false;

  void _registerAccount() async {
    try {
      UserCredential userCredential = await auth.createUserWithEmailAndPassword(
        email: _emailController.text,
        password: _passwordController.text,
      );

      if (userCredential.user != null) {
        String firstName = _firstNameController.text.split(' ')[0];
        await userCredential.user!.updateDisplayName(firstName);

        // Push the HomePage and remove all previous routes
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(
              builder: (context) =>
                  HomePage(firstName: firstName, isFirstVisit: true)),
          (Route<dynamic> route) =>
              false, // This will remove all routes beneath
        );
      }
    } on FirebaseAuthException catch (e) {
      // Handle errors
      if (e.code == 'weak-password') {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('The password provided is too weak.'),
            backgroundColor: Colors.redAccent,
          ),
        );
      } else if (e.code == 'email-already-in-use') {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('The account already exists for that email.'),
            backgroundColor: Colors.redAccent,
          ),
        );
      }
    } catch (e) {
      print(e); // Handle any other exceptions
    }
  }

  void _tryCreateAccount() {
    // Check for empty fields or unselected gender first
    if (_firstNameController.text.isEmpty ||
        _emailController.text.isEmpty ||
        _passwordController.text.isEmpty ||
        _confirmPasswordController.text.isEmpty ||
        _ageController.text.isEmpty ||
        (!_isMale && !_isFemale)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please fill out all the information.'),
          backgroundColor: Colors.redAccent,
        ),
      );
      return; // Stop further execution if fields are empty
    }

    // Check if the password is at least 6 characters long
    if (_passwordController.text.length < 6) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Password must be at least 6 characters.'),
          backgroundColor: Colors.redAccent,
        ),
      );
      return; // Stop further execution if password is too short
    }

    // Validate email format
    if (!_isEmailValid(_emailController.text)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please enter a valid email address.'),
          backgroundColor: Colors.redAccent,
        ),
      );
      return; // Stop further execution if email is invalid
    }

    // Check if passwords match
    if (_passwordController.text != _confirmPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('The passwords do not match.'),
          backgroundColor: Colors.redAccent,
        ),
      );
      return; // Stop further execution if passwords don't match
    }

    // All validations passed, proceed with account creation
    _registerAccount();
  }

  bool _isEmailValid(String email) {
    // Regular expression for email validation
    final RegExp emailRegexp =
        RegExp(r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]+');
    return emailRegexp.hasMatch(email);
  }

  @override
  void dispose() {
    _firstNameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _ageController.dispose();
    super.dispose();
  }

  void _handleGenderChange(String gender) {
    setState(() {
      _isMale = gender == 'M';
      _isFemale = gender == 'F';
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text(''),
          backgroundColor: Colors.white,
        ),
        body: SafeArea(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Form(
                key: _formKey,
                child: Column(
                  children: [
                    SizedBox(height: 20),
                    TextField(
                      controller: _firstNameController,
                      decoration: InputDecoration(
                        labelText: 'First Name',
                        labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                      ),
                      style: TextStyle(color: Color(0xFF0A84FF)),
                      textCapitalization: TextCapitalization
                          .words, // Enable auto capitalization

                      cursorColor:
                          Color(0xFF0A84FF), // Set the cursor color here
                    ),
                    SizedBox(height: 10),
                    TextFormField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        labelText: 'Email',
                        labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                      ),
                      style: TextStyle(color: Color(0xFF0A84FF)),
                      cursorColor:
                          Color(0xFF0A84FF), // Set the cursor color here

                      keyboardType: TextInputType.emailAddress,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your email';
                        }
                        String pattern =
                            r'^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]+';
                        if (!RegExp(pattern).hasMatch(value)) {
                          return 'Enter a valid email';
                        }
                        return null;
                      },
                    ),
                    SizedBox(height: 10),
                    TextField(
                      controller: _passwordController,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                      ),
                      obscureText: true,
                      style: TextStyle(color: Color(0xFF0A84FF)),
                      cursorColor:
                          Color(0xFF0A84FF), // Set the cursor color here
                    ),
                    SizedBox(height: 10),
                    TextField(
                      controller: _confirmPasswordController,
                      decoration: InputDecoration(
                        labelText: 'Confirm Password',
                        labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                      ),
                      obscureText: true,
                      style: TextStyle(color: Color(0xFF0A84FF)),
                      cursorColor:
                          Color(0xFF0A84FF), // Set the cursor color here
                    ),
                    SizedBox(height: 10),
                    TextField(
                      controller: _ageController,
                      decoration: InputDecoration(
                        labelText: 'Age',
                        labelStyle: TextStyle(color: Color(0xFF0A84FF)),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: Color(0xFF0A84FF)),
                        ),
                      ),
                      style: TextStyle(color: Color(0xFF0A84FF)),
                      cursorColor:
                          Color(0xFF0A84FF), // Set the cursor color here

                      keyboardType: TextInputType.number,
                    ),
                    SizedBox(height: 10),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Text(
                          'Gender:',
                          style:
                              TextStyle(color: Color(0xFF0A84FF), fontSize: 16),
                        ),
                        SizedBox(width: 1),
                        Theme(
                          data: ThemeData(
                              unselectedWidgetColor: Color(0xFF0A84FF)),
                          child: Checkbox(
                            value: _isMale,
                            onChanged: (bool? newValue) {
                              _handleGenderChange('M');
                            },
                            activeColor: Color(0xFF0A84FF),
                            checkColor: Colors.white,
                          ),
                        ),
                        Text(
                          'M',
                          style: TextStyle(color: Color(0xFF0A84FF)),
                        ),
                        Theme(
                          data: ThemeData(
                              unselectedWidgetColor: Color(0xFF0A84FF)),
                          child: Checkbox(
                            value: _isFemale,
                            onChanged: (bool? newValue) {
                              _handleGenderChange('F');
                            },
                            activeColor: Color(0xFF0A84FF),
                            checkColor: Colors.white,
                          ),
                        ),
                        Text(
                          'F',
                          style: TextStyle(color: Color(0xFF0A84FF)),
                        ),
                      ],
                    ),
                    SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: _tryCreateAccount,
                      child: Text('Create Account'),
                      style: ElevatedButton.styleFrom(
                        primary: Color(0xFF0A84FF),
                        onPrimary: Colors.white,
                        textStyle: TextStyle(fontSize: 16),
                        padding:
                            EdgeInsets.symmetric(vertical: 15, horizontal: 15),
                      ),
                    ),
                    SizedBox(height: 1),
                    TextButton(
                      onPressed: () {
                        Navigator.pop(context);
                      },
                      child: Text('Cancel',
                          style: TextStyle(
                              color: Color(0xFF0A84FF), fontSize: 14.0)),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
