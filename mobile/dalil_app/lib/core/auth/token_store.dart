import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final class TokenPair {
  const TokenPair({required this.access, required this.refresh});

  final String access;
  final String refresh;
}

final class TokenStore {
  TokenStore(this._storage);

  static const _accessKey = 'auth.access_token';
  static const _refreshKey = 'auth.refresh_token';
  final FlutterSecureStorage _storage;

  Future<String?> readAccess() => _storage.read(key: _accessKey);
  Future<String?> readRefresh() => _storage.read(key: _refreshKey);

  Future<void> save(TokenPair tokens) async {
    await Future.wait([
      _storage.write(key: _accessKey, value: tokens.access),
      _storage.write(key: _refreshKey, value: tokens.refresh),
    ]);
  }

  Future<void> clear() async {
    await Future.wait([
      _storage.delete(key: _accessKey),
      _storage.delete(key: _refreshKey),
    ]);
  }

  Future<bool> get hasSession async => (await readRefresh()) != null;
}
