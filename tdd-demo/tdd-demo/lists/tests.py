from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.models import Item, List
from lists.views import home_page

class NewItemTest(TestCase):
	def test_can_save_post_request_to_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'a new item for an existing list'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'a new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirect_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'new item'}
		)
		self.assertRedirects(response, f'/lists/{correct_list.id}/')

class ListViewTest(TestCase):
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)
		
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text="itemy1", list=correct_list)
		Item.objects.create(text="itemy2", list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text="other itemy1", list=other_list)
		Item.objects.create(text="other itemy2", list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemy1')
		self.assertContains(response, 'itemy2')
		self.assertNotContains(response, 'other itemy1')
		self.assertNotContains(response, 'other itemy2')

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
	def test_can_save_post_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_can_redirect_after_post(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')


class HomePageTest(TestCase):

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelsTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'the first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved = saved_items[0]
		second_saved = saved_items[1]
		self.assertEqual(first_saved.text, 'the first (ever) list item')
		self.assertEqual(first_item.list, list_)
		self.assertEqual(second_saved.text, 'Item the second')
		self.assertEqual(second_saved.list, list_)
