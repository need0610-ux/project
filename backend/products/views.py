import requests

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Bank, FinancialProduct, ProductOption
from .serializers import (
    FinancialProductListSerializer,
    FinancialProductDetailSerializer,
)

@api_view(['GET'])
def save_deposit_products(request):
    api_key = settings.FSS_API_KEY

    if not api_key:
        return Response({
            'message': 'FSS_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.'
        }, status=500)

    url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return Response({
            'message': '금감원 API 요청에 실패했습니다.',
            'status_code': response.status_code,
        }, status=500)

    data = response.json()
    result = data.get('result', {})

    base_list = result.get('baseList', [])
    option_list = result.get('optionList', [])

    saved_banks = 0
    saved_products = 0
    saved_options = 0

    # 1. 상품 기본 정보 저장
    for item in base_list:
        bank, bank_created = Bank.objects.get_or_create(
            code=item.get('fin_co_no'),
            defaults={
                'name': item.get('kor_co_nm', '')
            }
        )

        if bank_created:
            saved_banks += 1

        product, product_created = FinancialProduct.objects.update_or_create(
            bank=bank,
            fin_prdt_cd=item.get('fin_prdt_cd'),
            product_type='deposit',
            defaults={
                'name': item.get('fin_prdt_nm') or '',
                'join_way': item.get('join_way') or '',
                'mtrt_int': item.get('mtrt_int') or '',
                'spcl_cnd': item.get('spcl_cnd') or '',
                'join_deny': str(item.get('join_deny') or ''),
                'join_member': item.get('join_member') or '',
                'etc_note': item.get('etc_note') or '',
                'max_limit': item.get('max_limit'),
                'dcls_month': item.get('dcls_month') or '',
                'dcls_strt_day': item.get('dcls_strt_day') or '',
                'dcls_end_day': item.get('dcls_end_day') or '',
                'fin_co_subm_day': item.get('fin_co_subm_day') or '',
            }
        )

        if product_created:
            saved_products += 1

    # 2. 상품 금리 옵션 저장
    for option in option_list:
        bank_code = option.get('fin_co_no')
        product_code = option.get('fin_prdt_cd')

        try:
            product = FinancialProduct.objects.get(
                bank__code=bank_code,
                fin_prdt_cd=product_code,
                product_type='deposit'
            )
        except FinancialProduct.DoesNotExist:
            continue

        product_option, option_created = ProductOption.objects.update_or_create(
            product=product,
            intr_rate_type=option.get('intr_rate_type', ''),
            save_trm=int(option.get('save_trm')),
            defaults={
                'intr_rate_type_nm': option.get('intr_rate_type_nm', ''),
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2'),
            }
        )

        if option_created:
            saved_options += 1

    return Response({
        'message': '정기예금 상품 저장 완료',
        'saved_banks': saved_banks,
        'saved_products': saved_products,
        'saved_options': saved_options,
        'total_base_count': len(base_list),
        'total_option_count': len(option_list),
    })

@api_view(['GET'])
def deposit_product_list(request):
    products = FinancialProduct.objects.filter(
        product_type='deposit'
    ).prefetch_related('options').select_related('bank')

    serializer = FinancialProductListSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def deposit_product_detail(request, product_id):
    try:
        product = FinancialProduct.objects.select_related('bank').prefetch_related('options').get(
            id=product_id,
            product_type='deposit'
        )
    except FinancialProduct.DoesNotExist:
        return Response(
            {'message': '해당 정기예금 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FinancialProductDetailSerializer(product)

    return Response(serializer.data)