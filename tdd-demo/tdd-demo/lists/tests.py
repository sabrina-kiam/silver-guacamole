from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.models import Item
from lists.views import home_page

class HomePageTest(TestCase):

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_post_request(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_can_redirect_after_post(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_only_save_non_empty_items(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)

	def test_displays_all_list_items(self):
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')

		response = self.client.get('/')
		self.assertIn('item 1', response.content.decode())
		self.assertIn('item 2', response.content.decode())


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
