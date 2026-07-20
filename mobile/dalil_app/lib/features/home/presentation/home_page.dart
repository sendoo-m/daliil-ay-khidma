import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../../directory/presentation/business_card.dart';
import '../../directory/presentation/search_page.dart';

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
                    .map((item) => Chip(label: Text('${item['name_ar'] ?? ''}')))
                    .toList(),
              ),
              const SizedBox(height: 20),
              Text('أنشطة مميزة', style: Theme.of(context).textTheme.titleLarge),
              ...data.businesses.map((item) => BusinessCard(business: item)),
            ],
          ),
        ),
      ),
    );
  }
}
