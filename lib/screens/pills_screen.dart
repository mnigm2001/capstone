import 'package:flutter/material.dart';
import 'pill.dart';
import 'pill_details_screen.dart'; // Import your PillDetailsScreen

class PillsPage extends StatefulWidget {
  final Pill? detectedPill;  // Make detectedPill optional

  PillsPage({Key? key, this.detectedPill}) : super(key: key);  // No 'required' keyword

  @override
  _PillsPageState createState() => _PillsPageState();
}

class _PillsPageState extends State<PillsPage> {
  List<Pill> pills = [];

  @override
  void initState() {
    super.initState();
    // Initialize pills list with detectedPill if it is not null
    if (widget.detectedPill != null) {
      pills.add(widget.detectedPill!);
    }
    // Otherwise, pills will just be an empty list or you could initialize it with existing pills history
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0, // Remove app bar elevation
      ),
      body: Container(
        color: Colors.white, // Set background color to white
        child: ListView.builder(
          itemCount: pills.length,
          itemBuilder: (context, index) {
            return ListTile(
              onTap: () {
                // Navigate to PillDetailsScreen when a pill is tapped
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => PillDetailsScreen(pill: pills[index]), // Pass the selected pill to PillDetailsScreen
                  ),
                );
              },
              title: Text(
                pills[index].name,
                style: TextStyle(color: Colors.blue, fontSize: 20, fontWeight: FontWeight.bold),  // Set text color to blue, increase font size, and make it bold
              ),
              subtitle: Text(
                '${pills[index].color} - ${pills[index].imprint} - ${pills[index].shape}',
                style: TextStyle(color: Colors.blue),  // Set text color to blue
              ),
            );
          },
        ),
      ),
    );
  }
}
