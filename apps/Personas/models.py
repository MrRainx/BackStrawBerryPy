from django.db import models

from BackStrawBerryPy.models import BaseModel
# Create your models here.
from utils.constants.DefaultValuesModels import NO_REGISTRA
from utils.functions import concat_if_exist


class FuncionPersonal(BaseModel):
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField()

    class Meta:
        db_table = 'RolesPersonal'


class Discapacidad(BaseModel):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Discapacidades'


class Persona(BaseModel):
    identificacion = models.CharField(max_length=30, unique=True)
    tipo_identificacion = models.CharField(max_length=20, )
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)

    pais_nacimiento = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    genero = models.CharField(max_length=10, )
    estado_civil = models.CharField(max_length=20, null=True, blank=True)

    tiene_discapacidad = models.CharField(max_length=10, default="NO")
    discapacidades = models.ManyToManyField(Discapacidad, blank=True)
    carnet_conadis = models.CharField(max_length=50, default='NO REGISTRA')

    porcentaje_discapacidad = models.PositiveSmallIntegerField(default=0)
    etnia = models.CharField(max_length=30, null=True, blank=True)

    tipo_sangre = models.CharField(max_length=30, null=True, blank=True)

    pais_residencia = models.CharField(max_length=150, null=True, blank=True)
    provincia_residencia = models.CharField(max_length=150, null=True, blank=True)
    canton_residencia = models.CharField(max_length=150, null=True, blank=True)
    parroquia_residencia = models.CharField(max_length=150, null=True, blank=True)
    direccion_domiciliaria = models.TextField(null=True, blank=True)
    sector = models.TextField(null=True, blank=True)

    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular_uno = models.CharField(max_length=20, null=True, blank=True)
    celular_dos = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=30, null=True, blank=True)

    foto = models.URLField(null=True, blank=True)
    extras = models.JSONField(null=True, blank=True)

    def full_name(self):
        return f'{self.primer_nombre} {self.primer_apellido}'

    def get_nombres(self):
        return concat_if_exist(self.primer_nombre, self.segundo_nombre)

    def get_apellidos(self):
        return concat_if_exist(self.primer_apellido, self.segundo_apellido)

    def __str__(self):
        return f'{self.identificacion} {self.full_name()}'

    def get_nombres_apellidos(self):
        return concat_if_exist(
            self.primer_apellido,
            self.segundo_apellido,
            self.primer_nombre,
            self.segundo_nombre
        )

    def get_edad(self):
        today = self.fecha_nacimiento.today()
        born = self.fecha_nacimiento
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    class Meta:
        db_table = 'Personas'


class Personal(BaseModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    funciones = models.ManyToManyField(FuncionPersonal, blank=True)
    titulo = models.CharField(max_length=150)
    tipo_titulo = models.CharField(max_length=150)
    area_de_trabajo = models.TextField(null=True, blank=True, default=NO_REGISTRA)
    '''
    info:JSON
        {
         titulo_profesional
            
        }
    '''
    meta_data = models.JSONField(null=True, blank=True)
    historico = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'Personal'

    def full_name(self):
        return self.persona.full_name()

    def __str__(self):
        return self.persona.__str__()

    def get_funciones_str(self):
        return ",\n".join(self.funciones.values_list('nombre', flat=True).all())


class Alumno(BaseModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='alumno')

    padre = models.JSONField(null=True, blank=True)

    madre = models.JSONField(null=True, blank=True)

    representante = models.JSONField(null=True, blank=True)

    contacto_emergencia = models.JSONField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)

    historia_clinica = models.CharField(max_length=20, null=True, blank=True)

    trastornos_asociados = models.TextField(null=True, blank=True)

    grado_dependencia = models.TextField(null=True, blank=True)

    bono = models.CharField(max_length=50, default="Ninguno")
    tipo_bono = models.CharField(max_length=50)
    afiliacion_iess = models.CharField(max_length=10)
    quintil_pobreza = models.CharField(max_length=10)

    class Meta:
        db_table = 'Alumnos'

    def map_padres(self, padre="padre"):
        selected: dict = self.__dict__.get(padre)
        apellidos_nombres = concat_if_exist(
            selected.get('primer_apellido', ""),
            selected.get('segundo_apellido', ""),
            selected.get('primer_nombre', ""),
            selected.get('segundo_nomre', ""),
        )
        selected['apellidos_nombres'] = apellidos_nombres
        return selected
