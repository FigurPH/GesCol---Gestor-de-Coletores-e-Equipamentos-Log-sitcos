import wx

from controllers import atribuicao_controller


class TabAtribuicoes(wx.Panel):
    """
    Classe TabAtribuicoes
    Esta classe representa uma aba de atribuições em uma interface gráfica construída com wxPython. 
    Ela permite gerenciar a atribuição de equipamentos (como coletores, transpaleteiras e empilhadeiras) 
    a colaboradores, bem como exibir informações relacionadas.
    Atributos:
        atribuicao_lista (list): Lista de atribuições.
        controller (object): Controlador responsável pelas operações de atribuição.
        matricula (wx.TextCtrl): Campo de texto para entrada da matrícula do colaborador.
        btn_buscar (wx.Button): Botão para buscar informações do colaborador.
        lbl_nome (wx.StaticText): Rótulo para exibir o nome do colaborador.
        lbl_cargo (wx.StaticText): Rótulo para exibir o cargo do colaborador.
        txt_coletor_id (wx.TextCtrl): Campo de texto para entrada do ID do coletor.
        btn_atribuir_coletor (wx.Button): Botão para atribuir ou devolver coletor.
        data_coletor (wx.StaticText): Rótulo para exibir a data de atribuição do coletor.
        cb_transpaleteira (wx.CheckBox): Checkbox para indicar autorização para transpaleteira.
        txt_transpaleteira_id (wx.TextCtrl): Campo de texto para entrada do ID da transpaleteira.
        btn_atribuir_transpaleteira (wx.Button): Botão para atribuir transpaleteira.
        data_transpaleteira (wx.StaticText): Rótulo para exibir a data de atribuição da transpaleteira.
        cb_empilhadeira (wx.CheckBox): Checkbox para indicar autorização para empilhadeira.
        txt_empilhadeira_id (wx.TextCtrl): Campo de texto para entrada do ID da empilhadeira.
        btn_atribuir_empilhadeira (wx.Button): Botão para atribuir empilhadeira.
        data_empilhadeira (wx.StaticText): Rótulo para exibir a data de atribuição da empilhadeira.
    Métodos:
        __init__(parent): Inicializa a aba de atribuições e configura o layout e os bindings.
        limpa_tela(): Reseta os campos e botões da interface para o estado inicial.
        on_buscar_colaborador(event=None): Busca informações do colaborador com base na matrícula.
        on_atribuir_coletor(event=None): Atribui ou devolve um coletor ao colaborador.
        on_atribuir_transpaleteira(event=None): (Método a ser implementado) Atribui ou devolve uma transpaleteira.
        on_atribuir_empilhadeira(event=None): (Método a ser implementado) Atribui ou devolve uma empilhadeira.
        atribuir_equipamento(tipo_equipamento): Gerencia a atribuição de equipamentos com base no tipo especificado.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.atribuicao_lista = []
        self.controller = atribuicao_controller

        # --- Layout Principal ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Linha Superior: Campo de ID e Botão Buscar ---
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Adiciona o campo de texto para buscar pela matrícula e inclui captura de ação de Enter
        self.matricula = wx.TextCtrl(self, size=(200, -1), name="matricula", style=wx.TE_PROCESS_ENTER)
        self.matricula.SetHint("Matrícula")
        self.matricula.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.btn_buscar = wx.Button(self, label="Buscar", name="btn_buscar")
        search_sizer.Add(self.matricula, 0, wx.ALL, 5)
        search_sizer.Add(self.btn_buscar, 0, wx.ALL, 5)
        main_sizer.Add(search_sizer, 0, wx.EXPAND)

        # --- Informações do Colaborador ---
        colaborador_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=""), wx.VERTICAL)
        self.lbl_nome = wx.StaticText(self, label="Nome")
        # self.lbl_nome.SetLabelText("Xuleipa") # usar essa abordagem para atribuir valor
        self.lbl_cargo = wx.StaticText(self, label="Cargo")
        colaborador_sizer.Add(self.lbl_nome, 0, wx.ALL, 5)
        colaborador_sizer.Add(self.lbl_cargo, 0, wx.ALL, 5)

        # --- Linha do Coletor ---
        coletor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coletor_label = wx.StaticText(self, label="Coletor:")
        self.txt_coletor_id = wx.TextCtrl(self, size=(150, -1), name="coletor_id", 
                                        style=wx.TE_PROCESS_ENTER)
        self.btn_atribuir_coletor = wx.Button(self, label="Atribuir", name="btn_atribuir_coletor")
        self.data_coletor = wx.StaticText(self, label="data_coletor")
        coletor_sizer.Add(coletor_label, 0, wx.ALL, 5)
        coletor_sizer.Add(self.txt_coletor_id, 0, wx.ALL, 5)
        coletor_sizer.Add(self.btn_atribuir_coletor, 0, wx.ALL, 5)
        coletor_sizer.Add(self.data_coletor, 0, wx.ALL, 5)
        colaborador_sizer.Add(coletor_sizer, 0, wx.EXPAND)

        main_sizer.Add(colaborador_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --- Equipamentos ---
        equipamentos_sizer = wx.StaticBoxSizer(wx.StaticBox(self, label="Equipamentos"), wx.VERTICAL)

        # Linha da Transpaleteira
        transpaleteira_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_transpaleteira = wx.CheckBox(self, label="Transpaleteira")
        self.txt_transpaleteira_id = wx.TextCtrl(self, size=(150, -1), name="txt_transpaleteira_id", 
                                                style=wx.TE_PROCESS_ENTER)
        self.txt_transpaleteira_id.SetValue("Em breve...")
        self.btn_atribuir_transpaleteira = wx.Button(self, label="Atribuir", 
                                                    name="btn_atribuir_transpaleteira")
        self.data_transpaleteira = wx.StaticText(self, label="data_transpaleteira")
        transpaleteira_sizer.Add(self.cb_transpaleteira, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.txt_transpaleteira_id, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.btn_atribuir_transpaleteira, 0, wx.ALL, 5)
        transpaleteira_sizer.Add(self.data_transpaleteira, 0, wx.ALL, 5)
        equipamentos_sizer.Add(transpaleteira_sizer, 0, wx.EXPAND)

        # Linha da Empilhadeira
        empilhadeira_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_empilhadeira = wx.CheckBox(self, label="Empilhadeira  ")
        self.txt_empilhadeira_id = wx.TextCtrl(self, size=(150, -1), name="txt_empilhadeira_id",
                                                style=wx.TE_PROCESS_ENTER)
        self.txt_empilhadeira_id.SetValue("Em breve...")
        self.btn_atribuir_empilhadeira = wx.Button(self, label="Atribuir", name="btn_atribuir_empilhadeira")
        self.data_empilhadeira = wx.StaticText(self, label="data_empilhadeira")
        empilhadeira_sizer.Add(self.cb_empilhadeira, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.txt_empilhadeira_id, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.btn_atribuir_empilhadeira, 0, wx.ALL, 5)
        empilhadeira_sizer.Add(self.data_empilhadeira, 0, wx.ALL, 5)
        equipamentos_sizer.Add(empilhadeira_sizer, 0, wx.EXPAND)

        main_sizer.Add(equipamentos_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --- Botões e campos iniciam desativados ---
        self.txt_coletor_id.Disable()
        self.btn_atribuir_coletor.Disable()
        self.txt_transpaleteira_id.Disable()
        self.btn_atribuir_transpaleteira.Disable()
        self.txt_empilhadeira_id.Disable()
        self.btn_atribuir_empilhadeira.Disable()
        self.cb_transpaleteira.Disable()
        self.cb_empilhadeira.Disable()
        self.data_coletor.Hide()
        self.data_transpaleteira.Hide()
        self.data_empilhadeira.Hide()

        # --- Configuração Final ---
        self.SetSizer(main_sizer)

        # --- Bindings ---
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar_colaborador)
        self.matricula.Bind(wx.EVT_TEXT_ENTER, self.on_buscar_colaborador)
        self.btn_atribuir_coletor.Bind(wx.EVT_BUTTON,
                                            lambda x: self.atribuir_equipamento(tipo_equipamento='coletor'))
        self.btn_atribuir_transpaleteira.Bind(wx.EVT_BUTTON,
                                            lambda x: self.atribuir_equipamento('transpaleteira'))
        self.btn_atribuir_empilhadeira.Bind(wx.EVT_BUTTON,
                                            lambda x: self.atribuir_equipamento('empilhadeira'))
        self.txt_coletor_id.Bind(wx.EVT_TEXT_ENTER,
                                            lambda x: self.atribuir_equipamento(tipo_equipamento='coletor'))
        '''self.txt_transpaleteira_id.Bind(wx.EVT_TEXT_ENTER,
                                            lambda x: self.atribuir_equipamento('transpaleteira'))
        self.txt_empilhadeira_id.Bind(wx.EVT_TEXT_ENTER,
                                            lambda x: self.atribuir_equipamento('empilhadeira'))'''

        self.limpa_tela()

    def reset_screen(self):
        self.matricula.set('')
        self.limpa_tela()

    def limpa_tela(self):
        """
        Limpa e desativa os campos e botões relacionados às atribuições na interface.
        Este método realiza as seguintes ações:
        - Desativa o botão de atribuir coletor e redefine seu rótulo para 'Atribuir'.
        - Desativa os botões de atribuir empilhadeira e transpaleteira.
        - Desativa os campos de entrada de ID de coletor, empilhadeira e transpaleteira.
        - Limpa o valor do campo de entrada de ID de coletor.
        Uso:
        Este método é utilizado para redefinir a interface gráfica ao estado inicial,
        garantindo que nenhum campo ou botão relacionado às atribuições esteja ativo.
        """

        self.btn_atribuir_coletor.Disable()
        self.btn_atribuir_coletor.SetLabel('Atribuir')

        self.btn_atribuir_empilhadeira.Disable()
        self.btn_atribuir_transpaleteira.Disable()
        self.txt_coletor_id.Disable()
        self.txt_coletor_id.SetValue('')
        self.txt_empilhadeira_id.Disable()
        self.txt_transpaleteira_id.Disable()
        self.lbl_nome.SetLabelText('')
        self.lbl_cargo.SetLabelText('')
        self.matricula.SetFocus()

    def on_buscar_colaborador(self, evet=None):
        """
        Método responsável por buscar as informações de um colaborador com base na matrícula fornecida.
        Este método realiza as seguintes ações:
        - Limpa os campos da tela.
        - Carrega as informações do colaborador utilizando o controlador de atribuições.
        - Atualiza os rótulos de nome e cargo do colaborador na interface.
        - Habilita os campos e botões relacionados à atribuição de coletores.
        - Verifica se o colaborador possui um coletor atribuído e, se sim:
            - Preenche o campo do ID do coletor.
            - Atualiza o rótulo do botão para "Devolver".
            - Habilita os checkboxes e botões para transpaleteira e empilhadeira, caso o colaborador esteja autorizado.
        Args:
            evet (Event, opcional): Evento que pode ser passado ao método, geralmente associado a interações da interface gráfica.
        """

        self.limpa_tela()
        atribuicoes = atribuicao_controller.carregar_informacoes_colaborador(self.matricula.GetValue())
        if atribuicoes:
            self.lbl_nome.SetLabelText(atribuicoes.colaborador.nome)
            self.lbl_cargo.SetLabelText(atribuicoes.colaborador.cargo)
            self.txt_coletor_id.Enable()
            self.txt_coletor_id.SetFocus()
            self.btn_atribuir_coletor.Enable()
            try:
                if atribuicoes.coletor:
                    self.txt_coletor_id.SetValue(str(atribuicoes.coletor.id).zfill(3))
                    self.txt_coletor_id.SelectAll()
                    self.btn_atribuir_coletor.SetLabel('Devolver')
                    if atribuicoes.colaborador.autorizado_transpaleteira:
                        self.cb_transpaleteira.SetValue(True)
                        self.btn_atribuir_transpaleteira.Enable()
                    if atribuicoes.colaborador.autorizado_empilhadeira:
                        self.cb_empilhadeira.SetValue(True)
                        self.btn_atribuir_empilhadeira.Enable()
            except Exception:
                print('Nenhum coletor atribuído ainda (tab_atribuições)')
        else:
            resposta = wx.MessageBox(
                "Colaborador com a matrícula fornecida não existe. Deseja adicionar um novo colaborador?",
                "Colaborador não encontrado",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if resposta == wx.YES:
                from src.views.tab_colaboradores import TabColaboradores
                TabColaboradores(self.GetParent()).on_adicionar_colaborador()

    def on_atribuir_coletor(self, evet=None):
        """
        Método responsável por atribuir ou devolver um coletor a um colaborador.
        Args:
            evet (Event, opcional): Evento disparado pela interface gráfica. Padrão é None.
        Funcionalidade:
            - Se o botão "Atribuir" estiver selecionado:
                - Obtém o ID do coletor e a matrícula do colaborador.
                - Chama o método `atribuir_coletor` do controller para realizar a atribuição.
                - Exibe uma mensagem indicando sucesso ou falha na operação.
            - Caso contrário (botão "Devolver" selecionado):
                - Chama o método `devolver_coletor` do controller para realizar a devolução.
                - Exibe uma mensagem indicando sucesso ou falha na operação.
        Observação:
            Após a operação, o método `on_buscar_colaborador` é chamado para atualizar os dados exibidos.
        """

        coletor_id = self.txt_coletor_id.GetValue() or None
        matricula = self.matricula.GetValue() or None

        if self.btn_atribuir_coletor.GetLabel() == 'Atribuir':
            sucesso = self.controller.atribuir_coletor(matricula=matricula, coletor_id=coletor_id)
            mensagem = (f'Coletor {coletor_id} atribuído à Matrícula {matricula}'
                if sucesso else 'Não foi possível atribuir este coletor à matrícula fornecida')
            wx.MessageBox(mensagem, "Informação", wx.OK | wx.ICON_INFORMATION) if not sucesso else None
            # Tem que comparar not sucesso para mostrar apenas quando der erro.
        else:
            sucesso = self.controller.devolver_coletor(coletor_id)
            mensagem = (f'Coletor {coletor_id} devolvido.'
                if sucesso else 'Erro ao devolver coletor.')
            wx.MessageBox(mensagem, "Informação", wx.OK | wx.ICON_INFORMATION) if not sucesso else None
            # Tem que comparar not sucesso para mostrar apenas quando der erro.


        self.limpa_tela()
        self.matricula.SetValue('')

    def on_atribuir_transpaleteira(self, evet=None): ...

    def on_atribuir_empilhadeira(self, evet=None): ...

    def atribuir_equipamento(self, tipo_equipamento):

        match tipo_equipamento:
            case 'coletor':
                print('É um coletor, tentando adicionar')
                self.on_atribuir_coletor()

            case 'transpaleteira':
                print('É uma transpaleteira')

            case 'empilhadeira':
                print('É uma empilhadeira')
