import 'package:dalil_app/core/network/api_failure.dart';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('maps throttling responses to an Arabic message', () {
    final error = DioException(
      requestOptions: RequestOptions(path: '/auth/password-reset/'),
      response: Response<void>(
        requestOptions: RequestOptions(path: '/auth/password-reset/'),
        statusCode: 429,
      ),
    );

    expect(ApiFailure.message(error), contains('المحاولات'));
  });
}
