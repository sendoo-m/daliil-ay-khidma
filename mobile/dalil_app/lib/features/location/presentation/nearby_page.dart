import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../app/providers.dart';
import '../../directory/data/business.dart';
import '../../directory/presentation/business_card.dart';
import '../data/location_service.dart';

class NearbyPage extends ConsumerStatefulWidget {
  const NearbyPage({super.key});
  @override
  ConsumerState<NearbyPage> createState() => _NearbyPageState();
}

class _NearbyPageState extends ConsumerState<NearbyPage> {
  double _radius = 10;
  bool _loading = false;
  String? _message;
  List<Business> _items = const [];

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('بالقرب مني')),
        body: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  const Text('نطاق البحث:'),
                  const SizedBox(width: 12),
                  DropdownButton<double>(
                    value: _radius,
                    items: const [5, 10, 20, 50]
                        .map(
                          (value) => DropdownMenuItem(
                            value: value.toDouble(),
                            child: Text('$value كم'),
                          ),
                        )
                        .toList(),
                    onChanged: _loading
                        ? null
                        : (value) => setState(() => _radius = value ?? 10),
                  ),
                  const Spacer(),
                  FilledButton.icon(
                    onPressed: _loading ? null : _search,
                    icon: const Icon(Icons.my_location),
                    label: const Text('بحث'),
                  ),
                ],
              ),
            ),
            if (_loading) const LinearProgressIndicator(),
            if (_message != null)
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text(_message!),
              ),
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: _items.length,
                itemBuilder: (_, index) {
                  final item = _items[index];
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      if (item.distanceKm != null)
                        Text('${item.distanceKm!.toStringAsFixed(1)} كم'),
                      BusinessCard(business: item),
                    ],
                  );
                },
              ),
            ),
          ],
        ),
      );

  Future<void> _search() async {
    setState(() {
      _loading = true;
      _message = null;
    });
    try {
      final coordinates = await ref.read(locationServiceProvider).current();
      final businesses = await ref.read(businessRepositoryProvider).nearby(
            latitude: coordinates.latitude,
            longitude: coordinates.longitude,
            radiusKm: _radius,
          );
      if (mounted) {
        setState(() {
          _items = businesses;
          _message = businesses.isEmpty ? 'لا توجد أنشطة ضمن هذا النطاق' : null;
        });
      }
    } on LocationException catch (error) {
      if (!mounted) return;
      final message = switch (error.failure) {
        LocationFailure.serviceDisabled => 'فعّل خدمة الموقع ثم حاول مجددًا',
        LocationFailure.denied => 'لم يتم السماح باستخدام الموقع',
        LocationFailure.deniedForever =>
          'صلاحية الموقع مرفوضة دائمًا؛ افتح إعدادات التطبيق لتفعيلها',
      };
      setState(() => _message = message);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }
}
