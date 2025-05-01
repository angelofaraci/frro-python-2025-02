from kivy.app import App
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class MyGallery(StencilView):
    pass

class GalleryApp(App):
    def build(self):
        Window.size = (800, 600)

        root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Outer container (StencilView)
        stencil = MyGallery(size_hint=(1, 1))

        # ScrollView with fixed height
        scroll = ScrollView(size_hint=(1, None), height=220, do_scroll_y=False)

        # Inner layout for images
        inner = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), height=200)
        inner.bind(minimum_width=inner.setter('width'))

        # Add images
        for i in range(5):
            img = Image(
                source=f"../stencil_view_example/example_image{i}.jpg",
                size_hint=(None, None),
                size=(200, 200),
                allow_stretch=True,
                keep_ratio=True
            )
            inner.add_widget(img)

        scroll.add_widget(inner)
        stencil.add_widget(scroll)
        root.add_widget(stencil)

        return root

GalleryApp().run()
