from django.contrib import admin
from library.models.publisher import Publisher
from library.models.book import Book, PublishedBook


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        queryset = queryset.filter(owner=request.user)
        return queryset

    def get_fields(self, request, obj=None):
        all_fields = super().get_fields(request, obj)

        if not request.user.is_superuser:
            all_fields.remove('owner')

        return all_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            owner = form.cleaned_data.get('owner')

            if not owner:
                obj.owner = request.user

        super().save_model(request, obj, form, change)


@admin.register(PublishedBook)
class PublishedBookAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        queryset = queryset.filter(publisher__in=request.user.publishers.all())
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'publisher':
                kwargs['queryset'] = Publisher.objects.filter(owner=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "resource" and not request.user.is_superuser:
            kwargs["queryset"] = Resource.objects.filter(user=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Book)