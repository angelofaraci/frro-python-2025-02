import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.stencilview import StencilView
from kivy.core.window import Window

class StencilTestWidget(StencilView):

    def on_mouse_pos(self, *args):
        if args:
            self.size = (100,100)
            self.pos = args[1]
            self.pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
    def init(self):
        self.size = (100,100)
        Window.bind(mouse_pos=self.on_mouse_pos)

class CalculatorGrid(GridLayout):
    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except Exception:
                self.display.text = "Error"

class Calculator(App):
    def build(self):
        wid = StencilTestWidget(size_hint=(None, None), size=Window.size)
        wid.init()
        wid.add_widget(CalculatorGrid(size_hint=(None, None), size=Window.size))
        return wid

calc = Calculator()
calc.run()