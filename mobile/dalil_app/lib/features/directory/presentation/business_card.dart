import 'package:flutter/material.dart';

import '../data/business.dart';
import 'business_detail_page.dart';

class BusinessCard extends StatelessWidget {
  const BusinessCard({required this.business, super.key});
  final Business business;

  @override
  Widget build(BuildContext context) => Card(
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => BusinessDetailPage(slug: business.slug),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(14),
                  child: SizedBox.square(
                    dimension: 68,
                    child: business.logo == null || business.logo!.isEmpty
                        ? ColoredBox(
                            color:
                                Theme.of(context).colorScheme.primaryContainer,
                            child: const Icon(Icons.storefront, size: 30),
                          )
                        : Image.network(
                            business.logo!,
                            fit: BoxFit.cover,
                            errorBuilder: (_, __, ___) =>
                                const Icon(Icons.storefront, size: 30),
                          ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        business.nameAr,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          fontWeight: FontWeight.w800,
                          fontSize: 16,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(
                            Icons.star_rounded,
                            color: Color(0xFFFFB703),
                            size: 20,
                          ),
                          const SizedBox(width: 4),
                          Text(business.rating.toStringAsFixed(1)),
                          if (business.distanceKm != null) ...[
                            const Text('  •  '),
                            Text(
                              '${business.distanceKm!.toStringAsFixed(1)} كم',
                            ),
                          ],
                        ],
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
