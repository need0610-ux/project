import requests
from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


EXCHANGE_API_URL = 'https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON'


def get_exchange_rates_from_api():
    api_key = settings.EXCHANGE_API_KEY

    if not api_key:
        return None, 'EXCHANGE_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.'

    for i in range(7):
        search_date = datetime.today() - timedelta(days=i)

        # 주말은 건너뛰기
        if search_date.weekday() >= 5:
            continue

        params = {
            'authkey': api_key,
            'searchdate': search_date.strftime('%Y%m%d'),
            'data': 'AP01',
        }

        response = requests.get(EXCHANGE_API_URL, params=params)

        if response.status_code != 200:
            continue

        data = response.json()

        if data:
            return data, None

    return None, '최근 7일 이내 환율 데이터를 찾을 수 없습니다. 주말 또는 공휴일일 수 있습니다.'


def parse_rate(rate_text):
    """
    API 환율값이 '1,380.50'처럼 문자열로 오는 경우 숫자로 변환
    """
    if rate_text is None:
        return None

    return float(str(rate_text).replace(',', ''))


@api_view(['GET'])
def exchange_rate_list(request):
    data, error = get_exchange_rates_from_api()

    if error:
        return Response(
            {'message': error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    rates = []

    for item in data:
        rates.append({
            'currency_code': item.get('cur_unit'),
            'currency_name': item.get('cur_nm'),
            'rate': item.get('deal_bas_r'),
        })

    return Response({
        'date': datetime.today().strftime('%Y-%m-%d'),
        'rates': rates
    })


@api_view(['POST'])
def exchange_calculate(request):
    amount = request.data.get('amount')
    currency = request.data.get('currency')

    if amount is None or not currency:
        return Response(
            {'message': 'amount와 currency를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        amount = float(amount)
    except ValueError:
        return Response(
            {'message': 'amount는 숫자여야 합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    data, error = get_exchange_rates_from_api()

    if error:
        return Response(
            {'message': error},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    target = None

    for item in data:
        if item.get('cur_unit') == currency:
            target = item
            break

    if target is None:
        return Response(
            {'message': '해당 통화 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    rate = parse_rate(target.get('deal_bas_r'))

    if rate is None:
        return Response(
            {'message': '환율 정보를 숫자로 변환할 수 없습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    converted_amount = amount / rate

    return Response({
        'amount_krw': amount,
        'currency': target.get('cur_unit'),
        'currency_name': target.get('cur_nm'),
        'rate': rate,
        'converted_amount': round(converted_amount, 2)
    })

def get_recent_business_day():
    date = datetime.today()

    # 토요일이면 하루 전, 일요일이면 이틀 전으로 이동
    if date.weekday() == 5:  # 토요일
        date = date - timedelta(days=1)
    elif date.weekday() == 6:  # 일요일
        date = date - timedelta(days=2)

    return date.strftime('%Y%m%d')