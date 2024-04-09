class Pill {
  String name;
  String color;
  String imprint;
  String shape;
  String strength; // New property for dosage
  String purpose; // New property for purpose
  String application; // New property for application method
  String side_effects; // New property for side effects

  Pill({
    required this.name,
    required this.color,
    required this.imprint,
    required this.shape,
    required this.strength,
    required this.purpose,
    required this.application,
    required this.side_effects,
  });

  factory Pill.fromMap(Map<String, dynamic> map) {
    return Pill(
      name: map['name'] ?? '',
      color: map['color'] ?? '',
      imprint: map['imprint'] ?? '',
      shape: map['shape'] ?? '',
      strength: map['strength'] ?? '', // Initialize new properties from the map
      purpose: map['purpose'] ?? '',
      application: map['application'] ?? '',
      side_effects: map['side_effects'] ?? '',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'color': color,
      'imprint': imprint,
      'shape': shape,
      'strength': strength, // Include new properties in the map
      'purpose': purpose,
      'application': application,
      'side_effects': side_effects,
    };
  }
}
