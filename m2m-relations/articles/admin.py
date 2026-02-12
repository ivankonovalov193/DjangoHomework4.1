from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        super().clean()

        main_count = 0
        has_data = False

        for form in self.forms:
            if self._should_skip_form(form):
                continue

            has_data = True
            if form.cleaned_data.get('is_main'):
                main_count += 1

        if has_data:
            if main_count == 0:
                raise ValidationError('Укажите основной раздел')
            elif main_count > 1:
                raise ValidationError('Основным может быть только один раздел')

    def _should_skip_form(self, form):
        if not form.cleaned_data:
            return True
        if form.cleaned_data.get('DELETE'):
            return True
        if not form.cleaned_data.get('tag'):
            return True
        return False


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    autocomplete_fields = ['tag']
    verbose_name = 'Раздел'
    verbose_name_plural = 'Разделы статьи'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'text']
    list_filter = ['published_at', 'tags']
    date_hierarchy = 'published_at'

    inlines = [ScopeInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'text', 'published_at')
        }),
        ('Медиа', {
            'fields': ('image',),
            'classes': ('wide',)
        }),
    )