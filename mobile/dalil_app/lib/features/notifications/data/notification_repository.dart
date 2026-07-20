import 'package:dio/dio.dart';

final class AppNotification {
  const AppNotification({
    required this.id,
    required this.title,
    required this.body,
    required this.isRead,
  });
  factory AppNotification.fromJson(Map<String, dynamic> json) => AppNotification(
        id: json['id'] as int,
        title: json['title'] as String? ?? '',
        body: json['body'] as String? ?? '',
        isRead: json['is_read'] as bool? ?? false,
      );
  final int id;
  final String title;
  final String body;
  final bool isRead;
}

final class NotificationRepository {
  NotificationRepository(this._dio);
  final Dio _dio;
  Future<List<AppNotification>> list() async {
    final response = await _dio.get<Map<String, dynamic>>('notifications/');
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results.cast<Map<String, dynamic>>().map(AppNotification.fromJson).toList();
  }
  Future<void> markRead(int id) => _dio.post<void>('notifications/$id/read/');
}
