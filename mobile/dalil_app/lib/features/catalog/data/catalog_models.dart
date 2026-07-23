final class ProductSummary {
  const ProductSummary({
    required this.id,
    required this.name,
    required this.slug,
    required this.price,
    required this.businessName,
    required this.businessSlug,
    required this.productType,
    this.image,
    this.oldPrice,
  });
  factory ProductSummary.fromJson(Map<String, dynamic> json) => ProductSummary(
        id: json['id'] as int,
        name: json['name_ar'] as String? ?? '',
        slug: json['slug'] as String? ?? '',
        price: '${json['price'] ?? ''}',
        oldPrice: json['old_price'] == null ? null : '${json['old_price']}',
        businessName:
            (json['business'] as Map<String, dynamic>?)?['name_ar'] as String? ??
                '',
        businessSlug:
            (json['business'] as Map<String, dynamic>?)?['slug'] as String? ??
                '',
        productType: json['product_type'] as String? ?? 'product',
        image: (json['primary_image'] as Map<String, dynamic>?)?['image'] as String?,
      );
  final int id;
  final String name;
  final String slug;
  final String price;
  final String? oldPrice;
  final String businessName;
  final String businessSlug;
  final String productType;
  final String? image;

  double get numericPrice => double.tryParse(price) ?? double.infinity;
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
