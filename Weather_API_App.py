import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
  def __init__(self):
    super().__init__()
    self.city_label=QLabel("Enter city name: ", self)
    self.city_input= QLineEdit(self)
    self.get_weather_button = QPushButton("Get Weather", self)
    self.temparature_label= QLabel(self)
    self.emoji_label= QLabel(self)
    self.description_label= QLabel(self)
    self.initUI()


  def initUI(self):
    self.setWindowTitle("Weather App")
    self.setGeometry(700, 300, 300, 200)

    vbox= QVBoxLayout()
    vbox.addWidget(self.city_label)
    vbox.addWidget(self.city_input)
    vbox.addWidget(self.get_weather_button)
    vbox.addWidget(self.temparature_label)
    vbox.addWidget(self.emoji_label)
    vbox.addWidget(self.description_label)

    self.setLayout(vbox)

    self.city_label.setAlignment(Qt.AlignCenter)
    self.city_input.setAlignment(Qt.AlignCenter)
    self.temparature_label.setAlignment(Qt.AlignCenter)
    self.emoji_label.setAlignment(Qt.AlignCenter)
    self.description_label.setAlignment(Qt.AlignCenter)

    self.city_label.setObjectName("city_label")
    self.city_input.setObjectName("city_input")
    self.get_weather_button.setObjectName("get_weather_button")
    self.temparature_label.setObjectName("temparature_label")
    self.emoji_label.setObjectName("emoji_label")
    self.description_label.setObjectName("description_label")

    self.setStyleSheet("""
            QLabel, QPushButton{
                       font_family: calibri;
                       }
            QLabel#city_label{
                       font-size: 40px;
                       font-style: italic;
                       }
            QLineEdit#city_input{
                       font-size: 40px;
                       }
            QPushButton#get_weather_button{
                       font-size: 30px;
                       font-weight: bold; 
                       }
            QLabel#temparature_label{
                      font-size: 50px;
                        }           
            QLabel#emoji_label{
                       font-size: 100px;
                       font-family: segoe UI emoji
                       } 
            QLabel#description_label{
                       font-size: 50px
                       }               
                       """)
    
    self.get_weather_button.clicked.connect(self.get_weather)
    self.city_input.returnPressed.connect(self.get_weather)
    
  def get_weather(self):
    
    api_key= "6ece4ac4d5d4a65e0a4e1f654b7b8971"
    city= self.city_input.text()
    url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
      response= requests.get(url)
      response.raise_for_status()
      data= response.json()

      if data["cod"] == 200:
        self.display_weather(data)  
    except requests.exceptions.HTTPError as Httperror:
      match response.status_code:
        case 400:
          self.display_error("Bad request:\nPlease check your input")
        case 401:
          self.display_error("Unathorized:\nInvalid API key")
        case 403:
          self.display_error("Forbidden:\nAccess Denied")
        case 404:
          self.display_error("Not Found:\nCity Not Found")
        case 500:
          self.display_error("Interal Server Error:\nPlease try again later")
        case 502:
          self.display_error("Bad Gateway:\nInvalid response from the server")
        case 503:
          self.display_error("Service Unavailable:\nServer is down")
        case 504:
          self.display_error("Gateway Timeout:\nNo response from the server")
        case _:
          self.display_error(f"HTTP error occured:\n{Httperror}")

    except requests.exceptions.ConnectionError:
      self.display_error("Connection Error:\nCheck your internet connection")  
 
    except requests.exceptions.Timeout:
      self.display_error("Timeout Error:\nThe request timed out")  

    except requests.exceptions.TooManyRedirects:
      self.display_error("Too many requests:\nCheck the URL")  

    except requests.exceptions.RequestException as req_error:
      self.display_error(f"Request Error:\n{req_error}")  


  def display_error(self, message):
    self.temparature_label.setStyleSheet("font-size: 30px;")
    self.temparature_label.setText(message)
    self.emoji_label.clear()
    self.description_label.clear()

  def display_weather(self,data):
    self.temparature_label.setStyleSheet("font-size: 50px;")
    temperature_k= data["main"]["temp"]
    temperature_c= temperature_k - 273.15
    temperature_f= (temperature_k * 9/5) - 495.67
    weather_id= data["weather"][0]["id"]
    weather_description= data["weather"][0]["description"]

    self.temparature_label.setText(f"{temperature_c:.0f}°C")
    self.emoji_label.setText(self.get_weather_emoji(weather_id))
    self.description_label.setText(weather_description)
  
  @staticmethod
  def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"  # Thunderstorm
    elif 300 <= weather_id <= 321:
        return "🌦️"  # Drizzle
    elif 500 <= weather_id <= 531:
        return "🌧️"  # Rain
    elif 600 <= weather_id <= 622:
        return "❄️"  # Snow
    elif weather_id == 701:
        return "🌫️"  # Mist
    elif weather_id == 711:
        return "💨"  # Smoke
    elif weather_id == 721:
        return "🌁"  # Haze
    elif weather_id == 731 or weather_id == 761:
        return "🌪️"  # Dust / Sand / Whirl
    elif weather_id == 741:
        return "🌫️"  # Fog
    elif weather_id == 751:
        return "🌬️"  # Sand
    elif weather_id == 762:
        return "🌋"  # Volcanic Ash
    elif weather_id == 771:
        return "🌬️"  # Squalls
    elif weather_id == 781:
        return "🌪️"  # Tornado
    elif weather_id == 800:
        return "☀️"  # Clear sky
    elif 801 <= weather_id <= 804:
        return "☁️"  # Clouds
    else:
        return "🌍"  # Default / Unknown


if __name__== "__main__":
  app= QApplication(sys.argv)
  weather_app = WeatherApp()
  weather_app.show()
  sys.exit(app.exec())