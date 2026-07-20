import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../l10n/app_localizations.dart';
import 'providers.dart';

class DalilApp extends ConsumerWidget {
  const DalilApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final config = ref.watch(appConfigProvider);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      onGenerateTitle: (context) => AppLocalizations.of(context)!.appName,
      locale: const Locale('ar'),
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF006C51)),
        useMaterial3: true,
      ),
      home: config.when(
        loading: () => const Scaffold(
          body: Center(child: CircularProgressIndicator()),
        ),
        error: (_, __) => const _HomePage(isOffline: true),
        data: (value) => value.maintenanceMode
            ? const _MaintenancePage()
            : const _HomePage(),
      ),
    );
  }
}

class _HomePage extends StatelessWidget {
  const _HomePage({this.isOffline = false});
  final bool isOffline;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: Text(AppLocalizations.of(context)!.appName)),
        body: Center(
          child: Text(
            isOffline
                ? 'تعذر تحميل الإعدادات، تحقق من الاتصال'
                : AppLocalizations.of(context)!.welcome,
          ),
        ),
      );
}

class _MaintenancePage extends StatelessWidget {
  const _MaintenancePage();

  @override
  Widget build(BuildContext context) => const Scaffold(
        body: Center(child: Text('التطبيق تحت الصيانة حاليًا')),
      );
}
