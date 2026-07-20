import 'package:dio/dio.dart';

final class CatalogRepository {
  CatalogRepository(this._dio);
  final Dio _dio;

  Future<Map<String, dynamic>> productDetail(String slug) async {
    final response = await _dio.get<Map<String, dynamic>>('products/$slug/');
    return response.data!;
  }

  Future<Map<String, dynamic>> dealDetail(String slug) async {
    final response = await _dio.get<Map<String, dynamic>>('deals/$slug/');
    return response.data!;
  }

  Future<String> claimDeal(String slug) async {
    final response = await _dio.post<Map<String, dynamic>>('deals/$slug/claim/');
    return response.data?['code'] as String? ??
        response.data?['claim_code'] as String? ??
        'تمت المطالبة بالعرض';
  }
}
