import requests

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


KAKAO_LOCAL_KEYWORD_URL = 'https://dapi.kakao.com/v2/local/search/keyword.json'


@api_view(['GET'])
def search_bank_branches(request):
    keyword = request.GET.get('keyword', '은행')
    x = request.GET.get('x')  # 경도
    y = request.GET.get('y')  # 위도
    radius = request.GET.get('radius', 2000)

    api_key = settings.KAKAO_REST_API_KEY

    if not api_key:
        return Response(
            {'message': 'KAKAO_REST_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인해주세요.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    params = {
        'query': keyword,
        'size': 15,
    }

    # 사용자의 현재 위치가 있으면 주변 검색
    if x and y:
        params.update({
            'x': x,
            'y': y,
            'radius': radius,
            'sort': 'distance',
        })

    headers = {
        'Authorization': f'KakaoAK {api_key}'
    }

    response = requests.get(
        KAKAO_LOCAL_KEYWORD_URL,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        return Response(
            {
                'message': '카카오 로컬 API 요청에 실패했습니다.',
                'status_code': response.status_code,
                'detail': response.text,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    data = response.json()
    documents = data.get('documents', [])

    branches = []

    for item in documents:
        branches.append({
            'place_name': item.get('place_name'),
            'address_name': item.get('address_name'),
            'road_address_name': item.get('road_address_name'),
            'phone': item.get('phone'),
            'x': item.get('x'),  # 경도
            'y': item.get('y'),  # 위도
            'place_url': item.get('place_url'),
            'distance': item.get('distance'),
        })

    return Response({
        'keyword': keyword,
        'count': len(branches),
        'branches': branches
    })