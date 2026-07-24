import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../features/auth/presentation/login_page.dart';
import '../features/directory/presentation/favorites_page.dart';
import '../features/directory/presentation/search_page.dart';
import '../features/home/presentation/home_page.dart';
import '../features/profile/presentation/profile_page.dart';
import '../features/catalog/presentation/deals_page.dart';
import 'providers.dart';

class MainShell extends ConsumerStatefulWidget {
  const MainShell({super.key});

  @override
  ConsumerState<MainShell> createState() => _MainShellState();
}

class _MainShellState extends ConsumerState<MainShell> {
  int _index = 0;
  int _favoritesRevision = 0;

  @override
  Widget build(BuildContext context) {
    final isAuthenticated =
        ref.watch(authControllerProvider).valueOrNull ?? false;
    final pages = <Widget>[
      HomePage(onSearchTap: () => setState(() => _index = 1)),
      const SearchPage(embedded: true),
      const DealsPage(),
      isAuthenticated
          ? FavoritesPage(
              key: ValueKey('favorites-$_favoritesRevision'),
              embedded: true,
            )
          : const _GuestGate(
              icon: Icons.favorite_outline,
              title: 'احتفظ بالأماكن التي تحبها',
              description:
                  'سجّل دخولك لإضافة المحلات والخدمات إلى مفضّلتك والعودة إليها بسهولة.',
            ),
      isAuthenticated
          ? const ProfilePage(embedded: true)
          : const _GuestGate(
              icon: Icons.person_outline,
              title: 'مرحبًا بك في دليل أي خدمة',
              description:
                  'أنشئ حسابًا أو سجّل الدخول لإدارة مفضّلتك وتقييماتك وإشعاراتك.',
            ),
    ];

    return Scaffold(
      body: IndexedStack(index: _index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() {
          _index = value;
          if (value == 3) _favoritesRevision++;
        }),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'الرئيسية',
          ),
          NavigationDestination(
            icon: Icon(Icons.search),
            label: 'البحث',
          ),
          NavigationDestination(
            icon: Icon(Icons.local_offer_outlined),
            selectedIcon: Icon(Icons.local_offer),
            label: 'العروض',
          ),
          NavigationDestination(
            icon: Icon(Icons.favorite_outline),
            selectedIcon: Icon(Icons.favorite),
            label: 'المفضلة',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'حسابي',
          ),
        ],
      ),
    );
  }
}

class _GuestGate extends StatelessWidget {
  const _GuestGate({
    required this.icon,
    required this.title,
    required this.description,
  });

  final IconData icon;
  final String title;
  final String description;

  @override
  Widget build(BuildContext context) => SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircleAvatar(
                  radius: 42,
                  backgroundColor:
                      Theme.of(context).colorScheme.primaryContainer,
                  child: Icon(icon, size: 40),
                ),
                const SizedBox(height: 24),
                Text(
                  title,
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.w800,
                      ),
                ),
                const SizedBox(height: 10),
                Text(
                  description,
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        color: const Color(0xFF64736C),
                        height: 1.6,
                      ),
                ),
                const SizedBox(height: 28),
                FilledButton.icon(
                  icon: const Icon(Icons.login),
                  label: const Text('تسجيل الدخول'),
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (_) => const LoginPage(),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
}
