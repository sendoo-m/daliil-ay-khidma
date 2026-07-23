import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:maplibre_gl/maplibre_gl.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../app/providers.dart';
import '../../auth/presentation/login_page.dart';
import '../../reviews/presentation/reviews_page.dart';
import '../data/business.dart';

const _openFreeMapStyle = 'https://tiles.openfreemap.org/styles/liberty';

class BusinessDetailPage extends ConsumerStatefulWidget {
  const BusinessDetailPage({required this.slug, super.key});
  final String slug;

  @override
  ConsumerState<BusinessDetailPage> createState() => _BusinessDetailPageState();
}

class _BusinessDetailPageState extends ConsumerState<BusinessDetailPage> {
  late Future<Business> _future;
  bool _favorite = false;
  bool _savingFavorite = false;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<Business> _load() =>
      ref.read(businessRepositoryProvider).detail(widget.slug).then((business) {
        _favorite = business.isFavorite;
        return business;
      });

  @override
  Widget build(BuildContext context) => FutureBuilder<Business>(
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
          return _detailScaffold(snapshot.data!);
        },
      );

  Widget _detailScaffold(Business business) => Scaffold(
        body: CustomScrollView(
          slivers: [
            SliverAppBar.large(
              expandedHeight: 265,
              pinned: true,
              title: Text(business.displayName),
              actions: [
                IconButton(
                  tooltip: _favorite ? 'إزالة من المفضلة' : 'إضافة للمفضلة',
                  onPressed:
                      _savingFavorite ? null : () => _toggleFavorite(business),
                  icon: _savingFavorite
                      ? const SizedBox.square(
                          dimension: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : Icon(
                          _favorite ? Icons.favorite : Icons.favorite_border,
                        ),
                ),
              ],
              flexibleSpace: FlexibleSpaceBar(
                background: _HeroImage(business: business),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 18, 16, 32),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  _BusinessHeading(business: business),
                  if (business.hasContactMethods) ...[
                    const SizedBox(height: 18),
                    _ContactActions(
                      business: business,
                      onLaunch: _launch,
                    ),
                  ],
                  if (business.description.isNotEmpty) ...[
                    const SizedBox(height: 24),
                    _Section(
                      title: 'عن المكان',
                      icon: Icons.info_outline,
                      child: Text(
                        business.description,
                        style: const TextStyle(height: 1.65),
                      ),
                    ),
                  ],
                  if (business.address.isNotEmpty || business.area.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _Section(
                      title: 'العنوان',
                      icon: Icons.location_on_outlined,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          if (business.address.isNotEmpty)
                            Text(business.address),
                          if (business.area.isNotEmpty)
                            Padding(
                              padding: const EdgeInsets.only(top: 4),
                              child: Text(
                                business.area,
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                            ),
                        ],
                      ),
                    ),
                  ],
                  if (business.hasCoordinates || business.locationUrl.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _LocationSection(
                      business: business,
                      onDirections: () => _openDirections(business),
                    ),
                  ],
                  if (business.workingHours.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    _Section(
                      title: 'ساعات العمل',
                      icon: Icons.schedule_outlined,
                      child: Text(
                        business.workingHours,
                        style: const TextStyle(height: 1.6),
                      ),
                    ),
                  ],
                  if (business.images.isNotEmpty) ...[
                    const SizedBox(height: 24),
                    _Gallery(images: business.images),
                  ],
                  if (business.hasSocialLinks) ...[
                    const SizedBox(height: 16),
                    _SocialLinks(business: business, onLaunch: _launch),
                  ],
                  const SizedBox(height: 16),
                  Card(
                    child: ListTile(
                      leading: const Icon(Icons.reviews_outlined),
                      title: const Text('تقييمات الزوار'),
                      subtitle: Text('${business.totalReviews} تقييم'),
                      trailing: const Icon(Icons.chevron_left),
                      onTap: () => Navigator.of(context).push(
                        MaterialPageRoute<void>(
                          builder: (_) => ReviewsPage(
                            businessId: business.id,
                            businessName: business.displayName,
                            averageRating: business.rating,
                            totalReviews: business.totalReviews,
                          ),
                        ),
                      ),
                    ),
                  ),
                ]),
              ),
            ),
          ],
        ),
      );

  Future<void> _toggleFavorite(Business business) async {
    final isAuthenticated =
        ref.read(authControllerProvider).valueOrNull ?? false;
    if (!isAuthenticated) {
      await Navigator.of(context).push(
        MaterialPageRoute<void>(builder: (_) => const LoginPage()),
      );
      return;
    }
    setState(() => _savingFavorite = true);
    try {
      final value = await ref
          .read(businessRepositoryProvider)
          .toggleFavorite(business.id);
      if (mounted) {
        setState(() => _favorite = value);
        _showMessage(
          value ? 'تمت الإضافة إلى المفضلة' : 'تمت الإزالة من المفضلة',
        );
      }
    } catch (_) {
      if (mounted) _showMessage('تعذر تحديث المفضلة، حاول مرة أخرى');
    } finally {
      if (mounted) setState(() => _savingFavorite = false);
    }
  }

  Future<void> _launch(Uri uri) async {
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication) && mounted) {
      _showMessage('لا يوجد تطبيق مناسب لفتح هذا الرابط');
    }
  }

  Future<void> _openDirections(Business business) async {
    if (business.hasCoordinates) {
      await _launch(
        Uri.https('www.google.com', '/maps/dir/', {
          'api': '1',
          'destination': '${business.latitude},${business.longitude}',
        }),
      );
    } else if (business.locationUrl.isNotEmpty) {
      await _launch(_webUri(business.locationUrl));
    }
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }
}

