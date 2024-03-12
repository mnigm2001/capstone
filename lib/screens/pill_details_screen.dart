import 'package:flutter/material.dart';
import 'pill.dart'; // Import your Pill model

class PillDetailsScreen extends StatefulWidget {
  final Pill pill;

  PillDetailsScreen({Key? key, required this.pill}) : super(key: key);

  @override
  _PillDetailsScreenState createState() => _PillDetailsScreenState();
}

class _PillDetailsScreenState extends State<PillDetailsScreen> {
  // This function shows a date picker dialog and returns the chosen date.
  Future<void> _pickDate(BuildContext context) async {
    final DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2100),
    );
    if (pickedDate != null) {
      // Once a date is picked, proceed to pick a time.
      _pickTime(context, pickedDate);
    }
  }

  // This function shows a time picker dialog and combines the chosen time with the provided date.
  Future<void> _pickTime(BuildContext context, DateTime pickedDate) async {
    final TimeOfDay? pickedTime = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );
    if (pickedTime != null) {
      // Combine the date and time into a single DateTime object.
      DateTime finalDateTime = DateTime(
        pickedDate.year,
        pickedDate.month,
        pickedDate.day,
        pickedTime.hour,
        pickedTime.minute,
      );
      // Here, you can call your function to schedule the reminder.
      // For demonstration, we'll just print the selected date and time.
      print("Reminder set for: $finalDateTime");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(
          color: Color(0xFF0A84FF),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start, // Aligns items at the start of the cross axis
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0), // Adjust the top padding here
                        child: Text(
                          widget.pill.name,
                          style: TextStyle(
                            color: Color(0xFF0A84FF),
                            fontSize: 37.5,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      Text(
                        widget.pill.dosage, // Add the dosage here
                        style: TextStyle(
                          color: Color(0xFF0A84FF),
                          fontSize: 18,
                        ),
                      ),
                    ],
                  ),
                ),
                // Ensure there's no extra padding/margin affecting alignment
                Image.asset(
                  widget.pill.imageUrl,
                  width: 125,
                  height: 125,
                ),
              ],
            ),
            SizedBox(height: 20),
            Text(
              "• ${widget.pill.purpose}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              "• ${widget.pill.applicationMethod}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              "• ${widget.pill.sideEffects}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            Spacer(), // This will push the button to the bottom of the screen
            ElevatedButton(
              onPressed: () => _pickDate(context),
              child: Text('Set Reminder'),
              style: ElevatedButton.styleFrom(
                primary: Color(0xFF0A84FF),
                onPrimary: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
