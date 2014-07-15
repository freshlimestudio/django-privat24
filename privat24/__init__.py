from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

def get_privat24_transaction_model():
    "Return the Privat24Transaction model that is active in this project"
    from . import app_settings
    from django.db.models import get_model
    transaction_model = None
    try:
        transaction_model_name = app_settings.PRIVAT24_TRANSACTION_MODEL
        app_label, model_name = transaction_model_name.split('.')
        transaction_model = get_model(app_label, model_name)
        if transaction_model is None:
            raise ImproperlyConfigured(_("PRIVAT24_TRANSACTION_MODEL refers to model '%s' that has not been installed") % transaction_model_name)
    except ValueError:
        raise ImproperlyConfigured(_("PRIVAT24_TRANSACTION_MODEL must be of the form 'app_label.model_name'"))
    except AttributeError:
        raise ImportError
    return transaction_model
