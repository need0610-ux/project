from openai import OpenAI

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from products.models import FinancialProduct


def get_gms_client():
    """
    GMS API 클라이언트를 생성한다.
    API KEY는 프론트엔드가 아니라 Django .env에서 관리한다.
    """
    if not getattr(settings, 'GMS_API_KEY', None):
        return None

    return OpenAI(
        api_key=settings.GMS_API_KEY,
        base_url=settings.GMS_BASE_URL,
    )


def find_product_context(message):
    """
    사용자의 질문에 상품명이 포함되어 있으면
    DB에 저장된 예금 상품 정보를 찾아 LLM에게 넘길 context를 만든다.
    """

    products = FinancialProduct.objects.filter(
        product_type='deposit'
    ).select_related('bank').prefetch_related('options')

    matched_product = None

    # 1차: 상품명이 질문에 정확히 포함된 경우
    for product in products:
        if product.name and product.name in message:
            matched_product = product
            break

    # 2차: 상품명 일부가 질문에 포함된 경우
    if matched_product is None:
        for product in products:
            if not product.name:
                continue

            product_words = product.name.replace('(', ' ').replace(')', ' ').split()

            for word in product_words:
                if len(word) >= 2 and word in message:
                    matched_product = product
                    break

            if matched_product:
                break

    # 3차: 은행명이 질문에 포함된 경우
    if matched_product is None:
        matched_products = []

        for product in products:
            if product.bank.name and product.bank.name in message:
                matched_products.append(product)

        if len(matched_products) == 1:
            matched_product = matched_products[0]

        elif len(matched_products) > 1:
            product_names = [
                f'- {product.name}'
                for product in matched_products[:5]
            ]

            return {
                'type': 'product_list',
                'context': (
                    f'{matched_products[0].bank.name}의 정기예금 상품이 여러 개 있습니다.\n'
                    f'사용자에게 어떤 상품을 설명할지 상품명을 더 자세히 입력해달라고 안내하세요.\n\n'
                    + '\n'.join(product_names)
                )
            }

    if matched_product is None:
        return None

    product = matched_product
    options = product.options.all()

    option_lines = []

    for option in options:
        option_lines.append(
            f'- 가입기간: {option.save_trm}개월, '
            f'기본금리: {option.intr_rate}%, '
            f'최고우대금리: {option.intr_rate2}%'
        )

    if option_lines:
        options_text = '\n'.join(option_lines)
    else:
        options_text = '저장된 금리 옵션 정보가 없습니다.'

    product_context = f"""
다음은 DB에 저장된 금융상품 정보입니다.

은행명: {product.bank.name}
상품명: {product.name}
상품유형: {product.product_type}
가입방법: {product.join_way or '정보 없음'}
가입대상: {product.join_member or '정보 없음'}
가입한도: {product.max_limit or '정보 없음'}
우대조건: {product.spcl_cnd or '정보 없음'}
기타 유의사항: {product.etc_note or '정보 없음'}

금리 옵션:
{options_text}
"""

    return {
        'type': 'product',
        'context': product_context
    }


def create_system_prompt():
    return """
너는 예적금 추천 서비스의 금융 설명 챗봇이다.

역할:
- 사용자가 입력한 금융용어, 예금, 적금, 금리, 우대금리, 환율, 은행, 금융상품 관련 질문을 쉽게 설명한다.
- 사용자가 금융상품명을 물어보면 제공된 상품 정보를 바탕으로 쉽게 설명한다.
- 초보자도 이해할 수 있도록 어려운 말을 풀어서 설명한다.

답변 규칙:
1. 반드시 한국어로 답변한다.
2. 답변은 3~7문장 정도로 작성한다.
3. 금융 초보자도 이해할 수 있게 쉽게 설명한다.
4. 투자 권유처럼 단정적으로 말하지 않는다.
5. 상품 설명 시 금리, 가입기간, 우대조건, 중도해지, 만기 조건을 확인해야 한다고 안내한다.
6. 금융과 관련 없는 질문이면 "금융상품과 금융용어 설명만 도와드릴 수 있어요."라고 답변한다.
7. 모르는 정보를 아는 것처럼 지어내지 않는다.
"""


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_response(request):
    message = request.data.get('message', '').strip()

    if not message:
        return Response(
            {
                'success': False,
                'message': '질문을 입력해주세요.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    client = get_gms_client()

    if client is None:
        return Response(
            {
                'success': False,
                'message': 'GMS API KEY가 설정되어 있지 않습니다.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    product_info = find_product_context(message)
    system_prompt = create_system_prompt()

    if product_info:
        user_prompt = f"""
사용자 질문:
{message}

참고할 상품 정보:
{product_info['context']}

위 정보를 바탕으로 사용자에게 쉽게 설명해줘.
"""
        response_type = product_info['type']

    else:
        user_prompt = f"""
사용자 질문:
{message}

위 질문이 금융용어, 예금, 적금, 금리, 환율, 은행, 금융상품과 관련 있다면 쉽게 설명해줘.
관련 없는 질문이면 금융상품과 금융용어 설명만 도와드릴 수 있다고 답변해줘.
"""
        response_type = 'llm'

    try:
        completion = client.chat.completions.create(
            model=getattr(settings, 'GMS_MODEL', 'gpt-5-nano'),
            messages=[
                {
                    'role': 'developer',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
        )

        answer = completion.choices[0].message.content.strip()

        return Response(
            {
                'success': True,
                'data': {
                    'type': response_type,
                    'question': message,
                    'answer': answer
                }
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                'success': False,
                'message': '챗봇 응답 생성 중 오류가 발생했습니다.',
                'error': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )