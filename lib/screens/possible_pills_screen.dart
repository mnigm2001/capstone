import 'package:flutter/material.dart';
import 'pill.dart'; // Assuming this class exists and has the necessary fields
import 'pill_details_screen.dart'; // Make sure to import the Pill Details Page

class ProbablePillsPage extends StatefulWidget {
  @override
  _ProbablePillsPageState createState() => _ProbablePillsPageState();
}

class _ProbablePillsPageState extends State<ProbablePillsPage> {
  final List<Pill> pills = [
    Pill(
      name: "Aspirin",
      dosage: "325 mg",
      description: "Pain relief",
      imageUrl: "assets/images/aspirin.png",
      purpose: "Used to reduce pain, fever, or inflammation.",
      applicationMethod:
          "Take this medication by mouth with a full glass of water.",
      sideEffects: "May cause nausea, vomiting, or upset stomach.",
      imprint: "ABC",
      shape: "Oval",
      color: "Blue",
    ),
    Pill(
      name: "Amoxicillin",
      dosage: "875 mg",
      description: "Bacterial Treater",
      imageUrl: "assets/images/amoxicillin.png",
      purpose:
          "Commonly used to treat a wide variety of bacterial infections. It's particularly effective against infections in the ear, nose, throat, urinary tract, skin, and lower respiratory system.",
      applicationMethod:
          "Often taken orally with water, and can be taken with or without food.",
      sideEffects:
          "May cause nausea, vomiting, or diarrhea. Allergic reactions are possible, especially in individuals with a history of penicillin allergy",
      imprint: "ABC",
      shape: "Oval",
      color: "Blue",
    ),
    Pill(
        name: "Ibuprofen",
        dosage: "200 mg",
        description: "Anti-inflammatory",
        imageUrl: "assets/images/ibuprofen.png",
        purpose:
            "Widely used as an analgesic for relieving pain, as an antipyretic for reducing fever, and as an anti-inflammatory medication. Effective for treating headaches, toothaches, back pain, arthritis, menstrual cramps, and minor injuries.",
        applicationMethod:
            "Usually taken orally with a full glass of water, and it's recommended to take it with food or milk to decrease the chance of stomach upset.",
        sideEffects:
            "May cause upset stomach, nausea, dizziness, or drowsiness. More serious but rare side effects include heart problems or gastrointestinal bleeding.",
        imprint: "123",
        shape: "Round",
        color: "White"),
  ];

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
              'Imprint: ${pill.imprint} - Shape: ${pill.shape} - Color: ${pill.color}',
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
