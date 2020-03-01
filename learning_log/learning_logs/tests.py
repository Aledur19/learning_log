import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Entry


class EntryModelTests(TestCase):

    def test_was_published_recently_with_future_Entry(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_Entry = Entry(date_added=time)
        self.assertIs(future_Entry.was_published_recently(), False)

    def test_was_published_recently_with_old_Entry(self):
        """
        was_published_recently() returns False for Entrys whose date_added
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_Entry = Entry(date_added=time)
        self.assertIs(old_Entry.was_published_recently(), False)

    def test_was_published_recently_with_recent_Entry(self):
        """
        was_published_recently() returns True for Entrys whose date_added
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_Entry = Entry(date_added=time)
        self.assertIs(recent_Entry.was_published_recently(), True)


def create_Entry(Entry_text, days):
    """
    Create a Entry with the given `Entry_text` and published the
    given number of `days` offset to now (negative for Entrys published
    in the past, positive for Entrys that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Entry.objects.create(Entry_text=Entry_text, date_added=time)


class EntryIndexViewTests(TestCase):
    def test_no_Entrys(self):
        """
        If no Entrys exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_Entry_list'], [])

    def test_past_Entry(self):
        """
        Entrys with a date_added in the past are displayed on the
        index page.
        """
        create_Entry(Entry_text="Past Entry.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_Entry_list'],
            ['<Entry: Past Entry.>']
        )

    def test_future_Entry(self):
        """
        Entrys with a date_added in the future aren't displayed on
        the index page.
        """
        create_Entry(Entry_text="Future Entry.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_Entry_list'], [])

    def test_future_Entry_and_past_Entry(self):
        """
        Even if both past and future Entrys exist, only past Entrys
        are displayed.
        """
        create_Entry(Entry_text="Past Entry.", days=-30)
        create_Entry(Entry_text="Future Entry.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_Entry_list'],
            ['<Entry: Past Entry.>']
        )

    def test_two_past_Entrys(self):
        """
        The Entrys index page may display multiple Entrys.
        """
        create_Entry(Entry_text="Past Entry 1.", days=-30)
        create_Entry(Entry_text="Past Entry 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_Entry_list'],
            ['<Entry: Past Entry 2.>', '<Entry: Past Entry 1.>']
        )


class EntryDetailViewTests(TestCase):
    def test_future_Entry(self):
        """
        The detail view of a Entry with a date_added in the future
        returns a 404 not found.
        """
        future_Entry = create_Entry(Entry_text='Future Entry.', days=5)
        url = reverse('polls:detail', args=(future_Entry.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_Entry(self):
        """
        The detail view of a Entry with a date_added in the past
        displays the Entry's text.
        """
        past_Entry = create_Entry(Entry_text='Past Entry.', days=-5)
        url = reverse('polls:detail', args=(past_Entry.id,))
        response = self.client.get(url)
        self.assertContains(response, past_Entry.Entry_text)
