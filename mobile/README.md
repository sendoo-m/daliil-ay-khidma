# Daliil Mobile

Flutter client foundation for Android and iOS. The first application is the
public Daliil app and consumes `/api/v2/`.

## Bootstrap native projects

Install Flutter 3.22+ and run:

```bash
cd mobile/dalil_app
flutter create --platforms=android,ios --org com.daliilaykhidma .
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

For a physical device, replace `10.0.2.2` with the development machine IP.
Production builds must supply the HTTPS API URL through `--dart-define`.

## Foundation included

- Riverpod application bootstrap
- API v2 client with access-token injection and one-time refresh/retry
- Secure JWT storage
- Remote app configuration loading
- FCM/APNs device-token registration contract
- Arabic/English localization setup and Material 3 theme

Run `tool/bootstrap_native.sh` with the team's pinned Flutter SDK to generate
and validate both native projects. Then follow `FIREBASE_SETUP.md` to connect
the Firebase project without committing credentials.
