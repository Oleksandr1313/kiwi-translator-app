from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import requests
from bs4 import BeautifulSoup as bs
from googletrans import Translator

def parse_quotes():
    url = requests.get("http://quotes.toscrape.com/")
    soup = bs(url.content, "html.parser")

    quotes = soup.find_all("span", class_="text")
    quotes = [quote.get_text() for quote in quotes]

    return quotes

class RoundedButton(Button):
    pass

class ModernTextInput(TextInput):
    pass

class ModernApp(App):
    def build(self):
        self.quotes = parse_quotes()
        self.current_quote_index = 0

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Set white background for the entire window
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # White background color
            self.rect = Rectangle(size=(1000, 1000), pos=layout.pos)

        self.title = "Translator"  # Set the window title
        self.caption = "Kivy Translator App"  # Set the window caption

        app_name_label = Label(text='Translator', size_hint=(1, None), height=40)
        app_name_label.color = (0.2, 0.4, 0.6, 1)  # Blue accent color
        app_name_label.font_size = '28sp'
        layout.add_widget(app_name_label)

        self.text_input = ModernTextInput(text=self.quotes[self.current_quote_index], size_hint=(1, 0.5))
        layout.add_widget(self.text_input)

        self.translation_input = ModernTextInput(hint_text='Enter a word for translation', size_hint=(1, 0.1))
        layout.add_widget(self.translation_input)

        self.translation_output = ModernTextInput(readonly=True, size_hint=(1, 0.1))
        layout.add_widget(self.translation_output)

        arrows_layout = BoxLayout(size_hint=(1, 0.1))
        left_arrow = RoundedButton(text='<', size_hint=(0.5, 1))
        left_arrow.bind(on_press=self.show_previous_quote)
        right_arrow = RoundedButton(text='>', size_hint=(0.5, 1))
        right_arrow.bind(on_press=self.show_next_quote)
        arrows_layout.add_widget(left_arrow)
        arrows_layout.add_widget(right_arrow)
        layout.add_widget(arrows_layout)

        translate_button = RoundedButton(text='Translate', size_hint=(1, 0.1))
        translate_button.bind(on_press=self.translate_word)
        layout.add_widget(translate_button)

        return layout

    def show_previous_quote(self, instance):
        self.current_quote_index -= 1
        if self.current_quote_index < 0:
            self.current_quote_index = len(self.quotes) - 1
        self.update_quote()

    def show_next_quote(self, instance):
        self.current_quote_index += 1
        if self.current_quote_index >= len(self.quotes):
            self.current_quote_index = 0
        self.update_quote()

    def update_quote(self):
        self.text_input.text = self.quotes[self.current_quote_index]

    def translate_word(self, instance):
        word = self.translation_input.text
        if word:
            translator = Translator()
            translation = translator.translate(word, src='en', dest='es')
            self.translation_output.text = translation.text

if __name__ == '__main__':
    ModernApp().run()
