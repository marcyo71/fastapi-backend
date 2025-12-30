from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ✅ importa qui tutti i tuoi modelli, così Alembic li vede
import app.models.user
import app.models.item
import app.models.order
import app.models.payment
import app.models.product
import app.models.category
import app.models.address
import app.models.session