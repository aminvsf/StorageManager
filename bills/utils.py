from config.DateTimeRelated.DateTimeRanges import (
    month_range,
    week_range,
    yesterday_range,
    now,
)


def check_input_delete_permission(obj):
    if obj:
        for detail in obj.inputdetail_set.all():
            product_record = detail.get_product_record()
            if not product_record:
                return False
            if product_record.inventory - detail.value < 0:
                return False
        return True
    else:
        return False


def date_filters(exact_datetime, model, user):
    """
    This function returns the <model> objects in four date ranges:
    > a month ago
    > a week ago
    > yesterday
    > today
    """
    monthly = model.objects.filter(timestamp__range=[month_range, exact_datetime], store__user=user)
    weekly = model.objects.filter(timestamp__range=[week_range, exact_datetime], store__user=user)
    yesterday = model.objects.filter(timestamp__range=[yesterday_range, now], store__user=user)
    today = model.objects.filter(timestamp__range=[now, exact_datetime], store__user=user)
    return [monthly, weekly, yesterday, today]
