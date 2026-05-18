from ninja import Schema

class AnnouncementOut(Schema):
    id: int
    title: str
    price: float
    image: str

    @staticmethod
    def resolve_image(obj):
        if obj.image:
            try:
                return obj.image.url
            except Exception:
                pass
        # Твоя локальная картинка-заглушка из папки static
        return "/static/img/no-photo.png"