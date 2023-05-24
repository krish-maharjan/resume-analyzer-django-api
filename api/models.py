from django.db import models
import os

def get_upload_path(instance, filename):
    return os.path.join('rdocs', instance.profile.email, filename)


class Profile(models.Model):
    email = models.CharField(max_length=140, default='', blank=False)
    keywords_received = models.CharField(max_length=10000, null=True, blank=False)

    def __str__(self):
        return self.email
    
class File(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='files')

    # saving files in a folder with email/date/
    rdoc = models.FileField(upload_to=get_upload_path, blank=False)
    
    # saving files in a folder with year date/month/day
    # rdoc = models.FileField(upload_to='rdocs/%Y/%m/%d/', blank=False)

    class Meta:
        verbose_name_plural = "Files"
    
# In order to delete files in media/rdocs as soon as they are being deleted in admin pannel
from django.db.models.signals import post_delete
from django.dispatch import receiver

def delete_file(sender, instance, **kwargs):
    """
    Deletes the file when the corresponding Profile instance is deleted
    """
    if instance.rdoc:
        if os.path.isfile(instance.rdoc.path):
            os.remove(instance.rdoc.path)

@receiver(post_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    """
    Calls delete_file when a Profile instance is deleted
    """
    delete_file(sender, instance, **kwargs)
