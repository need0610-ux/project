from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from products.models import FinancialProduct


TERM_EXPLANATIONS = {
    '우대금리': '우대금리는 특정 조건을 만족했을 때 추가로 받을 수 있는 금리입니다. 예를 들어 급여이체, 카드 사용, 자동이체 같은 조건을 충족하면 기본금리보다 더 높은 금리를 받을 수 있습니다.',
    '기본금리': '기본금리는 별도의 우대조건을 충족하지 않아도 받을 수 있는 기본 이자율입니다.',
    '최고금리': '최고금리는 기본금리에 우대금리를 모두 더했을 때 받을 수 있는 가장 높은 금리입니다. 다만 조건을 모두 충족해야 받을 수 있습니다.',
    '세전이자': '세전이자는 이자소득세를 떼기 전의 이자입니다. 실제로 받는 금액은 세금을 제외한 세후이자입니다.',
    '세후이자': '세후이자는 세전이자에서 이자소득세를 제외하고 실제로 받는 이자입니다.',
    '만기': '만기는 예금에 돈을 맡기기로 약속한 기간이 끝나는 날입니다. 만기가 되면 원금과 이자를 받을 수 있습니다.',
    '정기예금': '정기예금은 일정 금액을 정해진 기간 동안 은행에 맡기고, 만기 때 원금과 이자를 받는 금융상품입니다.',
    '예금자보호': '예금자보호는 금융회사가 영업정지나 파산 등으로 돈을 돌려주기 어려운 경우, 예금보험공사가 일정 한도까지 보호해주는 제도입니다. 일반적으로 원금과 이자를 합쳐 1인당 5천만 원까지 보호됩니다.',
}


def find_term_answer(message):
    for term, explanation in TERM_EXPLANATIONS.items():
        if term in message:
            return explanation

    return None


def build_product_explanation(product):
    options = product.options.all()

    max_rate = None
    best_option = None

    for option in options:
        if option.intr_rate2 is None:
            continue

        if max_rate is None or option.intr_rate2 > max_rate:
            max_rate = option.intr_rate2
            best_option = option

    if max_rate is None:
        rate_sentence = '현재 저장된 금리 옵션 정보는 없습니다.'
    else:
        rate_sentence = f'저장된 금리 옵션 기준으로 최고 우대금리는 {max_rate}%입니다'
        if best_option:
            rate_sentence += f'. 해당 금리는 {best_option.save_trm}개월 가입 기간 기준입니다.'

    max_limit_sentence = ''
    if product.max_limit:
        max_limit_sentence = f' 가입 한도는 최대 {product.max_limit:,}원입니다.'

    explanation = (
        f'{product.bank.name}의 "{product.name}"은 정기예금 상품입니다. '
        f'정기예금은 일정 기간 돈을 맡기고 만기 때 원금과 이자를 받는 상품입니다. '
        f'이 상품은 {product.join_way or "은행에서 안내하는 방식"}으로 가입할 수 있습니다. '
        f'{rate_sentence} '
        f'가입 대상은 {product.join_member or "상품 설명을 확인해야 합니다"}.'
        f'{max_limit_sentence} '
    )

    if product.spcl_cnd and product.spcl_cnd.strip() not in ['해당사항 없음', '해당 없음', '없음']:
        explanation += (
            f' 우대조건은 다음과 같습니다: {product.spcl_cnd} '
            f'쉽게 말하면, 최고금리를 받으려면 은행이 정한 조건을 충족해야 할 수 있습니다.'
        )
    else:
        explanation += ' 이 상품은 별도의 우대조건이 없거나, 우대조건 정보가 제공되지 않은 상품입니다.'

    if product.etc_note:
        explanation += f' 기타 유의사항은 다음과 같습니다: {product.etc_note}'

    return explanation


def find_product_answer(message):
    products = FinancialProduct.objects.filter(
        product_type='deposit'
    ).select_related('bank').prefetch_related('options')

    # 1차: 상품명이 질문에 정확히 포함된 경우
    for product in products:
        if product.name and product.name in message:
            return build_product_explanation(product)

    # 2차: 상품명 일부가 질문에 포함된 경우
    # 예: "하나의 정기예금 설명해줘"처럼 일부만 입력한 경우
    for product in products:
        product_words = product.name.replace('(', ' ').replace(')', ' ').split()
        for word in product_words:
            if len(word) >= 2 and word in message:
                return build_product_explanation(product)

    # 3차: 은행명이 질문에 포함된 경우
    matched_products = []

    for product in products:
        if product.bank.name and product.bank.name in message:
            matched_products.append(product)

    if len(matched_products) == 1:
        return build_product_explanation(matched_products[0])

    if len(matched_products) > 1:
        product_names = [
            f'- {product.name}'
            for product in matched_products[:5]
        ]

        return (
            f'{matched_products[0].bank.name}의 정기예금 상품이 여러 개 있어요. '
            f'어떤 상품을 설명할지 상품명을 조금 더 자세히 입력해주세요.\n\n'
            + '\n'.join(product_names)
        )

    return None



@api_view(['POST'])
def chatbot_response(request):
    message = request.data.get('message', '').strip()

    if not message:
        return Response(
            {'answer': '질문을 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    term_answer = find_term_answer(message)
    if term_answer:
        return Response({
            'answer': term_answer,
            'type': 'term'
        })

    product_answer = find_product_answer(message)
    if product_answer:
        return Response({
            'answer': product_answer,
            'type': 'product'
        })

    return Response({
        'answer': '아직 해당 질문에 대한 답변을 찾지 못했어요. 금융 용어나 정기예금 상품명을 포함해서 질문해 주세요. 예: "우대금리가 뭐야?", "하나은행 정기예금 쉽게 설명해줘"',
        'type': 'unknown'
    })