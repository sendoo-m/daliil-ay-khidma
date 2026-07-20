import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../../directory/presentation/business_card.dart';
import '../../directory/presentation/search_page.dart';
import '../../directory/presentation/favorites_page.dart';
import '../../notifications/presentation/notifications_page.dart';
import '../../catalog/presentation/catalog_detail_pages.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final home = ref.watch(homeProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('دليل أي خدمة'),
        actions: [
          IconButton(
            icon: const Icon(Icons.favorite_outline),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => const FavoritesPage(),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => const NotificationsPage(),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => ref.read(authControllerProvider.notifier).logout(),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.of(context).push(
          MaterialPageRoute<void>(builder: (_) => const SearchPage()),
        ),
        child: const Icon(Icons.search),
      ),
      body: home.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, __) => Center(
          child: FilledButton(
            onPressed: () => ref.invalidate(homeProvider),
            child: const Text('إعادة المحاولة'),
          ),
        ),
        data: (data) => RefreshIndicator(
          onRefresh: () => ref.refresh(homeProvider.future),
          child: ListView(
            padding: const EdgeInsets.all(12),
            children: [
              Text('التصنيفات', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                children: data.categories
                    .map(
                      (item) => Chip(
                        label: Text('${item['name_ar'] ?? ''}'),
                      ),
                    )
                    .toList(),
              ),
              const SizedBox(height: 20),
              Text(
                'أنشطة مميزة',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              ...data.businesses.map(
                (item) => BusinessCard(business: item),
              ),
              const SizedBox(height: 20),
              Text('منتجات مميزة', style: Theme.of(context).textTheme.titleLarge),
              ...data.products.map(
                (item) => ListTile(
                  leading: const Icon(Icons.shopping_bag_outlined),
                  title: Text(item.name),
                  subtitle: Text('${item.price} جنيه'),
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (_) => ProductDetailPage(slug: item.slug),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Text('عروض مميزة', style: Theme.of(context).textTheme.titleLarge),
              ...data.deals.map(
                (item) => ListTile(
                  leading: const Icon(Icons.local_offer_outlined),
                  title: Text(item.title),
                  subtitle: Text('${item.finalPrice} جنيه • ${item.daysRemaining} يوم'),
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (_) => DealDetailPage(slug: item.slug),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
