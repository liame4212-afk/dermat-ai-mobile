from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
import io
from kivy.core.image import Image as CoreImage

KV = '''
MDScreen:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        MDLabel:
            text: 'DermatAI'
            halign: 'center'
            font_style: 'H4'
        MDRaisedButton:
            text: 'Pick Photo'
            pos_hint: {'center_x': .5}
            on_release: app.pick_photo()
        Image:
            id: img
            size_hint_y: .4
        MDLabel:
            id: result
            text: ''
            halign: 'center'
            font_style: 'Body1'
'''

class DermatAIApp(MDApp):
    def build(self):
        self.title = 'DermatAI'
        return Builder.load_string(KV)

    def pick_photo(self):
        from plyer import filechooser
        filechooser.open_file(on_selection=self.upload)

    def upload(self, selection):
        if not selection:
            return
        img_path = selection[0]
        self.root.ids.img.source = img_path
        self.root.ids.result.text = 'Analyzing…'
        with open(img_path, 'rb') as f:
            body = f.read()
        from urllib.parse import urlencode
        UrlRequest(
            url='http://192.168.1.113:8000/predict',
            req_body=body,
            req_headers={'Content-Type': 'image/jpeg'},
            method='POST',
            on_success=self.show_result,
            on_failure=self.show_error
        )

    def show_result(self, req, result):
        self.root.ids.result.text = f'{result["diagnosis"]} ({result["confidence"]:.2%})'

    def show_error(self, req, result):
        self.root.ids.result.text = 'Error contacting server'

DermatAIApp().run()
