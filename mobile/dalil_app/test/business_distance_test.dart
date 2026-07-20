import 'package:dalil_app/features/directory/data/business.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('parses nearby distance as a double', () {
    final business = Business.fromJson({
      'id': 1,
      'name_ar': 'نشاط قريب',
      'slug': 'nearby',
      'distance_km': 2.75,
    });

    expect(business.distanceKm, 2.75);
  });
}
