import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';

class ReviewsPage extends ConsumerStatefulWidget {
  const ReviewsPage({required this.businessId, super.key});
  final int businessId;
  @override
  ConsumerState<ReviewsPage> createState() => _ReviewsPageState();
}

class _ReviewsPageState extends ConsumerState<ReviewsPage> {
  int _reload = 0;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('التقييمات')),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: _addReview,
          icon: const Icon(Icons.rate_review_outlined),
          label: const Text('أضف تقييمًا'),
        ),
        body: FutureBuilder(
          key: ValueKey(_reload),
          future: ref.read(reviewRepositoryProvider).list(widget.businessId),
          builder: (context, snapshot) {
            if (!snapshot.hasData) {
              return const Center(child: CircularProgressIndicator());
            }
            final items = snapshot.data!;
            if (items.isEmpty) {
              return const Center(child: Text('لا توجد تقييمات معتمدة بعد'));
            }
            return ListView.builder(
              itemCount: items.length,
              itemBuilder: (_, index) {
                final item = items[index];
                return ListTile(
                  leading: CircleAvatar(child: Text('${item.rating}')),
                  title: Text(item.username),
                  subtitle: Text(item.comment),
                );
              },
            );
          },
        ),
      );

  Future<void> _addReview() async {
    var rating = 5;
    final comment = TextEditingController();
    final submitted = await showDialog<bool>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('تقييم النشاط'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButton<int>(
                value: rating,
                items: List.generate(
                  5,
                  (index) => DropdownMenuItem(
                    value: index + 1,
                    child: Text('${index + 1} نجوم'),
                  ),
                ),
                onChanged: (value) => setDialogState(() => rating = value ?? 5),
              ),
              TextField(
                controller: comment,
                maxLines: 3,
                decoration: const InputDecoration(labelText: 'تعليقك'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('إلغاء'),
            ),
            FilledButton(
              onPressed: () => Navigator.pop(context, true),
              child: const Text('إرسال'),
            ),
          ],
        ),
      ),
    );
    if (submitted == true) {
      await ref.read(reviewRepositoryProvider).create(
            businessId: widget.businessId,
            rating: rating,
            comment: comment.text,
          );
      if (mounted) setState(() => _reload++);
    }
    comment.dispose();
  }
}
