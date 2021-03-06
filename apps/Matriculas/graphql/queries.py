import graphene
import graphene_django_optimizer as gql_optimizer

from BackStrawBerryPy.models import BaseModel
from apps.Matriculas.graphql.types import PeriodoLectivoType, AulaType, AlumnoAulaType, \
    EstadosPeriodoLectivoEnum
from apps.Matriculas.models import PeriodoLectivo, Aula, AlumnoAula


class MatriculasQueries(graphene.ObjectType):
    periodos_lectivos = graphene.List(
        PeriodoLectivoType,
        estados=graphene.List(EstadosPeriodoLectivoEnum, default_value=[])
    )
    periodo_lectivo = graphene.Field(PeriodoLectivoType, id=graphene.ID(required=True))

    aulas = graphene.List(AulaType)
    aulas_periodo_abierto = graphene.List(AulaType)
    aula = graphene.Field(AulaType, id=graphene.ID(required=True))

    matriculas = graphene.List(AlumnoAulaType)
    matricula = graphene.Field(AlumnoAulaType, id=graphene.ID(required=True))

    def resolve_periodo_lectivo(self, info, id):
        return PeriodoLectivo.objects.filter(pk=id).first()

    def resolve_periodos_lectivos(self, info, estados: list):
        if estados.__len__() == 0:
            return gql_optimizer.query(PeriodoLectivo.objects.filter(auth_estado=BaseModel.ACTIVO), info)
        return gql_optimizer.query(
            PeriodoLectivo.objects.filter(estado__in=estados, auth_estado=BaseModel.ACTIVO),
            info
        )

    def resolve_aula(self, info, id):
        return Aula.objects.filter(pk=id).first()

    def resolve_aulas(self, info, **kwargs):
        return gql_optimizer.query(
            Aula.objects.filter(periodo__auth_estado=BaseModel.ACTIVO),
            info
        )

    def resolve_aulas_periodo_abierto(self, info, **kwargs):
        return gql_optimizer.query(
            Aula.objects.filter(
                periodo__estado=PeriodoLectivo.EstadosPeriodo.ABIERTO,
                periodo__auth_estado=BaseModel.ACTIVO
            ),
            info
        )

    def resolve_matriculas(self, info, **kwargs):
        return AlumnoAula.objects.filter(auth_estado=BaseModel.ACTIVO).order_by(
            'aula__periodo__nombre',
            'aula__nombre',
            'alumno__persona__identificacion'
        )

    def resolve_matricula(self, info, id):
        return AlumnoAula.objects.filter(pk=id).first()
