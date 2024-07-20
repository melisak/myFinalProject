import os
import xml.etree.ElementTree as ET
import re
import logging


# Get the logger instance


class BasePage:
    def __init__(self, page):
        self.page = page
        self.context = page.context
        self.browser = page.context.browser
        self.base_url = "https://openlibrary.org/"

        self.username = self.get_data_from_xml("USER_NAME")
        self.password = self.get_data_from_xml("PASSWORD")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("BasePage initialized")

    @staticmethod
    def get_data_from_xml(node_name):
        try:
            # Get the directory of the current script
            base_dir = os.path.dirname(__file__)
            # Construct the full path to data.xml
            xml_path = os.path.join(base_dir, "..", "tests", "data.xml")
            root = ET.parse(xml_path).getroot()
            node = root.find(".//" + node_name)
            if node is None:
                raise ValueError(f"Node {node_name} not found in XML")
            return node.text
        except Exception as e:
            print(f"Error reading XML data for {node_name}: {str(e)}")
            raise

    def handle_dialog(self, dialog, status):
        print("\ndialog text is: ", dialog.message)
        if status == "accept":
            dialog.accept()
        else:
            dialog.dismiss()

    def set_dialog_handler(self, status):
        self.page.once("dialog", lambda dialog: self.handle_dialog(dialog, status))

    def extract_results_count(self, text):
        match = re.search(r'[\d,]+', text)
        if match:
            return int(match.group().replace(',', ''))
        return None

    def highlight(self, selector, selector_type='xpath', name=None, index=0):
        if selector_type == 'css':
            self.logger.info(f"Highlighting CSS selector: {selector}")
            self.page.evaluate("""
                (selector) => {
                    const element = document.querySelector(selector);
                    if (element) {
                        element.style.border = '2px solid red';
                        element.style.backgroundColor = 'yellow';
                        element.style.color = 'black';
                    }
                }
            """, selector)
        elif selector_type == 'xpath':
            self.logger.info(f"Highlighting XPath selector: {selector}")
            self.page.evaluate("""
                ({ xpath, index }) => {
                    const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    const item = result.snapshotItem(index);
                    if (item) {
                        item.style.border = '2px solid red';
                        item.style.backgroundColor = 'yellow';
                        item.style.color = 'black';
                    }
                }
            """, {"xpath": selector, "index": index})
        elif selector_type == 'role' and name is not None:
            self.logger.info(f"Highlighting Role selector: role={selector}, name={name}")
            self.page.evaluate("""
                ({ role, name, index }) => {
                    const elements = document.querySelectorAll(`[role='${role}']`);
                    const item = Array.from(elements).filter(element => element.getAttribute('aria-label') === name)[index];
                    if (item) {
                        item.style.border = '2px solid red';
                        item.style.backgroundColor = 'yellow';
                        item.style.color = 'black';
                    }
                }
            """, {"role": selector, "name": name, "index": index})
        elif selector_type == 'text':
            self.logger.info(f"Highlighting Text selector: {selector}")
            self.page.evaluate("""
                ({ text, index }) => {
                    const elements = Array.from(document.querySelectorAll('*')).filter(element => element.textContent.trim() === text);
                    const item = elements[index];
                    if (item) {
                        item.style.border = '2px solid red';
                        item.style.backgroundColor = 'yellow';
                        item.style.color = 'black';
                    }
                }
            """, {"text": selector, "index": index})
        else:
            raise ValueError("Invalid selector type or missing name for 'role' selector type")

    def click(self, selector, selector_type='xpath', name=None, index=0):
        self.highlight(selector, selector_type, name, index)
        if selector_type == 'css':
            self.page.locator(selector).nth(index).click()
        elif selector_type == 'xpath':
            self.page.locator(f"xpath={selector}").nth(index).click()
        elif selector_type == 'role' and name is not None:
            self.page.get_by_role(selector, name=name).nth(index).click()
        elif selector_type == 'text':
            self.page.get_by_text(selector).nth(index).click()
        else:
            raise ValueError("Invalid selector type or missing name for 'role' selector type")

    def fill(self, selector, text, selector_type='xpath', name=None, index=0):
        self.highlight(selector, selector_type, name, index)
        if selector_type == 'css':
            self.page.locator(selector).nth(index).fill(text)
        elif selector_type == 'xpath':
            self.page.locator(f"xpath={selector}").nth(index).fill(text)
        elif selector_type == 'role' and name is not None:
            self.page.get_by_role(selector, name=name).nth(index).fill(text)
        elif selector_type == 'text':
            self.page.get_by_text(selector).nth(index).fill(text)
        else:
            raise ValueError("Invalid selector type or missing name for 'role' selector type")

    def text(self, selector, selector_type='xpath', name=None, index=0):
        self.highlight(selector, selector_type, name, index)
        if selector_type == 'css':
            return self.page.locator(selector).nth(index).inner_text()
        elif selector_type == 'xpath':
            return self.page.locator(f"xpath={selector}").nth(index).inner_text()
        elif selector_type == 'role' and name is not None:
            return self.page.get_by_role(selector, name=name).nth(index).inner_text()
        elif selector_type == 'text':
            return self.page.get_by_text(selector).nth(index).inner_text()
        else:
            raise ValueError("Invalid selector type or missing name for 'role' selector type")
