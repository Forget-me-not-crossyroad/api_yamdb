from django.db.models.query import prefetch_related_objects
from rest_framework.response import Response


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects(
                [instance],
                *queryset._prefetch_related_lookups)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
