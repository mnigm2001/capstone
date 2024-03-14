import 'package:flutter/material.dart';
import 'pill.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

class PillDetailsScreen extends StatefulWidget {
  final Pill pill;

  PillDetailsScreen({Key? key, required this.pill}) : super(key: key);

  @override
  _PillDetailsScreenState createState() => _PillDetailsScreenState();
}

class _PillDetailsScreenState extends State<PillDetailsScreen> {
  FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

  @override
  void initState() {
    super.initState();
    tz.initializeTimeZones();
    var initializationSettingsAndroid = AndroidInitializationSettings('@mipmap/ic_launcher');
    var initializationSettingsIOS = DarwinInitializationSettings();
    var initializationSettings = InitializationSettings(
      android: initializationSettingsAndroid,
      iOS: initializationSettingsIOS,
    );
    flutterLocalNotificationsPlugin.initialize(initializationSettings);
  }

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

  void _showRepeatIntervalSelection(BuildContext context, DateTime scheduledDateTime) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext context) {
        return SafeArea(
          child: Wrap(
            children: <Widget>[
              ListTile(
                  leading: Icon(Icons.calendar_today),
                  title: Text('No Repeat'),
                  onTap: () {
                    Navigator.pop(context);
                    _scheduleNotification(scheduledDateTime, null);
                  }),
              ListTile(
                leading: Icon(Icons.repeat),
                title: Text('Hourly'),
                onTap: () {
                  Navigator.pop(context);
                  _scheduleNotification(scheduledDateTime, RepeatInterval.hourly);
                },
              ),
              ListTile(
                leading: Icon(Icons.repeat),
                title: Text('Daily'),
                onTap: () {
                  Navigator.pop(context);
                  _scheduleNotification(scheduledDateTime, RepeatInterval.daily);
                },
              ),
              // Add more intervals as needed
            ],
          ),
        );
      },
    );
  }

  Future<void> _scheduleNotification(DateTime scheduledNotificationDateTime, RepeatInterval? repeatInterval) async {
    var androidPlatformChannelSpecifics = AndroidNotificationDetails(
      'med_reminder_id',
      'Medication Reminder',
      channelDescription: 'Channel for Medication Reminder',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: false,
    );
    var iOSPlatformChannelSpecifics = DarwinNotificationDetails();
    var platformChannelSpecifics = NotificationDetails(
      android: androidPlatformChannelSpecifics,
      iOS: iOSPlatformChannelSpecifics,
    );

    if (repeatInterval != null) {
      flutterLocalNotificationsPlugin.periodicallyShow(
        0, // Notification ID
        'Pill Reminder', // Notification Title
        'Don\'t forget to take your ${widget.pill.name}', // Notification Body
        repeatInterval,
        platformChannelSpecifics,
        androidAllowWhileIdle: true,
      );
    } else {
      flutterLocalNotificationsPlugin.zonedSchedule(
        0, // Notification ID
        'Pill Reminder', // Notification Title
        'Don\'t forget to take your ${widget.pill.name}', // Notification Body
        tz.TZDateTime.from(scheduledNotificationDateTime, tz.local), // Scheduled Date & Time
        platformChannelSpecifics,
        androidAllowWhileIdle: true,
        uiLocalNotificationDateInterpretation:
            UILocalNotificationDateInterpretation.absoluteTime,
        matchDateTimeComponents: DateTimeComponents.time,
      );
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
                        widget.pill.dosage,
                        style: TextStyle(
                          color: Color(0xFF0A84FF),
                          fontSize: 18,
                        ),
                      ),
                    ],
                  ),
                ),
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
            Spacer(),
            ElevatedButton(
              onPressed: () => _pickDate(context),
              child: Text('Set Reminder'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF0A84FF),
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
