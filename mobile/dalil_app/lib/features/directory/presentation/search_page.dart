import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import 'business_card.dart';

class SearchPage extends ConsumerStatefulWidget {
  const SearchPage({super.key});
  @override
  ConsumerState<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends ConsumerState<SearchPage> {
  String _query = '';

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: TextField(
            autofocus: true,
            textInputAction: TextInputAction.search,
            decoration: const InputDecoration(hintText: 'ابحث عن خدمة أو محل'),
            onSubmitted: (value) => setState(() => _query = value.trim()),
          ),
        ),
        body: _query.isEmpty
            ? const Center(child: Text('اكتب ما تريد البحث عنه'))
            : FutureBuilder(
                future: ref.read(businessRepositoryProvider).search(_query),
                builder: (context, snapshot) {
                  if (snapshot.connectionState != ConnectionState.done) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  if (snapshot.hasError) {
                    return const Center(child: Text('تعذر تنفيذ البحث'));
                  }
                  final items = snapshot.data ?? const [];
                  if (items.isEmpty) return const Center(child: Text('لا توجد نتائج'));
                  return ListView.builder(
                    padding: const EdgeInsets.all(12),
                    itemCount: items.length,
                    itemBuilder: (_, index) => BusinessCard(business: items[index]),
                  );
                },
              ),
      );
}
