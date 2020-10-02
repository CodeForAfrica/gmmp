from django.db import models

class _ObjectsQuerySet(models.query.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.deleted = True
            # Mark all Newspaper Person and Journalists as deleted too
            obj.newspaperperson_set.update(deleted=True)
            obj.newspaperjournalist_set.update(deleted=True)
            obj.save()

class CustomManager(models.Manager):
    def get_queryset(self):
        return _ObjectsQuerySet(self.model, using=self._db).filter(deleted=False)
