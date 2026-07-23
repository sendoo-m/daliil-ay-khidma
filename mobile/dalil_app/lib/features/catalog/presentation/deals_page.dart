import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../app/providers.dart';
import '../data/catalog_models.dart';
import 'catalog_detail_pages.dart';

final _dealsProvider = FutureProvider.autoDispose
    .family<List<DealSummary>, ({String search, String ordering})>(
  (ref, query) => ref.watch(catalogRepositoryProvider).deals(
        search: query.search,
        ordering: query.ordering,
      ),
);

class DealsPage extends ConsumerStatefulWidget {
  const DealsPage({super.key});

  @override
  ConsumerState<DealsPage> createState() => _DealsPageState();
}

class _DealsPageState extends ConsumerState<DealsPage> {
  final _searchController = TextEditingController();
  Timer? _debounce;
  String _search = '';
  String _ordering = '-created_at';

  ({String search, String ordering}) get _query =>
      (search: _search, ordering: _ordering);

  @override
  void dispose() {
    _debounce?.cancel();
    _searchController.dispose();
    super.dispose();
  }

  void _onSearch(String value) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 350), () {
      if (mounted) setState(() => _search = value.trim());
    });
  }

  @override
  Widget build(BuildContext context) {
    final deals = ref.watch(_dealsProvider(_query));
    return Scaffold(
      appBar: AppBar(title: const Text('العروض والخصومات')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
            child: Column(
              children: [
                SearchBar(
                  controller: _searchController,
                  hintText: 'ابحث في العروض أو أسماء المحلات',
                  leading: const Icon(Icons.search),
                  trailing: [
                    if (_searchController.text.isNotEmpty)
                      IconButton(
                        tooltip: 'مسح البحث',
                        onPressed: () {
                          _searchController.clear();
                          setState(() => _search = '');
                        },
                        icon: const Icon(Icons.close),
                      ),
                  ],
                  onChanged: (value) {
                    setState(() {});
                    _onSearch(value);
                  },
                ),
                const SizedBox(height: 10),
                SegmentedButton<String>(
                  segments: const [
                    ButtonSegment(
                      value: '-created_at',
                      label: Text('الأحدث'),
                      icon: Icon(Icons.auto_awesome_outlined),
                    ),
                    ButtonSegment(
                      value: 'end_date',
                      label: Text('ينتهي قريبًا'),
                      icon: Icon(Icons.timer_outlined),
                    ),
                    ButtonSegment(
                      value: '-view_count',
                      label: Text('الأكثر مشاهدة'),
                      icon: Icon(Icons.trending_up),
                    ),
                  ],
                  selected: {_ordering},
                  showSelectedIcon: false,
                  onSelectionChanged: (value) =>
                      setState(() => _ordering = value.first),
                ),
              ],
            ),
          ),
          Expanded(
            child: deals.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (_, __) => _MessageState(
                icon: Icons.cloud_off_outlined,
                message: 'تعذر تحميل العروض',
                action: () => ref.invalidate(_dealsProvider(_query)),
              ),
              data: (items) {
                if (items.isEmpty) {
                  return _MessageState(
                    icon: Icons.local_offer_outlined,
                    message: _search.isEmpty
                        ? 'لا توجد عروض متاحة الآن'
                        : 'لا توجد عروض تطابق بحثك',
                  );
                }
                return RefreshIndicator(
                  onRefresh: () => ref.refresh(_dealsProvider(_query).future),
                  child: ListView.separated(
                    padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
                    itemCount: items.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 12),
                    itemBuilder: (_, index) => _DealCard(deal: items[index]),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _DealCard extends StatelessWidget {
  const _DealCard({required this.deal});
  final DealSummary deal;

  @override
  Widget build(BuildContext context) => Card(
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => DealDetailPage(slug: deal.slug),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Stack(
                children: [
                  _DealImage(url: deal.image),
                  PositionedDirectional(
                    top: 12,
                    start: 12,
                    child: _Badge(
                      text: deal.typeLabel,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                  if (deal.daysRemaining <= 3)
                    const PositionedDirectional(
                      top: 12,
                      end: 12,
                      child: _Badge(
                        text: 'ينتهي قريبًا',
                        color: Colors.deepOrange,
                      ),
                    ),
                ],
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      deal.title,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w800,
                          ),
                    ),
                    if (deal.businessName.isNotEmpty) ...[
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(Icons.storefront_outlined, size: 18),
                          const SizedBox(width: 6),
                          Expanded(child: Text(deal.businessName)),
                        ],
                      ),
                    ],
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        if (deal.hasPrice) ...[
                          Text(
                            _money(deal.finalPrice!),
                            style:
                                Theme.of(context).textTheme.titleLarge?.copyWith(
                                      color: Theme.of(context).colorScheme.primary,
                                      fontWeight: FontWeight.w900,
                                    ),
                          ),
                          if (deal.hasDiscount) ...[
                            const SizedBox(width: 8),
                            Text(
                              _money(deal.originalPrice!),
                              style: const TextStyle(
                                decoration: TextDecoration.lineThrough,
                              ),
                            ),
                          ],
                        ] else
                          Text(
                            deal.typeLabel,
                            style: const TextStyle(fontWeight: FontWeight.w800),
                          ),
                        const Spacer(),
                        const Icon(Icons.schedule, size: 17),
                        const SizedBox(width: 4),
                        Text('متبقي ${deal.daysRemaining} يوم'),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
}

class _DealImage extends StatelessWidget {
  const _DealImage({this.url});
  final String? url;

  @override
  Widget build(BuildContext context) => SizedBox(
        height: 180,
        width: double.infinity,
        child: url == null || url!.isEmpty
            ? ColoredBox(
                color: Theme.of(context).colorScheme.primaryContainer,
                child: const Icon(Icons.local_offer_outlined, size: 52),
              )
            : Image.network(
                url!,
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => ColoredBox(
                  color: Theme.of(context).colorScheme.primaryContainer,
                  child: const Icon(Icons.local_offer_outlined, size: 52),
                ),
              ),
      );
}

class _Badge extends StatelessWidget {
  const _Badge({required this.text, required this.color});
  final String text;
  final Color color;

  @override
  Widget build(BuildContext context) => DecoratedBox(
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(999),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          child: Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.w800,
            ),
          ),
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
              Icon(icon, size: 52, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 16),
              Text(message, textAlign: TextAlign.center),
              if (action != null) ...[
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: action,
                  icon: const Icon(Icons.refresh),
                  label: const Text('إعادة المحاولة'),
                ),
              ],
            ],
          ),
        ),
      );
}

String _money(double value) =>
    '${NumberFormat('#,##0.##', 'ar').format(value)} ج.م';
