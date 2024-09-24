import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Liferea', '3.0')
from gi.repository import GObject, Gtk, Liferea

class MyPlugin(GObject.Object, Liferea.ShellActivatable):
    __gtype_name__ = 'MyPlugin'

    object = GObject.property(type=GObject.Object)
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        # Obter a toolbar
        maintoolbar = self.shell.lookup("maintoolbar")
        
        self.itemlist = self.shell.lookup("itemlist")
        print(self.itemlist)

        # Criar o botão e o associar a um Gtk.ToolItem
        button = Gtk.Button(label="Meu Botão")
        tool_item = Gtk.ToolItem()
        tool_item.add(button)
        
        # Adicionar o botão ao toolbar
        maintoolbar.insert(tool_item, -1)
        maintoolbar.show_all()

        # Conectar o evento de clique ao botão
        button.connect("clicked", self.on_button_click)

    def on_button_click(self, button):
        # Criar o menu
        menu = Gtk.Menu()

        # Opções do menu
        first_item = Gtk.MenuItem(label="Primeiro Botão")
        second_item = Gtk.MenuItem(label="Segundo Botão")
        third_item = Gtk.MenuItem(label="Terceiro Botão")

        # Adicionar itens ao menu
        menu.append(first_item)
        menu.append(second_item)
        menu.append(third_item)

        # Conectar ações dos botões
        first_item.connect("activate", self.on_first_button)
        second_item.connect("activate", self.on_second_button)
        third_item.connect("activate", self.on_third_button)

        # Mostrar menu
        menu.show_all()
        menu.popup_at_pointer(None)

    def on_first_button(self, menu_item):
        print("Primeiro Botão")
        print(self.itemlist)

    def on_second_button(self, menu_item):
        print("Segundo Botão")

    def on_third_button(self, menu_item):
        print("Terceiro Botão")

    def do_deactivate(self):
        # Limpar ações ao desativar o plugin
        pass

