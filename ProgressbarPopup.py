from kivy.uix.popup import Popup
from kivy.properties import NumericProperty

class ProgressbarPopup(Popup):
  """
  ROLE: Display the progressbar for any process
  """

  progressbarValue = NumericProperty(0)


  def __init__(self, progressbarMax, **kwargs):
    """
    ROLE: Constructor
    """

    self.progressbarMax = progressbarMax
    super(ProgressbarPopup, self).__init__(**kwargs)
