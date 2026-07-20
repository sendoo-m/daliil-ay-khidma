import 'package:dio/dio.dart';

import '../../../core/auth/token_store.dart';

final class UserProfile {
  const UserProfile({
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.phone,
  });
  factory UserProfile.fromJson(Map<String, dynamic> json) => UserProfile(
        username: json['username'] as String? ?? '',
        firstName: json['first_name'] as String? ?? '',
        lastName: json['last_name'] as String? ?? '',
        email: json['email'] as String? ?? '',
        phone: json['phone'] as String? ?? '',
      );
  final String username;
  final String firstName;
  final String lastName;
  final String email;
  final String phone;
}

final class ProfileRepository {
  ProfileRepository(this._dio, this._tokens);
  final Dio _dio;
  final TokenStore _tokens;

  Future<UserProfile> get() async {
    final response = await _dio.get<Map<String, dynamic>>('auth/profile/');
    return UserProfile.fromJson(response.data!);
  }

  Future<UserProfile> update({
    required String firstName,
    required String lastName,
    required String email,
    required String phone,
  }) async {
    final response = await _dio.patch<Map<String, dynamic>>(
      'auth/profile/update/',
      data: {
        'first_name': firstName.trim(),
        'last_name': lastName.trim(),
        'email': email.trim(),
        'phone': phone.trim(),
      },
    );
    return UserProfile.fromJson(
      response.data?['user'] as Map<String, dynamic>,
    );
  }

  Future<void> changePassword({
    required String oldPassword,
    required String newPassword,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      'auth/change-password/',
      data: {
        'old_password': oldPassword,
        'new_password': newPassword,
        'new_password_confirm': newPassword,
      },
    );
    final tokens = response.data?['tokens'] as Map<String, dynamic>;
    await _tokens.save(
      TokenPair(
        access: tokens['access'] as String,
        refresh: tokens['refresh'] as String,
      ),
    );
  }
}
