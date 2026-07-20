import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../core/auth/token_store.dart';
import '../core/network/api_client.dart';
import '../core/notifications/push_service.dart';
import '../features/auth/data/auth_repository.dart';
import '../features/auth/presentation/auth_controller.dart';
import '../features/directory/data/business_repository.dart';
import '../features/home/data/home_repository.dart';
import '../features/app_config/data/app_config_repository.dart';
import '../features/notifications/data/device_repository.dart';
import '../features/notifications/data/notification_repository.dart';
import '../features/reviews/data/review_repository.dart';

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
final notificationRepositoryProvider = Provider(
  (ref) => NotificationRepository(ref.watch(apiClientProvider).dio),
);
final reviewRepositoryProvider = Provider(
  (ref) => ReviewRepository(ref.watch(apiClientProvider).dio),
);
final pushServiceProvider = Provider(
  (ref) => PushService(ref.watch(deviceRepositoryProvider)),
);
final authRepositoryProvider = Provider(
  (ref) => AuthRepository(
    ref.watch(apiClientProvider).dio,
    ref.watch(tokenStoreProvider),
  ),
);
final authControllerProvider = StateNotifierProvider<AuthController, AsyncValue<bool>>(
  (ref) => AuthController(
    ref.watch(authRepositoryProvider),
    ref.watch(tokenStoreProvider).hasSession,
  ),
);
final homeRepositoryProvider = Provider(
  (ref) => HomeRepository(ref.watch(apiClientProvider).dio),
);
final homeProvider = FutureProvider((ref) => ref.watch(homeRepositoryProvider).fetch());
final businessRepositoryProvider = Provider(
  (ref) => BusinessRepository(ref.watch(apiClientProvider).dio),
);
final appConfigProvider = FutureProvider(
  (ref) => ref.watch(appConfigRepositoryProvider).fetch(),
);
