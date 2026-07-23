import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../data/profile_repository.dart';

class ProfilePage extends ConsumerStatefulWidget {
  const ProfilePage({this.embedded = false, super.key});
  final bool embedded;
  @override
  ConsumerState<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends ConsumerState<ProfilePage> {
  final _firstName = TextEditingController();
  final _lastName = TextEditingController();
  final _email = TextEditingController();
  final _phone = TextEditingController();
  bool _loaded = false;

  @override
  void dispose() {
    for (final item in [_firstName, _lastName, _email, _phone]) {
      item.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: !widget.embedded,
          title: const Text('الملف الشخصي'),
          actions: [
            IconButton(
              tooltip: 'تسجيل الخروج',
              onPressed: () =>
                  ref.read(authControllerProvider.notifier).logout(),
              icon: const Icon(Icons.logout),
            ),
          ],
        ),
        body: FutureBuilder<UserProfile>(
          future: ref.read(profileRepositoryProvider).get(),
          builder: (context, snapshot) {
            if (!snapshot.hasData) {
              return const Center(child: CircularProgressIndicator());
            }
            if (!_loaded) {
              final profile = snapshot.data!;
              _firstName.text = profile.firstName;
              _lastName.text = profile.lastName;
              _email.text = profile.email;
              _phone.text = profile.phone;
              _loaded = true;
            }
            return ListView(
              padding: const EdgeInsets.all(24),
              children: [
                Text('@${snapshot.data!.username}'),
                _field(_firstName, 'الاسم الأول'),
                _field(_lastName, 'اسم العائلة'),
                _field(_email, 'البريد الإلكتروني'),
                _field(_phone, 'رقم الهاتف'),
                FilledButton(
                  onPressed: _save,
                  child: const Text('حفظ التعديلات'),
                ),
                TextButton(
                  onPressed: _changePassword,
                  child: const Text('تغيير كلمة المرور'),
                ),
              ],
            );
          },
        ),
      );

  Widget _field(TextEditingController controller, String label) => Padding(
        padding: const EdgeInsets.only(top: 12),
        child: TextField(
          controller: controller,
          decoration: InputDecoration(labelText: label),
        ),
      );

  Future<void> _save() async {
    await ref.read(profileRepositoryProvider).update(
          firstName: _firstName.text,
          lastName: _lastName.text,
          email: _email.text,
          phone: _phone.text,
        );
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('تم تحديث الملف الشخصي')),
      );
    }
  }

  Future<void> _changePassword() async {
    final oldPassword = TextEditingController();
    final newPassword = TextEditingController();
    final submit = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('تغيير كلمة المرور'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: oldPassword,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'الحالية'),
            ),
            TextField(
              controller: newPassword,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'الجديدة'),
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
            child: const Text('تغيير'),
          ),
        ],
      ),
    );
    if (submit == true) {
      await ref.read(profileRepositoryProvider).changePassword(
            oldPassword: oldPassword.text,
            newPassword: newPassword.text,
          );
    }
    oldPassword.dispose();
    newPassword.dispose();
  }
}
