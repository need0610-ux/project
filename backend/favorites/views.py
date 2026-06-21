from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from products.models import FinancialProduct
from .models import FavoriteProduct
from .serializers import FavoriteProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    favorites = FavoriteProduct.objects.filter(
        user=request.user
    ).select_related(
        'product',
        'product__bank'
    ).prefetch_related(
        'product__options'
    )

    serializer = FavoriteProductSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_toggle(request, product_id):
    try:
        product = FinancialProduct.objects.get(
            id=product_id,
            product_type='deposit'
        )
    except FinancialProduct.DoesNotExist:
        return Response(
            {'message': '해당 정기예금 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    favorite = FavoriteProduct.objects.filter(
        user=request.user,
        product=product
    ).first()

    if favorite:
        favorite.delete()
        return Response(
            {
                'message': '관심상품에서 삭제되었습니다.',
                'is_favorite': False
            },
            status=status.HTTP_200_OK
        )

    FavoriteProduct.objects.create(
        user=request.user,
        product=product
    )

    return Response(
        {
            'message': '관심상품에 추가되었습니다.',
            'is_favorite': True
        },
        status=status.HTTP_201_CREATED
    )