import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

import os.path
import utils


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Civil UPatras Announcements')
        self.set_border_width(5)
        self.set_default_size(800, 350)

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.layout)

        self.add_menu_bar()
        self.add_tree_view()

        button = Gtk.Button(label='Select')
        button.connect("clicked", self.btn_select)
        self.layout.pack_start(button, True, True, 0)

    def add_tree_view(self):
        # Convert data to ListStore (lists that
        # tree views can display)
        self.list_store = Gtk.ListStore(str, str, str)
        if os.path.isfile('announcements.csv'):
            self.update_tree_view(False)
        else:
            self.update_tree_view(True)

        # TreeView is the item that's displayed
        self.tree_view = Gtk.TreeView(self.list_store)

        for i, col_title in enumerate(["Date", "Title"]):
            # Render means how to draw the data
            renderer = Gtk.CellRendererText()
            # Create columns (text is column number)
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            # Make column sortable
            column.set_sort_column_id(i)
            # Add column to the tree
            self.tree_view.append_column(column)

        # Handle selection
        self.selected_row = self.tree_view.get_selection()
        self.tree_view.connect("row-activated", self.item_selected)

        # Add tree view to layout
        self.layout.pack_start(self.tree_view, True, True, 0)

    def add_menu_bar(self):
        # Main menu container
        main_menu_bar = Gtk.MenuBar()
        # Drop down menu
        file_menu_dropdown = Gtk.MenuItem('File')
        file_menu = Gtk.Menu()
        # File menu items
        file_refresh = Gtk.MenuItem('Refresh')
        file_refresh.connect("activate", self.menu_refresh)
        file_exit = Gtk.MenuItem('Exit')
        file_exit.connect("activate", self.menu_quit)

        file_menu_dropdown.set_submenu(file_menu)
        file_menu.append(file_refresh)
        file_menu.append(Gtk.SeparatorMenuItem())
        file_menu.append(file_exit)

        main_menu_bar.append(file_menu_dropdown)

        self.layout.pack_start(main_menu_bar, True, True, 0)

    @staticmethod
    def menu_quit(self, menuitem):
        Gtk.main_quit()

    def menu_refresh(self, menuitem):
        self.update_tree_view(True)

    def update_tree_view(self, download):
        self.list_store.clear()
        if download:
            utils.get_announcements(count=10)
        list = utils.csv_to_dict('announcements.csv')
        for item in list:
            self.list_store.append((item['date'], item['title'], item['link']))

    def item_selected(self, treeview, treepath, treecolumn):
        model = treeview.get_model()
        row = treepath
        if row is not None:
            date = model[row][0]
            title = model[row][1]
            link = model[row][2]
            details_window = DetailsWindow(date, title, link)
            details_window.connect("destroy", Gtk.Window.destroy)
            details_window.show_all()

    def btn_select(self, widget):
        model, row = self.tree_view.get_selection().get_selected()
        if row is not None:
            date = model[row][0]
            title = model[row][1]
            link = model[row][2]
            details_window = DetailsWindow(date, title, link)
            details_window.connect("destroy", Gtk.Window.destroy)
            details_window.show_all()


class DetailsWindow(Gtk.Window,):
    def __init__(self, date, title, link):
        self.date = date
        self.title = title
        self.link = link
        Gtk.Window.__init__(self, title='{} | {}'.format(date, title))
        self.set_default_size(800, 600)
        self.set_border_width(5)

        self.scrollwindow = Gtk.ScrolledWindow()
        self.scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.add(self.scrollwindow)

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.btn_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        details = utils.get_single_announcement(link)
        text_body = utils.formatted_print(details[0])
        label = Gtk.Label(text_body)

        self.layout.pack_start(label, True, True, 0)
        self.layout.pack_start(self.btn_layout, True, True, 0)

        self.scrollwindow.add(self.layout)

        for item in details[1]:
            link_button = Gtk.LinkButton(details[1][item], item)
            self.btn_layout.pack_start(link_button, False, False, 0)


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
