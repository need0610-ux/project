from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class FinancialProduct(models.Model):
    # 금감원 정기예금 api, 적금 api 넣을 것을 대비해서 넣음
    PRODUCT_TYPE_CHOICES = [
        ('deposit', '예금'),
        ('saving', '적금'),
    ]

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='products'
    )

    # 아래도 일단 놔둠
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES
    )
    fin_prdt_cd = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    join_way = models.TextField(blank=True)
    mtrt_int = models.TextField(blank=True)
    spcl_cnd = models.TextField(blank=True)
    join_deny = models.CharField(max_length=20, blank=True)
    join_member = models.TextField(blank=True)
    etc_note = models.TextField(blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)
    dcls_month = models.CharField(max_length=6)
    dcls_strt_day = models.CharField(max_length=8, blank=True)
    dcls_end_day = models.CharField(max_length=8, blank=True)
    fin_co_subm_day = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bank', 'fin_prdt_cd', 'product_type')

    def __str__(self):
        return f'[{self.bank.name}] {self.name}'


class ProductOption(models.Model):
    product = models.ForeignKey(
        FinancialProduct,
        on_delete=models.CASCADE,
        related_name='options'
    )
    intr_rate_type = models.CharField(max_length=20, blank=True)
    intr_rate_type_nm = models.CharField(max_length=50, blank=True)
    save_trm = models.IntegerField()
    intr_rate = models.FloatField(null=True, blank=True)
    intr_rate2 = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('product', 'intr_rate_type', 'save_trm')

    def __str__(self):
        return f'{self.product.name} / {self.save_trm}개월 / 최고 {self.intr_rate2}%'