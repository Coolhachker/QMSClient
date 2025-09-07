from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp

# Импортируем ваш класс для работы с БД
from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine

from src.tools_for_registrate_device.start_reg import reg
from src.tools_for_rmq.consumer import Consumer

from threading import Thread


# Устанавливаем белый фон
Window.clearcolor = (1, 1, 1, 1)

class ConfigInput(TextInput):
    def __init__(self, setting_type, db_engine, **kwargs):
        super().__init__(**kwargs)
        self.setting_type = setting_type
        self.db_engine = db_engine
        
        # Настройка внешнего вида
        self.background_color = (0.95, 0.95, 0.95, 1)
        self.foreground_color = (0.2, 0.2, 0.2, 1)
        self.multiline = False
        self.padding = [dp(15), dp(12)]
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = dp(16)
        self.halign = 'left'
        self.write_tab = False
        
        # Загружаем значение из базы данных
        self.load_value()
    
    def load_value(self):
        """Загрузка значения из базы данных"""
        try:
            if self.setting_type == 'web_server':
                value = self.db_engine.get_ip_of_web_server()
            elif self.setting_type == 'rmq_server':
                value = self.db_engine.get_ip_of_rmq_sever()
            elif self.setting_type == 'device_name':
                value = self.db_engine.get_device_name()
            
            self.text = str(value) if value else ''
        except Exception as e:
            print(f"Ошибка загрузки значения: {e}")
            self.text = ''
    
    def on_text_validate(self):
        """Вызывается при нажатии Enter"""
        self.save_value()
    
    def on_focus(self, instance, value):
        """Вызывается при потере фокуса"""
        if not value:  # Если потеряли фокус
            self.save_value()
    
    def save_value(self):
        """Сохранение значения в базу данных"""
        if self.text.strip():
            try:
                if self.setting_type == 'web_server':
                    self.db_engine.update_ip_of_web_server(self.text.strip())
                elif self.setting_type == 'rmq_server':
                    self.db_engine.update_ip_of_rmq_server(self.text.strip())
                elif self.setting_type == 'device_name':
                    self.db_engine.update_device_name(self.text.strip())
                
                print(f"Значение {self.setting_type} сохранено: {self.text.strip()}")
            except Exception as e:
                print(f"Ошибка сохранения значения: {e}")

class MainAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(30), dp(20)]
        self.spacing = dp(20)
        
        # Инициализируем движок базы данных
        self.db_engine = sqlite_engine
        
        self.setup_ui()
    
    def setup_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        main_container = BoxLayout(
            orientation='vertical',
            spacing=dp(25),
            size_hint=(1, 1),
            padding=[dp(0), dp(10)]
        )
        
        # Заголовок
        title = Label(
            text='Настройки устройства',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(45),
            font_size='24sp',
            bold=True
        )
        main_container.add_widget(title)
        
        # Контейнер для полей ввода
        input_container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(400)
        )
        
        # IP адрес web сервера
        web_ip_container = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(80))
        web_ip_label = Label(
            text='Web Server IP:',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            font_size='16sp',
            halign='left'
        )
        web_ip_container.add_widget(web_ip_label)
        
        self.web_ip_input = ConfigInput(
            'web_server', 
            self.db_engine,
            hint_text='Введите IP web сервера',
            size_hint_x=1
        )
        web_ip_container.add_widget(self.web_ip_input)
        input_container.add_widget(web_ip_container)
        
        # IP адрес RMQ сервера
        rmq_ip_container = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(80))
        rmq_ip_label = Label(
            text='RMQ Server IP:',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            font_size='16sp',
            halign='left'
        )
        rmq_ip_container.add_widget(rmq_ip_label)
        
        self.rmq_ip_input = ConfigInput(
            'rmq_server', 
            self.db_engine,
            hint_text='Введите IP RMQ сервера',
            size_hint_x=1
        )
        rmq_ip_container.add_widget(self.rmq_ip_input)
        input_container.add_widget(rmq_ip_container)
        
        # Название устройства
        device_container = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(80))
        device_label = Label(
            text='Название устройства:',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            font_size='16sp',
            halign='left'
        )
        device_container.add_widget(device_label)
        
        self.device_input = ConfigInput(
            'device_name', 
            self.db_engine,
            hint_text='Введите название устройства',
            size_hint_x=1
        )
        device_container.add_widget(self.device_input)
        input_container.add_widget(device_container)
        
        main_container.add_widget(input_container)
        
        # Кнопка регистрации
        button_container = BoxLayout(size_hint_y=None, height=dp(70))
        self.register_button = Button(
            text='Зарегистрировать устройство',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(55),
            font_size=dp(18),
            bold=True
        )
        self.register_button.bind(on_press=self.on_register)
        button_container.add_widget(self.register_button)
        
        main_container.add_widget(button_container)
        
        self.add_widget(main_container)
    
    def on_register(self, instance):
        """Обработчик нажатия кнопки регистрации"""
        # Сохраняем все значения перед регистрацией
        self.web_ip_input.save_value()
        self.rmq_ip_input.save_value()
        self.device_input.save_value()
        
        # Вызываем основную функцию
        self.main()
    
    def main(self):
        """Основная функция регистрации/подключения"""
        try:
            # Получаем текущие значения из базы данных
            web_ip = self.db_engine.get_ip_of_web_server()
            rmq_ip = self.db_engine.get_ip_of_rmq_sever()
            device_name = self.db_engine.get_device_name()
            
            print(f"Регистрация устройства:")
            print(f"Web Server IP: {web_ip}")
            print(f"RMQ Server IP: {rmq_ip}")
            print(f"Device Name: {device_name}")
            
            # Здесь должна быть ваша логика регистрации/подключения
            reg()
            self.show_registration_status("Устройство успешно зарегистрировано!")
            consumer = Consumer(sqlite_engine.get_ip_of_rmq_sever())
            thread = Thread(target=consumer.channel.start_consuming, daemon=True)
            thread.start()
            
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            self.show_registration_status("Ошибка регистрации!")
    
    def show_registration_status(self, message):
        """Показать статус регистрации"""
        self.register_button.text = message
    
    def reset_button_text(self, dt):
        """Восстановление исходного текста кнопки"""
        self.register_button.text = 'Зарегистрировать устройство'

class ConfigApp(App):
    def build(self):
        return MainAppLayout()