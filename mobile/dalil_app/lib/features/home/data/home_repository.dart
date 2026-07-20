import 'package:dio/dio.dart';

import '../../directory/data/business.dart';

final class HomeData {
  const HomeData({required this.businesses, required this.categories});
  final List<Business> businesses;
  final List<Map<String, dynamic>> categories;
}

final class HomeRepository {
  HomeRepository(this._dio);
  final Dio _dio;

  Future<HomeData> fetch() async {
    final response = await _dio.get<Map<String, dynamic>>('home/');
    final json = response.data ?? const <String, dynamic>{};
    return HomeData(
      businesses: (json['featured_businesses'] as List<dynamic>? ?? const [])
          .cast<Map<String, dynamic>>()
          .map(Business.fromJson)
          .toList(growable: false),
      categories: (json['categories'] as List<dynamic>? ?? const [])
          .cast<Map<String, dynamic>>(),
    );
  }
}
