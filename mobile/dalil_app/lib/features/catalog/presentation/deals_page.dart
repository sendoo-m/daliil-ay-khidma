import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import 'catalog_detail_pages.dart';

class DealsPage extends ConsumerWidget {
  const DealsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final home = ref.watch(homeProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('العروض والخصومات')),
      body: home.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, __) => _MessageState(
          icon: Icons.cloud_off_outlined,
          message: 'تعذر تحميل العروض',
          action: () => ref.invalidate(homeProvider),
        ),
        data: (data) {
          if (data.deals.isEmpty) {
            return const _MessageState(
              icon: Icons.local_offer_outlined,
              message: 'لا توجد عروض متاحة الآن',
            );
          }
          return RefreshIndicator(
            onRefresh: () => ref.refresh(homeProvider.future),
            child: ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: data.deals.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final deal = data.deals[index];
                return Card(
                  clipBehavior: Clip.antiAlias,
                  child: InkWell(
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute<void>(
                        builder: (_) => DealDetailPage(slug: deal.slug),
                      ),
                    ),
                    child: Row(
                      children: [
                        _DealImage(url: deal.image),
                        Expanded(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  deal.title,
                                  maxLines: 2,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.w800,
                                    fontSize: 16,
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  '${deal.finalPrice} جنيه',
                                  style: TextStyle(
                                    color:
                                        Theme.of(context).colorScheme.primary,
                                    fontWeight: FontWeight.w800,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  'متبقي ${deal.daysRemaining} يوم',
                                  style: Theme.of(context).textTheme.bodySmall,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class _DealImage extends StatelessWidget {
  const _DealImage({this.url});
  final String? url;

  @override
  Widget build(BuildContext context) => SizedBox(
        width: 116,
        height: 128,
        child: url == null || url!.isEmpty
            ? ColoredBox(
                color: Theme.of(context).colorScheme.primaryContainer,
                child: const Icon(Icons.local_offer_outlined, size: 36),
              )
            : Image.network(
                url!,
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) =>
                    const Icon(Icons.local_offer_outlined, size: 36),
              ),
      );
}

class _MessageState extends StatelessWidget {
  const _MessageState({
    required this.icon,
    required this.message,
    this.action,
  });
  final IconData icon;
  final String message;
  final VoidCallback? action;

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 48, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 16),
              Text(message),
              if (action != null) ...[
                const SizedBox(height: 16),
                FilledButton(
                  onPressed: action,
                  child: const Text('إعادة المحاولة'),
                ),
              ],
            ],
          ),
        ),
      );
}
