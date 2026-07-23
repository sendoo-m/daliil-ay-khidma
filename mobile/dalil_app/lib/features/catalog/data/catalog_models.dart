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

final class ProductDetail {
  const ProductDetail({
    required this.id,
    required this.name,
    required this.slug,
    required this.description,
    required this.productType,
    required this.price,
    required this.businessName,
    required this.businessSlug,
    required this.isAvailable,
    required this.isInStock,
    required this.hasDelivery,
    required this.isFeatured,
    required this.viewCount,
    this.oldPrice,
    this.discountPercentage = 0,
    this.stockQuantity,
    this.deliveryCost,
    this.deliveryTime = '',
    this.images = const [],
  });

  factory ProductDetail.fromJson(Map<String, dynamic> json) {
    final business = json['business'] as Map<String, dynamic>? ?? const {};
    return ProductDetail(
      id: json['id'] as int,
      name: json['name_ar'] as String? ?? json['name_en'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      description: json['description_ar'] as String? ??
          json['description_en'] as String? ??
          '',
      productType: json['product_type'] as String? ?? 'product',
      price: _number(json['price']),
      oldPrice: json['old_price'] == null ? null : _number(json['old_price']),
      discountPercentage: _number(json['discount_percentage']),
      businessName:
          business['name_ar'] as String? ?? business['name_en'] as String? ?? '',
      businessSlug: business['slug'] as String? ?? '',
      isAvailable: json['is_available'] as bool? ?? false,
      isInStock: json['is_in_stock'] as bool? ?? true,
      hasDelivery: json['has_delivery'] as bool? ?? false,
      isFeatured: json['is_featured'] as bool? ?? false,
      viewCount: json['view_count'] as int? ?? 0,
      stockQuantity: json['stock_quantity'] as int?,
      deliveryCost:
          json['delivery_cost'] == null ? null : _number(json['delivery_cost']),
      deliveryTime: json['delivery_time_ar'] as String? ??
          json['delivery_time_en'] as String? ??
          '',
      images: (json['images'] as List<dynamic>? ?? const [])
          .whereType<Map<String, dynamic>>()
          .map(ProductImage.fromJson)
          .where((image) => image.url.isNotEmpty)
          .toList(growable: false),
    );
  }

  final int id;
  final String name;
  final String slug;
  final String description;
  final String productType;
  final double price;
  final double? oldPrice;
  final double discountPercentage;
  final String businessName;
  final String businessSlug;
  final bool isAvailable;
  final bool isInStock;
  final bool hasDelivery;
  final bool isFeatured;
  final int viewCount;
  final int? stockQuantity;
  final double? deliveryCost;
  final String deliveryTime;
  final List<ProductImage> images;

  bool get hasDiscount => oldPrice != null && oldPrice! > price;
  bool get canOrder => isAvailable && (productType == 'service' || isInStock);
  bool get hasBusiness => businessName.isNotEmpty && businessSlug.isNotEmpty;
  String get typeLabel => productType == 'service' ? 'خدمة' : 'منتج';
}

final class ProductImage {
  const ProductImage({
    required this.url,
    this.altText = '',
    this.isPrimary = false,
  });

  factory ProductImage.fromJson(Map<String, dynamic> json) => ProductImage(
        url: json['image'] as String? ?? '',
        altText: json['alt_text_ar'] as String? ??
            json['alt_text_en'] as String? ??
            '',
        isPrimary: json['is_primary'] as bool? ?? false,
      );

  final String url;
  final String altText;
  final bool isPrimary;
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

double _number(Object? value) {
  if (value is num) return value.toDouble();
  return double.tryParse('$value') ?? 0;
}
