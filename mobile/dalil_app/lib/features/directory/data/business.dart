final class Business {
  const Business({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    required this.slug,
    required this.rating,
    this.logo,
    this.description = '',
    this.phone = '',
    this.distanceKm,
  });

  factory Business.fromJson(Map<String, dynamic> json) => Business(
        id: json['id'] as int,
        nameAr: json['name_ar'] as String? ?? '',
        nameEn: json['name_en'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        rating: double.tryParse('${json['average_rating'] ?? 0}') ?? 0,
        logo: json['logo'] as String?,
        description: json['description_ar'] as String? ?? '',
        phone: json['phone'] as String? ?? '',
        distanceKm: (json['distance_km'] as num?)?.toDouble(),
      );

  final int id;
  final String nameAr;
  final String nameEn;
  final String slug;
  final double rating;
  final String? logo;
  final String description;
  final String phone;
  final double? distanceKm;
}
