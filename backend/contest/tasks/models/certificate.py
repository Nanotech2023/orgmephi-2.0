from common import get_current_db
from common.media_types import CertificateImage, Json
from contest.tasks.models import UserStatusEnum

db = get_current_db()


class CertificateType(db.Model):
    certificate_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    certificates = db.relationship('Certificate', lazy='select', cascade='all,delete',
                                   back_populates='certificate_type')


class Certificate(db.Model):
    __table_args__ = (db.UniqueConstraint('certificate_type_id', 'certificate_category'),)
    certificate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    certificate_type_id = db.Column(db.Integer, db.ForeignKey(CertificateType.certificate_type_id), nullable=False)
    certificate_category = db.Column(db.Enum(UserStatusEnum), nullable=False)
    certificate_image = db.Column(CertificateImage.as_mutable(Json), nullable=False)
    text_fields = db.Column(db.JSON, nullable=False)
    certificate_type = db.relationship('CertificateType', lazy='select', back_populates='certificates')
