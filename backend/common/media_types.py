import functools
import io
import json
from sqlalchemy import TypeDecorator, Unicode
from sqlalchemy_media import StoreManager, Image, ImageAnalyzer, ImageValidator, ImageProcessor, Store, File, \
    ContentTypeValidator, MagicAnalyzer
from sqlalchemy_media.constants import MB

_in_memory_store_dict = dict()


class InMemoryStore(Store):
    def put(self, filename: str, stream):
        _in_memory_store_dict[filename] = stream.read()
        return len(_in_memory_store_dict[filename])

    def delete(self, filename: str):
        del _in_memory_store_dict[filename]

    def open(self, filename: str, mode: str = 'rb'):
        return io.BytesIO(_in_memory_store_dict[filename])

    def locate(self, attachment) -> str:
        return f':memory:/{attachment.path}'


class DefaultStore(Store):
    def put(self, filename: str, stream):
        raise NotImplementedError

    def delete(self, filename: str):
        raise NotImplementedError

    def open(self, filename: str, mode: str = 'rb'):
        raise NotImplementedError

    def locate(self, attachment) -> str:
        raise NotImplementedError


StoreManager.register(
    'default',
    functools.partial(DefaultStore),
    default=True
)


class Json(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None
        return json.loads(value)


class ProfileImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(600, 800),
            min_aspect_ratio=0.75,
            content_types=['image/jpeg', 'image/png']
        ),
        ImageProcessor(
            fmt='jpeg',
            width=120
        )
    ]


class AnswerFile(File):
    __pre_processors__ = [
        MagicAnalyzer(),
        ContentTypeValidator(['application/pdf', 'application/msword', 'application/zip', 'image/jpeg', 'image/png',
                              'image/gif', 'text/plain'])
    ]

    __max_length__ = 16 * MB


class TaskImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(20, 20),
            maximum=(1920, 1080),
            content_types=['image/jpeg', 'image/png']
        )
    ]


class NewsImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(20, 20),
            maximum=(1920, 1080),
            content_types=['image/jpeg', 'image/png']
        )
    ]


class CertificateImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(20, 20),
            maximum=(3840, 2160),
            content_types=['image/jpeg', 'image/png']
        )
    ]