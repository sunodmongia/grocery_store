from rest_framework import viewsets, permissions
from .models import Product, Movement_of_Items
from .serializer import ProductSerializer, StockMovementSerializer
from .pagination import TenPerPage
from rest_framework import mixins, viewsets

class ProductViewSet(viewsets.ModelViewSet):
    """
    Replaces:
      • ProductListView  (list)
      • ProductCreateView (create)
      • ProductUpdateView (update / partial_update)
      • ProductDeleteView (destroy)
    Extra: retrieve
    """
    queryset           = Product.objects.all().order_by('-id')
    serializer_class   = ProductSerializer
    pagination_class   = TenPerPage
    permission_classes = [permissions.AllowAny]      # tighten later
    


class StockMovementViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    Replaces StockMovementCreateView (and optionally gives you a list endpoint).
      list   → GET    /api/inventory/stock-movements/
      create → POST   /api/inventory/stock-movements/
    """
    queryset           = Movement_of_Items.objects.all().order_by('-id')
    serializer_class   = StockMovementSerializer
    permission_classes = [permissions.AllowAny]

