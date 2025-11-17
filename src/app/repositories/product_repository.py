from app.repositories.base_repository import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)

    def get_products_by_category(self, category_id):
        return self.model.objects.filter(category_id=category_id)

    def search(self, filters):
        qs = Product.objects.all()

        name = filters.get('name')
        min_price = filters.get('min_price')
        max_price = filters.get('max_price')
        fabricator = filters.get('fabricator')
        categories = filters.get('categories')

        if name:
            qs = qs.filter(name__icontains=name)

        if min_price is not None:
            qs = qs.filter(price__gte=min_price)

        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        if fabricator:
            qs = qs.filter(fabricator__icontains=fabricator)

        if categories:
            qs = qs.filter(categories__in=categories).distinct()

        return qs
