from typing import Type, Optional, Any
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class BaseRepository:
    def __init__(self, model: Type[models.Model]):
        self.model: Type[models.Model] = model

    def get_all(self) -> models.QuerySet:
        return self.model.objects.all()

    def get_by_id(self, id: int) -> Optional[models.Model]:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs: Any) -> models.Model:
        instance: models.Model = self.model.objects.create(**kwargs)
        return instance

    def update(self, id: int, **kwargs: Any) -> Optional[models.Model]:
        instance = self.get_by_id(id)
        if not instance:
            return None

        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if not instance:
            return False
        instance.delete()
        return True
