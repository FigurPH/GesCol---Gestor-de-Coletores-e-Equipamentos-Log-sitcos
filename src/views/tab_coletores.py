import wx

from src.controllers import coletor_controller
from src.controllers import atribuicao_controller


class TabColetores(wx.Panel):
    """
    Classe TabColetores
    --------------
    A classe TabColetores é responsável por gerenciar a interface gráfica da aba de coletores em um aplicativo wxPython. 
    Ela permite a exibição, adição, edição, exclusão e atualização de uma lista de coletores, além de carregar dados de 
    coletores a partir de um controlador.
    --------------
    TabColetores(wx.Panel):
    bm
    Classe responsável por gerenciar a interface gráfica da aba de coletores em um aplicativo wxPython. 
    Permite a exibição, adição, edição, exclusão e atualização de uma lista de coletores, além de carregar 
    dados de coletores a partir de um controlador.
    Atributos:
        coletores_lista (list): Lista de coletores a serem exibidos na interface.
        controller (object): Referência ao controlador responsável por gerenciar os dados dos coletores.
        list_ctrl (wx.ListCtrl): Componente de lista para exibir os coletores.
        btn_adicionar (wx.Button): Botão para adicionar um novo coletor.
        btn_editar (wx.Button): Botão para editar o coletor selecionado.
        btn_excluir (wx.Button): Botão para excluir o coletor selecionado.
        btn_atualizar (wx.Button): Botão para atualizar a lista de coletores.
        btn_upload_csv (wx.Button): Botão para carregar coletores a partir de um arquivo CSV.
    Métodos:
        __init__(parent):
            Inicializa a interface gráfica e configura os elementos da aba de coletores.
        on_atualizar_lista(event):
            Atualiza a lista de coletores exibida na interface.
        carregar_coletores():
            Carrega os coletores do controlador e os exibe na lista.
        atualizar_estado_botoes():
            Atualiza o estado dos botões "Editar" e "Excluir" com base na seleção atual da lista.
        on_adicionar_coletor(event=None):
            Abre um diálogo para adicionar um novo coletor e atualiza a lista após a adição.
        on_editar_coletor(event):
            Abre um diálogo para editar o coletor selecionado e atualiza a lista após a edição.
        on_excluir_coletor(event=None):
            Exclui o coletor selecionado após confirmação do usuário e atualiza a lista.
        upload_csv():
            Método reservado para implementar a funcionalidade de carregar coletores a partir de um arquivo CSV.
    """

    def __init__(self, parent):
        """
        Inicializa a interface gráfica da aba de coletores.
        Args:
            parent: Referência ao elemento pai da interface.
        Atributos:
            coletores_lista (list): Lista de coletores a serem exibidos.
            controller: Referência ao controlador responsável pelos coletores.
            list_ctrl (wx.ListCtrl): Componente de lista para exibição dos coletores.
            btn_adicionar (wx.Button): Botão para adicionar um novo coletor.
            btn_editar (wx.Button): Botão para editar o coletor selecionado.
            btn_excluir (wx.Button): Botão para excluir o coletor selecionado.
            btn_atualizar (wx.Button): Botão para atualizar a lista de coletores.
            btn_upload_csv (wx.Button): Botão para upload de arquivos CSV.
        Layout:
            - Um sizer principal (sizer_principal) organiza os elementos verticalmente.
            - Um sizer de botões (sizer_botoes) organiza os botões horizontalmente.
        Eventos:
            - Botões possuem eventos associados para adicionar, editar, excluir e atualizar coletores.
            - A lista captura eventos de seleção, deseleção e duplo clique para interação com os itens.
        Inicialização:
            - Carrega os coletores para exibição na lista.
            - Atualiza o estado dos botões "Editar" e "Excluir" com base na seleção atual.
        """
        super().__init__(parent)
        self.coletores_lista = []  # Criação da lista de coletores a serem exibidos
        self.controller = coletor_controller  # Referencia ao controller

        # --- Elementos da Interface ---
        self.list_ctrl = (
            wx.ListCtrl(  # Cria um elemento de lista controlado pelo wx
                self,
                style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL,
            )
        )

        # Criação das colunas ID, modelo, disponibilidade no elemento de lista
        self.list_ctrl.InsertColumn(0, 'Número Col.', width=100)
        self.list_ctrl.InsertColumn(1, 'Modelo Col.', width=100)
        self.list_ctrl.InsertColumn(2, 'Disponível', width=80)

        self.btn_adicionar = wx.Button(self, label='Adicionar')
        self.btn_editar = wx.Button(self, label='Editar')
        self.btn_excluir = wx.Button(self, label='Excluir')
        self.btn_atualizar = wx.Button(self, label='Atualizar Lista')
        self.btn_upload_csv = wx.Button(self, label='...')
        """
        #TODO fazer essa lógica aqui do "...". Replicar depois nas outras TABS.
        #INFO Manter essa anotação de ToDo até terminar todas TABS!
        """

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_botoes.Add(self.btn_adicionar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_editar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_excluir, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_atualizar, 0, wx.ALL, 5)
        sizer_botoes.AddStretchSpacer()
        sizer_botoes.Add(self.btn_upload_csv, 0, wx.ALL, 5)

        sizer_principal.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer_principal)

        # --- Captura de eventos ---
        self.btn_adicionar.Bind(wx.EVT_BUTTON, self.on_adicionar_coletor)
        self.btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_coletor)
        self.btn_excluir.Bind(wx.EVT_BUTTON, self.on_excluir_coletor)
        self.btn_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar_lista)
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.on_editar_coletor
        )  # Duplo clique
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_SELECTED, lambda event: self.atualizar_estado_botoes())
        self.list_ctrl.Bind(
            wx.EVT_LIST_ITEM_DESELECTED, lambda event: self.atualizar_estado_botoes())
        self.btn_upload_csv.Bind(wx.EVT_BUTTON, self.on_upload_csv)

        # --- Inicialização dos Widgets ---
        self.carregar_coletores()  # Carrega os coletores para exibição
        self.atualizar_estado_botoes()  # Atualiza os estados dos botões Editar e Excluir

    def on_upload_csv(self, event=None):
        """Evento chamado ao clicar no botão 'Upload CSV'."""
        with wx.FileDialog(
            self,
            'Escolha um arquivo CSV',
            wildcard='CSV files (*.csv)|*.csv',
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                caminho_arquivo = dlg.GetPath()
                try:
                    self.controller.carregar_coletores_csv(caminho_arquivo)
                    wx.MessageBox(
                        'Colaboradores carregados com sucesso!',
                        'Sucesso',
                        wx.OK | wx.ICON_INFORMATION,
                    )
                    self.carregar_coletores()
                except Exception as e:
                    wx.MessageBox(
                        f'Erro ao carregar colaboradores: {str(e)}',
                        'Erro',
                        wx.OK | wx.ICON_ERROR,
                    )



    def on_atualizar_lista(self, event=None):
        """
        Manipula o evento para atualizar a lista de coletores.

        Este método é acionado por um evento e realiza as seguintes ações:
        1. Atualiza o estado dos botões na interface.
        2. Carrega ou atualiza a lista de coletores.

        Args:
            event: O objeto de evento que acionou este método.
        """
        self.atualizar_estado_botoes()
        self.carregar_coletores()

    def carregar_coletores(self):
        """
        Carrega a lista de coletores no controle de lista da interface.
        Este método limpa todos os itens existentes no controle de lista e, em seguida,
        preenche-o com os dados dos coletores obtidos do controlador. Para cada coletor,
        são exibidos o ID (com 3 dígitos, preenchido com zeros à esquerda), o modelo
        e a disponibilidade (exibida como 'Sim' ou 'Não').
        Returns:
            None
        """

        self.list_ctrl.DeleteAllItems()
        self.coletores_lista = self.controller.listar_coletores()
        for index, coletor in enumerate(self.coletores_lista):
            list_index = self.list_ctrl.InsertItem(
                index, str(coletor['id']).zfill(3)
            )
            self.list_ctrl.SetItem(list_index, 1, coletor['modelo'])
            self.list_ctrl.SetItem(
                list_index,
                2,
                'Sim' if coletor['disponibilidade'] else 'Não',
            )

    def atualizar_estado_botoes(self):
        """
        Atualiza o estado dos botões "Editar" e "Excluir" com base na seleção da lista.

        Este método verifica se há algum item selecionado na lista controlada por `list_ctrl`.
        Caso exista uma seleção, os botões "Editar" e "Excluir" são habilitados; caso contrário,
        eles são desabilitados.

        Returns:
            None
        """
        tem_selecao = self.list_ctrl.GetFirstSelected() != -1
        self.btn_editar.Enable(tem_selecao)
        self.btn_excluir.Enable(tem_selecao)

    def on_adicionar_coletor(self, event=None):
        """
        Método chamado ao adicionar um novo coletor.
        Este método exibe um diálogo para o usuário inserir as informações de um novo coletor.
        Caso o usuário confirme a operação, os dados do coletor são obtidos do diálogo e 
        enviados para o controlador para serem adicionados ao sistema. Após a adição bem-sucedida, 
        uma mensagem de sucesso é exibida e a lista de coletores é recarregada.
        Args:
            event (wx.Event, opcional): Evento que disparou a ação. Padrão é None.
        Retorna:
            bool: Retorna True após a execução bem-sucedida do método.
        """

        dlg = AdiconarColetorDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            numero = dlg.txt_numero.GetValue()
            modelo = dlg.txt_modelo.GetValue()
            disponivel = dlg.cb_disponivel.GetValue()
            coletor = self.controller.adicionar_coletor(
                id=numero,
                modelo=modelo,
                disponibilidade=disponivel,
            )

            if coletor:
                wx.MessageBox(
                    f'Coletor {numero} adicionado com sucesso!',
                    'Sucesso',
                    wx.OK | wx.ICON_INFORMATION,
                )
                self.carregar_coletores()
        dlg.Destroy()
        self.atualizar_estado_botoes()
        return True

    def on_editar_coletor(self, event):
        """
        Evento chamado ao clicar no botão 'Editar' ou ao dar duplo clique na lista de coletores.
        Este método permite editar as informações de um coletor selecionado na lista.
        Ele exibe um diálogo de edição com os dados do coletor, permitindo que o usuário
        altere o número, modelo e disponibilidade do coletor. Após a confirmação, as
        alterações são salvas e a lista de coletores é atualizada.
        Args:
            event: O evento disparado pelo clique no botão ou duplo clique na lista.
        Comportamento:
            - Obtém o índice do coletor selecionado na lista.
            - Busca os dados do coletor correspondente através do controlador.
            - Exibe um diálogo de edição com os dados do coletor.
            - Atualiza os dados do coletor no sistema se o usuário confirmar as alterações.
            - Exibe mensagens de sucesso ou erro dependendo do resultado da operação.
            - Atualiza o estado dos botões da interface.
        """

        select_index = self.list_ctrl.GetFirstSelected()
        if select_index != -1:
            id = self.list_ctrl.GetItemText(select_index, 0)
            coletor = self.controller.buscar_coletor(int(id))
            atribuicao =  atribuicao_controller.buscar_atribuicao_por_chave(
                chave='coletor',
                valor=coletor.id
            )
            if not atribuicao:
                if coletor:
                    dlg = EditarColetorDialog(self, coletor)
                    if dlg.ShowModal() == wx.ID_OK:
                        numero = dlg.txt_numero.GetValue()
                        modelo = dlg.txt_modelo.GetValue()
                        disponivel = dlg.cb_disponivel.GetValue()

                        if self.controller.editar_coletor(
                            numero, modelo, disponivel
                        ):
                            wx.MessageBox(
                                f'Coletor {numero} atualizado com sucesso!',
                                'Sucesso',
                                wx.OK | wx.ICON_INFORMATION,
                            )
                            self.carregar_coletores()
                        else:
                            wx.MessageBox(
                                f'Erro ao atualizar o coletor {str(numero).zfill(3)}.',
                                'Erro',
                                wx.OK | wx.ICON_ERROR,
                            )
                    dlg.Destroy()
            else:
                wx.MessageBox(
                            f'O {str(coletor).zfill(3)} não pode ser alterado pois está atribuído ao colaborador {atribuicao.colaborador.nome}, matrícula {atribuicao.colaborador.matricula}.',
                            'Erro',
                            wx.OK | wx.ICON_ERROR,
                        )
            self.atualizar_estado_botoes()

    def on_excluir_coletor(self, event=None):
        """
        Método responsável por excluir um coletor selecionado na lista.
        Este método é acionado ao clicar no botão de exclusão. Ele verifica se há
        um coletor selecionado na lista, solicita confirmação do usuário para a
        exclusão e, caso confirmado, tenta excluir o coletor utilizando o
        controlador. Após a exclusão, a lista de coletores é recarregada.
        Parâmetros:
            event (wx.Event, opcional): Evento que acionou o método. Padrão é None.
        Funcionalidade:
            - Obtém o índice do coletor selecionado na lista.
            - Exibe uma mensagem de confirmação para o usuário.
            - Caso confirmado, tenta excluir o coletor através do controlador.
            - Exibe mensagens de sucesso ou erro dependendo do resultado.
            - Atualiza a lista de coletores e o estado dos botões.
        Observação:
            Este método utiliza a biblioteca wxPython para exibir diálogos e
            mensagens ao usuário.
        """

        selected_index = self.list_ctrl.GetFirstSelected()
        if selected_index != -1:
            coletor_numero = self.list_ctrl.GetItemText(selected_index, 0)
            print(f'Tentando excluir coletor {coletor_numero}')
            coletor = self.controller.buscar_coletor(coletor_numero)
            if coletor:
                dlg = wx.MessageDialog(
                    self,
                    f'Deseja mesmo excluir o coletor {coletor_numero}?',
                    'Confirmar Exclusão',
                    wx.YES_NO | wx.ICON_QUESTION,
                )
                if dlg.ShowModal() == wx.ID_YES:
                    if self.controller.excluir_coletor(coletor_numero):
                        wx.MessageBox(
                            f'Coletor {coletor_numero} excluído com sucesso!',
                            'Sucesso',
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        self.carregar_coletores()
                    else:
                        wx.MessageBox(
                            f'Erro ao excluir o coletor {coletor_numero}',
                            'Erro',
                            wx.OK | wx.ICON_ERROR,
                        )
            dlg.Destroy()
        self.atualizar_estado_botoes()

    def upload_csv(self):
        print('Longpress')


class AdiconarColetorDialog(wx.Dialog):
    """
    Classe AdiconarColetorDialog
    -----------
    Esta classe representa um diálogo para adicionar um coletor no sistema, utilizando a biblioteca wxPython.
    Atributos:
    -----------
    - txt_numero (wx.TextCtrl): Campo de texto para entrada do número do coletor.
    - txt_modelo (wx.TextCtrl): Campo de texto para entrada do modelo do coletor.
    - cb_disponivel (wx.CheckBox): Caixa de seleção para indicar se o coletor está disponível.
    - btn_salvar (wx.Button): Botão para salvar as informações do coletor.
    - btn_cancelar (wx.Button): Botão para cancelar a operação.
    Métodos:
    --------
    - __init__(parent): Construtor da classe que inicializa os elementos da interface e organiza o layout.
    Layout:
    -------
    - sizer_principal (wx.BoxSizer): Gerenciador de layout principal que organiza os elementos verticalmente.
    - sizer_campos (wx.FlexGridSizer): Gerenciador de layout para organizar os campos de entrada em uma grade flexível.
    - sizer_checkboxes (wx.BoxSizer): Gerenciador de layout para organizar as caixas de seleção (atualmente não utilizado).
    - sizer_botoes (wx.BoxSizer): Gerenciador de layout para organizar os botões horizontalmente.
    """

    def __init__(self, parent):
        super().__init__(parent, title='Adicionar Coletor', size=(400, 300))

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(self)
        self.txt_modelo = wx.TextCtrl(self)
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(True)  # Define como marcado por padrão.

        self.btn_salvar = wx.Button(self, wx.ID_OK, 'Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, 'Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)

        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (wx.StaticText(self, label='Número:'), 0,
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_numero, 0, wx.EXPAND),
            (wx.StaticText(self, label='Modelo:'), 0,
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.txt_modelo, 0, wx.EXPAND),
            (wx.StaticText(self, label='Disponível:'), 0,
             wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
            (self.cb_disponivel, 0, wx.EXPAND),
            (wx.StaticText(self, label=''), 0,),  # Espaço vazio
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        # sizer_checkboxes.Add(self.cb_disponivel, 0, wx.ALL, 5)

        sizer_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()


class EditarColetorDialog(wx.Dialog):
    """
    Classe EditarColetorDialog
    -----------
    Esta classe representa um diálogo para editar as informações de um coletor no sistema. 
    Ela utiliza a biblioteca wxPython para criar uma interface gráfica.
    Atributos:
    -----------
    coletor : object
        Objeto que contém as informações do coletor a serem editadas.
    txt_numero : wx.TextCtrl
        Campo de texto para exibir o ID do coletor (somente leitura).
    txt_modelo : wx.TextCtrl
        Campo de texto para editar o modelo do coletor.
    cb_disponivel : wx.CheckBox
        Caixa de seleção para indicar a disponibilidade do coletor.
    btn_salvar : wx.Button
        Botão para salvar as alterações realizadas.
    btn_cancelar : wx.Button
        Botão para cancelar a edição e fechar o diálogo.
    Métodos:
    --------
    __init__(parent, coletor)
        Construtor da classe. Inicializa os elementos da interface e configura o layout.
    """
    

    def __init__(self, parent, coletor):
        super().__init__(parent, title='Editar Coletor', size=(400, 300))
        self.coletor = coletor

        # --- Elementos da Interface ---
        self.txt_numero = wx.TextCtrl(
            self,
            value=str(self.coletor.id),
            style=wx.TE_READONLY,
        )  # Não permitir editar o ID
        self.txt_modelo = wx.TextCtrl(self, value=self.coletor.modelo)
        self.cb_disponivel = wx.CheckBox(self, label='Disponível')
        self.cb_disponivel.SetValue(self.coletor.disponibilidade)

        self.btn_salvar = wx.Button(self, wx.ID_OK, 'Salvar')
        self.btn_cancelar = wx.Button(self, wx.ID_CANCEL, 'Cancelar')

        # --- Layout ---
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_campos = wx.FlexGridSizer(rows=4, cols=2, vgap=5, hgap=5)

        sizer_checkboxes = wx.BoxSizer(wx.VERTICAL)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)

        sizer_campos.AddMany([
            (
                wx.StaticText(self, label='Número:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_numero, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Modelo:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.txt_modelo, 0, wx.EXPAND),
            (
                wx.StaticText(self, label='Disponível:'),
                0,
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL,
            ),
            (self.cb_disponivel, 0, wx.EXPAND),
            (
                wx.StaticText(self, label=''),
                0,
            ),  # Espaço vazio
            (sizer_checkboxes, 0, wx.EXPAND),
        ])

        sizer_botoes.Add(self.btn_salvar, 0, wx.ALL, 5)
        sizer_botoes.Add(self.btn_cancelar, 0, wx.ALL, 5)

        sizer_principal.Add(sizer_campos, 0, wx.EXPAND | wx.ALL, 10)
        sizer_principal.Add(sizer_botoes, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.SetSizer(sizer_principal)
        self.Fit()
