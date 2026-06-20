from rest_framework import serializers
from .models import Bank, FinancialProduct, ProductOption


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'name', 'code')


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = (
            'id',
            'intr_rate_type',
            'intr_rate_type_nm',
            'save_trm',
            'intr_rate',
            'intr_rate2',
        )


class FinancialProductListSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    max_interest_rate = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProduct
        fields = (
            'id',
            'bank',
            'name',
            'join_way',
            'max_limit',
            'dcls_month',
            'max_interest_rate',
        )

    def get_max_interest_rate(self, obj):
        options = obj.options.all()
        rates = [
            option.intr_rate2
            for option in options
            if option.intr_rate2 is not None
        ]

        if not rates:
            return None

        return max(rates)


class FinancialProductDetailSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = FinancialProduct
        fields = (
            'id',
            'bank',
            'name',
            'join_way',
            'mtrt_int',
            'spcl_cnd',
            'join_deny',
            'join_member',
            'etc_note',
            'max_limit',
            'dcls_month',
            'dcls_strt_day',
            'dcls_end_day',
            'fin_co_subm_day',
            'options',
        )