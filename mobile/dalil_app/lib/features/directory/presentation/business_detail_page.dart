import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../../reviews/presentation/reviews_page.dart';

class BusinessDetailPage extends ConsumerStatefulWidget {
  const BusinessDetailPage({required this.slug, super.key});
  final String slug;
  @override
  ConsumerState<BusinessDetailPage> createState() => _BusinessDetailPageState();
}

class _BusinessDetailPageState extends ConsumerState<BusinessDetailPage> {
  bool _favorite = false;

  @override
  Widget build(BuildContext context) => FutureBuilder(
        future: ref.read(businessRepositoryProvider).detail(widget.slug),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
          final business = snapshot.data!;
          return Scaffold(
            appBar: AppBar(
              title: Text(business.nameAr),
              actions: [
                IconButton(
                  icon: Icon(
                    _favorite ? Icons.favorite : Icons.favorite_border,
                  ),
                  onPressed: () async {
                    final value = await ref
                        .read(businessRepositoryProvider)
                        .toggleFavorite(business.id);
                    if (mounted) {
                      setState(() => _favorite = value);
                    }
                  },
                ),
              ],
            ),
            body: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                if (business.logo != null)
                  Image.network(
                    business.logo!,
                    height: 180,
                    fit: BoxFit.contain,
                  ),
                const SizedBox(height: 16),
                Text(
                  business.nameAr,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                Text('⭐ ${business.rating.toStringAsFixed(1)}'),
                const SizedBox(height: 16),
                Text(business.description),
                ListTile(
                  leading: const Icon(Icons.reviews_outlined),
                  title: const Text('عرض التقييمات'),
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (_) => ReviewsPage(businessId: business.id),
                    ),
                  ),
                ),
                if (business.phone.isNotEmpty)
                  ListTile(
                    leading: const Icon(Icons.phone),
                    title: Text(business.phone),
                  ),
              ],
            ),
          );
        },
      );
}
