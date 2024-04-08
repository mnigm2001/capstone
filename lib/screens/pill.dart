class Pill {
  final String name;
  final String dosage;
  final String description;
  final String imageUrl;
  final String purpose;
  final String applicationMethod;
  final String sideEffects;
  final String imprint;
  final String shape;
  final String color;

  Pill({
    required this.name,
    required this.dosage,
    required this.description,
    required this.imageUrl,
    required this.purpose,
    required this.applicationMethod,
    required this.sideEffects,
    required this.imprint,
    required this.shape,
    required this.color,
  });

  // Add a factory constructor to create a Pill instance from a map.
  factory Pill.fromMap(Map<String, dynamic> map) {
    return Pill(
      name: map['name'] ?? '',
      dosage: map['dosage'] ?? '',
      description: map['description'] ?? '',
      imageUrl: map['imageUrl'] ?? '',
      purpose: map['purpose'] ?? '',
      applicationMethod: map['applicationMethod'] ?? '',
      sideEffects: map['sideEffects'] ?? '',
      imprint: map['imprint'] ?? '',
      shape: map['shape'] ?? '',
      color: map['color'] ?? '',
    );
  }
}
