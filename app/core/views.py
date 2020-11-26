from core.helper import CommonListCreateAPIView, CommonRetrieveUpdateDestroyAPIView
from core.models import Plan
from core.serializers import PlanReadSerializer
from core.serializers import PlanWriteSerializer


class PlanListCreateAPIView(CommonListCreateAPIView):
    """
    get:
    Return a list of plan instances.

    post:
    Create a plan instance.
    """
    queryset = Plan.objects.filter(deleted=False)
    read_serializer_class = PlanReadSerializer
    write_serializer_class = PlanWriteSerializer
    internal_name = 'plan'


class PlanRetrieveUpdateDestroyAPIView(CommonRetrieveUpdateDestroyAPIView):
    """
    get:
    Return a plan instance.

    put:
    Update a plan instance.

    delete:
    Delete a plan instance.

    patch:
    Update a plan instance partially.
    """
    queryset = Plan.objects.filter(deleted=False)
    read_serializer_class = PlanReadSerializer
    write_serializer_class = PlanWriteSerializer
    internal_name = 'plan'
