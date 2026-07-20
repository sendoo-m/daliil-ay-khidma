import 'package:flutter/material.dart';

import '../data/business.dart';
import 'business_detail_page.dart';

class BusinessCard extends StatelessWidget {
  const BusinessCard({required this.business, super.key});
  final Business business;

  @override
  Widget build(BuildContext context) => Card(
        child: ListTile(
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute<void>(
              builder: (_) => BusinessDetailPage(slug: business.slug),
            ),
          ),
          leading: business.logo == null
              ? const CircleAvatar(child: Icon(Icons.storefront))
              : CircleAvatar(backgroundImage: NetworkImage(business.logo!)),
          title: Text(business.nameAr),
          subtitle: Text('⭐ ${business.rating.toStringAsFixed(1)}'),
        ),
      );
}
