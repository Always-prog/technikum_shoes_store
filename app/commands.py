import click

from app.extensions import db
from app.models import Category, Product


def register_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("seed-demo")
    def seed_demo_command():
        db.create_all()

        if Category.query.count() > 0 or Product.query.count() > 0:
            click.echo("Seed skipped: demo data already exists.")
            return

        categories = [
            Category(name="Кроссовки", slug="sneakers"),
            Category(name="Ботинки", slug="boots"),
            Category(name="Сандалии", slug="sandals"),
        ]
        db.session.add_all(categories)
        db.session.flush()

        products = [
            Product(
                name="Urban Sprint X1",
                slug="urban-sprint-x1",
                description="Лёгкие городские кроссовки для ежедневной носки.",
                price=4990,
                brand="Technikum",
                gender="unisex",
                season="all-season",
                category_id=categories[0].id,
            ),
            Product(
                name="Trail Guard Mid",
                slug="trail-guard-mid",
                description="Прочные ботинки для межсезонья и прогулок.",
                price=7490,
                brand="Technikum",
                gender="male",
                season="autumn",
                category_id=categories[1].id,
            ),
            Product(
                name="Sea Breeze Lite",
                slug="sea-breeze-lite",
                description="Удобные сандалии на тёплый сезон.",
                price=3590,
                brand="Technikum",
                gender="female",
                season="summer",
                category_id=categories[2].id,
            ),
        ]
        db.session.add_all(products)
        db.session.commit()
        click.echo("Demo data created.")
