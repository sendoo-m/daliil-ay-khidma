import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';

class RegisterPage extends ConsumerStatefulWidget {
  const RegisterPage({super.key});
  @override
  ConsumerState<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends ConsumerState<RegisterPage> {
  final _key = GlobalKey<FormState>();
  final _username = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _firstName = TextEditingController();
  final _lastName = TextEditingController();

  @override
  void dispose() {
    for (final controller in [
      _username,
      _email,
      _password,
      _firstName,
      _lastName,
    ]) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('إنشاء حساب')),
        body: Form(
          key: _key,
          child: ListView(
            padding: const EdgeInsets.all(24),
            children: [
              _field(_firstName, 'الاسم الأول'),
              _field(_lastName, 'اسم العائلة'),
              _field(_username, 'اسم المستخدم', required: true),
              _field(_email, 'البريد الإلكتروني', required: true),
              _field(_password, 'كلمة المرور', required: true, password: true),
              const SizedBox(height: 20),
              FilledButton(
                onPressed: ref.watch(authControllerProvider).isLoading ? null : _submit,
                child: const Text('إنشاء الحساب'),
              ),
              if (ref.watch(authControllerProvider).hasError)
                const Padding(
                  padding: EdgeInsets.only(top: 12),
                  child: Text('تعذر إنشاء الحساب، راجع البيانات'),
                ),
            ],
          ),
        ),
      );

  Widget _field(
    TextEditingController controller,
    String label, {
    bool required = false,
    bool password = false,
  }) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: TextFormField(
          controller: controller,
          obscureText: password,
          keyboardType: label.contains('البريد') ? TextInputType.emailAddress : null,
          decoration: InputDecoration(labelText: label),
          validator: required
              ? (value) => value == null || value.trim().isEmpty ? '$label مطلوب' : null
              : null,
        ),
      );

  Future<void> _submit() async {
    if (!_key.currentState!.validate()) return;
    final ok = await ref.read(authControllerProvider.notifier).register(
          username: _username.text,
          email: _email.text,
          password: _password.text,
          firstName: _firstName.text,
          lastName: _lastName.text,
        );
    if (ok && mounted) Navigator.of(context).pop();
  }
}
