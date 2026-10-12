from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.config import Config
import math

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')

class MainApp(MDApp):
    def build(self):
        # Lots of learning! KivyMD 2.0 styling standards
        self.theme_cls.theme_style = "Dark" 
        self.theme_cls.primary_palette = "AliceBlue" 
        
        self.error_state = False
        
        # Main container
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)
        
        # Swapped to MDLabel
        self.solution = MDLabel(
            text="",
            halign="right",
            font_style="Display", #New MD3 typography
            role="medium",
            size_hint_y=0.3
        )
        main_layout.add_widget(self.solution)
        
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "+", "**"],
            ["C", "del", "(", ")"],
            ["sqrt(", "="]
        ]
        
        for row in buttons:
            h_layout = MDBoxLayout(spacing=10, size_hint_y=0.15)
            for label in row:
                btn = MDButton(
                    MDButtonText(text=label),
                    style="elevated",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint_x=1
                )
                 
                btn.action_value = label 
                
                if label == "=":
                    btn.bind(on_release=self.on_solution)
                else:
                    btn.bind(on_release=self.on_button_press)
                    
                h_layout.add_widget(btn)
            main_layout.add_widget(h_layout)

        return main_layout

    def on_button_press(self, instance):
        # Retrieve our safely stored string
        button_text = instance.action_value 
        
        if self.error_state:
            self.solution.text = ""
            self.error_state = False
            
        current = self.solution.text

        if button_text == "C":
            self.solution.text = ""
        elif button_text == "del":
            self.solution.text = current[:-1]
        else:
            self.solution.text = current + button_text

    def on_solution(self, instance):
        text = self.solution.text
        if not text:
            return
            
        try:
            # Figured out eval() security leak :|
            safe_dict = {"sqrt": math.sqrt, "__builtins__": None}
            solution = str(eval(text, {"__builtins__": None}, safe_dict))
            
            if solution.endswith(".0"):
                solution = solution[:-2]
                
            self.solution.text = solution
            self.error_state = False
            
        except Exception:
            self.solution.text = "Error"
            self.error_state = True

if __name__ == "__main__":
    app = MainApp()
    app.run()
