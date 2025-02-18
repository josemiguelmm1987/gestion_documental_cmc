from django.contrib import admin
from .models import Dependencia, Ente, Documento, TipoDocumento

# Register your models here.
@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'dependencia')

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sigla')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('tipo_documento', 'identificacion', 'referencia', 'fecha_hora_recepcion', 'enlace_drive')
    filter_horizontal = ('remitentes', 'destinatarios')  # Para selección múltiple en el admin