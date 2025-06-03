from dj_rql.filter_cls import AutoRQLFilterClass
from home.models import Company, EmissionScope, DocumentUpload, EmissionData 


class CompanyFilterClass(AutoRQLFilterClass):
    MODEL = Company


class EmissionScopeFilterClass(AutoRQLFilterClass):
    MODEL = EmissionScope


class DocumentUploadFilterClass(AutoRQLFilterClass):
    MODEL = DocumentUpload


class EmissionDataFilterClass(AutoRQLFilterClass):
    MODEL = EmissionData
