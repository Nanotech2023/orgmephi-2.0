import enum

from common import get_current_db
from common.media_types import CertificateImage, Json
from contest.tasks.models import UserStatusEnum

db = get_current_db()


class LocationEnum(enum.Enum):
    OlympiadLocation = "OlympiadLocation"
    OnlineOlympiadLocation = "OnlineOlympiadLocation"
    RussiaOlympiadLocation = "RussiaOlympiadLocation"
    OtherOlympiadLocation = "OtherOlympiadLocation"


class CertificateType(db.Model):
    certificate_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String)


class Certificate(db.Model):
    certificate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    certificate_type_id = db.Column(db.Integer, db.ForeignKey(CertificateType.certificate_type_id), nullable=False)
    certificate_category = db.Column(db.Enum(UserStatusEnum), nullable=False)
    certificate_image = db.Column(CertificateImage.as_mutable(Json), nullable=False)
    text_fields = db.Column(db.JSON, nullable=False)
