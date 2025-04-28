## Sobre o Projeto

Este programa se propõe a registrar as atribuições de equipamentos em ambiente de armazém logístico, provendo, inclusive, relatórios de uso.

### Funcionalidades

- Registro de atribuições de equipamentos.
- Geração de relatórios detalhados de uso. (em breve)
- Interface amigável para fácil navegação.
- Exportação de relatórios em formatos populares como PDF e Excel. (ainda não implementado)

### Tecnologias Utilizadas

- **Python**: Linguagem principal para desenvolvimento.
- **SQLite**: Banco de dados leve e eficiente.

### SQL
```bash
-- Criação da Tabela: colaborador
-- Armazena informações sobre os colaboradores.
CREATE TABLE colaborador (
    matricula VARCHAR(255) NOT NULL PRIMARY KEY, -- Chave primária: Matrícula única do colaborador
    nome VARCHAR(255) NOT NULL,                 -- Nome do colaborador
    cargo VARCHAR(255) NOT NULL,                -- Cargo do colaborador
    autorizado_transpaleteira INTEGER NOT NULL, -- Flag indicando autorização para transpaleteira (0=Não, 1=Sim)
    autorizado_empilhadeira INTEGER NOT NULL    -- Flag indicando autorização para empilhadeira (0=Não, 1=Sim)
);

-- Criação da Tabela: coletor
-- Armazena informações sobre os coletores de dados.
CREATE TABLE coletor (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Chave primária: ID único do coletor (auto-incremento)
    modelo VARCHAR(255) NOT NULL,                -- Modelo do coletor
    disponibilidade INTEGER NOT NULL             -- Status de disponibilidade (ex: 1=Disponível, 0=Indisponível)
);

-- Criação da Tabela: empilhadeira
-- Armazena informações sobre as empilhadeiras.
CREATE TABLE empilhadeira (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Chave primária: ID único da empilhadeira (auto-incremento)
    modelo VARCHAR(255) NOT NULL,                -- Modelo da empilhadeira
    disponibilidade INTEGER NOT NULL             -- Status de disponibilidade (ex: 1=Disponível, 0=Indisponível)
);

-- Criação da Tabela: transpaleteira
-- Armazena informações sobre as transpaleteiras.
CREATE TABLE transpaleteira (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Chave primária: ID único da transpaleteira (auto-incremento)
    modelo VARCHAR(255) NOT NULL,                -- Modelo da transpaleteira
    disponibilidade INTEGER NOT NULL             -- Status de disponibilidade (ex: 1=Disponível, 0=Indisponível)
);

-- Criação da Tabela: atribuicao
-- Registra a atribuição de equipamentos (coletor, empilhadeira, transpaleteira) a colaboradores.
CREATE TABLE atribuicao (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Chave primária: ID único da atribuição (auto-incremento)
    colaborador_id VARCHAR(255) NOT NULL,          -- Chave estrangeira referenciando colaborador(matricula)
    coletor_id INTEGER,                            -- Chave estrangeira referenciando coletor(id)
    empilhadeira_id INTEGER,                       -- Chave estrangeira referenciando empilhadeira(id)
    transpaleteira_id INTEGER,                     -- Chave estrangeira referenciando transpaleteira(id)
    data_inicio DATETIME NOT NULL,                 -- Data e hora de início da atribuição
    data_fim DATETIME,                             -- Data e hora de fim da atribuição (pode ser NULL se ativa)

    -- Definição das chaves estrangeiras para garantir a integridade referencial
    FOREIGN KEY (colaborador_id) REFERENCES colaborador (matricula),
    FOREIGN KEY (coletor_id) REFERENCES coletor (id),
    FOREIGN KEY (empilhadeira_id) REFERENCES empilhadeira (id),
    FOREIGN KEY (transpaleteira_id) REFERENCES transpaleteira (id)
);

-- Criação dos Índices
-- Índices melhoram o desempenho das consultas filtrando ou ordenando por estas colunas.
CREATE INDEX atribuicao_colaborador_id ON atribuicao (colaborador_id);
CREATE INDEX atribuicao_coletor_id ON atribuicao (coletor_id);
CREATE INDEX atribuicao_empilhadeira_id ON atribuicao (empilhadeira_id);
CREATE INDEX atribuicao_transpaleteira_id ON atribuicao (transpaleteira_id);
CREATE INDEX coletor_modelo ON coletor (modelo);
CREATE INDEX empilhadeira_id ON empilhadeira (id); -- Índice na PK, geralmente redundante mas presente na imagem
CREATE INDEX transpaleteira_modelo ON transpaleteira (modelo);

-- Nota: Para que as chaves estrangeiras (FOREIGN KEY) funcionem no SQLite,
-- você pode precisar habilitá-las com o comando: PRAGMA foreign_keys = ON;
-- Este comando geralmente é executado uma vez por conexão.
```

### Como Executar

1. Clone o repositório:
    ```bash
    git clone https://github.com/FigurPH/GesCol---Gestor-de-Coletores-e-Equipamentos-Log-sitcos.git GesCol
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd GesCol
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute a aplicação (TASKIPY):
    ```bash
    task run
    ```
    --- ver mais em pyproject.py

### Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
    ```bash
    git checkout -b minha-feature
    ```
3. Commit suas alterações:
    ```bash
    git commit -m 'Adiciona minha nova feature'
    ```
4. Envie para o repositório remoto:
    ```bash
    git push origin minha-feature
    ```
5. Abra um Pull Request.

### Precisa-se de ajuda!

Estou com dificuldades em gerar um spec funcional para o PyInstaller gerar um programa nativo para Windows (preferencialmente OneFolder). Se alguém conseguir me ajudar, fico eternamente grato!

## Licença

Este projeto é licenciado sob os termos da [GNU General Public License v3.0](LICENSE).

