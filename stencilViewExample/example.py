from kivy.app import App
from kivy.uix.stencilview import StencilView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class StencilViewExample(App):
    def build(self):
        image_width = 400
        image_height = 400
        layout = BoxLayout(orientation='vertical')
        def imageSizer(self):
            image.size = (image.size[0] + self.num, image.size[1] + self.num)
            return imageSizer
        # Create a StencilView
        stencil = StencilView(size_hint=(1, None), size=(400, 400))
        
        # Add an image inside the StencilView
        image = Image(source='example_image.jpg', size_hint=(None, None), size=(image_width, image_height), pos_hint=(0, 0))
        stencil.add_widget(image)
        add_button = Button(text='add size', size_hint=(None, None), size=(100, 50))
        add_button.num = 50
        reduce_button = Button(text='reduce size', size_hint=(None, None), size=(100, 50))
        reduce_button.num = -50
        add_button.bind(on_press=imageSizer) 
        reduce_button.bind(on_press=imageSizer) 
        layout.add_widget(stencil)
        layout.add_widget(add_button)
        layout.add_widget(reduce_button)
        return layout

if __name__ == '__main__':
    StencilViewExample().run()