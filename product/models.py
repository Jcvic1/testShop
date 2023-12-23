from django.db import models

# Create your models here.


class Discount(models.Model):
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return str(self.discount)


class Tax(models.Model):
    tax = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return str(self.tax)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    url = models.URLField(null=True)
    currency = models.CharField(max_length=15)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    tax = models.ForeignKey(Tax, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def get_discount(self):
        return "{0:.2f}".format(((1 - self.discount) * self.price))

    def get_price_cent(self):
        return int(self.price * 100)

    class Meta:
        ordering = ['name']


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)

    def get_total_price(self):
        total_price = sum(item.item.price * item.quantity for item in self.items.all())
        return total_price

    def get_discount(self):
        return int(self.discount.discount * 100)
    
    def get_tax(self):
        return int(self.tax.tax * 100)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.item.name} {self.quantity}'

    class Meta:
        unique_together = [['order', 'item']]
