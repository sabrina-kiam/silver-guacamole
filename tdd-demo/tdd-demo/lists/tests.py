from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.models import Item
from lists.views import home_page

class ListViewTest(TestCase):
	def test_displays_all_items(self):
		Item.objects.create(text="itemy1")
		Item.objects.create(text="itemy2")

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemy1')
		self.assertContains(response, 'itemy2')

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
	def test_can_save_post_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_can_redirect_after_post(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class HomePageTest(TestCase):

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'the first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved = saved_items[0]
		second_saved = saved_items[1]
		self.assertEqual(first_saved.text, 'the first (ever) list item')
		self.assertEqual(second_saved.text, 'Item the second')
