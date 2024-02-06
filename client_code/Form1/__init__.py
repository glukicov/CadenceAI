from ._anvil_designer import Form1Template
from anvil import *
import anvil.server


class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def button_1_click(self, **event_args):
        user_input = self.text_area_1.text
        description = anvil.server.call('generate_response', user_input)
        self.rich_text_2.content = description

    def text_box_1_pressed_enter(self, **event_args):
        pass
