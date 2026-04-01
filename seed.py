from app import create_app
from app.extensions import db
from app.models import Category, Product

app = create_app()


def seed():
    with app.app_context():
        db.create_all()
        if Product.query.count() > 0:
            print("Seed skipped: products already exist.")
            return

        sneakers = Category(name="Кроссовки", slug="sneakers")
        boots = Category(name="Ботинки", slug="boots")
        db.session.add_all([sneakers, boots])
        db.session.flush()

        db.session.add_all(
            [
                Product(
                    name="Street Flow Pro",
                    slug="street-flow-pro",
                    description="Универсальные кроссовки для города.",
                    price=5490,
                    brand="Technikum",
                    gender="unisex",
                    season="all-season",
                    category_id=sneakers.id,
                ),
                Product(
                    name="Nord Trek Warm",
                    slug="nord-trek-warm",
                    description="Тёплые ботинки для холодной погоды.",
                    price=8990,
                    brand="Technikum",
                    gender="male",
                    season="winter",
                    category_id=boots.id,
                ),
            ]
        )
        db.session.commit()
        print("Seed complete.")


if __name__ == "__main__":
    seed()
