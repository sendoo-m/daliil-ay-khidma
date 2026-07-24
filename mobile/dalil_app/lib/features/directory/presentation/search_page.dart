import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../../catalog/data/catalog_models.dart';
import '../../catalog/presentation/catalog_detail_pages.dart';
import '../../home/data/home_repository.dart';
import '../data/business.dart';
import 'business_card.dart';

enum _SearchKind { businesses, products }

class SearchPage extends ConsumerStatefulWidget {
  const SearchPage({
    this.embedded = false,
    this.initialQuery = '',
    this.initialCategoryId,
    super.key,
  });

  final bool embedded;
  final String initialQuery;
  final int? initialCategoryId;

  @override
  ConsumerState<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends ConsumerState<SearchPage> {
  late final TextEditingController _controller =
      TextEditingController(text: widget.initialQuery);
  late String _query = widget.initialQuery.trim();
  late int? _categoryId = widget.initialCategoryId;
  int? _governorateId;
  String? _businessType;
  String? _productType;
  double? _minRating;
  double? _minPrice;
  double? _maxPrice;
  var _kind = _SearchKind.businesses;
  var _comparePrices = false;
  var _revision = 0;
  Timer? _searchDebounce;

  bool get _hasFilters =>
      _categoryId != null ||
      _governorateId != null ||
      _businessType != null ||
      _productType != null ||
      _minRating != null ||
      _minPrice != null ||
      _maxPrice != null;

  @override
  void dispose() {
    _searchDebounce?.cancel();
    _controller.dispose();
    super.dispose();
  }

  void _scheduleSearch() {
    _searchDebounce?.cancel();
    _searchDebounce = Timer(const Duration(milliseconds: 450), _runSearch);
  }

  void _runSearch() {
    FocusScope.of(context).unfocus();
    setState(() {
      _query = _controller.text.trim();
      _revision++;
    });
  }

  void _clearFilters() => setState(() {
        _categoryId = widget.initialCategoryId;
        _governorateId = null;
        _businessType = null;
        _productType = null;
        _minRating = null;
        _minPrice = null;
        _maxPrice = null;
        _comparePrices = false;
        _revision++;
      });

  @override
  Widget build(BuildContext context) {
    final home = ref.watch(homeProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('البحث والمقارنة'),
        actions: [
          IconButton(
            tooltip: 'الفلاتر',
            onPressed: home.valueOrNull == null
                ? null
                : () => _showFilters(home.requireValue),
            icon: Badge(
              isLabelVisible: _hasFilters,
              child: const Icon(Icons.tune),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 10),
            child: SearchBar(
              controller: _controller,
              autoFocus: !widget.embedded,
              hintText: 'اسم محل، منتج أو خدمة',
              leading: const Icon(Icons.search),
              trailing: [
                IconButton(
                  tooltip: 'تنفيذ البحث',
                  onPressed: _runSearch,
                  icon: const Icon(Icons.arrow_back),
                ),
                if (_controller.text.isNotEmpty)
                  IconButton(
                    tooltip: 'مسح',
                    onPressed: () {
                      _controller.clear();
                      _runSearch();
                    },
                    icon: const Icon(Icons.close),
                  ),
              ],
              onChanged: (_) {
                setState(() {});
                _scheduleSearch();
              },
              onSubmitted: (_) => _runSearch(),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: SegmentedButton<_SearchKind>(
              showSelectedIcon: false,
              segments: const [
                ButtonSegment(
                  value: _SearchKind.businesses,
                  icon: Icon(Icons.storefront_outlined),
                  label: Text('المحلات'),
                ),
                ButtonSegment(
                  value: _SearchKind.products,
                  icon: Icon(Icons.shopping_bag_outlined),
                  label: Text('المنتجات والخدمات'),
                ),
              ],
              selected: {_kind},
              onSelectionChanged: (value) => setState(() {
                _kind = value.first;
                _comparePrices = false;
                _revision++;
              }),
            ),
          ),
          if (_hasFilters || _kind == _SearchKind.products)
            _ActiveActions(
              hasFilters: _hasFilters,
              comparing: _comparePrices,
              productsSelected: _kind == _SearchKind.products,
              onClear: _clearFilters,
              onCompare: () => setState(() {
                _comparePrices = !_comparePrices;
                _revision++;
              }),
            ),
          Expanded(
            child: (_query.isEmpty && !_hasFilters)
                ? const _SearchHint()
                : _kind == _SearchKind.businesses
                    ? _businessResults()
                    : _productResults(),
          ),
        ],
      ),
    );
  }

  Widget _businessResults() => FutureBuilder<List<Business>>(
        key: ValueKey('business-$_revision'),
        future: ref.read(businessRepositoryProvider).search(
              _query,
              categoryId: _categoryId,
              governorateId: _governorateId,
              businessType: _businessType,
              minRating: _minRating,
              ordering: _minRating == null ? '-is_featured' : '-average_rating',
            ),
        builder: (context, snapshot) => _ResultsFrame<Business>(
          snapshot: snapshot,
          itemBuilder: (item) => BusinessCard(business: item),
        ),
      );

  Widget _productResults() => FutureBuilder<List<ProductSummary>>(
        key: ValueKey('product-$_revision-$_comparePrices'),
        future: ref.read(catalogRepositoryProvider).searchProducts(
              _query,
              categoryId: _categoryId,
              governorateId: _governorateId,
              productType: _productType,
              minPrice: _minPrice,
              maxPrice: _maxPrice,
              ordering: _comparePrices ? 'price' : '-is_featured',
            ),
        builder: (context, snapshot) => _ResultsFrame<ProductSummary>(
          snapshot: snapshot,
          header: _comparePrices && (snapshot.data?.isNotEmpty ?? false)
              ? _ComparisonHeader(items: snapshot.data!)
              : null,
          itemBuilder: (item) => _ProductResultCard(
            item: item,
            cheapest: _comparePrices &&
                snapshot.data!.first.numericPrice == item.numericPrice,
          ),
        ),
      );

  Future<void> _showFilters(HomeData home) async {
    var categoryId = _categoryId;
    var governorateId = _governorateId;
    var businessType = _businessType;
    var productType = _productType;
    var minRating = _minRating;
    final minPriceController =
        TextEditingController(text: _minPrice?.toStringAsFixed(0) ?? '');
    final maxPriceController =
        TextEditingController(text: _maxPrice?.toStringAsFixed(0) ?? '');

    final apply = await showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      builder: (context) => StatefulBuilder(
        builder: (context, setModalState) => SafeArea(
          child: Padding(
            padding: EdgeInsets.fromLTRB(
              20,
              16,
              20,
              20 + MediaQuery.viewInsetsOf(context).bottom,
            ),
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'تصفية النتائج',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 18),
                  DropdownButtonFormField<int?>(
                    initialValue: categoryId,
                    decoration: const InputDecoration(labelText: 'القسم'),
                    items: [
                      const DropdownMenuItem(
                        value: null,
                        child: Text('كل الأقسام'),
                      ),
                      ...home.categories.map(
                        (item) => DropdownMenuItem(
                          value: item['id'] as int,
                          child: Text(item['name_ar'] as String? ?? ''),
                        ),
                      ),
                    ],
                    onChanged: (value) =>
                        setModalState(() => categoryId = value),
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField<int?>(
                    initialValue: governorateId,
                    decoration: const InputDecoration(labelText: 'المحافظة'),
                    items: [
                      const DropdownMenuItem(
                        value: null,
                        child: Text('كل المحافظات'),
                      ),
                      ...home.governorates.map(
                        (item) => DropdownMenuItem(
                          value: item['id'] as int,
                          child: Text(item['name_ar'] as String? ?? ''),
                        ),
                      ),
                    ],
                    onChanged: (value) =>
                        setModalState(() => governorateId = value),
                  ),
                  const SizedBox(height: 12),
                  if (_kind == _SearchKind.businesses) ...[
                    DropdownButtonFormField<String?>(
                      initialValue: businessType,
                      decoration: const InputDecoration(labelText: 'نوع النشاط'),
                      items: const [
                        DropdownMenuItem(value: null, child: Text('الكل')),
                        DropdownMenuItem(value: 'shop', child: Text('محلات')),
                        DropdownMenuItem(value: 'craft', child: Text('حرفيون')),
                        DropdownMenuItem(
                          value: 'public',
                          child: Text('خدمات عامة'),
                        ),
                      ],
                      onChanged: (value) =>
                          setModalState(() => businessType = value),
                    ),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<double?>(
                      initialValue: minRating,
                      decoration:
                          const InputDecoration(labelText: 'أقل تقييم'),
                      items: const [
                        DropdownMenuItem(value: null, child: Text('أي تقييم')),
                        DropdownMenuItem(value: 3, child: Text('3 نجوم فأكثر')),
                        DropdownMenuItem(value: 4, child: Text('4 نجوم فأكثر')),
                        DropdownMenuItem(
                          value: 4.5,
                          child: Text('4.5 نجمة فأكثر'),
                        ),
                      ],
                      onChanged: (value) =>
                          setModalState(() => minRating = value),
                    ),
                  ] else ...[
                    DropdownButtonFormField<String?>(
                      initialValue: productType,
                      decoration: const InputDecoration(labelText: 'النوع'),
                      items: const [
                        DropdownMenuItem(value: null, child: Text('الكل')),
                        DropdownMenuItem(
                          value: 'product',
                          child: Text('منتجات'),
                        ),
                        DropdownMenuItem(
                          value: 'service',
                          child: Text('خدمات'),
                        ),
                      ],
                      onChanged: (value) =>
                          setModalState(() => productType = value),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: minPriceController,
                            keyboardType: TextInputType.number,
                            decoration:
                                const InputDecoration(labelText: 'أقل سعر'),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: TextField(
                            controller: maxPriceController,
                            keyboardType: TextInputType.number,
                            decoration:
                                const InputDecoration(labelText: 'أعلى سعر'),
                          ),
                        ),
                      ],
                    ),
                  ],
                  const SizedBox(height: 20),
                  FilledButton(
                    onPressed: () => Navigator.pop(context, true),
                    child: const Text('عرض النتائج'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
    final minPrice = double.tryParse(minPriceController.text);
    final maxPrice = double.tryParse(maxPriceController.text);
    minPriceController.dispose();
    maxPriceController.dispose();
    if (apply != true || !mounted) return;
    setState(() {
      _categoryId = categoryId;
      _governorateId = governorateId;
      _businessType = businessType;
      _productType = productType;
      _minRating = minRating;
      _minPrice = minPrice;
      _maxPrice = maxPrice;
      _revision++;
    });
  }
}

class _ActiveActions extends StatelessWidget {
  const _ActiveActions({
    required this.hasFilters,
    required this.comparing,
    required this.productsSelected,
    required this.onClear,
    required this.onCompare,
  });

  final bool hasFilters;
  final bool comparing;
  final bool productsSelected;
  final VoidCallback onClear;
  final VoidCallback onCompare;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 10, 16, 0),
        child: Row(
          children: [
            if (productsSelected)
              FilterChip(
                selected: comparing,
                avatar: const Icon(Icons.compare_arrows, size: 18),
                label: Text(comparing ? 'إنهاء المقارنة' : 'مقارنة الأسعار'),
                onSelected: (_) => onCompare(),
              ),
            const Spacer(),
            if (hasFilters)
              TextButton.icon(
                onPressed: onClear,
                icon: const Icon(Icons.filter_alt_off_outlined),
                label: const Text('مسح الفلاتر'),
              ),
          ],
        ),
      );
}

class _ResultsFrame<T> extends StatelessWidget {
  const _ResultsFrame({
    required this.snapshot,
    required this.itemBuilder,
    this.header,
  });

  final AsyncSnapshot<List<T>> snapshot;
  final Widget Function(T item) itemBuilder;
  final Widget? header;

  @override
  Widget build(BuildContext context) {
    if (snapshot.connectionState != ConnectionState.done) {
      return const Center(child: CircularProgressIndicator());
    }
    if (snapshot.hasError) {
      return const _MessageState(
        icon: Icons.cloud_off_outlined,
        title: 'تعذر تنفيذ البحث',
        subtitle: 'تحقق من الاتصال وحاول مرة أخرى',
      );
    }
    final items = snapshot.data ?? const [];
    if (items.isEmpty) {
      return const _MessageState(
        icon: Icons.search_off,
        title: 'لا توجد نتائج',
        subtitle: 'جرّب كلمة أخرى أو وسّع نطاق الفلاتر',
      );
    }
    return ListView.separated(
      padding: const EdgeInsets.all(16),
      itemCount: items.length + (header == null ? 0 : 1),
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (_, index) {
        if (header != null && index == 0) return header!;
        return itemBuilder(items[index - (header == null ? 0 : 1)]);
      },
    );
  }
}

class _ComparisonHeader extends StatelessWidget {
  const _ComparisonHeader({required this.items});
  final List<ProductSummary> items;

  @override
  Widget build(BuildContext context) {
    final lowest = items.first.numericPrice;
    final highest = items.last.numericPrice;
    return Card(
      color: Theme.of(context).colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${items.length} أسعار مرتبة من الأقل',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            if (highest.isFinite && lowest.isFinite && highest > lowest)
              Text('يمكنك توفير ${(highest - lowest).toStringAsFixed(0)} ج.م'),
          ],
        ),
      ),
    );
  }
}

