import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../../app/providers.dart';
import '../../../core/network/api_failure.dart';
import '../../notifications/presentation/notifications_page.dart';
import '../data/profile_repository.dart';

class ProfilePage extends ConsumerStatefulWidget {
  const ProfilePage({this.embedded = false, super.key});

  final bool embedded;

  @override
  ConsumerState<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends ConsumerState<ProfilePage> {
  final _formKey = GlobalKey<FormState>();
  final _firstName = TextEditingController();
  final _lastName = TextEditingController();
  final _email = TextEditingController();
  final _phone = TextEditingController();
  final _city = TextEditingController();
  final _bio = TextEditingController();
  UserProfile? _profile;
  bool _loading = true;
  bool _saving = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    for (final item in [_firstName, _lastName, _email, _phone, _city, _bio]) {
      item.dispose();
    }
    super.dispose();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final profile = await ref.read(profileRepositoryProvider).get();
      if (!mounted) return;
      _setProfile(profile);
    } catch (error) {
      if (mounted) setState(() => _error = ApiFailure.message(error));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _setProfile(UserProfile profile) {
    _profile = profile;
    _firstName.text = profile.firstName;
    _lastName.text = profile.lastName;
    _email.text = profile.email;
    _phone.text = profile.phone;
    _city.text = profile.city;
    _bio.text = profile.bio;
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: !widget.embedded,
          title: const Text('حسابي'),
          actions: [
            IconButton(
              tooltip: 'الإشعارات',
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute<void>(
                  builder: (_) => const NotificationsPage(),
                ),
              ),
              icon: const Icon(Icons.notifications_none_rounded),
            ),
            IconButton(
              tooltip: 'تسجيل الخروج',
              onPressed: _confirmLogout,
              icon: const Icon(Icons.logout_rounded),
            ),
          ],
        ),
        body: _body(),
      );

  Widget _body() {
    if (_loading) return const Center(child: CircularProgressIndicator());
    if (_error != null || _profile == null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.person_off_outlined, size: 64),
              const SizedBox(height: 16),
              Text(_error ?? 'تعذر تحميل الملف الشخصي'),
              const SizedBox(height: 18),
              OutlinedButton.icon(
                onPressed: _load,
                icon: const Icon(Icons.refresh),
                label: const Text('إعادة المحاولة'),
              ),
            ],
          ),
        ),
      );
    }
    final profile = _profile!;
    return RefreshIndicator(
      onRefresh: _load,
      child: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 36),
          children: [
            _ProfileHeader(profile: profile),
            const SizedBox(height: 24),
            Text(
              'البيانات الشخصية',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _field(_firstName, 'الاسم الأول')),
                const SizedBox(width: 12),
                Expanded(child: _field(_lastName, 'اسم العائلة')),
              ],
            ),
            _field(
              _email,
              'البريد الإلكتروني',
              keyboardType: TextInputType.emailAddress,
              validator: _validateEmail,
            ),
            _field(
              _phone,
              'رقم الهاتف',
              keyboardType: TextInputType.phone,
              validator: _validatePhone,
            ),
            _field(_city, 'المدينة'),
            _field(
              _bio,
              'نبذة عنك',
              maxLines: 3,
              maxLength: 500,
            ),
            const SizedBox(height: 18),
            FilledButton.icon(
              onPressed: _saving ? null : _save,
              icon: _saving
                  ? const SizedBox.square(
                      dimension: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.save_outlined),
              label: Text(_saving ? 'جارٍ الحفظ...' : 'حفظ التعديلات'),
            ),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: _saving ? null : _changePassword,
              icon: const Icon(Icons.lock_reset_rounded),
              label: const Text('تغيير كلمة المرور'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _field(
    TextEditingController controller,
    String label, {
    TextInputType? keyboardType,
    String? Function(String?)? validator,
    int maxLines = 1,
    int? maxLength,
  }) =>
      Padding(
        padding: const EdgeInsets.only(top: 12),
        child: TextFormField(
          controller: controller,
          keyboardType: keyboardType,
          validator: validator,
          maxLines: maxLines,
          maxLength: maxLength,
          textInputAction:
              maxLines == 1 ? TextInputAction.next : TextInputAction.newline,
          decoration: InputDecoration(labelText: label),
        ),
      );

  String? _validateEmail(String? value) {
    final email = value?.trim() ?? '';
    if (email.isEmpty) return 'البريد الإلكتروني مطلوب';
    if (!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email)) {
      return 'أدخل بريدًا إلكترونيًا صحيحًا';
    }
    return null;
  }

  String? _validatePhone(String? value) {
    final phone = value?.trim() ?? '';
    if (phone.isEmpty) return 'رقم الهاتف مطلوب';
    if (!RegExp(r'^01[0125][0-9]{8}$').hasMatch(phone)) {
      return 'أدخل رقم هاتف مصري صحيحًا';
    }
    return null;
  }

  Future<void> _save() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;
    setState(() => _saving = true);
    try {
      final profile = await ref.read(profileRepositoryProvider).update(
            firstName: _firstName.text,
            lastName: _lastName.text,
            email: _email.text,
            phone: _phone.text,
            bio: _bio.text,
            city: _city.text,
          );
      if (!mounted) return;
      setState(() => _setProfile(profile));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('تم تحديث الملف الشخصي بنجاح')),
      );
    } catch (error) {
      if (mounted) _showError(error);
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Future<void> _changePassword() async {
    final oldPassword = TextEditingController();
    final newPassword = TextEditingController();
    final confirmation = TextEditingController();
    var hideOld = true;
    var hideNew = true;
    String? dialogError;
    var submitting = false;
    await showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (dialogContext) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('تغيير كلمة المرور'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: oldPassword,
                  obscureText: hideOld,
                  decoration: InputDecoration(
                    labelText: 'كلمة المرور الحالية',
                    suffixIcon: IconButton(
                      onPressed: () =>
                          setDialogState(() => hideOld = !hideOld),
                      icon: Icon(hideOld ? Icons.visibility : Icons.visibility_off),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: newPassword,
                  obscureText: hideNew,
                  decoration: InputDecoration(
                    labelText: 'كلمة المرور الجديدة',
                    suffixIcon: IconButton(
                      onPressed: () =>
                          setDialogState(() => hideNew = !hideNew),
                      icon: Icon(hideNew ? Icons.visibility : Icons.visibility_off),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: confirmation,
                  obscureText: hideNew,
                  decoration:
                      const InputDecoration(labelText: 'تأكيد كلمة المرور'),
                ),
                if (dialogError != null) ...[
                  const SizedBox(height: 12),
                  Text(
                    dialogError!,
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.error,
                    ),
                  ),
                ],
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed:
                  submitting ? null : () => Navigator.pop(dialogContext),
              child: const Text('إلغاء'),
            ),
            FilledButton(
              onPressed: submitting
                  ? null
                  : () async {
                      if (newPassword.text.length < 8) {
                        setDialogState(
                          () => dialogError =
                              'كلمة المرور الجديدة يجب ألا تقل عن 8 أحرف',
                        );
                        return;
                      }
                      if (newPassword.text != confirmation.text) {
                        setDialogState(
                          () => dialogError = 'كلمتا المرور غير متطابقتين',
                        );
                        return;
                      }
                      setDialogState(() {
                        submitting = true;
                        dialogError = null;
                      });
                      try {
                        await ref.read(profileRepositoryProvider).changePassword(
                              oldPassword: oldPassword.text,
                              newPassword: newPassword.text,
                            );
                        if (!dialogContext.mounted) return;
                        Navigator.pop(dialogContext);
                        ScaffoldMessenger.of(this.context).showSnackBar(
                          const SnackBar(
                            content: Text('تم تغيير كلمة المرور بنجاح'),
                          ),
                        );
                      } catch (error) {
                        if (dialogContext.mounted) {
                          setDialogState(() {
                            submitting = false;
                            dialogError = ApiFailure.message(error);
                          });
                        }
                      }
                    },
              child: Text(submitting ? 'جارٍ التغيير...' : 'تغيير'),
            ),
          ],
        ),
      ),
    );
    oldPassword.dispose();
    newPassword.dispose();
    confirmation.dispose();
  }

  Future<void> _confirmLogout() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('تسجيل الخروج؟'),
        content: const Text('يمكنك تسجيل الدخول إلى حسابك مرة أخرى في أي وقت.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('إلغاء'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('تسجيل الخروج'),
          ),
        ],
      ),
    );
    if (confirmed == true) {
      await ref.read(authControllerProvider.notifier).logout();
    }
  }

  void _showError(Object error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(ApiFailure.message(error))),
    );
  }
}

