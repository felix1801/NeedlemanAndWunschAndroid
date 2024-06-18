from kivy.uix.popup import Popup
from kivy.properties import StringProperty

class Notification(Popup):
  """
  ROLE: Popup containing the message of the notification
  """

  notificationText = StringProperty()
