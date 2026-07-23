import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../app/providers.dart';
import '../../auth/presentation/login_page.dart';
import '../../directory/presentation/business_detail_page.dart';
import '../data/catalog_models.dart';

class ProductDetailPage extends ConsumerStatefulWidget {
  const ProductDetailPage({required this.slug, super.key});
  final String slug;

  @override
  ConsumerState<ProductDetailPage> createState() => _ProductDetailPageState();
}

class _ProductDetailPageState extends ConsumerState<ProductDetailPage> {
  late Future<ProductDetail> _future;
  int _selectedImage = 0;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<ProductDetail> _load() =>
      ref.read(catalogRepositoryProvider).productDetail(widget.slug);

  @override
  Widget build(BuildContext context) => FutureBuilder<ProductDetail>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
          if (snapshot.hasError || !snapshot.hasData) {
            return Scaffold(
              appBar: AppBar(),
              body: _ErrorState(
                onRetry: () => setState(() => _future = _load()),
              ),
            );
          }
          return _ProductScaffold(
            product: snapshot.data!,
            selectedImage: _selectedImage,
            onSelectImage: (index) => setState(() => _selectedImage = index),
          );
        },
      );
}

class _ProductScaffold extends StatelessWidget {
  const _ProductScaffold({
    required this.product,
    required this.selectedImage,
    required this.onSelectImage,
  });

  final ProductDetail product;
  final int selectedImage;
  final ValueChanged<int> onSelectImage;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: Text('تفاصيل ${product.typeLabel}'),
        ),
        body: ListView(
          padding: const EdgeInsets.only(bottom: 32),
          children: [
            _ProductGallery(
              product: product,
              selectedImage: selectedImage,
              onSelectImage: onSelectImage,
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _ProductHeading(product: product),
                  const SizedBox(height: 18),
                  _PriceCard(product: product),
                  if (product.description.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _Section(
                      title: 'التفاصيل',
                      icon: Icons.description_outlined,
                      child: Text(
                        product.description,
                        style: const TextStyle(height: 1.65),
                      ),
                    ),
                  ],
                  if (product.hasDelivery) ...[
                    const SizedBox(height: 16),
                    _DeliveryCard(product: product),
                  ],
                  if (product.hasBusiness) ...[
                    const SizedBox(height: 16),
                    _BusinessCard(product: product),
                  ],
                ],
              ),
            ),
          ],
        ),
      );
}

class _ProductGallery extends StatelessWidget {
  const _ProductGallery({
    required this.product,
    required this.selectedImage,
    required this.onSelectImage,
  });

  final ProductDetail product;
  final int selectedImage;
  final ValueChanged<int> onSelectImage;

  @override
  Widget build(BuildContext context) {
    final images = product.images;
    final safeIndex = selectedImage < images.length ? selectedImage : 0;
    return Column(
      children: [
        AspectRatio(
          aspectRatio: 4 / 3,
          child: ColoredBox(
            color: Theme.of(context).colorScheme.surfaceContainer,
            child: images.isEmpty
                ? Icon(
                    product.productType == 'service'
                        ? Icons.design_services_outlined
                        : Icons.inventory_2_outlined,
                    size: 80,
                  )
                : Image.network(
                    images[safeIndex].url,
                    fit: BoxFit.cover,
                    semanticLabel: images[safeIndex].altText,
                    errorBuilder: (_, __, ___) => const Center(
                      child: Icon(Icons.broken_image_outlined, size: 72),
                    ),
                  ),
          ),
        ),
        if (images.length > 1)
          SizedBox(
            height: 88,
            child: ListView.separated(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
              scrollDirection: Axis.horizontal,
              itemCount: images.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, index) => InkWell(
                onTap: () => onSelectImage(index),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  width: 72,
                  clipBehavior: Clip.antiAlias,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: index == safeIndex
                          ? Theme.of(context).colorScheme.primary
                          : Theme.of(context).colorScheme.outlineVariant,
                      width: index == safeIndex ? 2.5 : 1,
                    ),
                  ),
                  child: Image.network(
                    images[index].url,
                    fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) =>
                        const Icon(Icons.broken_image_outlined),
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }
}

class _ProductHeading extends StatelessWidget {
  const _ProductHeading({required this.product});
  final ProductDetail product;

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Text(
                  product.name,
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.w900,
                      ),
                ),
              ),
              if (product.isFeatured)
                const Padding(
                  padding: EdgeInsetsDirectional.only(start: 8),
                  child: Icon(Icons.workspace_premium, color: Colors.amber),
                ),
            ],
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              Chip(
                avatar: Icon(
                  product.productType == 'service'
                      ? Icons.design_services_outlined
                      : Icons.inventory_2_outlined,
                  size: 18,
                ),
                label: Text(product.typeLabel),
              ),
              Chip(
                avatar: Icon(
                  product.canOrder
                      ? Icons.check_circle_outline
                      : Icons.cancel_outlined,
                  size: 18,
                  color: product.canOrder ? Colors.green : Colors.red,
                ),
                label: Text(product.canOrder ? 'متاح الآن' : 'غير متاح حاليًا'),
              ),
              if (product.viewCount > 0)
                Chip(
                  avatar: const Icon(Icons.visibility_outlined, size: 18),
                  label: Text('${product.viewCount} مشاهدة'),
                ),
            ],
          ),
        ],
      );
}

