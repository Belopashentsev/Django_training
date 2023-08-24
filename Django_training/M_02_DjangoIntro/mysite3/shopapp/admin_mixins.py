from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse
import csv


class ExportAsCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta # для импорта полей из любой модели получаем метаданные принимаемой сущности
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv') # сюда пишем результат
        response['Content-Disposition'] = f'attachment; filename={meta}-export.csv' # добавляем заголовок на ответ
        csv_writer = csv.writer(response)
        csv_writer.writerow(field_names)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field)for field in field_names])

        return response

    export_csv.short_description = 'Export as CSV' # укажем описание метода
