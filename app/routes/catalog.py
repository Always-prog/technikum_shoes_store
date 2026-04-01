from decimal import Decimal

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import Category, Product

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.get("/")
def index():
    return redirect(url_for("catalog.catalog"))


@catalog_bp.get("/catalog")
def catalog():
    base_query = Product.query.filter_by(is_active=True)
    category_slug = request.args.get("category", "").strip()
    brand = request.args.get("brand", "").strip()
    gender = request.args.get("gender", "").strip()
    season = request.args.get("season", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()

    if category_slug:
        base_query = base_query.join(Category).filter(Category.slug == category_slug)
    if brand:
        base_query = base_query.filter(Product.brand == brand)
    if gender:
        base_query = base_query.filter(Product.gender == gender)
    if season:
        base_query = base_query.filter(Product.season == season)

    try:
        if min_price:
            base_query = base_query.filter(Product.price >= Decimal(min_price))
        if max_price:
            base_query = base_query.filter(Product.price <= Decimal(max_price))
    except Exception:  # noqa: BLE001
        flash("Цена в фильтрах указана неверно.", "error")

    products = (
        base_query.options(selectinload(Product.images), selectinload(Product.category))
        .order_by(Product.id.asc())
        .all()
    )

    categories = Category.query.order_by(Category.name.asc()).all()
    brands = [item[0] for item in db.session.query(Product.brand).distinct().order_by(Product.brand)]
    genders = [item[0] for item in db.session.query(Product.gender).distinct().order_by(Product.gender)]
    seasons = [item[0] for item in db.session.query(Product.season).distinct().order_by(Product.season)]

    selected_filters = {
        "category": category_slug,
        "brand": brand,
        "gender": gender,
        "season": season,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render_template(
        "catalog.html",
        products=products,
        categories=categories,
        brands=brands,
        genders=genders,
        seasons=seasons,
        selected_filters=selected_filters,
    )


@catalog_bp.get("/product/<string:slug>")
def product_detail(slug: str):
    product = (
        Product.query.options(selectinload(Product.images), selectinload(Product.category))
        .filter_by(slug=slug, is_active=True)
        .first()
    )
    if not product:
        abort(404)
    return render_template("product_detail.html", product=product)
