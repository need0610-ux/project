from django.conf import settings
from django.db import models

from products.models import Bank


class BankTestResult(models.Model):
    ACCESS_CHOICES = [
        ('mobile', '모바일 선호'),
        ('offline', '영업점 선호'),
        ('both', '상관없음'),
    ]

    BENEFIT_CHOICES = [
        ('high_interest', '높은 금리 선호'),
        ('simple_condition', '간단한 조건 선호'),
        ('stability', '안정성 선호'),
    ]

    STABILITY_CHOICES = [
        ('major_bank', '시중은행 선호'),
        ('internet_bank', '인터넷은행 선호'),
        ('no_preference', '상관없음'),
    ]

    PURPOSE_CHOICES = [
        ('saving', '목돈 보관'),
        ('interest', '이자 수익'),
        ('short_term', '단기 운용'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_test_results'
    )
    recommended_bank = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recommended_results'
    )

    access_preference = models.CharField(max_length=30, choices=ACCESS_CHOICES)
    benefit_preference = models.CharField(max_length=30, choices=BENEFIT_CHOICES)
    stability_preference = models.CharField(max_length=30, choices=STABILITY_CHOICES)
    usage_purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)

    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        bank_name = self.recommended_bank.name if self.recommended_bank else '추천 은행 없음'
        return f'{self.user.username} - {bank_name}'