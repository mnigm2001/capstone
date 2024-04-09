import 'package:flutter/material.dart';
import 'pill.dart';
import 'discussion_screen.dart';

class PillDetailsScreen extends StatefulWidget {
  final Pill pill;

  PillDetailsScreen({Key? key, required this.pill}) : super(key: key);

  @override
  _PillDetailsScreenState createState() => _PillDetailsScreenState();
}

class _PillDetailsScreenState extends State<PillDetailsScreen> {
  Future<void> _pickDate(BuildContext context) async {
    final DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2101),
    );
    if (pickedDate != null) {
      _pickTime(context, pickedDate);
    }
  }

  Future<void> _pickTime(BuildContext context, DateTime pickedDate) async {
    final TimeOfDay? pickedTime = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );
    if (pickedTime != null) {
      DateTime finalDateTime = DateTime(
        pickedDate.year,
        pickedDate.month,
        pickedDate.day,
        pickedTime.hour,
        pickedTime.minute,
      );
      _showRepeatIntervalSelection(context, finalDateTime);
    }
  }

  void _showRepeatIntervalSelection(
      BuildContext context, DateTime scheduledDateTime) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Repeat Daily?'),
          content: Text('Would you like to set this reminder to repeat daily?'),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.pop(context);
                _scheduleNotification(scheduledDateTime, false);
              },
              child: Text('No'),
            ),
            TextButton(
              onPressed: () {
                Navigator.pop(context);
                _scheduleNotification(scheduledDateTime, true);
              },
              child: Text('Yes'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _scheduleNotification(
      DateTime scheduledNotificationDateTime, bool repeatDaily) async {
    // Implement your notification scheduling logic here
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        iconTheme: IconThemeData(color: Color(0xFF0A84FF)),
        actions: <Widget>[
          IconButton(
            icon:
                Icon(Icons.forum, size: 32.5),
            padding: EdgeInsets.only(
                right: 16.0),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DiscussionPage(pill: widget.pill),
                ),
              );
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(top: 8.0),
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
                        widget.pill.strength,
                        style: TextStyle(
                          color: Color(0xFF0A84FF),
                          fontSize: 18,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            SizedBox(height: 10),
            Text(
              "Purpose:",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              "${widget.pill.purpose}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              "Application:",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              "${widget.pill.application}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              "Side Effects:",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              "${widget.pill.side_effects}",
              style: TextStyle(
                color: Color(0xFF0A84FF),
                fontSize: 18,
              ),
            ),
            Spacer(),
            ElevatedButton(
              onPressed: () => _pickDate(context),
              child: Text('Set Reminder'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF0A84FF),
                foregroundColor: Colors.white,
              ),
            ),
            SizedBox(height: 15),
          ],
        ),
      ),
    );
  }
}



