import json
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Order, OrderItem, Product

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.get("/cart")
def cart():
    return render_template("cart.html")


@checkout_bp.get("/checkout")
def checkout():
    return render_template("checkout.html")


@checkout_bp.post("/checkout")
def checkout_submit():
    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    delivery_address = request.form.get("delivery_address", "").strip()
    comment = request.form.get("comment", "").strip()
    cart_payload = request.form.get("cart_payload", "[]")

    if not all([customer_name, phone, email, delivery_address]):
        flash("Заполни имя, телефон, email и адрес доставки.", "error")
        return redirect(url_for("checkout.checkout"))

    try:
        raw_items = json.loads(cart_payload)
    except json.JSONDecodeError:
        flash("Не удалось прочитать корзину. Попробуй снова.", "error")
        return redirect(url_for("checkout.checkout"))

    if not isinstance(raw_items, list) or not raw_items:
        flash("Корзина пуста.", "error")
        return redirect(url_for("checkout.cart"))

    validated_items = []
    product_ids = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        product_id = int(item.get("product_id", 0))
        quantity = int(item.get("quantity", 0))
        if product_id > 0 and quantity > 0:
            validated_items.append({"product_id": product_id, "quantity": quantity})
            product_ids.append(product_id)

    if not validated_items:
        flash("Корзина пуста.", "error")
        return redirect(url_for("checkout.cart"))

    products = Product.query.filter(Product.id.in_(product_ids), Product.is_active.is_(True)).all()
    products_map = {product.id: product for product in products}

    order = Order(
        customer_name=customer_name,
        phone=phone,
        email=email,
        delivery_address=delivery_address,
        comment=comment or None,
        payment_method="prikolkcoin",
        payment_status="paid_prikolkcoin",
        order_status="placed",
        total_amount=Decimal("0"),
    )
    db.session.add(order)
    db.session.flush()

    total_amount = Decimal("0")
    for item in validated_items:
        product = products_map.get(item["product_id"])
        if not product:
            continue
        quantity = item["quantity"]
        unit_price = Decimal(product.price)
        line_total = unit_price * quantity
        total_amount += line_total
        db.session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price=unit_price,
                quantity=quantity,
                line_total=line_total,
            )
        )

    if total_amount <= 0:
        db.session.rollback()
        flash("Не удалось оформить заказ: корзина невалидна.", "error")
        return redirect(url_for("checkout.cart"))

    order.total_amount = total_amount
    db.session.commit()
    return redirect(url_for("checkout.order_success", order_id=order.id))


@checkout_bp.get("/order/success/<int:order_id>")
def order_success(order_id: int):
    order = Order.query.get_or_404(order_id)
    return render_template("order_success.html", order=order)
