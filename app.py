from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'teste'

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

noticias = []
exemplo_noticia = {
    'titulo': 'Título da Notícia',
    'conteudo': 'Conteúdo da notícia...',
    'autor': 'casa119',  # Usuário que postou a notícia
    'data': '2024-01-13 12:00:00'  # Data e hora da postagem
}

noticias.append(exemplo_noticia)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/exibir_noticias')
def exibir_noticias():
    return render_template('noticias.html', noticias=noticias)

@app.route('/postar_noticia', methods=['GET', 'POST'])
def postar_noticia():
    # Verifique se o usuário está logado
    usuario_logado = session.get('usuario_logado')
    if not usuario_logado:
        flash('Faça login para criar uma nova notícia.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtenha os dados do formulário
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']

        # Crie uma string representando a data e hora atual
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Crie um dicionário representando a nova notícia
        nova_noticia = {
            'titulo': titulo,
            'conteudo': conteudo,
            'autor': usuario_logado,
            'data': data_atual
        }

        # Adicione a nova notícia à lista
        noticias.append(nova_noticia)

        # Exiba uma mensagem de sucesso
        flash('Notícia criada com sucesso!', 'success')

        # Redirecione de volta para a página de notícias
        return redirect(url_for('exibir_noticias'))

    # Se o método for GET, exiba o formulário para postar notícia
    return render_template('postar_noticia.html')

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

@app.route('/alterar_senha')
def alterar_senha():
    # Obtém o usuário logado da sessão
    usuario_logado = session.get('usuario_logado')

    # Se não houver usuário logado, redireciona para a página de login
    if not usuario_logado:
        return redirect(url_for('login'))

    return render_template('alterar_senha.html')

# ...

@app.route('/atualizar_senha', methods=['POST'])
def atualizar_senha():
    # Obtém o usuário logado da sessão
    usuario_logado = session.get('usuario_logado')

    # Se não houver usuário logado, redireciona para a página de login
    if not usuario_logado:
        return redirect(url_for('login'))

    # Obtém os detalhes do usuário a partir da lista de usuários
    usuario = usuarios.get(usuario_logado)

    erro_senha_atual = None  # Defina a variável antes das condições

    if request.method == 'POST':
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']
        confirmar_nova_senha = request.form['confirmar_nova_senha']

        # Verifica se a senha atual está correta
        if senha_atual != usuario['senha']:
            # Adicione uma mensagem de erro, se desejar
            erro_senha_atual = 'A senha atual está incorreta. Tente novamente.'

        # Verifica se a nova senha e a confirmação coincidem
        elif nova_senha != confirmar_nova_senha:
            # Adicione uma mensagem de erro, se desejar
            erro_confirmar_nova_senha = 'As senhas não coincidem. Tente novamente.'
            return render_template('alterar_senha.html', usuario_logado=usuario_logado, erro_confirmar_nova_senha=erro_confirmar_nova_senha)

        else:
            # Atualiza a senha do usuário
            usuario['senha'] = nova_senha

            # Remova o usuário logado da sessão (efetuar logout)
            session.pop('usuario_logado', None)

            # Redireciona para a página de login
            return redirect(url_for('login'))

    return render_template('alterar_senha.html', usuario_logado=usuario_logado, erro_senha_atual=erro_senha_atual)

@app.route('/logout')
def logout():
    # Remova o usuário logado da sessão
    session.pop('usuario_logado', None)
    # Redirecione para a página inicial
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
