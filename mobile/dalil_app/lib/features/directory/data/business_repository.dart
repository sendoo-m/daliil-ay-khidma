import 'package:dio/dio.dart';

import 'business.dart';

final class BusinessRepository {
  BusinessRepository(this._dio);
  final Dio _dio;

  Future<List<Business>> search(String query) async {
    final response = await _dio.get<Map<String, dynamic>>(
      'businesses/',
      queryParameters: {'search': query, 'page_size': 20},
    );
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results
        .cast<Map<String, dynamic>>()
        .map(Business.fromJson)
        .toList(growable: false);
  }
}
