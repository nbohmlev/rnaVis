from django.contrib import admin
import sumStats.models as SA
# Register your models here.

class SequenceLengthInline(admin.StackedInline):
    model = SA.SequenceLength
    extra = 0

class threeUTRlengthInline(admin.TabularInline):
    model = SA.threeUTRlength
    extra = 0
    verbose_name = "Three UTR length"
    verbose_name_plural = "Three UTR lengths"

class GenotypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['genotype_name']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    
    inlines = [SequenceLengthInline, threeUTRlengthInline]
    
    list_display = ('genotype_name', 'pub_date', 'was_published_recently')
    search_fields = ['genotype_name', 'sequencelength__seqName']

admin.site.register(SA.Genotype, GenotypeAdmin)
