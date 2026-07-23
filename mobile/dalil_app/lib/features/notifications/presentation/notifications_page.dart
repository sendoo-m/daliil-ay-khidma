import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../app/providers.dart';
import '../../../core/network/api_failure.dart';
import '../data/notification_repository.dart';

class NotificationsPage extends ConsumerStatefulWidget {
  const NotificationsPage({super.key});

  @override
  ConsumerState<NotificationsPage> createState() => _NotificationsPageState();
}

class _NotificationsPageState extends ConsumerState<NotificationsPage> {
  List<AppNotification> _items = const [];
  bool _loading = true;
  bool _working = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final items = await ref.read(notificationRepositoryProvider).list();
      if (mounted) setState(() => _items = items);
    } catch (error) {
      if (mounted) setState(() => _error = ApiFailure.message(error));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          title: const Text('الإشعارات'),
          actions: [
            if (_items.any((item) => !item.isRead))
              TextButton(
                onPressed: _working ? null : _markAllRead,
                child: const Text('قراءة الكل'),
              ),
          ],
        ),
        body: _body(),
      );

  Widget _body() {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_error != null) {
      return _MessageState(
        icon: Icons.cloud_off_outlined,
        title: 'تعذر تحميل الإشعارات',
        message: _error!,
        actionLabel: 'إعادة المحاولة',
        onAction: _load,
      );
    }
    if (_items.isEmpty) {
      return _MessageState(
        icon: Icons.notifications_none_rounded,
        title: 'لا توجد إشعارات حتى الآن',
        message: 'ستظهر هنا أحدث العروض والتحديثات المهمة لحسابك.',
        actionLabel: 'تحديث',
        onAction: _load,
      );
    }
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.separated(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 28),
        itemCount: _items.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (_, index) {
          final item = _items[index];
          return Dismissible(
            key: ValueKey(item.id),
            direction: DismissDirection.endToStart,
            confirmDismiss: (_) => _confirmDelete(),
            onDismissed: (_) => _delete(item, index),
            background: Container(
              padding: const EdgeInsets.symmetric(horizontal: 22),
              alignment: Alignment.centerLeft,
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.errorContainer,
                borderRadius: BorderRadius.circular(18),
              ),
              child: Icon(
                Icons.delete_outline,
                color: Theme.of(context).colorScheme.onErrorContainer,
              ),
            ),
            child: _NotificationCard(
              item: item,
              onTap: item.isRead ? null : () => _markRead(item, index),
            ),
          );
        },
      ),
    );
  }

  Future<bool> _confirmDelete() async =>
      await showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('حذف الإشعار؟'),
          content: const Text('لن تتمكن من استعادته بعد الحذف.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('إلغاء'),
            ),
            FilledButton(
              onPressed: () => Navigator.pop(context, true),
              child: const Text('حذف'),
            ),
          ],
        ),
      ) ??
      false;

  Future<void> _markRead(AppNotification item, int index) async {
    setState(() => _items[index] = item.copyWith(isRead: true));
    try {
      final updated =
          await ref.read(notificationRepositoryProvider).markRead(item.id);
      if (mounted && index < _items.length) {
        setState(() => _items[index] = updated);
      }
    } catch (error) {
      if (!mounted) return;
      setState(() => _items[index] = item);
      _showError(error);
    }
  }

  Future<void> _markAllRead() async {
    final previous = _items;
    setState(() {
      _working = true;
      _items = _items.map((item) => item.copyWith(isRead: true)).toList();
    });
    try {
      await ref.read(notificationRepositoryProvider).markAllRead();
    } catch (error) {
      if (mounted) {
        setState(() => _items = previous);
        _showError(error);
      }
    } finally {
      if (mounted) setState(() => _working = false);
    }
  }

  Future<void> _delete(AppNotification item, int index) async {
    setState(() => _items.removeWhere((element) => element.id == item.id));
    try {
      await ref.read(notificationRepositoryProvider).delete(item.id);
    } catch (error) {
      if (!mounted) return;
      final restoredIndex = index > _items.length ? _items.length : index;
      setState(() => _items.insert(restoredIndex, item));
      _showError(error);
    }
  }

  void _showError(Object error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(ApiFailure.message(error))),
    );
  }
}

class _NotificationCard extends StatelessWidget {
  const _NotificationCard({required this.item, required this.onTap});

  final AppNotification item;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Material(
      color: item.isRead ? colors.surface : colors.primaryContainer.withValues(alpha: .4),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(18),
        side: BorderSide(color: colors.outlineVariant.withValues(alpha: .6)),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              CircleAvatar(
                backgroundColor: colors.primaryContainer,
                child: Icon(_iconFor(item.type), color: colors.primary),
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
                            item.title,
                            style: TextStyle(
                              fontWeight:
                                  item.isRead ? FontWeight.w600 : FontWeight.w900,
                            ),
                          ),
                        ),
                        if (!item.isRead)
                          Container(
                            width: 9,
                            height: 9,
                            decoration: BoxDecoration(
                              color: colors.primary,
                              shape: BoxShape.circle,
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(item.body, style: const TextStyle(height: 1.5)),
                    if (item.createdAt != null) ...[
                      const SizedBox(height: 9),
                      Text(
                        DateFormat('d MMM، h:mm a', 'ar')
                            .format(item.createdAt!.toLocal()),
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _iconFor(String type) => switch (type) {
        'deal' => Icons.local_offer_outlined,
        'business' => Icons.storefront_outlined,
        'review' => Icons.star_outline_rounded,
        'system' => Icons.settings_outlined,
        _ => Icons.notifications_none_rounded,
      };
}

class _MessageState extends StatelessWidget {
  const _MessageState({
    required this.icon,
    required this.title,
    required this.message,
    required this.actionLabel,
    required this.onAction,
  });

  final IconData icon;
  final String title;
  final String message;
  final String actionLabel;
  final VoidCallback onAction;

  @override
  Widget build(BuildContext context) => Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32),
          child: Column(
            children: [
              Icon(icon, size: 64, color: Theme.of(context).colorScheme.primary),
              const SizedBox(height: 18),
              Text(
                title,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w900,
                    ),
              ),
              const SizedBox(height: 8),
              Text(message, textAlign: TextAlign.center),
              const SizedBox(height: 20),
              OutlinedButton.icon(
                onPressed: onAction,
                icon: const Icon(Icons.refresh),
                label: Text(actionLabel),
              ),
            ],
          ),
        ),
      );
}
