from app.models import Product, Category
from app.repositories.product_repository import ProductRepository
from django.test import TestCase

class TestProductRepository(TestCase):
    def setUp(self):
        self.product_repo = ProductRepository()
        self.product_data = {
            'name':"Lipstick",
            'description':"A vibrant red lipstick",
            'price':75.00,
            'stock':100,
            'fabricator':"BeautyCo",
        }

    def create_product(self, product_data):
        product = self.product_repo.create(**product_data)

        categories = Category.objects.all()

        product.categories.set(categories)
        return product

    def test_create_product(self):
        product_data = self.product_data.copy()
        product = self.product_repo.create(**product_data)
        
        self.assertIsNotNone(product.id)
        self.assertEqual(product.name, "Lipstick")
        self.assertEqual(product.description, "A vibrant red lipstick")
        self.assertEqual(product.price, 75.00)
        self.assertEqual(product.stock, 100)
        self.assertEqual(product.fabricator, "BeautyCo")

    def test_get_by_id(self):
        product_data = self.product_data.copy()
        product = self.product_repo.create(**product_data)

        found = self.product_repo.get_by_id(product.id)
        self.assertEqual(found, product)

    def test_get_all_products(self):
        product_data = self.product_data.copy()
        product1 = self.product_repo.create(**product_data)
        product2 = self.product_repo.create(**product_data)

        products = self.product_repo.get_all()
        self.assertEqual(products.count(), 2)

    def test_update_product(self):
        product_data = self.product_data.copy()
        product = self.product_repo.create(**product_data)

        updated = self.product_repo.update(product.id, price=11.99, stock=45)
        self.assertEqual(updated.price, 11.99)
        self.assertEqual(updated.stock, 45)
    
    def test_delete_product(self):
        product_data = self.product_data.copy()
        product = self.product_repo.create(**product_data)

        deleted = self.product_repo.delete(product.id)
        self.assertTrue(deleted)
        self.assertEqual(Product.objects.count(), 0)

    def test_search_name(self):
        product_data1= self.product_data.copy()
        product_data2= self.product_data.copy()

        product_data2['name']='Lipstick 2'

        product1 = self.create_product(product_data1)
        product2 = self.create_product(product_data2)

        products1 = Product.objects.all()
        products2 = products1.exclude(id=product1.id)

        name_filters1 = {'name':'Lipstick'}
        name_filters2 = {'name':'Lipstick 2'}
        
        search1 = self.product_repo.search(name_filters1)
        search2 = self.product_repo.search(name_filters2)

        self.assertEqual(search1.count(),2)
        self.assertEqual(set(search1),set(products1))
        self.assertEqual(search2.count(),1)
        self.assertEqual(set(search2),set(products2))

    def test_search_min_max_price(self):
        product_data1= self.product_data.copy()
        product_data2= self.product_data.copy()
        product_data3= self.product_data.copy()

        product_data2['name']='product 2'
        product_data2['price']=10.00
        product_data3['name']='product 3'
        product_data3['price']=100.00

        product1 = self.create_product(product_data1)
        min_product = self.create_product(product_data2)
        max_product = self.create_product(product_data3)

        products = Product.objects.all()
        min_products = products.exclude(id=min_product.id)
        max_products = products.exclude(id=max_product.id)

        min_filters = {'min_price':35.00}
        max_filters = {'max_price':80.00}
        min_max_filters = {'min_price':45.00,'max_price':80.00}
        
        min_search = self.product_repo.search(min_filters)
        max_search = self.product_repo.search(max_filters)
        min_max_search = self.product_repo.search(min_max_filters)

        self.assertEqual(min_search.count(),2)
        self.assertEqual(set(min_search),set(min_products))
        self.assertEqual(max_search.count(),2)
        self.assertEqual(set(max_search),set(max_products))
        self.assertEqual(min_max_search.count(),1)
        self.assertEqual(min_max_search.first(),product1)

    def test_search_fabricator(self):
        product_data1= self.product_data.copy()
        product_data2= self.product_data.copy()

        product_data2['fabricator']='BeautyCo 2'

        product1 = self.create_product(product_data1)
        product2 = self.create_product(product_data2)

        products1 = Product.objects.all()
        products2 = products1.exclude(id=product1.id)

        department_filters1 = {'fabricator':'BeautyCo'}
        department_filters2 = {'fabricator':'BeautyCo 2'}
        
        search1 = self.product_repo.search(department_filters1)
        search2 = self.product_repo.search(department_filters2)

        self.assertEqual(search1.count(),2)
        self.assertEqual(set(search1),set(products1))
        self.assertEqual(search2.count(),1)
        self.assertEqual(set(search2),set(products2))

    def test_get_all_promoted_products(self):
        product_data1 = self.product_data.copy()
        product_data2 = self.product_data.copy()

        product_data2['isPromoted'] = True

        self.create_product(product_data1)
        self.create_product(product_data2)

        products = self.product_repo.get_all_promoted_products()

        self.assertEqual(products.count(),1)

    