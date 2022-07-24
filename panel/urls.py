from django.urls import path

from .views import PanelView
from products.views import (
    MeasuringUnitsView,
    MeasuringUnitsCreateView,
    MeasuringUnitsUpdateView,
    MeasuringUnitsDeleteView,
    ProductsView,
    ProductsCreateView,
    ProductsUpdateView,
    ProductsDeleteView,
)
from bills.views import (
    InputsView,
    InputsCreateView,
    InputsDetailView,
    InputsBillView,
    InputsUpdateView,
    InputsDeleteView,
    OutputsView,
    OutputsCreateView,
    OutputsDetailView,
    OutputsBillView,
    OutputsUpdateView,
    OutputsDeleteView,
)
from stores.views import (
    StoresView,
    StoresCreateView,
    StoresDetailView,
    StoresUpdateView,
    StoresDeleteView,
    ProductRecordsView,
)

urlpatterns = [
    path('panel', PanelView.as_view(), name='panel'),
    # Measuring Units Urls
    path('measuring-units', MeasuringUnitsView.as_view(), name='measuring-units'),
    path('measuring-units-create', MeasuringUnitsCreateView.as_view(), name='measuring-units-create'),
    path('measuring-units-update/<pk>', MeasuringUnitsUpdateView.as_view(), name='measuring-units-update'),
    path('measuring-units-delete/<pk>', MeasuringUnitsDeleteView.as_view(), name='measuring-units-delete'),
    # Products Urls
    path('products', ProductsView.as_view(), name='products'),
    path('products-create', ProductsCreateView.as_view(), name='products-create'),
    path('products-update/<pk>', ProductsUpdateView.as_view(), name='products-update'),
    path('products-delete/<pk>', ProductsDeleteView.as_view(), name='products-delete'),
    # Inputs Urls
    path('inputs', InputsView.as_view(), name='inputs'),
    path('inputs-create', InputsCreateView.as_view(), name='inputs-create'),
    path('inputs-update/<pk>', InputsUpdateView.as_view(), name='inputs-update'),
    path('inputs-delete/<pk>', InputsDeleteView.as_view(), name='inputs-delete'),
    path('inputs/<pk>', InputsDetailView.as_view(), name='inputs-detail'),
    path('inputs/bill/<pk>', InputsBillView.as_view(), name='inputs-bill'),
    # Outputs Urls
    path('outputs', OutputsView.as_view(), name='outputs'),
    path('outputs-create', OutputsCreateView.as_view(), name='outputs-create'),
    path('outputs-update/<pk>', OutputsUpdateView.as_view(), name='outputs-update'),
    path('outputs-delete/<pk>', OutputsDeleteView.as_view(), name='outputs-delete'),
    path('outputs/<pk>', OutputsDetailView.as_view(), name='outputs-detail'),
    path('outputs/bill/<pk>', OutputsBillView.as_view(), name='outputs-bill'),
    # Stores Urls
    path('stores', StoresView.as_view(), name='stores'),
    path('stores-create', StoresCreateView.as_view(), name='stores-create'),
    path('stores-update/<pk>', StoresUpdateView.as_view(), name='stores-update'),
    path('stores-delete/<pk>', StoresDeleteView.as_view(), name='stores-delete'),
    path('stores/<pk>', StoresDetailView.as_view(), name='stores-detail'),
    # ProductRecords Urls
    path('product-records', ProductRecordsView.as_view(), name='product-records'),
]
