"""
Sistema de Gestão de Estoque e Vendas
--------------------------------------
Mini-SaaS full stack (Flask + SQLAlchemy + SQLite) para controle de
produtos, estoque e vendas, com dashboard de indicadores.

Como rodar:
    pip install -r requirements.txt
    python seed.py      # cria o banco e popula com dados de exemplo
    python app.py        # inicia o servidor em http://localhost:5000
"""
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db"
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"
db = SQLAlchemy(app)


# ---------------------------------------------------------------- MODELS ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(40), unique=True, nullable=False)
    category = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_qty = db.Column(db.Integer, nullable=False, default=0)
    min_stock = db.Column(db.Integer, nullable=False, default=5)

    @property
    def is_low_stock(self):
        return self.stock_qty <= self.min_stock

    @property
    def stock_value(self):
        return round(self.price * self.stock_qty, 2)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    sold_at = db.Column(db.Date, nullable=False, default=date.today)

    product = db.relationship("Product", backref=db.backref("sales", lazy=True))

    @property
    def total(self):
        return round(self.unit_price * self.quantity, 2)


# ---------------------------------------------------------------- ROUTES ---
@app.route("/")
def dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock_qty <= Product.min_stock).all()
    stock_value = sum(p.stock_value for p in Product.query.all())

    sales_total = db.session.query(
        func.sum(Sale.unit_price * Sale.quantity)
    ).scalar() or 0
    sales_count = Sale.query.count()

    top_products = (
        db.session.query(
            Product.name, func.sum(Sale.quantity).label("qty")
        )
        .join(Sale, Sale.product_id == Product.id)
        .group_by(Product.id)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(5)
        .all()
    )

    recent_sales = Sale.query.order_by(Sale.sold_at.desc(), Sale.id.desc()).limit(6).all()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        low_stock=low_stock,
        stock_value=round(stock_value, 2),
        sales_total=round(sales_total, 2),
        sales_count=sales_count,
        top_products=top_products,
        recent_sales=recent_sales,
    )


@app.route("/produtos")
def products():
    category = request.args.get("category", "")
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    items = query.order_by(Product.name).all()
    categories = [c[0] for c in db.session.query(Product.category).distinct()]
    return render_template("products.html", products=items, categories=categories, selected=category)


@app.route("/produtos/novo", methods=["GET", "POST"])
def product_new():
    if request.method == "POST":
        p = Product(
            name=request.form["name"],
            sku=request.form["sku"],
            category=request.form["category"],
            price=float(request.form["price"]),
            stock_qty=int(request.form["stock_qty"]),
            min_stock=int(request.form["min_stock"] or 5),
        )
        db.session.add(p)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for("products"))
    return render_template("product_form.html", product=None)


@app.route("/produtos/<int:pid>/editar", methods=["GET", "POST"])
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    if request.method == "POST":
        p.name = request.form["name"]
        p.sku = request.form["sku"]
        p.category = request.form["category"]
        p.price = float(request.form["price"])
        p.stock_qty = int(request.form["stock_qty"])
        p.min_stock = int(request.form["min_stock"] or 5)
        db.session.commit()
        flash("Produto atualizado!", "success")
        return redirect(url_for("products"))
    return render_template("product_form.html", product=p)


@app.route("/produtos/<int:pid>/excluir", methods=["POST"])
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Produto removido.", "success")
    return redirect(url_for("products"))


@app.route("/vendas")
def sales():
    items = Sale.query.order_by(Sale.sold_at.desc(), Sale.id.desc()).all()
    return render_template("sales.html", sales=items)


@app.route("/vendas/nova", methods=["GET", "POST"])
def sale_new():
    products_list = Product.query.order_by(Product.name).all()
    if request.method == "POST":
        product = Product.query.get_or_404(int(request.form["product_id"]))
        qty = int(request.form["quantity"])
        s = Sale(
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
            sold_at=datetime.strptime(request.form["sold_at"], "%Y-%m-%d").date(),
        )
        product.stock_qty = max(0, product.stock_qty - qty)
        db.session.add(s)
        db.session.commit()
        flash("Venda registrada!", "success")
        return redirect(url_for("sales"))
    return render_template("sale_form.html", products=products_list, today=date.today().isoformat())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