class _HeroImage extends StatelessWidget {
  const _HeroImage({required this.business});
  final Business business;

  @override
  Widget build(BuildContext context) {
    final image = business.coverImage ?? business.logo;
    return ColoredBox(
      color: Theme.of(context).colorScheme.surfaceContainer,
      child: image == null || image.isEmpty
          ? const Center(
              child: Icon(Icons.storefront_outlined, size: 72),
            )
          : Image.network(
              image,
              fit: BoxFit.cover,
              errorBuilder: (_, __, ___) => const Center(
                child: Icon(Icons.storefront_outlined, size: 72),
              ),
            ),
    );
  }
}

class _BusinessHeading extends StatelessWidget {
  const _BusinessHeading({required this.business});
  final Business business;

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  business.displayName,
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.w900,
                      ),
                ),
              ),
              if (business.isVerified)
                Icon(
                  Icons.verified,
                  color: Theme.of(context).colorScheme.primary,
                ),
            ],
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 10,
            runSpacing: 8,
            children: [
              if (business.categoryName.isNotEmpty)
                Chip(
                  avatar: const Icon(Icons.category_outlined, size: 18),
                  label: Text(business.categoryName),
                ),
              Chip(
                avatar: const Icon(Icons.star, size: 18, color: Colors.amber),
                label: Text(
                  '${business.rating.toStringAsFixed(1)}'
                  ' (${business.totalReviews})',
                ),
              ),
            ],
          ),
        ],
      );
}

class _ContactActions extends StatelessWidget {
  const _ContactActions({required this.business, required this.onLaunch});
  final Business business;
  final Future<void> Function(Uri uri) onLaunch;

  @override
  Widget build(BuildContext context) {
    final actions = <Widget>[
      if (business.phone.isNotEmpty)
        _ActionButton(
          icon: Icons.phone_outlined,
          label: 'اتصال',
          onTap: () => onLaunch(Uri(scheme: 'tel', path: business.phone)),
        ),
      if (business.whatsapp.isNotEmpty)
        _ActionButton(
          icon: Icons.chat_outlined,
          label: 'واتساب',
          onTap: () => onLaunch(
            Uri.https('wa.me', '/${_internationalPhone(business.whatsapp)}'),
          ),
        ),
      if (business.email.isNotEmpty)
        _ActionButton(
          icon: Icons.email_outlined,
          label: 'بريد',
          onTap: () => onLaunch(Uri(scheme: 'mailto', path: business.email)),
        ),
      if (business.website.isNotEmpty)
        _ActionButton(
          icon: Icons.language,
          label: 'الموقع',
          onTap: () => onLaunch(_webUri(business.website)),
        ),
    ];
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (var i = 0; i < actions.length; i++) ...[
          if (i > 0) const SizedBox(width: 8),
          Expanded(child: actions[i]),
        ],
      ],
    );
  }
}

class _ActionButton extends StatelessWidget {
  const _ActionButton({
    required this.icon,
    required this.label,
    required this.onTap,
  });
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Ink(
          padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 4),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            children: [
              Icon(icon, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 6),
              Text(label, maxLines: 1),
            ],
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

class _LocationSection extends StatelessWidget {
  const _LocationSection({
    required this.business,
    required this.onDirections,
  });
  final Business business;
  final VoidCallback onDirections;

