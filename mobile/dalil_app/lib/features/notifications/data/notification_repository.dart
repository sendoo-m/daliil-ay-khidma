import 'package:dio/dio.dart';

final class AppNotification {
  const AppNotification({
    required this.id,
    required this.title,
    required this.body,
    required this.isRead,
    required this.type,
    required this.data,
    required this.createdAt,
  });
  factory AppNotification.fromJson(Map<String, dynamic> json) => AppNotification(
        id: json['id'] as int,
        title: json['title'] as String? ?? '',
        body: json['body'] as String? ?? '',
        isRead: json['is_read'] as bool? ?? false,
        type: json['notification_type'] as String? ?? 'general',
        data: (json['data'] as Map?)?.cast<String, dynamic>() ?? const {},
        createdAt: DateTime.tryParse(json['created_at'] as String? ?? ''),
      );
  final int id;
  final String title;
  final String body;
  final bool isRead;
  final String type;
  final Map<String, dynamic> data;
  final DateTime? createdAt;

  AppNotification copyWith({bool? isRead}) => AppNotification(
        id: id,
        title: title,
        body: body,
        isRead: isRead ?? this.isRead,
        type: type,
        data: data,
        createdAt: createdAt,
      );
}

final class NotificationRepository {
  NotificationRepository(this._dio);
  final Dio _dio;
  Future<List<AppNotification>> list() async {
    final response = await _dio.get<Map<String, dynamic>>('notifications/');
    final results = response.data?['results'] as List<dynamic>? ?? const [];
    return results
        .cast<Map<String, dynamic>>()
        .map(AppNotification.fromJson)
        .toList();
  }

  Future<AppNotification> markRead(int id) async {
    final response = await _dio.post<Map<String, dynamic>>(
      'notifications/$id/read/',
    );
    return AppNotification.fromJson(response.data!);
  }

  Future<int> unreadCount() async {
    final response = await _dio.get<Map<String, dynamic>>(
      'notifications/unread-count/',
    );
    return response.data?['count'] as int? ?? 0;
  }

  Future<int> markAllRead() async {
    final response = await _dio.post<Map<String, dynamic>>(
      'notifications/read-all/',
    );
    return response.data?['updated'] as int? ?? 0;
  }

  Future<void> delete(int id) => _dio.delete<void>('notifications/$id/');
}
