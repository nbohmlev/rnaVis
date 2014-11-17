from django.test import TestCase

import datetime
from django.utils import timezone
from sumStats.models import Genotype, SequenceLength
from django.core.urlresolvers import reverse
# Create your tests here.

class GenotypeMethodTests(TestCase):
    def test_was_published_recently_with_future_genotype(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_genotype = Genotype(pub_date=time)
        self.assertEqual(future_genotype.was_published_recently(), False)
        
    def test_was_published_recently_with_old_genotype(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_genotype = Genotype(pub_date=time)
        self.assertEqual(old_genotype.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_genotype = Genotype(pub_date=time)
        self.assertEqual(recent_genotype.was_published_recently(), True)

def create_genotype(genotype_name, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Genotype.objects.create(genotype_name=genotype_name,
                                       pub_date=time)

class GenotypeViewTests(TestCase):
    def test_index_view_with_no_genotypes(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('sumStats:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No genotypes are available.")
        self.assertQuerysetEqual(response.context['latest_genotype_list'], [])

    def test_index_view_with_a_past_genotype(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page
        """
        create_genotype(genotype_name="Past genotype.", days=-30)
        response = self.client.get(reverse('sumStats:index'))
        self.assertQuerysetEqual(
            response.context['latest_genotype_list'],
            ['<Genotype: Past genotype.>']
        )

    def test_index_view_with_a_future_genotype(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_genotype(genotype_name="Future genotype.", days=30)
        response = self.client.get(reverse('sumStats:index'))
        self.assertContains(response, "No genotypes are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_genotype_list'], [])

    def test_index_view_with_future_genotype_and_past_genotype(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_genotype(genotype_name="Past genotype.", days=-30)
        create_genotype(genotype_name="Future genotype.", days=30)
        response = self.client.get(reverse('sumStats:index'))
        self.assertQuerysetEqual(
            response.context['latest_genotype_list'],
            ['<Genotype: Past genotype.>']
        )

    def test_index_view_with_two_past_genotypes(self):
        """
        The questions index page may display multiple questions.
        """
        create_genotype(genotype_name="Past genotype 1.", days=-30)
        create_genotype(genotype_name="Past genotype 2.", days=-5)
        response = self.client.get(reverse('sumStats:index'))
        self.assertQuerysetEqual(
            response.context['latest_genotype_list'],
            ['<Genotype: Past genotype 2.>', '<Genotype: Past genotype 1.>']
        )

class GenotypeResultTests(TestCase):

    def test_all_genotypes_are_populated(self):
        genotypes_all = Genotype.objects.all()
        pop = False
        for genotype in genotypes_all:
            if len(genotype.sequencelength_set.values()):
                pop = True
            else:
                pop = False
        self.assertEqual(pop, True)
