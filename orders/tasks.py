from celery import task
from django.core.mail import send_mail
from .models import Order
import time

@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {}, \n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    time.sleep(10)
    return mail_sent