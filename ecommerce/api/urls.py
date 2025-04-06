from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views.user_views import UserViewSet
from api.views.market_views import MarketViewSet
from api.views.product_views import ProductViewSet
from api.views.supplier_views import SupplierViewSet
from api.views.login_view import LoginViewSet
from api.views.customer_view import CustomerViewSet
from api.views.order_views import OrderViewSet
from api.views.percentage_view import PercentageViewSet
from api.views.SupplierProfit_view import SupplierProfitViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'markets', MarketViewSet, basename='market')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'percentage', PercentageViewSet, basename='percentage')  # Fixed basename
router.register(r'supplierprofit', SupplierProfitViewSet, basename='supplierprofit')  # Fixed basename

# Register LoginViewSet for user access
router.register(r'useraccess', LoginViewSet, basename='useraccess')
urlpatterns = [
    path('', include(router.urls)),  # Include router URLs (don't add 'api/' here)
]
