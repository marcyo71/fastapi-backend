from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ✅ importa solo i modelli che esistono davvero
import app.models.user
import app.models.payment
import app.models.referral
import app.models.stripe_event
import app.models.subscription
import app.models.transaction_model
import app.models.user_status
import app.models.plan
import app.models.status_model
import app.models.stripe_payment
import app.models.survey_model