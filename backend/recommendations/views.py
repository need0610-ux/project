from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import Bank, FinancialProduct
from .models import BankTestResult
from .serializers import BankTestResultSerializer


def find_bank_by_keywords(keywords):
    for keyword in keywords:
        bank = Bank.objects.filter(name__icontains=keyword).first()
        if bank:
            return bank
    return Bank.objects.first()


def recommend_bank(data):
    access = data.get('access_preference')
    benefit = data.get('benefit_preference')
    stability = data.get('stability_preference')
    purpose = data.get('usage_purpose')

    # 1. 인터넷은행 선호
    if stability == 'internet_bank' or access == 'mobile':
        bank = find_bank_by_keywords(['카카오', '케이', '토스'])
        reason = (
            '모바일 접근성을 중요하게 생각하는 성향으로 보입니다. '
            '비대면 가입과 앱 사용 편의성을 고려해 인터넷은행 계열 상품이 잘 맞을 수 있습니다.'
        )
        return bank, reason

    # 2. 높은 금리 선호
    if benefit == 'high_interest' or purpose == 'interest':
        product = FinancialProduct.objects.filter(
            product_type='deposit',
            options__intr_rate2__isnull=False
        ).select_related('bank').order_by('-options__intr_rate2').first()

        if product:
            reason = (
                f'높은 금리를 중요하게 생각하는 성향으로 보입니다. '
                f'현재 저장된 정기예금 상품 중 금리 조건이 좋은 상품을 기준으로 '
                f'{product.bank.name}을 추천합니다.'
            )
            return product.bank, reason

    # 3. 안정성/시중은행 선호
    if stability == 'major_bank' or benefit == 'stability':
        bank = find_bank_by_keywords(['국민', '신한', '우리', '하나', '농협'])
        reason = (
            '안정성과 익숙한 금융거래를 중요하게 생각하는 성향으로 보입니다. '
            '시중은행 중심의 정기예금 상품이 잘 맞을 수 있습니다.'
        )
        return bank, reason

    # 4. 조건 단순 선호
    if benefit == 'simple_condition':
        product = FinancialProduct.objects.filter(
            product_type='deposit',
            spcl_cnd__icontains='해당사항 없음'
        ).select_related('bank').first()

        if product:
            reason = (
                '복잡한 우대조건보다 단순한 상품을 선호하는 성향으로 보입니다. '
                '우대조건이 비교적 단순한 정기예금 상품을 기준으로 추천했습니다.'
            )
            return product.bank, reason

    # 기본값
    bank = Bank.objects.first()
    reason = (
        '입력한 성향을 종합했을 때, 현재 저장된 정기예금 상품을 보유한 은행 중 '
        '기본 추천 은행을 제안합니다.'
    )
    return bank, reason


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def main_bank_recommendation(request):
    serializer = BankTestResultSerializer(data=request.data)

    if serializer.is_valid():
        bank, reason = recommend_bank(serializer.validated_data)

        result = BankTestResult.objects.create(
            user=request.user,
            recommended_bank=bank,
            access_preference=serializer.validated_data['access_preference'],
            benefit_preference=serializer.validated_data['benefit_preference'],
            stability_preference=serializer.validated_data['stability_preference'],
            usage_purpose=serializer.validated_data['usage_purpose'],
            reason=reason
        )

        return Response(
            BankTestResultSerializer(result).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_recommendation_history(request):
    results = BankTestResult.objects.filter(
        user=request.user
    ).select_related('recommended_bank').order_by('-created_at')

    serializer = BankTestResultSerializer(results, many=True)
    return Response(serializer.data)