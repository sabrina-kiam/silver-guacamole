from selenium import webdriver
import unittest

class NewVisitorTeset(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# We go to check out the homepage
		self.browser.get('http://localhost:8000')

		# We want to confirm title has to do lists
		self.assertIn('To-Do', self.browser.title)

		self.fail('finish the test!')

		# she is invited to enter a to do item

		# she types "buy feathers" into a text box

		# when she hits enter, the page updates, and now the page
		# lists "1: buy peacock feathers" as a to do item

		# there is a text box to add anotehr item.
		# she enteres "use feathers to make a fly"

		# page updates again, show both items in thel ist

		# we wonder if site will remember her list.

		# sees a unique url
		# visit that URL. and to do list is still there

		# goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')