/* import 'package:flutter/material.dart';
import 'pill.dart'; // Import your Pill model
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
  FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  @override
  void initState() {
    super.initState();
    tz.initializeTimeZones();
    var initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
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

  void _showRepeatIntervalSelection(
      BuildContext context, DateTime scheduledDateTime) {
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
                  _scheduleNotification(
                      scheduledDateTime, RepeatInterval.hourly);
                },
              ),
              ListTile(
                leading: Icon(Icons.repeat),
                title: Text('Daily'),
                onTap: () {
                  Navigator.pop(context);
                  _scheduleNotification(
                      scheduledDateTime, RepeatInterval.daily);
                },
              ),
              // Add more intervals as needed
            ],
          ),
        );
      },
    );
  }

  String getReminderMessage(String pillName, DateTime scheduledTime) {
    int hour = scheduledTime.hour;
    String partOfDay;

    if (hour >= 6 && hour < 12) {
      partOfDay = 'morning';
    } else if (hour >= 12 && hour < 18) {
      partOfDay = 'afternoon';
    } else if (hour >= 18 && hour < 22) {
      partOfDay = 'evening';
    } else {
      partOfDay = 'night';
    }

    return "Don't forget to take your $partOfDay $pillName";
  }

  Future<void> _scheduleNotification(DateTime scheduledNotificationDateTime,
      RepeatInterval? repeatInterval) async {
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

    String notificationMessage =
        getReminderMessage(widget.pill.name, scheduledNotificationDateTime);

    if (repeatInterval != null) {
      flutterLocalNotificationsPlugin.periodicallyShow(
        0, // Notification ID
        'Pill Reminder', // Notification Title
        notificationMessage, // Customized Notification Body
        repeatInterval,
        platformChannelSpecifics,
        androidAllowWhileIdle: true,
      );
    } else {
      flutterLocalNotificationsPlugin.zonedSchedule(
        0, // Notification ID
        'Pill Reminder', // Notification Title
        notificationMessage, // Customized Notification Body
        tz.TZDateTime.from(
            scheduledNotificationDateTime, tz.local), // Scheduled Date & Time
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
 */

import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:flutter/material.dart';
import 'pill.dart';

class PillDetailsScreen extends StatefulWidget {
  final Pill pill;

  PillDetailsScreen({Key? key, required this.pill}) : super(key: key);

  @override
  _PillDetailsScreenState createState() => _PillDetailsScreenState();
}

class _PillDetailsScreenState extends State<PillDetailsScreen> {
  @override
  void initState() {
    super.initState();
    AwesomeNotifications().initialize(
      'resource://drawable/ic_stat_notify', // <-- Specify your icon here
      [
        NotificationChannel(
          channelKey: 'basic_channel',
          channelName: 'Basic notifications',
          channelDescription: 'Notification channel for basic tests',
          defaultColor: Color(0xFF9D50DD),
          ledColor: Colors.white,
          importance: NotificationImportance.High,
          channelShowBadge: true,
        ),
      ],
    );
    AwesomeNotifications().isNotificationAllowed().then(
      (isAllowed) {
        if (!isAllowed) {
          // Insert dialog or another approach to encourage users to allow notifications
        }
      },
    );
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
    String notificationBody =
        getReminderMessage(widget.pill.name, scheduledNotificationDateTime);

    if (repeatDaily) {
      await AwesomeNotifications().createNotification(
        content: NotificationContent(
          id: createUniqueId(),
          channelKey: 'basic_channel',
          title: 'Pill Reminder',
          body: notificationBody,
          notificationLayout: NotificationLayout.Default,
        ),
        schedule: NotificationCalendar(
          year: scheduledNotificationDateTime.year,
          month: scheduledNotificationDateTime.month,
          day: scheduledNotificationDateTime.day,
          hour: scheduledNotificationDateTime.hour,
          minute: scheduledNotificationDateTime.minute,
          second: 0,
          millisecond: 0,
          repeats: true,
        ),
      );
    } else {
      await AwesomeNotifications().createNotification(
        content: NotificationContent(
          id: createUniqueId(),
          channelKey: 'basic_channel',
          title: 'Pill Reminder',
          body: notificationBody,
          notificationLayout: NotificationLayout.Default,
        ),
        schedule:
            NotificationCalendar.fromDate(date: scheduledNotificationDateTime),
      );
    }
  }

  String getReminderMessage(String pillName, DateTime scheduledTime) {
    int hour = scheduledTime.hour;
    String partOfDay;

    if (hour >= 6 && hour < 12) {
      partOfDay = 'morning';
    } else if (hour >= 12 && hour < 18) {
      partOfDay = 'afternoon';
    } else if (hour >= 18 && hour < 22) {
      partOfDay = 'evening';
    } else {
      partOfDay = 'night time';
    }

    return "Don't forget to take your $partOfDay $pillName";
  }

  int createUniqueId() {
    return DateTime.now().millisecondsSinceEpoch.remainder(100000);
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
