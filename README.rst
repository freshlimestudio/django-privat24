========
Privat24
========

privat24 - это интеграция для работы с платежной системой http://privat24.ua/

Быстрый старт
-------------

1. Добавьте "privat24" в список INSTALLED_APPS::

      INSTALLED_APPS = (
          ...
          'privat24',
      )

2. Добавьте урлы интеграции в urls.py вашего проекта::

      from privat24.integration import Privat24Integration

      url(r'^p24/', include(Privat24Integration().urls)),

3. В settings.py пропишите настройки:

      # Privat24 setting
      PRIVAT24_OPTIONS = {
        'merchant': 'ваш_мерчант_id',
        'password': 'ваш_пароль',
        'ccy': 'UAH', # валюта
        'test_mode': True,
        'return_url':'http://proj/***/', #страница, принимающая клиента после оплаты
        'server_url':'http://proj/p24/notify-handler/', #страница, принимающая ответ API о результате платежа
    }


4. Интеграция содержит модель транзакций. Для большенства случаев ее хватает.
   Если же нужно добавить еще какие-нибудь поля, модель транзакций можно
   переопределить:

      ..
      from privat24.models import AbstractPrivat24Transaction

      ..
      ..

      class CustomPrivat24Transaction(AbstractPrivat24Transaction):

          created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
          updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)

          class Meta:
              verbose_name = _('privat24 transaction')
              verbose_name_plural = _('privat24 transactions')

   а в settings.py добавить:

          PRIVAT24_TRANSACTION_MODEL = 'your_app.customprivat24transaction'


5. Интеграция содержит встроенную форму для запроса данных. В случае необходимости
   ее можно переопределить:

          from privat24.forms import Privat24FrontForm

          ..
          ..

          class CustomPrivat24Form(Privat24FrontForm):
              amt = forms.CharField(widget=forms.HiddenInput())
              ccy = forms.CharField(widget=forms.HiddenInput())


   Пример создания формы в view:

          from privat24.integration import Privat24Integration

          ..
          ..

          template = 'payments/pay_privat24.html'
          p24 = Privat24Integration({
              "amt": order.sum,
              "ccy": "UAH",
              "order": order.pk,
              "details": order.product_name,
              'form_class': CustomPrivat24Form,
          })
          ctx['integration'] = p24

   Пример шаблона формы (pay_privat24.html):

          <form action="{{ integration.service_url }}" method="post" id="privat24_pay_form">
              {% csrf_token %}
              <div id="form1">
                  {% with integration.generate_form as form %}
                      {{ form.as_p }}
                      <p class="blue_text_popup">Всього: {{ form.amt.value }} грн</p>
                  {% endwith %}
              </div>
              <div class="clear10"></div>
              <button class="light_blue_bg btn_add  fr">Сплатити</button>
          </form>


6. Интеграция имеет встроенный view для получения результатов транзакции.
   В стучае удачного завершения транзакции вызывается сигнал transaction_was_successful.
   Написав обработчик для него можно выполнить некоторые действия, зависящие от результата
   транзакции:

    signals.py:

        def privat24_transaction_successfull(sender, type, response, **kwargs):
            from privat24 import get_privat24_transaction_model
            TransactionModel = get_privat24_transaction_model()
            transaction_id = response.get('local_trans_id', None)
            if transaction_id:
                transaction = TransactionModel.objects.get(pk=transaction_id)
                update_order(transaction)

    models.py:

        from privat24.signals import transaction_was_successful as privat24_transaction_was_successful
        ..
        ..

        privat24_transaction_was_successful.connect(privat24_transaction_successfull, dispatch_uid="proj.payments.models")


Автор: Игорь Нефедов igonef@pisem.net

Лицензия: MIT
