from django.contrib import admin
from sumStats.models import Genotype, SequenceLength
# Register your models here.

admin.site.register(Genotype, GenotypeAdmin)

class SequenceLengthInline(admin.TabularInline):
    model = SequenceLength
    extra = 1

class GenotypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['genotype_name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    
    inlines = [SequenceLengthInline]
    
    list_display = ('genotype_name', 'pub_date', 'was_published_recently')

    search_fields = ['genotype_name', 'sequencelength__seqName']
    
