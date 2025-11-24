from app.models.product import Product
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.cart_item_service import CartService
from app.models.order import Order
from app.models.cart_item import CartItem
from django.core.exceptions import ValidationError
from django.urls import reverse
import stripe
from django.db import transaction
from django.http import HttpRequest
from app.forms.checkout.checkout_form import CheckoutForm
from app.services.user_service import UserService
from app.utils.email.resend_util import send_email

class OrderService():

    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_item_repo= OrderItemRepository()
        self.user_service = UserService()
        self.cart_service = CartService()
        self.product_repo = ProductRepository()

    def create_current_order(self,user_id:int | None, session_key: int | None, address: str, delivery_method, pay_method, email, request) -> Order:
        with transaction.atomic():
            if user_id is not None:
                cart_items: list[CartItem] = self.cart_service.get_cart_items_by_user_id(user_id)
                user = self.user_service.get_user_by_id(user_id)
                order = self.order_repository.create(user=user,address=address,
                                                    delivery_method=delivery_method,pay_method=pay_method)
                self.cart_service.clear_cart_by_user_id(user_id)
            else:
                cart_items: list[CartItem] = self.cart_service.get_cart_items_by_session_key(session_key)
                self.cart_service.clear_cart_by_session_key(session_key=session_key)
                order = self.order_repository.create(address=address,delivery_method=delivery_method,pay_method=pay_method)

            self._create_order_items(cart_items, order)
            try:
              send_email(email=email, order_identifier=order.identifier,request=request)
            except Exception as e:
              print(e)

        return order


    def _create_order_items(self, cart_items, order):
        for cart_item in cart_items:
            quantity = cart_item.quantity
            if isinstance(cart_item.item,Product):
                self.product_repo.update(id=cart_item.item.id,stock=cart_item.item.stock - quantity)
                self.order_item_repo.create(quantity=quantity,product=cart_item.item,order=order)
            else:
                self.order_item_repo.create(quantity=quantity,service=cart_item.item,order=order)


    def get_total_cost_by_order_id(self, order_id:int):
        return round(self.order_item_repo.get_total_amount(order_id),2)

    def create_stripe_session(self,request:HttpRequest, form: CheckoutForm):

        success_url = reverse(viewname="checkout_success")
        cancel_url = reverse(viewname="checkout_cancel")

        cart_items_stripefied =[item.stripify() for item in self.cart_service.get_cart_items(request)]

        if len(cart_items_stripefied) == 0:
            raise Exception("El carrito no puede estar vacío")

        user = request.user

        if user.is_anonymous:
            if not request.session.session_key:
              request.session.create()
            owner_data = {"session_key": str(request.session.session_key)}
        else:
            owner_data = {"user_id": str(user.id)}

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=cart_items_stripefied,
            mode="payment",
            success_url=request.build_absolute_uri(
                success_url)+ '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(cancel_url)+ '?session_id={CHECKOUT_SESSION_ID}',
            metadata={
            **owner_data,
            **form.cleaned_data
        }
        )

        return session.url

    def get_all_orders(self):
        return self.order_repository.get_all()

    def get_order_by_id(self, order_id:int) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")
        return order

    def get_orders_by_user_id(self, user_id:int):
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValidationError("No se ha encontrado el usuario")
        return self.order_repository.get_by_user_id(user_id)

    def get_services_by_order_id(self, order_id:int):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")
        return self.order_item_repo.get_services_of_order(order_id)

    def get_products_by_order_id(self, order_id:int):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")
        return self.order_item_repo.get_products_of_order(order_id)

    def get_items_by_order_id(self, order_id:int):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")
        return self.order_item_repo.get_items_by_order_id(order_id)

    def update_order_status_to_shipped(self, order_id:int):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")

        if order.status != Order.StatusOptions.PENDING:
            raise ValidationError("Solo las órdenes pendientes pueden ser enviadas.")
        return self.order_repository.update(id=order_id, status=Order.StatusOptions.SHIPPED)

    def update_order_status_to_delivered(self, order_id:int):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValidationError("No se ha encontrado la orden")
        if order.status != Order.StatusOptions.SHIPPED:
            raise ValidationError("Solo las órdenes enviadas pueden ser entregadas.")
        return self.order_repository.update(id=order_id, status=Order.StatusOptions.DELIVERED)

    def get_order_by_identifier(self, form_data: dict):
        identifier = form_data["identifier"]
        order = self.order_repository.get_order_by_identifier(identifier)
        if not order:
            raise ValidationError("No se ha encontrado la orden con el identificador proporcionado")
        return order.first()

    def get_order_by_identifier_2(self, identifier):
        order = self.order_repository.get_order_by_identifier(identifier)
        if not order:
            raise ValidationError("No se ha encontrado la orden con el identificador proporcionado")
        return order.first()
