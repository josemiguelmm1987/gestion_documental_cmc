from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Cargo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Cargo", unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Tipo de Documento", unique=True)
    sigla = models.CharField(max_length=255, verbose_name="Sigla del Tipo de Documento", blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.sigla})"
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

class Entidad(models.Model):
    class TipoPersona:
        PERSONA_NATURAL = 'Persona Natural'
        PERSONA_JURIDICA = 'Persona Jurídica'
        choices = [
            (PERSONA_NATURAL, 'Persona Natural'),
            (PERSONA_JURIDICA, 'Persona Jurídica'),
        ]

    tipo_persona = models.CharField(max_length=20, choices=TipoPersona.choices)
    nombre = models.CharField(max_length=255, verbose_name="Nombre")

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
    

class Documento(models.Model):
    # Campos obligatorios
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, verbose_name="Tipo de Documento")
    fecha_hora_recepcion = models.DateTimeField(verbose_name="Fecha y Hora de Recepción")
    referencia = models.TextField(verbose_name="Referencia")
    observaciones = models.TextField(verbose_name="Observaciones", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Campo opcional (para documentos sin identificación)
    identificacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Identificación del Documento")
    enlace_drive = models.URLField(max_length=500, blank=True, null=True, verbose_name="Enlace")

    def __str__(self):
        return f"Documento {self.id} - {self.identificacion}"

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

class EntidadRemitente(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, verbose_name="Documento")
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="entidad_remitente_documento", verbose_name="Entidad")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='Cargo', blank=True, null=True)  # Solo aplica si es una persona_natural
    dependencia = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="dependencia_remitente_documento", verbose_name="Dependencia", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Validar según el tipo de persona de la entidad

        if self.entidad.tipo_persona == Entidad.TipoPersona.PERSONA_JURIDICA:
            # Si es Persona Jurídica, no se permiten cargo ni dependencia
            if self.cargo:
                raise ValidationError("El campo 'cargo' no debe estar definido para una Persona Jurídica.")
            if self.dependencia:
                raise ValidationError("El campo 'dependencia' no debe estar definido para una Persona Jurídica.")
        
        # elif self.entidad.tipo_persona == Entidad.TipoPersona.PERSONA_NATURAL:
        #     # Si es Persona Natural, cargo y dependencia son obligatorios
        #     if not self.cargo:
        #         raise ValidationError("El campo 'cargo' es obligatorio para una Persona Natural.")
        #     if not self.dependencia:
        #         raise ValidationError("El campo 'dependencia' es obligatorio para una Persona Natural.")
        #     # Verificar que la dependencia sea una Persona Jurídica
        #     if self.dependencia and self.dependencia.tipo_persona != Entidad.TipoPersona.PERSONA_JURIDICA:
        #         raise ValidationError("La 'dependencia' debe ser una Persona Jurídica para una Persona Natural.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entidad.nombre} - {self.documento}"
    
class EntidadDestinatario(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, verbose_name="Documento")
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="entidad_destinatario_documento", verbose_name="Entidad")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='Cargo', blank=True, null=True)  # Solo aplica si es una persona_natural
    dependencia = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name="dependencia_destinatario_documento", verbose_name="Dependencia", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Validar según el tipo de persona de la entidad
        if self.entidad.tipo_persona == Entidad.TipoPersona.PERSONA_NATURAL:
            # Si es Persona Natural, cargo y dependencia son obligatorios
            if not self.cargo:
                raise ValidationError("El campo 'cargo' es obligatorio para una Persona Natural.")
            if not self.dependencia:
                raise ValidationError("El campo 'dependencia' es obligatorio para una Persona Natural.")
            # Verificar que la dependencia sea una Persona Jurídica
            if self.dependencia and self.dependencia.tipo_persona != Entidad.TipoPersona.PERSONA_JURIDICA:
                raise ValidationError("La 'dependencia' debe ser una Persona Jurídica para una Persona Natural.")

        elif self.entidad.tipo_persona == Entidad.TipoPersona.PERSONA_JURIDICA:
            # Si es Persona Jurídica, no se permiten cargo ni dependencia
            if self.cargo:
                raise ValidationError("El campo 'cargo' no debe estar definido para una Persona Jurídica.")
            if self.dependencia:
                raise ValidationError("El campo 'dependencia' no debe estar definido para una Persona Jurídica.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entidad.nombre} - {self.documento}"