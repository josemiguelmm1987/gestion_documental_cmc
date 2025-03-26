from django.db import models
from django.utils import timezone
from recepcion.models import Documento  # Importamos el modelo Documento de la app recepcion

class HojaRuta(models.Model):
    # Campo para el número correlativo (se generará automáticamente)
    numero_correlativo = models.PositiveIntegerField(verbose_name="Número Correlativo", editable=False)
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    codigo = models.CharField(max_length=11, unique=True, verbose_name="Código", editable=False)
    
    # Relación ManyToMany con Documento (puede tener varios documentos asociados, opcional al crear)
    documentos = models.ManyToManyField(Documento, blank=True, verbose_name="Documentos Asociados")
    
    # Campo opcional para observaciones
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def generar_codigo(self):
        """Genera el código en formato NNNN/MM/AAAA basado en el número correlativo y la fecha."""
        mes = self.fecha_creacion.strftime("%m")  # Mes en dos dígitos
        anio = self.fecha_creacion.strftime("%Y")  # Año en cuatro dígitos
        correlativo = f"{self.numero_correlativo:04d}"  # Número correlativo con 4 dígitos rellenados con ceros
        return f"{correlativo}/{mes}/{anio}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo si es un objeto nuevo
            # Obtener el último número correlativo del año actual
            anio_actual = self.fecha_creacion.year
            ultimo_correlativo = HojaRuta.objects.filter(
                fecha_creacion__year=anio_actual
            ).aggregate(models.Max('numero_correlativo'))['numero_correlativo__max'] or 0
            self.numero_correlativo = ultimo_correlativo + 1
        
        # Generar y asignar el código antes de guardar
        self.codigo = self.generar_codigo()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = "Hoja de Ruta"
        verbose_name_plural = "Hojas de Ruta"
        ordering = ['-fecha_creacion', 'numero_correlativo']