import os
import json
from gi.repository import GObject, Peas, PeasGtk, Liferea, Gtk
from ollama import Client


def send_smart_quote(configuration,system_msg,ordered_values):
    
    user_msg='';
    for value in ordered_values:
        user_msg = user_msg + value + "\n\n";
    
    res = client_request(   system_msg,
                            user_msg,
                            url_server='http://'+configuration["host"]+':'+str(configuration["port"]), 
                            model=configuration["model"])
    print(res)


def client_request( system_msg,
                    user_msg,
                    url_server='http://10.104.1.120:11434', 
                    model='llama3.1:8b'):
    client = Client(host=url_server)

    response = client.chat(model=model, messages=[
      {
        'role': 'system',
        'content': system_msg,
      },
      {
        'role': 'user',
        'content': user_msg,
      },
    ])
    
    msg = response["message"]['content'];
    
    return msg;

def default_conf_json_file(nome_arquivo):
    """Cria um arquivo JSON com as informações de configuração.
    
    Args:
    nome_arquivo: Nome do arquivo JSON a ser criado.
    """
    
    # Cria um dicionário com os dados do botão
    dados_conf = {
        "host": "localhost",
        "port": "11434",
        "model":"llama3.1:8b"
    }

    # Abre o arquivo no modo escrita e escreve os dados em formato JSON
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados_conf, arquivo, indent=4)
        

def default_json_file(nome_arquivo):
    """Cria um arquivo JSON com as informações do botão.
    
    Args:
    nome_arquivo: Nome do arquivo JSON a ser criado.
    """
    
    # Cria um dicionário com os dados do botão
    dados_botao = {
        "name": "Sumario das últimas 40 noticias",
        "system_msg": '''
Como redator e repórter de notícias experiente, você receberá uma lista de notícias organizadas por parágrafos, 
com as mais recentes no topo. Seu objetivo é fornecer um resumo claro de todas as notícias, 
priorizando as mais recentes ou as que aparecem com mais frequência.

Se você não realizar bem o seu trabalho, poderá ser demitido.
        '''
    }

    # Abre o arquivo no modo escrita e escreve os dados em formato JSON
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados_botao, arquivo, indent=4)


class SmartNewsSummary(GObject.Object, Liferea.ShellActivatable):
    __gtype_name__ = 'SmartNewsSummary'

    object = GObject.property(type=GObject.Object)
    shell = GObject.property(type=Liferea.Shell)

    def do_activate(self):
        # Pasta onde os arquivos JSON estão localizados
        plugin_conf_rel_path="~/.config/liferea/plugins/smart_news_summary"
        plugin_conf_path = os.path.expanduser(plugin_conf_rel_path)
        conf_filepath = os.path.join(plugin_conf_path,"configuration.json");
        if not os.path.exists(conf_filepath):
            os.makedirs(plugin_conf_path,exist_ok=True);
            default_conf_json_file(conf_filepath);
        with open(conf_filepath, 'r') as f:
            self.configuration = json.load(f)
        
    
        # Localizando o maintoolbar
        maintoolbar = self.shell.lookup("maintoolbar")
        
        
        # Model e treeview        
        normalviewitems = self.shell.lookup ("normalViewItems")
        self.treeview = normalviewitems.get_child().get_child()

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
        plugin_rel_path="~/.config/liferea/plugins/smart_news_summary/buttons"
        
        # Pasta onde os arquivos JSON estão localizados
        plugin_path = os.path.expanduser(plugin_rel_path)
        os.makedirs(plugin_path,exist_ok=True);
        
        json_files = [f for f in os.listdir(plugin_path) if f.endswith('.json')]

        if len(json_files)==0:
            new_path = os.path.join(plugin_path,"item1.json");
            default_json_file(new_path);
            json_files.append(new_path);
        
        # Criar um menu pop-up
        menu = Gtk.Menu()

        for json_file in json_files:
            file_path = os.path.join(plugin_path, json_file)
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Criar um item de menu com o nome e conteúdo do arquivo JSON
            menu_item = Gtk.MenuItem(label=data["name"])
            menu_item.connect("activate", self.on_menu_item_activate, data["system_msg"])
            menu.append(menu_item)

        # Mostrar o menu
        menu.show_all()
        menu.popup(None, None, None, widget, 0, Gtk.get_current_event_time())

    def on_menu_item_activate(self, widget, system_msg):
        # Quando um item do menu é clicado, exibe o conteúdo do arquivo JSON

        model = self.treeview.get_model()
        dado=dict()
        for k in range(len(model)):
            # Get path pointing to 6th row in list store
            path = Gtk.TreePath(k)
            treeiter = model.get_iter(path)
            Text = model.get_value(treeiter, 2)
            ID = model.get_value(treeiter, 4)
            #print(ID,Text)
            dado[ID]=Text;
        ordered_values = [dado[key] for key in sorted(dado.keys())]
        
        msg=send_smart_quote(self.configuration,system_msg,ordered_values);
        
        print(msg)

