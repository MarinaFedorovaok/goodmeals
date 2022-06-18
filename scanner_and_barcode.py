import kivy
kivy.require('2.1.0')

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.uix.label import Label
#импортируем камеру, делаем снимок

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')

class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("barcode1.png".format(timestr))
        print("Captured")
class TestCamera(App):

    def build(self):
        return CameraClick()

TestCamera().run()
# второй этап: распознаем штрихкод
from pyzbar.pyzbar import decode
from PIL import Image
print(decode(Image.open('barcode1.png')))
res = decode(Image.open('barcode1.png'))
barcode_str= res[0].data.decode('utf-8') #извлекаем штрихкод
barcode_str= str(barcode_str)
print(barcode_str)
print(type(barcode_str))
#print(type(barcode_str))
import requests #посылаем запрос на сервер
headers = {
    'accept': 'application/json',
}
response = requests.get('http://hotel-murino.ru:49363/api/product/'+ barcode_str, headers=headers)
print(response.text)
response_parsed = response.json()
print(response_parsed)
# третий этап : выводим сообщение (в перспективе состав, сейчас - штрихкод)

class MyApp(App):

    def build(self):
        return Label(text=barcode_str)
#camera.take_picture('buttom.png', print)#доступ к камере

if __name__ == '__main__':
    MyApp().run()