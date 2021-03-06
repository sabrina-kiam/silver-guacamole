from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		MAX_WAIT = 10
		start_time = time.time()

		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(
					row_text, [row.text for row in rows]
				)
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_and_retrieve_it_later(self):
		# We go to check out the homepage
		self.browser.get(self.live_server_url)

		# We want to confirm title has to do lists
		self.assertIn('To-Do', self.browser.title)

		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# she is invited to enter a to do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# she types "buy feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')

		# when she hits enter, the page updates, and now the page
		# lists "1: buy peacock feathers" as a to do item
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# there is a text box to add anotehr item.
		# she enteres "use feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make fly')
		inputbox.send_keys(Keys.ENTER)

		# page updates again, show both items in thel ist
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make fly')

		self.fail('finish the test!')

		# we wonder if site will remember her list.

		# sees a unique url
		# visit that URL. and to do list is still there

		# goes back to sleep