class _ProfileHeader extends StatelessWidget {
  const _ProfileHeader({required this.profile});

  final UserProfile profile;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final picture = Uri.tryParse(profile.profilePicture ?? '');
    final pictureUrl =
        picture != null && picture.hasScheme ? picture.toString() : null;
    final initials = [
      if (profile.firstName.isNotEmpty) profile.firstName.characters.first,
      if (profile.lastName.isNotEmpty) profile.lastName.characters.first,
    ].join();
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [colors.primary, colors.secondary],
        ),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 34,
            backgroundColor: Colors.white,
            foregroundImage:
                pictureUrl == null ? null : NetworkImage(pictureUrl),
            child: pictureUrl == null
                ? Text(
                    initials.isEmpty ? profile.username.characters.first : initials,
                    style: TextStyle(
                      color: colors.primary,
                      fontSize: 23,
                      fontWeight: FontWeight.w900,
                    ),
                  )
                : null,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  profile.firstName.isEmpty && profile.lastName.isEmpty
                      ? profile.username
                      : '${profile.firstName} ${profile.lastName}'.trim(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 19,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                Text(
                  '@${profile.username}',
                  style: const TextStyle(color: Color(0xFFE1F3EC)),
                ),
                if (profile.dateJoined != null)
                  Text(
                    'عضو منذ ${DateFormat('MMMM yyyy', 'ar').format(profile.dateJoined!.toLocal())}',
                    style: const TextStyle(color: Color(0xFFE1F3EC)),
                  ),
              ],
            ),
          ),
          Tooltip(
            message: profile.emailVerified
                ? 'البريد الإلكتروني موثّق'
                : 'البريد الإلكتروني غير موثّق',
            child: Icon(
              profile.emailVerified
                  ? Icons.verified_rounded
                  : Icons.info_outline_rounded,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
