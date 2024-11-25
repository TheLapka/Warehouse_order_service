from apps.supplier_management.views import SupplierView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("Supplier", SupplierView)

urlpatterns = router.urls + []
