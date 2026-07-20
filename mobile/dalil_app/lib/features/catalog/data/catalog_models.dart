final class ProductSummary {
  const ProductSummary({
    required this.name,
    required this.slug,
    required this.price,
    this.image,
  });
  factory ProductSummary.fromJson(Map<String, dynamic> json) => ProductSummary(
        name: json['name_ar'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        price: '${json['price'] ?? ''}',
        image: (json['primary_image'] as Map<String, dynamic>?)?['image'] as String?,
      );
  final String name;
  final String slug;
  final String price;
  final String? image;
}

final class DealSummary {
  const DealSummary({
    required this.title,
    required this.slug,
    required this.finalPrice,
    required this.daysRemaining,
    this.image,
  });
  factory DealSummary.fromJson(Map<String, dynamic> json) => DealSummary(
        title: json['title_ar'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        finalPrice: '${json['final_price'] ?? ''}',
        daysRemaining: json['days_remaining'] as int? ?? 0,
        image: json['image'] as String?,
      );
  final String title;
  final String slug;
  final String finalPrice;
  final int daysRemaining;
  final String? image;
}
