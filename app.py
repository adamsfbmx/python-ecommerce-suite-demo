from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
app.secret_key = 'demo_only_secret_key'

# ==========================================
# CONFIGURACIÓN DE BASE DE DATOS (DEMO)
# ==========================================
# Nota: En Render, usarás las variables de entorno para conectar esto.
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "DB_USER_PLACEHOLDER"),
    "password": os.environ.get("DB_PASSWORD", "DB_PASSWORD_PLACEHOLDER"),
    "dbname": os.environ.get("DB_NAME", "DB_NAME_PLACEHOLDER")
}

def get_db():
    DB_CONFIG['sslmode'] = 'require' # NUEVO: Requerido por Neon
    return psycopg2.connect(**DB_CONFIG)

# ==========================================
# SISTEMA DE IDIOMAS (i18n)
# ==========================================
@app.before_request
def set_language():
    if 'lang' not in session:
        session['lang'] = 'en'

from translations.i18n import TRANSLATIONS

@app.context_processor
def inject_language():
    lang = session.get('lang', 'en')
    t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return dict(lang=lang, t=t)

@app.route("/set-lang/<lang>")
def set_lang(lang):
    if lang in ['en', 'es', 'fr', 'it']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# ==========================================
# RUTAS PÚBLICAS (SOLO VISTAS)
# ==========================================
@app.route("/")
def index():
    search = request.args.get('q', '').strip()
    gender = request.args.get('gender', '').strip()
    conn = get_db(); cur = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        query += " AND (name ILIKE %s OR description ILIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    if gender:
        query += " AND gender = %s"
        params.append(gender)
    query += " ORDER BY created_at DESC"
    cur.execute(query, tuple(params))
    products = cur.fetchall()
    cur.close(); conn.close()
    return render_template('shop.html', products=products, search=search, current_gender=gender)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/product/<int:id>")
def product_detail(id):
    conn = get_db(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT p.*, c.name as category, COALESCE(AVG(r.rating), 0) as average_rating, COUNT(r.id) as total_reviews
        FROM products p LEFT JOIN categories c ON p.category_id = c.id LEFT JOIN reviews r ON p.id = r.product_id
        WHERE p.id = %s GROUP BY p.id, c.name
    """, (id,))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close(); return "Product not found", 404

    cur.execute("SELECT * FROM variants WHERE product_id = %s", (id,))
    variants = cur.fetchall()
    cur.execute("SELECT image_path FROM product_images WHERE product_id = %s", (id,))
    gallery = cur.fetchall()
    cur.execute("SELECT * FROM reviews WHERE product_id = %s ORDER BY created_at DESC", (id,))
    reviews = cur.fetchall()
    cur.execute("SELECT * FROM products WHERE category_id = %s AND id != %s AND stock > 0 ORDER BY created_at DESC LIMIT 4", (product['category_id'], id))
    related_products = cur.fetchall()

    cur.close(); conn.close()
    return render_template('product.html', product=product, reviews=reviews, related_products=related_products, gallery=gallery, variants=variants)

# ==========================================
# BLOQUEO DE RUTAS DE ACCIÓN (MODO DEMO)
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():
    return redirect(url_for('index'))

@app.route("/cart")
def view_cart():
    return redirect(url_for('index'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    return redirect(url_for('index'))

@app.route("/admin")
def admin_index():
    return redirect(url_for('index'))

@app.route("/customer/login", methods=["GET", "POST"])
def customer_login():
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
