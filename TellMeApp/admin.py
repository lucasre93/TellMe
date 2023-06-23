from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Story

# UNREGISTER.

admin.site.unregister(Group)
# MIX PROFILE INFO INTO USER INFO
class ProfileInline(admin.StackedInline):
    model = Profile

#EXTEND USER MODEL
class UserAdmin(admin.ModelAdmin):
    model = User
    #Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]

# UNREGISTER INITIAL USER
admin.site.unregister(User)
# REGISTER USER
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

# REGISTER STORIES
admin.site.register(Story)


