import enum
from sqlalchemy.ext.hybrid import hybrid_property
from common import get_current_db, get_current_app
from .personal import UserInfo
from user.util import get_unfilled

db = get_current_db()
app = get_current_app()


class DocumentTypeEnum(enum.Enum):
    rf_passport = 'RFPassport'
    rf_international_passport = 'RFInternationalPassport'
    foreign_passport = 'ForeignPassport'
    other_document = 'OtherDocument'
    birth_certificate = 'BirthCertificate'


document_names = {
    DocumentTypeEnum.rf_passport: app.config['ORGMEPHI_NATIVE_DOCUMENT'],
    DocumentTypeEnum.rf_international_passport:  app.config['ORGMEPHI_INTERNATIONAL_DOCUMENT'],
    DocumentTypeEnum.foreign_passport: app.config['ORGMEPHI_FOREIGN_DOCUMENT'],
    DocumentTypeEnum.birth_certificate: app.config['ORGMEPHI_BIRTH_CERTIFICATE']
}

document_names_reverse = {val: key for key, val in document_names.items()}


class Document(db.Model):
    """
        Document ORM class

        insurance_policy: snils
    """
    user_id = db.Column(db.Integer, db.ForeignKey(UserInfo.user_id), primary_key=True)
    document_type = db.Column(db.Enum(DocumentTypeEnum), nullable=False)
    series = db.Column(db.String)
    number = db.Column(db.String)
    issuer = db.Column(db.String)
    issue_date = db.Column(db.Date)
    rf_code = db.Column(db.String(7))
    insurance_policy = db.Column(db.String)
    other_document_name = db.Column(db.String)

    @hybrid_property
    def code(self):
        return self.rf_code if self.document_type == DocumentTypeEnum.rf_passport else None

    @code.setter
    def code(self, value):
        self.rf_code = value

    @property
    def document_name(self):
        if self.document_type == DocumentTypeEnum.other_document:
            return self.other_document_name
        else:
            return document_names[self.document_type]

    @document_name.setter
    def document_name(self, value):
        self.other_document_name = value

    user = db.relationship('UserInfo', back_populates='document')

    _required_fields = {
        DocumentTypeEnum.rf_passport: ['series', 'number', 'issuer', 'issue_date', 'rf_code'],
        DocumentTypeEnum.rf_international_passport: ['series', 'number', 'issue_date'],
        DocumentTypeEnum.foreign_passport: ['number', 'issue_date'],
        DocumentTypeEnum.birth_certificate: ['series', 'number', 'issuer', 'issue_date'],
        DocumentTypeEnum.other_document: ['number', 'other_document_name']
    }

    def unfilled(self):
        return get_unfilled(self, self._required_fields[self.document_type], [])
