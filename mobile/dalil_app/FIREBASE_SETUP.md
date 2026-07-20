# Firebase setup

The backend device-registration API is ready. Native Firebase configuration
must be generated from the Firebase project that owns the production apps.
Never commit service account credentials or native Firebase configuration.

## 1. Generate Android and iOS projects

```bash
cd mobile/dalil_app
chmod +x tool/bootstrap_native.sh
./tool/bootstrap_native.sh
```

Application identifiers:

- Android: `com.daliilaykhidma.dalil_app`
- iOS: `com.daliilaykhidma.dalilApp`

## 2. Connect FlutterFire

```bash
dart pub global activate flutterfire_cli
firebase login
flutterfire configure \
  --platforms=android,ios \
  --android-package-name=com.daliilaykhidma.dalil_app \
  --ios-bundle-id=com.daliilaykhidma.dalilApp
```

This generates the platform configuration and `lib/firebase_options.dart`.
Initialize Firebase with `DefaultFirebaseOptions.currentPlatform` if the team
chooses to keep that generated Dart file in source control.

## 3. Platform capabilities

In Xcode enable Push Notifications and Background Modes > Remote notifications.
Upload the APNs authentication key in Firebase Console. Android requires no
additional runtime capability after FlutterFire configuration.

## 4. Backend

Set these production variables on the Django service:

```env
PUSH_NOTIFICATIONS_ENABLED=True
FIREBASE_CREDENTIALS_PATH=/run/secrets/firebase-service-account.json
```

The Firebase service-account JSON belongs in the deployment secret store, not
in this repository.
