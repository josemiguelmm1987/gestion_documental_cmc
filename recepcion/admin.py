from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Cargo, TipoDocumento, Entidad, Documento, EntidadRemitente, EntidadDestinatario

# Registro simple para modelos sin relaciones complejas
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sigla')
    search_fields = ('nombre', 'sigla')

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_persona')
    list_filter = ('tipo_persona',)
    search_fields = ('nombre',)

# Definición de los inlines
class EntidadRemitenteInline(admin.TabularInline):
    model = EntidadRemitente
    extra = 1
    autocomplete_fields = ('entidad', 'cargo', 'dependencia')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dependencia':
            kwargs['queryset'] = Entidad.objects.filter(tipo_persona=Entidad.TipoPersona.PERSONA_JURIDICA)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EntidadDestinatarioInline(admin.TabularInline):
    model = EntidadDestinatario
    extra = 1
    autocomplete_fields = ('entidad', 'cargo', 'dependencia')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dependencia':
            kwargs['queryset'] = Entidad.objects.filter(tipo_persona=Entidad.TipoPersona.PERSONA_JURIDICA)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Registro único para Documento con inlines
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'tipo_documento', 'get_fecha_hora_recepcion', 'get_remitentes', 'referencia', 'ver_archivo', 'mostrar_qr')
    list_filter = ('tipo_documento', 'fecha_hora_recepcion')
    search_fields = ('identificacion', 'referencia')
    date_hierarchy = 'fecha_hora_recepcion'
    inlines = [EntidadRemitenteInline, EntidadDestinatarioInline]

    # Función personalizada para formatear fecha_hora_recepcion
    def get_fecha_hora_recepcion(self, obj):
        return obj.fecha_hora_recepcion.strftime('%d/%m/%Y %H:%M')
    get_fecha_hora_recepcion.short_description = 'Fecha de Recepción'

    # Función para mostrar "Ver archivo" como enlace clickable
    def ver_archivo(self, obj):
        if obj.enlace_drive:
            return format_html('<a href="{}" target="_blank">Ver archivo</a>', obj.enlace_drive)
        return '-'
    ver_archivo.short_description = 'Archivo'

    # Función para mostrar los remitentes
    def get_remitentes(self, obj):
        remitentes = obj.entidadremitente_set.all()  # Accede a los remitentes relacionados
        if remitentes:
            # Concatenar los nombres de las entidades (puedes incluir cargo o dependencia si quieres)
            return ", ".join([str(remitente.entidad) for remitente in remitentes])
        return '-'
    get_remitentes.short_description = 'Remitentes'

    # Hacer el campo QR de solo lectura
    readonly_fields = ('qr_code', 'mostrar_qr')

    def mostrar_qr(self, obj):
        """Método personalizado para mostrar el código QR en el admin."""
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="150" height="150" />',
                obj.qr_code.url
            )
        return "No hay código QR generado aún."

    mostrar_qr.short_description = "Código QR"  # Nombre de la columna en la lista y formulario

# Registro individual para EntidadRemitente y EntidadDestinatario
@admin.register(EntidadRemitente)
class EntidadRemitenteAdmin(admin.ModelAdmin):
    list_display = ('entidad', 'documento', 'cargo', 'dependencia')
    list_filter = ('entidad__tipo_persona',)
    search_fields = ('entidad__nombre', 'documento__identificacion')
    autocomplete_fields = ('entidad', 'cargo', 'dependencia')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dependencia':
            kwargs['queryset'] = Entidad.objects.filter(tipo_persona=Entidad.TipoPersona.PERSONA_JURIDICA)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(EntidadDestinatario)
class EntidadDestinatarioAdmin(admin.ModelAdmin):
    list_display = ('entidad', 'documento', 'cargo', 'dependencia')
    list_filter = ('entidad__tipo_persona',)
    search_fields = ('entidad__nombre', 'documento__identificacion')
    autocomplete_fields = ('entidad', 'cargo', 'dependencia')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dependencia':
            kwargs['queryset'] = Entidad.objects.filter(tipo_persona=Entidad.TipoPersona.PERSONA_JURIDICA)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)