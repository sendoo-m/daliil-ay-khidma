import 'package:dio/dio.dart';

final class BusinessReview {
  const BusinessReview({
    required this.id,
    required this.rating,
    required this.comment,
    required this.username,
  });

  factory BusinessReview.fromJson(Map<String, dynamic> json) => BusinessReview(
        id: json['id'] as int,
        rating: json['rating'] as int? ?? 0,
        comment: json['comment'] as String? ?? '',
        username: json['user_name'] as String? ??
            json['user_username'] as String? ??
            '',
      );

  final int id;
  final int rating;
  final String comment;
  final String username;
}

final class ReviewRepository {
  ReviewRepository(this._dio);
  final Dio _dio;

  Future<List<BusinessReview>> list(int businessId) async {
    final response = await _dio.get<Map<String, dynamic>>(
      'reviews/',
      queryParameters: {'business': businessId},
    );
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results
        .cast<Map<String, dynamic>>()
        .map(BusinessReview.fromJson)
        .toList(growable: false);
  }

  Future<void> create({
    required int businessId,
    required int rating,
    required String comment,
  }) => _dio.post<void>(
        'reviews/',
        data: {
          'business': businessId,
          'rating': rating,
          'comment': comment.trim(),
        },
      );
}
