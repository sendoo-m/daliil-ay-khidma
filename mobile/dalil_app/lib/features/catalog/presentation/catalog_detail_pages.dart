import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';

class ProductDetailPage extends ConsumerWidget {
  const ProductDetailPage({required this.slug, super.key});
  final String slug;
  @override
  Widget build(BuildContext context, WidgetRef ref) => _JsonDetailPage(
        titleKey: 'name_ar',
        descriptionKey: 'description_ar',
        future: ref.read(catalogRepositoryProvider).productDetail(slug),
      );
}

class DealDetailPage extends ConsumerWidget {
  const DealDetailPage({required this.slug, super.key});
  final String slug;
  @override
  Widget build(BuildContext context, WidgetRef ref) => _JsonDetailPage(
        titleKey: 'title_ar',
        descriptionKey: 'description_ar',
        future: ref.read(catalogRepositoryProvider).dealDetail(slug),
        action: FilledButton.icon(
          icon: const Icon(Icons.redeem),
          label: const Text('المطالبة بالعرض'),
          onPressed: () async {
            final message = await ref.read(catalogRepositoryProvider).claimDeal(slug);
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(message)),
              );
            }
          },
        ),
      );
}

class _JsonDetailPage extends StatelessWidget {
  const _JsonDetailPage({
    required this.titleKey,
    required this.descriptionKey,
    required this.future,
    this.action,
  });
  final String titleKey;
  final String descriptionKey;
  final Future<Map<String, dynamic>> future;
  final Widget? action;

  @override
  Widget build(BuildContext context) => FutureBuilder(
        future: future,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Scaffold(body: Center(child: CircularProgressIndicator()));
          }
          final item = snapshot.data!;
          return Scaffold(
            appBar: AppBar(title: Text('${item[titleKey] ?? ''}')),
            body: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                if (item['image'] != null)
                  Image.network('${item['image']}', height: 200),
                const SizedBox(height: 16),
                Text('${item[titleKey] ?? ''}', style: Theme.of(context).textTheme.headlineSmall),
                const SizedBox(height: 12),
                Text('${item[descriptionKey] ?? ''}'),
                const SizedBox(height: 20),
                if (action != null) action!,
              ],
            ),
          );
        },
      );
}
