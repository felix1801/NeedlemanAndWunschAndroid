#!/usr/bin/python3

"""
Main file that will import Kivy and run the app
"""
import kivy
kivy.require('2.0.0')

from kivy.app import App

from AlignSequencesTool import AlignSequencesTool

from kivy.utils import platform


class NwApp(App):
  """
  ROLE: Main class that will run the application
  """

  def on_start(self):
    """
    ROLE: When the app is launch and if permissions hasn't already been accepted, ask storage permissions to the user
    """

    if platform == 'android':
      from android.permissions import request_permissions, Permission
      request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE, 
        Permission.READ_EXTERNAL_STORAGE
      ])


  def build(self):
    '''
    ROLE: Constructor.
    OUTPUT: application, AlignSequencesTool
    '''
    application = AlignSequencesTool()

    return application


# Run the app
if __name__ == "__main__":
  NwApp().run()
