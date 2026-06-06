from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import validates

from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)

    products = db.relationship("Product", back_populates="category", lazy=True)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="products")
    images = db.relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy=True,
    )
    order_items = db.relationship("OrderItem", back_populates="product", lazy=True)

    @property
    def main_image(self):
        ordered = sorted(self.images, key=lambda item: (not item.is_main, item.sort_order))
        return ordered[0] if ordered else None

    @property
    def main_image_url(self):
        image = self.main_image
        return image.image_url if image else None

    @validates("price")
    def validate_price(self, _key, value):
        if value is None:
            raise ValueError("Price is required.")
        if Decimal(value) < 0:
            raise ValueError("Price cannot be negative.")
        return value


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_main = db.Column(db.Boolean, nullable=False, default=False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product = db.relationship("Product", back_populates="images")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text, nullable=True)

    payment_method = db.Column(db.String(50), nullable=False, default="prikolkcoin")
    payment_status = db.Column(db.String(50), nullable=False, default="paid_prikolkcoin")
    order_status = db.Column(db.String(50), nullable=False, default="placed")
    total_amount = db.Column(Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy=True,
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    product_name = db.Column(db.String(255), nullable=False)
    unit_price = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")
