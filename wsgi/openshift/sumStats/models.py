from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Genotype(models.Model):

    genotype_name=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.genotype_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class SequenceLength(models.Model):
    
    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.IntegerField(default=None)

    def __unicode__(self):
        return ("Name: %s Length: %s") %(self.seqName, str(self.seqLen))

class fiveUTRlength(models.Model):
    
    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.IntegerField(default=None)

    def __unicode__(self):
        return ("Name: %s Length: %s") %(self.seqName, str(self.seqLen))

class threeUTRlength(models.Model):

    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.IntegerField(default=None)

    def __unicode__(self):
        return ("Name: %s Length: %s") %(self.seqName, str(self.seqLen))


class codingSeqLength(models.Model):

    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.IntegerField(default=None)

    def __unicode__(self):
        return ("Name: %s Length: %s") %(self.seqName, str(self.seqLen))

class sequenceGC(models.Model):
    
    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.FloatField(default=None)

    def __unicode__(self):
        return ("Name: %s gc-content: %s") %(self.seqName, str(self.seqLen))

class codingSeqGC(models.Model):

    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.FloatField(default=None)


    def __unicode__(self):
        return ("Name: %s gc-content: %s") %(self.seqName, str(self.seqLen))


class fiveUTRgc(models.Model):

    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.FloatField(default=None)

    def __unicode__(self):
        return ("Name: %s gc-content: %s") %(self.seqName, str(self.seqLen))

class threeUTRgc(models.Model):

    genotype = models.ForeignKey(Genotype)
    seqName = models.CharField(max_length=200)
    seqLen = models.FloatField(default=None)

    def __unicode__(self):
        return ("Name: %s gc-content: %s") %(self.seqName, str(self.seqLen))

class Mir(models.Model):
    
    genotype = models.ForeignKey(Genotype)
    mir_name = models.CharField(max_length=200)
    mir_reg = models.CharField(max_length=200)
    
    def __unicode__(self):
        return ("%s, %s")%(self.mir_name, self.mir_reg)


class mirTarget(models.Model):
    
    #genotype = models.ForeignKey(Genotype)
    mirName = models.ForeignKey(Mir)
    seqName = models.CharField(max_length=200)
    tScore = models.IntegerField(default=None)


    def __unicode__(self):
        return ("seqName: %s tScore: %s") %(self.seqName, str(self.tScore))
