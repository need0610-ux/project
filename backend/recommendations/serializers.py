from rest_framework import serializers
from .models import BankTestResult


class BankTestResultSerializer(serializers.ModelSerializer):
    recommended_bank_name = serializers.CharField(
        source='recommended_bank.name',
        read_only=True
    )

    class Meta:
        model = BankTestResult
        fields = (
            'id',
            'access_preference',
            'benefit_preference',
            'stability_preference',
            'usage_purpose',
            'recommended_bank',
            'recommended_bank_name',
            'reason',
            'created_at',
        )
        read_only_fields = (
            'recommended_bank',
            'recommended_bank_name',
            'reason',
            'created_at',
        )