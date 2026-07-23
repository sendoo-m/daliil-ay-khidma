import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import 'business_card.dart';

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
  late String _query = widget.initialQuery;
  late final TextEditingController _controller =
      TextEditingController(text: widget.initialQuery);

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: widget.embedded
            ? AppBar(title: const Text('البحث'))
            : AppBar(title: const Text('البحث')),
        body: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
              child: TextField(
                controller: _controller,
                autofocus: !widget.embedded,
                textInputAction: TextInputAction.search,
                decoration: InputDecoration(
                  hintText: 'ابحث عن خدمة أو محل',
                  prefixIcon: const Icon(Icons.search),
                  suffixIcon: _query.isEmpty
                      ? null
                      : IconButton(
                          icon: const Icon(Icons.close),
                          onPressed: () {
                            _controller.clear();
                            setState(() => _query = '');
                          },
                        ),
                ),
                onSubmitted: (value) =>
                    setState(() => _query = value.trim()),
              ),
            ),
            Expanded(
              child: _query.isEmpty && widget.initialCategoryId == null
                  ? const _SearchHint()
                  : FutureBuilder(
                      future:
                          ref.read(businessRepositoryProvider).search(
                                _query,
                                categoryId: widget.initialCategoryId,
                              ),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState != ConnectionState.done) {
                          return const Center(
                            child: CircularProgressIndicator(),
                          );
                        }
                        if (snapshot.hasError) {
                          return const Center(
                            child: Text('تعذر تنفيذ البحث'),
                          );
                        }
                        final items = snapshot.data ?? const [];
                        if (items.isEmpty) {
                          return const Center(child: Text('لا توجد نتائج'));
                        }
                        return ListView.separated(
                          padding: const EdgeInsets.all(16),
                          itemCount: items.length,
                          separatorBuilder: (_, __) =>
                              const SizedBox(height: 12),
                          itemBuilder: (_, index) =>
                              BusinessCard(business: items[index]),
                        );
                      },
                    ),
            ),
          ],
        ),
      );
}

class _SearchHint extends StatelessWidget {
  const _SearchHint();

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.manage_search,
                size: 56,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 16),
              const Text(
                'اكتب اسم المحل أو الخدمة التي تبحث عنها',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
}
