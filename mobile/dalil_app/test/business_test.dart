import 'package:dalil_app/features/directory/data/business.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('parses decimal ratings returned as strings by API v2', () {
    final business = Business.fromJson({
      'id': 7,
      'name_ar': 'صيدلية المدينة',
      'name_en': 'City Pharmacy',
      'slug': 'city-pharmacy',
      'average_rating': '4.75',
    });

    expect(business.id, 7);
    expect(business.rating, 4.75);
  });
}
