import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/auth_repository.dart';

final class AuthController extends StateNotifier<AsyncValue<bool>> {
  AuthController(this._repository, Future<bool> hasSession)
      : super(const AsyncLoading()) {
    hasSession.then((value) => state = AsyncData(value));
  }

  final AuthRepository _repository;

  Future<bool> login(String username, String password) async {
    state = const AsyncLoading();
    try {
      await _repository.login(username: username, password: password);
      state = const AsyncData(true);
      return true;
    } catch (error, stack) {
      state = AsyncError(error, stack);
      return false;
    }
  }

  Future<bool> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    state = const AsyncLoading();
    try {
      await _repository.register(
        username: username,
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      state = const AsyncData(true);
      return true;
    } catch (error, stack) {
      state = AsyncError(error, stack);
      return false;
    }
  }

  Future<void> logout() async {
    await _repository.logout();
    state = const AsyncData(false);
  }
}
