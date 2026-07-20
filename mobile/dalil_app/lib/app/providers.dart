import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../core/auth/token_store.dart';
import '../core/network/api_client.dart';
import '../features/app_config/data/app_config_repository.dart';
import '../features/notifications/data/device_repository.dart';

final tokenStoreProvider = Provider(
  (_) => TokenStore(const FlutterSecureStorage()),
);
final apiClientProvider = Provider((ref) => ApiClient(ref.watch(tokenStoreProvider)));
final appConfigRepositoryProvider = Provider(
  (ref) => AppConfigRepository(ref.watch(apiClientProvider).dio),
);
final deviceRepositoryProvider = Provider(
  (ref) => DeviceRepository(ref.watch(apiClientProvider).dio),
);
final appConfigProvider = FutureProvider(
  (ref) => ref.watch(appConfigRepositoryProvider).fetch(),
);
