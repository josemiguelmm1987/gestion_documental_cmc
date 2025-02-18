from django.db import models

# Create your models here.

class Dependencia(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la Dependencia")
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"

class Ente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    cargo = models.CharField(max_length=255, verbose_name="Cargo", blank=True, null=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, verbose_name="Dependencia")

    def __str__(self):
        return f"{self.nombre} ({self.cargo} - {self.dependencia})"
    
    class Meta:
        verbose_name = "Remitente/Destinatario"
        verbose_name_plural = "Remitentes/Destinatarios"

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Documento", unique=True)
    sigla = models.CharField(max_length=255, verbose_name="Sigla del Tipo de Documento", blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.sigla})"
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

class Documento(models.Model):
    # Campos obligatorios
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, verbose_name="Tipo de Documento")
    remitentes = models.ManyToManyField(Ente, verbose_name="Remitentes", related_name="documento_remitentes")
    fecha_hora_recepcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de Recepción")
    destinatarios = models.ManyToManyField(Ente, verbose_name="Destinatarios", related_name="documento_destinatarios")
    referencia = models.TextField(verbose_name="Referencia")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Campo opcional (para documentos sin identificación)
    identificacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Identificación del Documento")
    enlace_drive = models.URLField(max_length=500, blank=True, null=True, verbose_name="Enlace de Google Drive")

    def __str__(self):
        return f"Documento {self.id} - {self.identificacion}"

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"