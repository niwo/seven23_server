"""
    Terms and Conditions models
"""
import datetime
import calendar
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.datetime(year, month, day, sourcedate.hour, sourcedate.minute, sourcedate.second)

class Coupon(models.Model):

    """
        Discount token on puschase in SAAS mode.
    """
    code = models.CharField(_(u'id'),
                            unique=True,
                            max_length=128,
                            help_text=_(u'Ex: FALL25OFF'))
    name = models.CharField(_(u'Name'), help_text=_(u'Max 128 characters'), max_length=128)
    percent_off = models.IntegerField(_(u'Percentage off'), help_text=_(u'between 0 and 100'), default=0)
    valid_until = models.DateField(_(u'Valid until'), null=True, blank=True)
    max_redemptions = models.IntegerField(_(u'Max redemptions'), null=True, blank=True)
    affiliate = models.ForeignKey(User,
                    blank=True,
                    null=True, on_delete=models.CASCADE)
    affiliate_percent = models.IntegerField(_(u'Affiliate percent'), help_text=_(u'between 0 and 100'), default=0)
    enabled = models.BooleanField(_(u'Enabled'), default=True)

    def is_active(self):
        return self.enabled and \
            (not self.valid_until or self.valid_until < datetime.datetime.now()) and \
            (not self.max_redemptions or len(self.charges.all()) <= self.max_redemptions)

    def __str__(self):
        return u'%s' % (self.code)

    def save(self, *args, **kwargs):
        if (self.affiliate_percent + self.percent_off) > 100:
            raise Exception('Affiliate percent and percent off can\'t make more than 100% ')
        else:
            super(Coupon, self).save(*args, **kwargs) # Call the "real" save() method

class Product(models.Model):
    price = models.IntegerField(_(u'Price'))
    currency = models.CharField(_(u'Currency'), max_length=3, default='EUR')
    duration = models.IntegerField(_(u'How many month to add'), help_text=_(u'Per month'), default=12)
    valid_until = models.DateField(_(u'Valid until'), null=True, blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True)

    def is_active(self):
        return self.enabled and (not self.valid_until or self.valid_until < datetime.datetime.now())

    def __str__(self):
        return u'%s %s' % (self.price, self.currency)

    def apply_coupon(self, coupon_code):
        if (not coupon_code):
            return self.price
        coupon = Coupon.objects.get(code=coupon_code)
        return self.price - (self.price * coupon.percent_off / 100)

    def delete(self, *args, **kwargs):
        """
            If a category object is link to a transaction, it cannot be delete because
            we need to keep trace of all transactions. It is only disable/hide.
        """
        if self.charges.all():
            self.enabled = False
            self.save()
        else:
            super(Product, self).delete(*args, **kwargs) # Call the "real" save() method


class Charge(models.Model):
    """
        When a user try to buy a product
    """

    TYPE = (
        ('COUPON', 'Coupon'),
        ('STRIPE', 'Stripe'),
    )

    STATUS = (
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELED', 'Canceled'),
    )
    user = models.ForeignKey(User, related_name="charges", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="charges", on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, related_name="charges", null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(_(u'Date'), auto_now_add=True, editable=False)
    paiment_method = models.CharField(_(u'Paiment method'), max_length=20, choices=TYPE)
    reference_id = models.CharField(_(u'Reference ID'), max_length=128, null=True, blank=True)
    status = models.CharField(_(u'Status'), max_length=20, choices=STATUS)
    comment = models.TextField(_(u'Comment'), help_text=_(u'Will give context to the user'), null=True, blank=True)

    def apply_coupon(self):
        if (not self.coupon):
            return self.product.price
        return self.product.apply_coupon(self.coupon.code)

    def __str__(self):
        return u'%s %s' % (self.user, self.date)

    def save(self, *args, **kwargs):
        if self.status == "SUCCESS" and not self.pk:
            self.user.profile.valid_until = add_months(self.user.profile.valid_until, self.product.duration)
            self.user.save()
        super(Charge, self).save(*args, **kwargs) # Call the "real" save() method