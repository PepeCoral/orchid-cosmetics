from django.core.exceptions import ObjectDoesNotExist

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id):
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs):
        instance = self.model.objects.create(**kwargs)
        return instance

    def update(self, id, **kwargs):
        instance = self.get_by_id(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, id):
        instance = self.get_by_id(id)
        if not instance:
            return False
        instance.delete()
        return True
