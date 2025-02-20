from django.contrib import admin
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
    list_display = ('identificacion', 'tipo_documento', 'fecha_hora_recepcion', 'created', 'updated')
    list_filter = ('tipo_documento', 'fecha_hora_recepcion')
    search_fields = ('identificacion', 'referencia')
    date_hierarchy = 'fecha_hora_recepcion'
    inlines = [EntidadRemitenteInline, EntidadDestinatarioInline]

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