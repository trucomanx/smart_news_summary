import os
import json
from gi.repository import GObject, Liferea, Gtk

class MeuPlugin(GObject.Object, Liferea.ShellActivatable):
    __gtype_name__ = 'MeuPlugin'

    object = GObject.property(type=GObject.Object)
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        # Localizando o maintoolbar
        maintoolbar = self.shell.lookup("maintoolbar")

        # Criando um novo botão na toolbar
        self.button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        self.button.set_label("Menu Dinâmico")
        self.button.connect("clicked", self.on_button_clicked)
        
        # Adicionando o botão à toolbar
        maintoolbar.insert(self.button, -1)
        maintoolbar.show_all()

    def do_deactivate(self):
        # Remover o botão ao desativar o plugin
        maintoolbar = self.shell.lookup("maintoolbar")
        maintoolbar.remove(self.button)

    def on_button_clicked(self, widget):
        # Pasta onde os arquivos JSON estão localizados
        plugin_path = os.path.expanduser("~/.config/liferea/plugins/meu_plugin")
        json_files = [f for f in os.listdir(plugin_path) if f.endswith('.json')]

        # Criar um menu pop-up
        menu = Gtk.Menu()

        for json_file in json_files:
            file_path = os.path.join(plugin_path, json_file)
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Criar um item de menu com o nome e conteúdo do arquivo JSON
            menu_item = Gtk.MenuItem(label=data["name"])
            menu_item.connect("activate", self.on_menu_item_activate, data["content"])
            menu.append(menu_item)

        # Mostrar o menu
        menu.show_all()
        menu.popup(None, None, None, widget, 0, Gtk.get_current_event_time())

    def on_menu_item_activate(self, widget, content):
        # Quando um item do menu é clicado, exibe o conteúdo do arquivo JSON
        print(content)

