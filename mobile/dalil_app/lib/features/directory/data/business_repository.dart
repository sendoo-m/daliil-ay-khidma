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

  Future<Business> detail(String slug) async {
    final response = await _dio.get<Map<String, dynamic>>('businesses/$slug/');
    return Business.fromJson(response.data!);
  }

  Future<bool> toggleFavorite(int businessId) async {
    final response = await _dio.post<Map<String, dynamic>>(
      'favorites/toggle/',
      data: {'business_id': businessId},
    );
    return response.data?['is_favorite'] as bool? ?? false;
  }

  Future<List<Business>> favorites() async {
    final response = await _dio.get<Map<String, dynamic>>('favorites/');
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results
        .cast<Map<String, dynamic>>()
        .map(
          (item) => Business.fromJson(
            item['business'] as Map<String, dynamic>,
          ),
        )
        .toList(growable: false);
  }
}
