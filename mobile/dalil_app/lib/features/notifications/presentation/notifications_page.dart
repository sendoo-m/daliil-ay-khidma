import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';

class NotificationsPage extends ConsumerWidget {
  const NotificationsPage({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) => Scaffold(
        appBar: AppBar(title: const Text('الإشعارات')),
        body: FutureBuilder(
          future: ref.read(notificationRepositoryProvider).list(),
          builder: (context, snapshot) {
            if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
            final items = snapshot.data!;
            if (items.isEmpty) return const Center(child: Text('لا توجد إشعارات'));
            return ListView.builder(
              itemCount: items.length,
              itemBuilder: (_, index) {
                final item = items[index];
                return ListTile(
                  leading: Icon(item.isRead ? Icons.notifications_none : Icons.notifications_active),
                  title: Text(item.title),
                  subtitle: Text(item.body),
                  onTap: () => ref.read(notificationRepositoryProvider).markRead(item.id),
                );
              },
            );
          },
        ),
      );
}
