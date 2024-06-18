from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty, StringProperty

class RecycleInputPopup(Popup):
  """
  ROLE: Create the class which will display the content of the file input
  """
  def __init__(self, data_items, **kwargs):
    """
    ROLE: Constructor
    """

    self.data_items = data_items
    super(RecycleInputPopup, self).__init__(**kwargs)

