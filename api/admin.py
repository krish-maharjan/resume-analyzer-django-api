from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'keywords_received', 'rdoc_filename')
    
    def rdoc_filename(self, obj):
        """
        Custom function to display the filename in the admin panel
        """
        if obj.files.exists():
            return format_html("<br>".join([f.rdoc.name.split('/')[-1] for f in obj.files.all()]))
        return "-"
    
    rdoc_filename.short_description = "Uploaded Files"

admin.site.register(Profile, ProfileModelAdmin)
