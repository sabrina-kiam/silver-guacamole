from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# We go to check out the homepage
		self.browser.get('http://localhost:8000')

		# We want to confirm title has to do lists
		self.assertIn('To-Do', self.browser.title)

		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# she is invited to enter a to do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			' Enter a to-do item'
		)

		# she types "buy feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')

		# when she hits enter, the page updates, and now the page
		# lists "1: buy peacock feathers" as a to do item
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for row in rows)
		)

		# there is a text box to add anotehr item.
		# she enteres "use feathers to make a fly"
		self.fail('finish the test!')

		# page updates again, show both items in thel ist

		# we wonder if site will remember her list.

		# sees a unique url
		# visit that URL. and to do list is still there

		# goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')