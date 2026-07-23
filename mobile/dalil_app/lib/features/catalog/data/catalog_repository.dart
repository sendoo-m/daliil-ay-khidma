import 'package:dio/dio.dart';

import 'catalog_models.dart';

final class CatalogRepository {
  CatalogRepository(this._dio);
  final Dio _dio;

  Future<ProductDetail> productDetail(String slug) async {
    final response = await _dio.get<Map<String, dynamic>>('products/$slug/');
    return ProductDetail.fromJson(response.data!);
  }

  Future<List<ProductSummary>> searchProducts(
    String query, {
    int? categoryId,
    int? governorateId,
    String? productType,
    double? minPrice,
    double? maxPrice,
    String ordering = 'price',
  }) async {
    final response = await _dio.get<Map<String, dynamic>>(
      'products/',
      queryParameters: {
        if (query.isNotEmpty) 'search': query,
        if (categoryId != null) 'category': categoryId,
        if (governorateId != null) 'governorate': governorateId,
        if (productType != null) 'product_type': productType,
        if (minPrice != null) 'min_price': minPrice,
        if (maxPrice != null) 'max_price': maxPrice,
        'ordering': ordering,
        'page_size': 50,
      },
    );
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results
        .cast<Map<String, dynamic>>()
        .map(ProductSummary.fromJson)
        .toList(growable: false);
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