class _PriceCard extends StatelessWidget {
  const _PriceCard({required this.product});
  final ProductDetail product;

  @override
  Widget build(BuildContext context) => Card(
        color: Theme.of(context).colorScheme.primaryContainer,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      _money(product.price),
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            color: Theme.of(context).colorScheme.primary,
                            fontWeight: FontWeight.w900,
                          ),
                    ),
                  ),
                  if (product.hasDiscount)
                    Badge(
                      label: Text(
                        'خصم ${product.discountPercentage.toStringAsFixed(0)}٪',
                      ),
                    ),
                ],
              ),
              if (product.hasDiscount) ...[
                const SizedBox(height: 4),
                Text(
                  _money(product.oldPrice!),
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        decoration: TextDecoration.lineThrough,
                      ),
                ),
              ],
              if (product.productType == 'product' &&
                  product.stockQuantity != null) ...[
                const SizedBox(height: 12),
                Text(
                  product.stockQuantity! > 0
                      ? 'متبقي ${product.stockQuantity} في المخزون'
                      : 'نفد المخزون',
                ),
              ],
            ],
          ),
        ),
      );
}

class _DeliveryCard extends StatelessWidget {
  const _DeliveryCard({required this.product});
  final ProductDetail product;

  @override
  Widget build(BuildContext context) => _Section(
        title: 'التوصيل',
        icon: Icons.local_shipping_outlined,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              product.deliveryCost == null || product.deliveryCost == 0
                  ? 'التوصيل مجاني'
                  : 'تكلفة التوصيل: ${_money(product.deliveryCost!)}',
            ),
            if (product.deliveryTime.isNotEmpty) ...[
              const SizedBox(height: 6),
              Text('المدة المتوقعة: ${product.deliveryTime}'),
            ],
          ],
        ),
      );
}

class _BusinessCard extends StatelessWidget {
  const _BusinessCard({required this.product});
  final ProductDetail product;

  @override
  Widget build(BuildContext context) => Card(
        child: ListTile(
          contentPadding: const EdgeInsets.all(14),
          leading: CircleAvatar(
            child: Text(
              product.businessName.characters.first,
              style: const TextStyle(fontWeight: FontWeight.w800),
            ),
          ),
          title: const Text('مقدم بواسطة'),
          subtitle: Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(
              product.businessName,
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ),
          trailing: const Icon(Icons.chevron_left),
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => BusinessDetailPage(slug: product.businessSlug),
            ),
          ),
        ),
      );
}

class _Section extends StatelessWidget {
  const _Section({
    required this.title,
    required this.icon,
    required this.child,
  });

  final String title;
  final IconData icon;
  final Widget child;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Icon(icon, color: Theme.of(context).colorScheme.primary),
                  const SizedBox(width: 8),
                  Text(title, style: Theme.of(context).textTheme.titleMedium),
                ],
              ),
              const SizedBox(height: 12),
              child,
            ],
          ),
        ),
      );
}

class _ErrorState extends StatelessWidget {
  const _ErrorState({required this.onRetry});
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.cloud_off_outlined, size: 64),
              const SizedBox(height: 14),
              Text(
                'تعذر تحميل التفاصيل',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              const Text('تحقق من الاتصال ثم حاول مرة أخرى'),
              const SizedBox(height: 18),
              FilledButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: const Text('إعادة المحاولة'),
              ),
            ],
          ),
        ),
      );
}

String _money(double value) =>
    '${NumberFormat('#,##0.##', 'ar').format(value)} ج.م';

class DealDetailPage extends ConsumerWidget {
  const DealDetailPage({required this.slug, super.key});
  final String slug;

  @override
  Widget build(BuildContext context, WidgetRef ref) => _JsonDealPage(
        future: ref.read(catalogRepositoryProvider).dealDetail(slug),
        onClaim: () async {
          final isAuthenticated =
              ref.read(authControllerProvider).valueOrNull ?? false;
          if (!isAuthenticated) {
            await Navigator.of(context).push(
              MaterialPageRoute<void>(builder: (_) => const LoginPage()),
            );
            return;
          }
          final message =
              await ref.read(catalogRepositoryProvider).claimDeal(slug);
          if (context.mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(message)),
            );
          }
        },
      );
}

class _JsonDealPage extends StatelessWidget {
  const _JsonDealPage({required this.future, required this.onClaim});
  final Future<Map<String, dynamic>> future;
  final VoidCallback onClaim;

  @override
  Widget build(BuildContext context) => FutureBuilder<Map<String, dynamic>>(
        future: future,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
          final item = snapshot.data!;
          return Scaffold(
            appBar: AppBar(title: Text('${item['title_ar'] ?? ''}')),
            body: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                if (item['image'] != null)
                  Image.network('${item['image']}', height: 200),
                const SizedBox(height: 16),
                Text(
                  '${item['title_ar'] ?? ''}',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 12),
                Text('${item['description_ar'] ?? ''}'),
                const SizedBox(height: 20),
                FilledButton.icon(
                  icon: const Icon(Icons.redeem),
                  label: const Text('المطالبة بالعرض'),
                  onPressed: onClaim,
                ),
              ],
            ),
          );
        },
      );
}
