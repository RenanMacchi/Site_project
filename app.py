from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'teste'  # Certifique-se de alterar isso para uma chave segura em um ambiente de produção

# Lista de usuários fictícios (substitua por um banco de dados real)
usuarios = {
    'casa119': {
        'senha': '85063894020',
        'casa': 'casa119',
        'nome1': 'Renan',
        'contato1': '111',
        'instagram1': 'renan_insta',
        'nome2': '',
        'contato2': '222',
        'instagram2': '',
        'nome3': '',
        'contato3': '333',
        'instagram3': 'renan_insta3',
    },
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['senha']

        usuario = usuarios.get(username)
        if usuario and usuario['senha'] == password:
            # Autenticação bem-sucedida, armazenar usuário na sessão
            session['usuario_logado'] = username
            return redirect(url_for('index'))
        else:
            # Autenticação falhou, exibir mensagem de erro
            error_message = 'Credenciais inválidas. Tente novamente.'
            return render_template('login.html', error_message=error_message)

    # Se o método for GET, exibir o formulário de login
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    # Obtém o usuário logado da sessão
    usuario_logado = session.get('usuario_logado')

    # Se não houver usuário logado, redireciona para a página de login
    if not usuario_logado:
        return redirect(url_for('login'))

    # Obtém os detalhes do usuário a partir da lista de usuários
    usuario = usuarios.get(usuario_logado)

    if usuario:
        return render_template('perfil.html', usuario=usuario)
    else:
        return 'Usuário não encontrado', 404


@app.route('/alterar_perfil')
def alterar_perfil():
    # Obtém o usuário logado da sessão
    usuario_logado = session.get('usuario_logado')

    # Se não houver usuário logado, redireciona para a página de login
    if not usuario_logado:
        return redirect(url_for('login'))

    # Obtém os detalhes do usuário a partir da lista de usuários
    usuario = usuarios.get(usuario_logado)

    if usuario:
        return render_template('alterar_perfil.html', usuario=usuario)
    else:
        return 'Usuário não encontrado', 404

@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    # Obtém o usuário logado da sessão
    usuario_logado = session.get('usuario_logado')

    # Se não houver usuário logado, redireciona para a página de login
    if not usuario_logado:
        return redirect(url_for('login'))

    # Obtém os detalhes do usuário a partir da lista de usuários
    usuario = usuarios.get(usuario_logado)

    if request.method == 'POST':
        # Atualize as informações do perfil com os valores do formulário
        novo_nome1 = request.form['novo_nome1']
        novo_contato1 = request.form['novo_contato1']
        novo_instagram1 = request.form['novo_instagram1']

        if novo_nome1 != usuario['nome1']:
            usuario['nome1'] = novo_nome1

        if novo_contato1 != usuario['contato1']:
            usuario['contato1'] = novo_contato1

        if novo_instagram1 != usuario['instagram1']:
            usuario['instagram1'] = novo_instagram1

        novo_nome2 = request.form['novo_nome2']
        novo_contato2 = request.form['novo_contato2']
        novo_instagram2 = request.form['novo_instagram2']

        if novo_nome2 != usuario['nome2']:
            usuario['nome2'] = novo_nome2

        if novo_contato2 != usuario['contato2']:
            usuario['contato2'] = novo_contato2

        if novo_instagram2 != usuario['instagram2']:
            usuario['instagram2'] = novo_instagram2

        novo_nome3 = request.form['novo_nome3']
        novo_contato3 = request.form['novo_contato3']
        novo_instagram3 = request.form['novo_instagram3']

        if novo_nome1 != usuario['nome3']:
            usuario['nome3'] = novo_nome3

        if novo_contato1 != usuario['contato3']:
            usuario['contato3'] = novo_contato3

        if novo_instagram3 != usuario['instagram3']:
            usuario['instagram3'] = novo_instagram3

        # Repita o mesmo padrão para os outros campos, se necessário

    # Redireciona de volta para a página de perfil após as alterações
    return redirect(url_for('perfil'))

@app.route('/logout')
def logout():
    # Remova o usuário logado da sessão
    session.pop('usuario_logado', None)
    # Redirecione para a página inicial
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
