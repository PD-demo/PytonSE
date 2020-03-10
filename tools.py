import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import json
import os

class JsonTools(object):
    def loadjson(self, relative_path):
        base_path = os.path.abspath(os.path.dirname(__file__))
        data=None
        try:
            data = json.load(open(base_path + "\\" + relative_path))
        except:
            pass
        return data


    def getjsonstack(self, json_object, element_name, stack):
        result = []
        try:
            stack.append({"SelectorType": json_object["SelectorType"], "Selector": json_object["Selector"]})
        except:
            pass

        result = [element for element in json_object["Children"] if element["Name"] == element_name]
        if result:
            return result
        elif len(json_object["Children"]) > 0:
            for json_part in json_object["Children"]:
                next_step = self.getjsonstack(json_object=json_part, element_name = element_name, stack = stack)
                if next_step:
                    if {"SelectorType": next_step[0]["SelectorType"], "Selector": next_step[0]["Selector"]} not in stack:
                        stack.append({"SelectorType": next_step[0]["SelectorType"], "Selector": next_step[0]["Selector"]})
                    return next_step
                else:
                    stack.pop()


class Driver(object):
    def __init__(self):
        try:
            self.drv = webdriver.Chrome()
        except:
            pass

    def launch_browser(self):
        self.drv.maximize_window()
        return self.drv


class WebTools(object):
    def __init__(self, driver):
        self.drv = driver

    def find_elements(self, locator, l_type='css', root=None):
        root = self.verify_root(root)
        l_type = l_type.lower()
        if l_type == "css":
            return root.find_elements(By.CSS_SELECTOR, locator)
        elif l_type == "id":
            return root.find_elements(By.ID, locator)
        #elif list of the other locator types: Name, XPath, Class, Text
        else:
            print("No such locator type " + l_type)
        return False

    def find_element(self, locator, l_type='css', root=None):
        search_result = self.find_elements(locator, l_type=l_type, root=root)
        if len(search_result) == 0:
            raise NoSuchElementException(msg=("Locator " + locator + " not found"))
        return search_result[0]

    def verify_root(self, root):
        if root is None:
            return self.drv
        else:
            return root

    def get_element(self, element_name, data=None, stack=None):
        jsontools = JsonTools()
        if stack:
            element_stack = stack
        elif data:
            element_stack = []
            jsontools.getjsonstack(data, element_name, element_stack)
        else:
            print("Either data or stack should be provided to get_element")
        element = self.drv
        for layer in element_stack:
            element = self.find_element(layer["Selector"], layer["SelectorType"], element)
        return element

    def close_browser(self):
        self.drv.quit()

class Actions(object):
    def __init__(self):
        self.driver = Driver()
        self.drv = self.driver.launch_browser()
        self.drv.get("http://translate.google.com")
        self.jsontools = JsonTools()
        self.webtools = WebTools(self.drv)

    def select_source_language(self, language_code, pom):
        source_language_button = self.webtools.get_element(element_name="SourceLanguageList", data=pom)
        source_language_button.click()
        element_stack = []
        self.jsontools.getjsonstack(pom, "SelectSourceLanguage", element_stack)
        element_stack[-1]["Selector"] += language_code + "]"
        expected_language = self.webtools.get_element(element_name="SelectSourceLanguage", stack=element_stack)
        language_name = expected_language.text
        expected_language.click()
        return language_name.upper()

    def select_target_language(self, language_code, pom):
        source_language_button = self.webtools.get_element(element_name="TargetLanguageList", data=pom)
        source_language_button.click()
        element_stack = []
        self.jsontools.getjsonstack(pom, "SelectTargetLanguage", element_stack)
        element_stack[-1]["Selector"] += language_code + "]"
        expected_language = self.webtools.get_element(element_name="SelectTargetLanguage", stack=element_stack)
        language_name = expected_language.text
        expected_language.click()
        return language_name.upper()

    def input_source_text(self, text, pom):
        input_field = self.webtools.get_element(element_name="SourceTextArea", data=pom)
        actions = ActionChains(self.drv)
        actions.move_to_element(input_field).send_keys(text).perform()
        self.drv.switch_to.default_content()

    def get_target_text(self, pom):
        target_text_area = self.webtools.get_element(element_name="TranslationResult", data=pom)
        return target_text_area.text.upper()

    def clear_input(self, pom):
        clear_button = self.webtools.get_element(element_name="ClearButton", data=pom)
        clear_button.click()

    def swap_language(self, pom):
        language_swapper = self.webtools.get_element(element_name="SwapLanguageButton", data=pom)
        language_swapper.click()

    def set_autodetect_language(self, pom):
        detect_language_button = self.webtools.get_element(element_name="AutoDetectButton", data=pom)
        detect_language_button.click()

    def get_current_input_language(self, pom):
        active_button = self.webtools.get_element(element_name="ActiveSourceButton", data=pom)
        return active_button.text.upper()

    def get_current_target_language(self, pom):
        active_button = self.webtools.get_element(element_name="ActiveTargetButton", data=pom)
        return active_button.text.upper()

    def set_text_translation(self, pom):
        text_button = self.webtools.get_element(element_name="TextButton", data=pom)
        text_button.click()

    def set_doc_translation(self, pom):
        doc_button = self.webtools.get_element(element_name="DocButton", data=pom)
        doc_button.click()

    def upload_text_file(self, file_location, pom):
        self.set_doc_translation(pom)
        browse_button = self.webtools.get_element(element_name="FileInputButton", data=pom)
        browse_button.send_keys(file_location)

    def translate_text_file(self, pom):
        translate_button = self.webtools.get_element(element_name="FileTranslateButton", data=pom)
        translate_button.click()
        result = self.webtools.find_element("pre")
        return result.text.upper()

    def check_empty_translation(self, pom):
        input_field = self.webtools.get_element(element_name="SourceTextArea", data=pom)
        return input_field.text

    def quit_browser(self):
        self.webtools.close_browser()