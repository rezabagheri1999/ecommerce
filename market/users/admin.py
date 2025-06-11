from django.contrib import admin
from .models import User,UserProfile,ContactMessage
# Register your models here.
admin.site.register(UserProfile)
# admin.site.register(ContactMessage)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['__str__','name','subject','is_read']

    class Meta:
        model = ContactMessage

# Register your models here.



admin.site.register(ContactMessage,ContactMessageAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)