  @override
  Widget build(BuildContext context) => Card(
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (business.hasCoordinates)
              SizedBox(
                height: 210,
                child: IgnorePointer(
                  child: _BusinessMap(
                    latitude: business.latitude!,
                    longitude: business.longitude!,
                  ),
                ),
              ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: FilledButton.icon(
                onPressed: onDirections,
                icon: const Icon(Icons.directions_outlined),
                label: const Text('فتح الاتجاهات على الخريطة'),
              ),
            ),
          ],
        ),
      );
}

class _BusinessMap extends StatefulWidget {
  const _BusinessMap({required this.latitude, required this.longitude});
  final double latitude;
  final double longitude;

  @override
  State<_BusinessMap> createState() => _BusinessMapState();
}

class _BusinessMapState extends State<_BusinessMap> {
  MapLibreMapController? _controller;
  bool _styleLoaded = false;
  bool _markerAdded = false;

  @override
  Widget build(BuildContext context) => MapLibreMap(
        styleString: _openFreeMapStyle,
        initialCameraPosition: CameraPosition(
          target: LatLng(widget.latitude, widget.longitude),
          zoom: 15,
        ),
        compassEnabled: false,
        rotateGesturesEnabled: false,
        scrollGesturesEnabled: false,
        tiltGesturesEnabled: false,
        zoomGesturesEnabled: false,
        onMapCreated: (controller) {
          _controller = controller;
          _addMarker();
        },
        onStyleLoadedCallback: () {
          _styleLoaded = true;
          _addMarker();
        },
      );

  Future<void> _addMarker() async {
    final controller = _controller;
    if (controller == null || !_styleLoaded || _markerAdded) return;
    _markerAdded = true;
    await controller.addCircle(
      CircleOptions(
        geometry: LatLng(widget.latitude, widget.longitude),
        circleRadius: 10,
        circleColor: '#006C51',
        circleStrokeColor: '#FFFFFF',
        circleStrokeWidth: 4,
      ),
    );
  }
}

class _Gallery extends StatelessWidget {
  const _Gallery({required this.images});
  final List<BusinessImage> images;

  @override
  Widget build(BuildContext context) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('معرض الصور', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          SizedBox(
            height: 180,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: images.length,
              separatorBuilder: (_, __) => const SizedBox(width: 10),
              itemBuilder: (_, index) {
                final item = images[index];
                return ClipRRect(
                  borderRadius: BorderRadius.circular(18),
                  child: Image.network(
                    item.url,
                    width: 250,
                    fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) => const SizedBox(
                      width: 250,
                      child: ColoredBox(
                        color: Color(0xFFE7ECEA),
                        child: Icon(Icons.broken_image_outlined),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      );
}

class _SocialLinks extends StatelessWidget {
  const _SocialLinks({required this.business, required this.onLaunch});
  final Business business;
  final Future<void> Function(Uri uri) onLaunch;

  @override
  Widget build(BuildContext context) {
    final links = [
      if (business.facebook.isNotEmpty)
        ('فيسبوك', Icons.facebook_outlined, business.facebook),
      if (business.instagram.isNotEmpty)
        ('إنستغرام', Icons.camera_alt_outlined, business.instagram),
      if (business.twitter.isNotEmpty)
        ('X', Icons.alternate_email, business.twitter),
      if (business.tiktok.isNotEmpty)
        ('تيك توك', Icons.music_note_outlined, business.tiktok),
    ];
    return _Section(
      title: 'تابعنا',
      icon: Icons.share_outlined,
      child: Wrap(
        spacing: 8,
        runSpacing: 8,
        children: links
            .map(
              (link) => ActionChip(
                avatar: Icon(link.$2, size: 18),
                label: Text(link.$1),
                onPressed: () => onLaunch(_webUri(link.$3)),
              ),
            )
            .toList(growable: false),
      ),
    );
  }
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
              const Icon(Icons.cloud_off_outlined, size: 56),
              const SizedBox(height: 12),
              const Text('تعذر تحميل بيانات المحل'),
              const SizedBox(height: 12),
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

Uri _webUri(String value) {
  final parsed = Uri.tryParse(value);
  if (parsed != null && parsed.hasScheme) return parsed;
  return Uri.parse('https://$value');
}

String _internationalPhone(String value) {
  final digits = value.replaceAll(RegExp(r'\D'), '');
  if (digits.startsWith('20')) return digits;
  if (digits.startsWith('0')) return '20${digits.substring(1)}';
  return digits;
}
