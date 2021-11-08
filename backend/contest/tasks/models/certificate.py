from common import get_current_db
from common.media_types import CertificateImage, Json
from contest.tasks.models import UserStatusEnum

db = get_current_db()


class CertificateType(db.Model):
    certificate_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    certificates = db.relationship('Certificate', lazy='dynamic', cascade='all,delete',
                                   back_populates='certificate_type')
    contests = db.relationship('BaseContest', lazy='select',
                               backref=db.backref('certificate_type', lazy='select'))


class Certificate(db.Model):
    __table_args__ = (db.UniqueConstraint('certificate_type_id', 'certificate_category'),)
    certificate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    certificate_type_id = db.Column(db.Integer, db.ForeignKey(CertificateType.certificate_type_id), nullable=False)
    certificate_category = db.Column(db.Enum(UserStatusEnum), nullable=False)
    certificate_image = db.Column(CertificateImage.as_mutable(Json), nullable=False)

    text_x = db.Column(db.Integer, nullable=False)
    text_y = db.Column(db.Integer, nullable=False)
    text_width = db.Column(db.Integer, nullable=False)
    text_size = db.Column(db.Integer, nullable=False, default=14)
    text_style = db.Column(db.String, nullable=False, default='DejaVuSans')
    text_spacing = db.Column(db.Integer, nullable=False, default=0)
    text_color = db.Column(db.String(9), nullable=False, default='#000000ff')
    max_lines = db.Column(db.Integer, nullable=True, default=1)

    certificate_type = db.relationship('CertificateType', lazy='select', back_populates='certificates')
