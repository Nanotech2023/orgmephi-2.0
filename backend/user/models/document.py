import enum
from sqlalchemy.ext.hybrid import hybrid_property
from common import get_current_db, get_current_app
from .personal import UserInfo

db = get_current_db()
app = get_current_app()


class DocumentTypeEnum(enum.Enum):
    rf_passport = 'RFPassport'
    rf_international_passport = 'RFInternationalPassport'
    foreign_passport = 'ForeignPassport'
    other_document = 'OtherDocument'


document_names = {
    DocumentTypeEnum.rf_passport: app.config['ORGMEPHI_NATIVE_DOCUMENT'],
    DocumentTypeEnum.rf_international_passport:  app.config['ORGMEPHI_INTERNATIONAL_DOCUMENT'],
    DocumentTypeEnum.foreign_passport: app.config['ORGMEPHI_FOREIGN_DOCUMENT']
}

document_names_reverse = {val: key for key, val in document_names.items()}


class Document(db.Model):
    """
        Document ORM class
    """
    user_id = db.Column(db.Integer, db.ForeignKey(UserInfo.user_id), primary_key=True)
    document_type = db.Column(db.Enum(DocumentTypeEnum))
    series = db.Column(db.String)
    number = db.Column(db.String)
    issuer = db.Column(db.String)
    issue_date = db.Column(db.Date)
    rf_code = db.Column(db.String(7))
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
        self.document_type = DocumentTypeEnum.other_document

    user = db.relationship('UserInfo', back_populates='document')