class _ProductResultCard extends StatelessWidget {
  const _ProductResultCard({required this.item, required this.cheapest});
  final ProductSummary item;
  final bool cheapest;

  @override
  Widget build(BuildContext context) => Card(
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => ProductDetailPage(slug: item.slug),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: item.image == null
                      ? Container(
                          width: 76,
                          height: 76,
                          color: Theme.of(context).colorScheme.surfaceContainer,
                          child: const Icon(Icons.inventory_2_outlined),
                        )
                      : Image.network(
                          item.image!,
                          width: 76,
                          height: 76,
                          fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) =>
                              const SizedBox.square(
                            dimension: 76,
                            child: Icon(Icons.broken_image_outlined),
                          ),
                        ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              item.name,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              style: Theme.of(context).textTheme.titleMedium,
                            ),
                          ),
                          if (cheapest)
                            const Chip(
                              label: Text('الأقل سعرًا'),
                              visualDensity: VisualDensity.compact,
                            ),
                        ],
                      ),
                      Text(
                        item.businessName,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                      const SizedBox(height: 6),
                      Text(
                        '${item.price} ج.م',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              color: Theme.of(context).colorScheme.primary,
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                    ],
                  ),
                ),
                const Icon(Icons.chevron_left),
              ],
            ),
          ),
        ),
      );
}

class _SearchHint extends StatelessWidget {
  const _SearchHint();

  @override
  Widget build(BuildContext context) => const _MessageState(
        icon: Icons.manage_search,
        title: 'ابحث في دليل أي خدمة',
        subtitle: 'اكتب اسم محل أو منتج أو خدمة، أو استخدم الفلاتر',
      );
}

class _MessageState extends StatelessWidget {
  const _MessageState({
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  final IconData icon;
  final String title;
  final String subtitle;

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 58,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 14),
              Text(title, style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 6),
              Text(
                subtitle,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ),
        ),
      );
}
