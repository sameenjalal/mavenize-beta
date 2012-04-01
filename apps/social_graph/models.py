from django.db import models

class Forward(models.Model):
    source_id = models.BigIntegerField(db_index=True)
    destination_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)

class Backward(models.Model):
    destination_id = models.BigIntegerField(db_index=True)
    source_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "User #%s following User #%s" % (self.source_id,
            self.destination_id)
