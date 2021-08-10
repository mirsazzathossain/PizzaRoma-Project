from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class InstaPost(models.Model):
    title = models.CharField(max_length=100, null=False)
    url = models.CharField(max_length=10000, null=False)
    image = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '#'
        return url

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    description   = models.TextField(null=True)

    def __str__(self):
        return self.name

class Cheese(models.Model):
    name = models.CharField(max_length=200, null=False)
    quantity = models.FloatField(null=True, help_text='In gram')
    calories = models.FloatField(null=True, help_text='Per gram')

    def __str__(self):
        return self.name+' - '+str(self.quantity) + ' gm'
    
    @property
    def totalCal(self):
        try:
            cal = self.quantity * self.calories
        except:
            cal = 0
        return cal

class Crust(models.Model):
    name = models.CharField(max_length=200, null=False)
    size = models.FloatField(max_length=200, null=False, help_text='Diametere in inch')
    style = models.CharField(max_length=200, null=True)
    calories = models.FloatField(null=True)

    def __str__(self):
        return self.name + ' - '+self.style + ' ' + str(self.size) + '"'

class Topping(models.Model):
    name = models.CharField(max_length=200, null=False)
    calories = models.FloatField(null=True)

    def __str__(self):
        return self.name

class Choices(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True)
    price = models.FloatField(null=False)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    crust = models.ForeignKey(Crust, on_delete=models.SET_NULL, null=True)
    toppings = models.ManyToManyField(Topping)
    cheese = models.ForeignKey(Cheese, on_delete=models.SET_NULL, null=True)
    pizza_type = models.ManyToManyField(Choices)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def totalCalories(self):
        try:
            cal = self.cheese.totalCal
            for topping in self.toppings.all():
                cal = cal + topping.calories
            cal = cal + self.crust.calories
        except Exception as e:
            cal = 0
            print(e)
        return cal

class Offer(models.Model):
    tag = models.CharField(max_length=200, null=False)
    percentage = models.FloatField(null=False, help_text='In percentage')

    def __str__(self):
        return self.tag

class Banner(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=CASCADE)
    title = models.CharField(max_length=200, null=False)
    subtitle = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return 'Banner - '+self.pizza.name

    @property
    def discountPrice(self):
        try:
            price = self.pizza.price - self.pizza.price * (self.offer.percentage/100.0)
        except:
            price = self.pizza.price
        return price