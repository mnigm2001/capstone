import 'package:flutter/material.dart';
import 'pill.dart';
import 'pill_details_screen.dart'; // Make sure to import the Pill Details Page

class PillsPage extends StatefulWidget {
  @override
  _PillsPageState createState() => _PillsPageState();

  void addPill(Pill pill) {
    _PillsPageState state = _PillsPageState();
    state.addPill(pill);
  }
}

class _PillsPageState extends State<PillsPage> {
  final List<Pill> pills = [];

  void addPill(Pill pill) {
    setState(() {
      pills.add(pill);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(color: Color(0xFF0A84FF)),
      ),
      body: ListView.separated(
        itemCount: pills.length,
        itemBuilder: (context, index) {
          final pill = pills[index];
          return ListTile(
            title: Text(
              pill.name,
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            subtitle: Text(
              '${pill.dosage} - ${pill.description}',
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 17.5,
              ),
            ),
            onTap: () {
              // Navigate to the Pill Details Page with the selected pill's details
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => PillDetailsScreen(pill: pill),
                ),
              );
            },
          );
        },
        separatorBuilder: (context, index) => Divider(),
      ),
    );
  }
}
