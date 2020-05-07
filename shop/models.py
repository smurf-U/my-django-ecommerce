from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


# Create your models here.
class Customer(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user', 'type'])
        ]
        verbose_name = "Contact"

    name = models.CharField(max_length=200)
    street = models.CharField(max_length=240, blank=True)
    street2 = models.CharField(max_length=240, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    zipcode = models.CharField(max_length=120, blank=True)
    email = models.CharField(max_length=240, blank=True)
    mobile = models.CharField(max_length=32, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    parent_id = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(choices=[
        ('contact', 'Contact'),
        ('delivery', 'Shipping Address'),
        ('invoice', 'Invoice Address'),
        ], default='contact', max_length=32)

    def __str__(self):
        return self.parent_id.name + ', ' + self.name if self.parent_id else self.name

    @property
    def getChild(self):
        return Customer.objects.filter(parent_id=self)
    
    @property
    def is_address_set(self):
        return (self.street and self.city and self.state and self.country and self.email)

    @property
    def full_address(self):
        address = ''
        if self.street:
            address += self.street + ', '
        if self.street2:
            address += self.street2 + ', '
        if self.city:
            address += self.city + ', '
        if self.state:
            address += self.state + '- ' if self.zipcode else self.state + ', '
        if self.zipcode:
            address += self.zipcode + ', '
        if self.country:
            address += self.country + '\n '
        return address

class Product(models.Model):
    class Meta:
        # app_label = 'product'
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = "Product"
        unique_together = [['sku']]

    name = models.CharField(max_length=200)
    sale_ok = models.BooleanField('Can be Sold', default=True)
    active = models.BooleanField('Active', default=True)
    # currency_id = models.ForeignKey(Currency, on_delete=models.SET_NULL)
    price = models.FloatField('Price', default=1.0)    
    sku = models.CharField('SKU', max_length=64)
    image = models.ImageField('Image', upload_to='product_template/',
                              blank=True)
    description = models.TextField('Product Description', blank=True)
    type = models.CharField('Type', max_length=32, choices=[
        ('product', 'Storable'),
        ('consu', 'Consumable'),
        ('service', 'Service')
    ], default='consu', help_text='A storable product is a  product for which '
                                  'you manage stock. The Inventory app has to '
                                  'be installed.\nA consumable product is a '
                                  'product for which stock is not managed.\n'
                                  'A service is a non-material product you '
                                  'provide.')
    qty_available = models.FloatField('Available Stock',default=0.0)
    
    def __str__(self):
        return '[' + self.sku + '] ' + self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url if self.image else '/static/images/image.png'
        except:
            url = '/static/images/image.png'
        return url 


class Order(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['name', 'customer_id']),
        ]
        verbose_name = "Order"
    
    name = models.CharField(max_length=512)
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="customer_order_set")
    invoice_address_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="invoice_address_order_set")
    shipping_address_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="shipping_address_order_set")
    order_date = models.DateTimeField(auto_now_add=True)
    confirm_date = models.DateTimeField(blank=True, null=True)
    commitment_date = models.DateTimeField(blank=True, null=True)
    state = models.CharField(choices=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('sale', 'Sale'),
        ('done', 'Done'),
    ], max_length=32)

    def __str__(self):
        return self.name

    @property
    def getTotal(self):
        lines = self.orderlines_set.all()
        return sum([line.getTotal for line in lines])
    
    @property
    def getQuantity(self):
        lines = self.orderlines_set.all()
        return sum([line.product_qty for line in lines])
    
    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        dirty = False
        if not self.invoice_address_id:
            self.invoice_address_id = self.customer_id
            dirty = not dirty
        if not self.shipping_address_id:
            self.shipping_address_id = self.customer_id
            dirty = not dirty
        if dirty:
            self.save()    
        return res


class OrderLines(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['order_id'])
        ]
        verbose_name = "Order Line"
    
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=264)    
    unit_price = models.FloatField('Price', null=True)
    product_qty = models.FloatField('Qunatity', default=0.0)
    # untaxed_amount = models.FloatField('Untaxed Amount', default=0.0)
    # tax_amount = models.FloatField('Tax Amount', default=0.0)
    # sub_total = models.FloatField('Sub Total', default=0.0)
    # total = models.FloatField('Total', default=0.0)
    data_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        dirty = False
        if self.product_id and not self.unit_price:
            self.unit_price = self.product_id.price
            dirty = not dirty
        if dirty:
            self.save()
        return res
    
    @property
    def getTotal(self):
        total = self.unit_price * self.product_qty
        return total
    
    def __str__(self):
        return self.order_id.name + ' ' + self.product_id.name