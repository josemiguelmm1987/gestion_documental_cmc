from django.contrib import admin
from .models import HojaRuta
from recepcion.models import Documento

@admin.register(HojaRuta)
class HojaRutaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'fecha_creacion', 'numero_correlativo', 'observaciones')
    list_filter = ('fecha_creacion',)
    search_fields = ('codigo', 'observaciones')
    filter_horizontal = ('documentos',)  # Mejora la interfaz para seleccionar múltiples documentos

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "documentos":
            # Filtrar documentos que no estén asociados a ninguna HojaRuta
            kwargs["queryset"] = Documento.objects.filter(hojaruta__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)