import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AccountScreen extends StatefulWidget {
  @override
  _AccountScreenState createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen> {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _newPasswordController = TextEditingController();
  final TextEditingController _confirmNewPasswordController =
      TextEditingController();

  @override
  void initState() {
    super.initState();
    User? user = _auth.currentUser;
    _nameController.text = user?.displayName ?? '';
  }

  @override
  void dispose() {
    _nameController.dispose();
    _passwordController.dispose();
    _newPasswordController.dispose();
    _confirmNewPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    User? user = _auth.currentUser;
    _nameController.text =
        user != null && user.displayName != null ? user.displayName! : '';

    return Scaffold(
      appBar: AppBar(
        title: Text(''),
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(
            color: Color(0xFF0A84FF)), // Set the back arrow color here
      ),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Name',
                  labelStyle: TextStyle(
                    color: Color(0xFF0A84FF), // Color of the label text
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Color(
                          0xFF0A84FF), // Color of the border when not focused
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color:
                          Color(0xFF0A84FF), // Color of the border when focused
                    ),
                  ),
                ),
                cursorColor: Color(0xFF0A84FF), // Set the cursor color here
                style: TextStyle(
                  color: Color(0xFF0A84FF), // Color of the input text
                ),
                textCapitalization:
                    TextCapitalization.words, // Enable auto capitalization
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => _updateDisplayName(),
                child: Text('Update Name'),
                style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF0A84FF), foregroundColor: Colors.white),
              ),
              SizedBox(height: 20),
              TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Current Password',
                  border: OutlineInputBorder(),
                  labelStyle: TextStyle(
                    color: Color(0xFF0A84FF), // Color of the label text
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Color(
                          0xFF0A84FF), // Color of the border when not focused
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color:
                          Color(0xFF0A84FF), // Color of the border when focused
                    ),
                  ),
                ),
                cursorColor: Color(0xFF0A84FF), // Set the cursor color here
                style: TextStyle(
                  color: Color(0xFF0A84FF), // Color of the input text
                ),
              ),
              SizedBox(height: 20),
              TextField(
                controller: _newPasswordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'New Password',
                  border: OutlineInputBorder(),
                  labelStyle: TextStyle(
                    color: Color(0xFF0A84FF), // Color of the label text
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Color(
                          0xFF0A84FF), // Color of the border when not focused
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color:
                          Color(0xFF0A84FF), // Color of the border when focused
                    ),
                  ),
                ),
                cursorColor: Color(0xFF0A84FF), // Set the cursor color here
                style: TextStyle(
                  color: Color(0xFF0A84FF), // Color of the input text
                ),
              ),
              SizedBox(height: 20),
              TextField(
                controller: _confirmNewPasswordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Confirm New Password',
                  border: OutlineInputBorder(),
                  labelStyle: TextStyle(
                    color: Color(0xFF0A84FF), // Color of the label text
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Color(
                          0xFF0A84FF), // Color of the border when not focused
                    ),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                      color:
                          Color(0xFF0A84FF), // Color of the border when focused
                    ),
                  ),
                ),
                cursorColor: Color(0xFF0A84FF), // Set the cursor color here
                style: TextStyle(
                  color: Color(0xFF0A84FF), // Color of the input text
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => _changePassword(context),
                child: Text('Change Password'),
                style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF0A84FF), foregroundColor: Colors.white),
              ),
              ElevatedButton(
                onPressed: () => _signOut(context),
                child: Text('Log Out'),
                style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF0A84FF), foregroundColor: Colors.white),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _updateDisplayName() async {
    User? user = _auth.currentUser;
    if (user != null) {
      await user.updateDisplayName(_nameController.text);
      await user.reload();
      setState(() {});
      // Return the updated name to the previous screen
      Navigator.pop(context, _nameController.text);
    }
  }

  Future<void> _changePassword(BuildContext context) async {
    if (_newPasswordController.text != _confirmNewPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("New passwords do not match.")),
      );
      return;
    }

    User? user = _auth.currentUser;
    if (user != null && _passwordController.text.isNotEmpty) {
      // Reauthenticate the user
      UserCredential? userCredential;
      try {
        userCredential = await user.reauthenticateWithCredential(
          EmailAuthProvider.credential(
            email: user.email!,
            password: _passwordController.text,
          ),
        );
      } on FirebaseAuthException catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Reauthentication failed: ${e.message}")),
        );
        return;
      }

      // Change the password
      if (userCredential.user != null) {
        try {
          await userCredential.user!
              .updatePassword(_newPasswordController.text);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Password changed successfully.")),
          );
        } on FirebaseAuthException catch (e) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Failed to change password: ${e.message}")),
          );
        }
      }
    }
  }

  Future<void> _signOut(BuildContext context) async {
    await _auth.signOut();
    Navigator.of(context).pushReplacementNamed('/login');
  }
}
