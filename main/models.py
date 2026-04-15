import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while SubCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)


class Seller(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sellers/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=260, unique=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    amount = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=100, default="Uzbekistan")
    delivery = models.CharField(max_length=50, blank=True, null=True)

    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def get_main_media(self):
        medias = self.media_set.all()
        if medias.exists():
            media = medias.order_by('-main').first()
            return media
        return None


class Media(models.Model):
    image = models.ImageField(upload_to='media/')
    main = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Media of {self.product.name}"


class Property(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Choice(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='variants/', blank=True, null=True)
    delta_price = models.FloatField(default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def next_price(self):
        return self.choice.product.price + self.delta_price

    def __str__(self):
        return self.name


class Discount(models.Model):
    percentage = models.FloatField(blank=True, null=True)
    dis_price = models.FloatField(blank=True, null=True)
    new_price = models.FloatField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Discount for {self.product.name} [{self.percentage}%]"

    def save(self, *args, **kwargs):
        price = self.product.price
        if self.percentage:
            self.new_price = price * (100 - self.percentage) / 100
            self.dis_price = price - self.new_price
        elif self.dis_price:
            self.new_price = price - self.dis_price
            self.percentage = 100 - self.new_price * 100 / price
        elif self.new_price:
            self.percentage = 100 - self.new_price * 100 / price
            self.dis_price = price - self.new_price
        else:
            self.end_date = datetime.date.today() - datetime.timedelta(days=1)
        super().save(*args, **kwargs)


class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    rate = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.text


class Ad(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ads/')
    url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
