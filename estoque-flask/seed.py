"""Popula o banco com dados de exemplo para demonstração."""
import random
from datetime import date, timedelta
from app import app, db, Product, Sale

PRODUCTS = [
    ("Mouse sem fio", "MOU-001", "Periféricos", 59.90, 42, 10),
    ("Teclado mecânico", "TEC-002", "Periféricos", 249.90, 18, 5),
    ("Monitor 24'' Full HD", "MON-003", "Monitores", 699.00, 7, 5),
    ("Webcam Full HD", "WEB-004", "Periféricos", 189.90, 3, 5),
    ("Headset gamer", "HEA-005", "Áudio", 199.90, 25, 8),
    ("SSD 512GB NVMe", "SSD-006", "Armazenamento", 279.00, 4, 6),
    ("Cadeira ergonômica", "CAD-007", "Móveis", 899.00, 6, 3),
    ("Suporte para notebook", "SUP-008", "Acessórios", 79.90, 30, 10),
    ("Hub USB-C 7 em 1", "HUB-009", "Acessórios", 129.90, 2, 5),
    ("Microfone condensador", "MIC-010", "Áudio", 349.00, 12, 4),
]

with app.app_context():
    db.drop_all()
    db.create_all()

    products = []
    for name, sku, category, price, qty, min_stock in PRODUCTS:
        p = Product(name=name, sku=sku, category=category, price=price,
                    stock_qty=qty, min_stock=min_stock)
        db.session.add(p)
        products.append(p)
    db.session.commit()

    random.seed(42)
    today = date.today()
    for _ in range(35):
        p = random.choice(products)
        qty = random.randint(1, 4)
        days_ago = random.randint(0, 45)
        s = Sale(product_id=p.id, quantity=qty, unit_price=p.price,
                  sold_at=today - timedelta(days=days_ago))
        db.session.add(s)
    db.session.commit()

    print("Banco populado com sucesso: %d produtos, %d vendas" % (
        Product.query.count(), Sale.query.count()))
