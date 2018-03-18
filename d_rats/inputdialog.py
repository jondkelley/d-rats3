#!/usr/bin/python
#
# Copyright 2008 Dan Smith <dsmith@danplanet.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk

from miscwidgets import make_choice

class TextInputDialog(gtk.Dialog):
    def respond_ok(self, *args):
        self.response(gtk.RESPONSE_OK)

    def __init__(self, **args):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                   gtk.STOCK_OK, gtk.RESPONSE_OK)
        gtk.Dialog.__init__(self, buttons=buttons, **args)

        self.label = gtk.Label()
        self.label.set_size_request(300, 100)
        # pylint: disable-msg=E1101
        self.vbox.pack_start(self.label, 1, 1, 0)
       
        self.text = gtk.Entry()
        self.text.connect("activate", self.respond_ok, None)
        # pylint: disable-msg=E1101
        self.vbox.pack_start(self.text, 1, 1, 0)

        self.label.show()
        self.text.show()

class ChoiceDialog(gtk.Dialog):
    editable = False

    def __init__(self, choices, **args):
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                   gtk.STOCK_OK, gtk.RESPONSE_OK)
        gtk.Dialog.__init__(self, buttons=buttons, **args)

        self.label = gtk.Label()
        self.label.set_size_request(300, 100)
        # pylint: disable-msg=E1101
        self.vbox.pack_start(self.label, 1, 1, 0)
        self.label.show()

        try:
            default = choices[0]
        except IndexError:
            default = None

        self.choice = make_choice(sorted(choices), self.editable, default)
        # pylint: disable-msg=E1101
        self.vbox.pack_start(self.choice, 1, 1, 0)
        self.choice.show()

        self.set_default_response(gtk.RESPONSE_OK)

class EditableChoiceDialog(ChoiceDialog):
    editable = True

    def __init__(self, choices, **args):
        ChoiceDialog.__init__(self, choices, **args)

        self.choice.child.set_activates_default(True)

class ExceptionDialog(gtk.MessageDialog):
    def __init__(self, exception, **args):
        gtk.MessageDialog.__init__(self, buttons=gtk.BUTTONS_OK, **args)
        self.set_property("text", _("An error has occurred"))
        self.format_secondary_text(str(exception))

class FieldDialog(gtk.Dialog):
    def __init__(self, **kwargs):
        if "buttons" not in kwargs.keys():
            kwargs["buttons"] = (gtk.STOCK_OK, gtk.RESPONSE_OK,
                                 gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)

        self.__fields = {}

        gtk.Dialog.__init__(self, **kwargs)
        self.set_default_response(gtk.RESPONSE_OK)

        self.set_modal(True)
        self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)        

    def response(self, _):
        print "Blocking response"
        return

    def add_field(self, label, widget, validator=None, full=False):
        if full:
            box = gtk.VBox(False, 2)
        else:
            box = gtk.HBox(True, 2)

        lab = gtk.Label(label)
        lab.show()

        widget.set_size_request(150, -1)
        widget.show()

        box.pack_start(lab, 0, 0, 0)
        if full:
            box.pack_start(widget, 1, 1, 1)
        else:
            box.pack_start(widget, 0, 0, 0)
        box.show()

        # pylint: disable-msg=E1101
        if full:
            self.vbox.pack_start(box, 1, 1, 1)
        else:
            self.vbox.pack_start(box, 0, 0, 0)
    
        self.__fields[label] = widget

    def get_field(self, label):
        return self.__fields.get(label, None)

if __name__ == "__main__":
    # pylint: disable-msg=C0103
    d = FieldDialog(buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))
    d.add_field("Foo", gtk.Entry())
    d.add_field("Bar", make_choice(["A", "B"]))
    d.run()
    gtk.main()
    d.destroy()
