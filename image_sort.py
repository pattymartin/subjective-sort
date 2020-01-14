import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from trees import SaveStateTree

Builder.load_string("""
<SelectionLayout>:
    button_left: button_left
    button_right: button_right
    orientation: 'horizontal'
    ImageButton:
        id: button_left
        on_release: root.select_left()
    ImageButton:
        id: button_right
        on_release: root.select_right()

<ImageButton@ButtonBehavior+Image>:
""")


class CompareImage(str):
    """
    A string representing the name of an image file. Overrides
    comparison operators (<, <=, >, >=) to prompt the user to select an
    image in order to decide which image is "greater."
    """

    response = None  # update to 1, 0, or -1 when selection made
    UNDO = object()  # change response to this to undo
    EXIT = object()  # change response to this to exit
    event = threading.Event()  # so the thread can wait for response

    def compare(self, other):
        """
        Prompt the user to select which image is "greater."

        When a selection is made, `CompareImage.response` should be set
        to 1 if this image is "greater" than the other, -1 if this image
        is "less than" the other, or 0 if the items are equal.

        Wait for a selection to be made, then return
        `CompareImage.response`.

        :param other: The item to compare to
        :type other: CompareImage
        :return: 1 to indicate "greater than" other, -1 to indicate
                 "less than" other, or 0 to indicate equality
        :rtype: int
        """

        # get the layout from the running Kivy app
        layout = App.get_running_app().root
        # set left and right image
        layout.left_image = str(self)
        layout.right_image = str(other)
        CompareImage.response = None
        while CompareImage.response is None:
            # wait for response
            CompareImage.event.clear()
            CompareImage.event.wait()
            if CompareImage.response == CompareImage.UNDO:
                raise SaveStateTree.UndoClicked
            if CompareImage.response == CompareImage.EXIT:
                raise SaveStateTree.Exit
            if CompareImage.response is not None:
                return CompareImage.response

    def __lt__(self, other):
        return self.compare(other) == -1

    def __le__(self, other):
        return self.compare(other) in [-1, 0]

    def __gt__(self, other):
        return self.compare(other) == 1

    def __ge__(self, other):
        return self.compare(other) in [1, 0]


class SelectionLayout(BoxLayout):
    """
    Kivy layout which presents two images so the user can choose one.
    """

    left_image = StringProperty('')  # left image source
    right_image = StringProperty('')  # right image source

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None
        self.get_keyboard()  # for keyboard shortcuts
        # resume thread waiting for layout to be created
        CompareImage.event.set()

    def on_left_image(self, _instance, _value):
        """
        Update the left image in the layout when the attribute
        `left_image` is changed.

        :param _instance: The SelectionLayout instance
        :type _instance: SelectionLayout
        :param _value: The new value of `left_image`
        :type _value: str
        :return: None
        """

        # Use Clock to schedule setting the left button's source image
        # to self.left_image. this ensures that the UI is updated from
        # the main thread.
        def update(_dt):
            self.button_left.source = self.left_image
        Clock.schedule_once(update)

    def on_right_image(self, _instance, _value):
        """
        Update the right image in the layout when the attribute
        `right_image` is changed.

        :param _instance: The SelectionLayout instance
        :type _instance: SelectionLayout
        :param _value: The new value of `right_image`
        :type _value: str
        :return: None
        """

        # Use Clock to schedule setting the right button's source image
        # to self.right_image. This ensures that the UI is updated from
        # the main thread.
        def update(_dt):
            self.button_right.source = self.right_image
        Clock.schedule_once(update)

    @staticmethod
    def select_left():
        """
        Set `CompareImage.response` to 1 to indicate that the left image
        is "greater than" the right image.

        :return: None
        """

        CompareImage.response = 1
        CompareImage.event.set()  # resume the waiting thread

    @staticmethod
    def select_right():
        """
        Set `CompareImage.response` to -1 to indicate that the left
        image is "less than" the right image.

        :return: None
        """

        CompareImage.response = -1
        CompareImage.event.set()  # resume the waiting thread

    @staticmethod
    def undo():
        """
        Undo the last comparison.

        :return: None
        """

        CompareImage.response = CompareImage.UNDO
        CompareImage.event.set()  # resume the waiting thread

    def get_keyboard(self):
        """
        Get keyboard focus.

        :return: None
        """

        # get the keyboard instance
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)
        # bind to run _on_keyboard_down when a key is pressed
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, _keyboard, keycode, _text, modifiers):
        """
        Receive keypresses. Pressing '1' on will select the left image,
        pressing '2' will select the right image, and pressing 'Ctrl+Z'
        will undo.

        :param _keyboard: A Keyboard instance
        :type _keyboard: kivy.core.window.Keyboard
        :param keycode: An integer and a string representing the keycode
        :type keycode: tuple
        :param _text: The text of the pressed key
        :type _text: str
        :param modifiers: A list of modifier keys pressed
        :type modifiers: list
        :return: True to consume the key, otherwise False
        :rtype: bool
        """

        if keycode[1] in ['1', 'numpad1']:
            self.select_left()
            return True
        elif keycode[1] in ['2', 'numpad2']:
            self.select_right()
            return True
        elif keycode[1] == 'z' and 'ctrl' in modifiers:
            self.undo()
            return True
        return False

    def _keyboard_closed(self):
        """
        Remove keyboard binding when the keyboard is closed.

        :return: None
        """

        # unbind _on_keyboard_down
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


class SortApp(App):
    """A Kivy App with a SelectionLayout as its root layout."""
    def build(self):
        """
        Build the root layout of the app.

        :return: The root layout
        :rtype: SelectionLayout
        """

        return SelectionLayout()

    def on_stop(self):
        """
        When the app is closed, save the tree to file.

        :return:
        """

        CompareImage.response = CompareImage.EXIT
        CompareImage.event.set()


def image_sort(image_list, filename='tree.pickle'):
    """
    Sort a list of images based on user input. The images will be
    presented in a Kivy app two at a time, so that the user can select
    which image is "greater than" the other.

    If the app is closed before sorting is finished, the tree used to
    sort the images will be written to the file `filename` to be
    resumed at a later time, and this function will return an empty
    list.

    :param image_list: List of image filenames
    :type image_list: list
    :param filename: Name of the file to store the tree, defaults to
                     'tree.pickle'
    :type filename: str
    :return: The sorted list
    :rtype: list
    """

    if not image_list:
        return image_list

    def _sort():
        """
        Insert each string from image_list into a :class:`SaveStateTree`
        and then get the sorted list from the tree, placing the result
        in `sorted_list`.

        :return: None
        """

        # wait for the SelectionLayout to be initialized
        CompareImage.event.clear()
        CompareImage.event.wait()

        try:
            tree = SaveStateTree(filename)
            for image in image_list:
                # check if image already in tree, in case the sorting is
                # being resumed
                if image not in tree.values:
                    tree.insert(CompareImage(image))
        except SaveStateTree.Exit:
            return

        tree.delete_file()  # delete the file that stored the tree
        sorted_list.extend(tree.to_list())
        sort_event.set()  # resume the waiting thread
        app.stop()  # close the window

    sorted_list = []
    # threading event to wait for sorting to finish before returning
    sort_event = threading.Event()
    # start sorting in a new thread
    thread = threading.Thread(target=_sort)
    thread.start()

    app = SortApp()
    # make sure the thread doesn't keep waiting if the app closes
    app.bind(on_stop=lambda instance: sort_event.set())
    app.run()
    sort_event.wait()  # wait for sorting to finish
    return sorted_list
