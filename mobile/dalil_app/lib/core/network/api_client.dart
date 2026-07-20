import 'dart:async';

import 'package:dio/dio.dart';

import '../auth/token_store.dart';
import '../config/environment.dart';

final class ApiClient {
  ApiClient(this._tokens)
      : dio = Dio(
          BaseOptions(
            baseUrl: Environment.apiV2.toString(),
            connectTimeout: const Duration(seconds: 15),
            receiveTimeout: const Duration(seconds: 20),
            headers: const {'Accept': 'application/json'},
          ),
        ) {
    dio.interceptors.add(_AuthInterceptor(dio, _tokens));
  }

  final TokenStore _tokens;
  final Dio dio;
}

final class _AuthInterceptor extends Interceptor {
  _AuthInterceptor(this._dio, this._tokens);

  final Dio _dio;
  final TokenStore _tokens;
  Future<String?>? _refreshing;

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final access = await _tokens.readAccess();
    if (access != null) options.headers['Authorization'] = 'Bearer $access';
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException error,
    ErrorInterceptorHandler handler,
  ) async {
    final request = error.requestOptions;
    final canRetry = error.response?.statusCode == 401 &&
        request.extra['authRetried'] != true &&
        !request.path.contains('auth/refresh');
    if (!canRetry) return handler.next(error);

    try {
      final access = await (_refreshing ??= _refreshAccess());
      _refreshing = null;
      if (access == null) return handler.next(error);
      request.extra['authRetried'] = true;
      request.headers['Authorization'] = 'Bearer $access';
      handler.resolve(await _dio.fetch<dynamic>(request));
    } catch (_) {
      _refreshing = null;
      await _tokens.clear();
      handler.next(error);
    }
  }

  Future<String?> _refreshAccess() async {
    final refresh = await _tokens.readRefresh();
    if (refresh == null) return null;
    final response = await Dio().post<Map<String, dynamic>>(
      Environment.apiV2.resolve('auth/refresh/').toString(),
      data: {'refresh': refresh},
    );
    final access = response.data?['access'] as String?;
    if (access == null) return null;
    await _tokens.save(TokenPair(access: access, refresh: refresh));
    return access;
  }
}
