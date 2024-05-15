from rest_framework.filters import OrderingFilter


class UserOrderFilter(OrderingFilter):
    allowed_custom_filters = ["name", "country", "created"]
    fields_related = {
        "name": "user__first_name",
        "country": "country__name",
        "created": "created_at",
    }

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(",")]
            ordering = [
                f for f in fields if f.lstrip("-") in self.allowed_custom_filters
            ]
            if ordering:
                return ordering

        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        order_fields = []
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            for field in ordering:
                symbol = "-" if "-" in field else ""
                order_fields.append(symbol + self.fields_related[field.lstrip("-")])
        if order_fields:
            return queryset.order_by(*order_fields)

        return queryset
