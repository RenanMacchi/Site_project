from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'teste'

# Função auxiliar para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuração do diretório de upload
UPLOAD_FOLDER = 'C:\\Users\\renan\\Desktop\\img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Lista de usuários fictícios
usuarios = {
    'casa119': {
        'senha': '85063894020',
        'casa': 'casa119',
        'perfis': [
            {
                'nome': 'Renan',
                'contato': '111',
                'instagram': 'renan_insta',
            },
            {
                'nome': '',
                'contato': '222',
                'instagram': '',
            },
            {
                'nome': '',
                'contato': '333',
                'instagram': 'renan_insta3',
            },
        ],
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

@app.route('/exibir_noticia_expandida/<int:noticia_id>')
def exibir_noticia_expandida(noticia_id):
    # Adicione lógica para recuperar a notícia específica com base no ID
    noticia = noticias[noticia_id]
    return render_template('noticia_expandida.html', noticia=noticia)

@app.route('/postar_noticia', methods=['GET', 'POST'])
def postar_noticia():
    # Verifique se o usuário está logado
    usuario_logado = session.get('usuario_logado')
    if not usuario_logado:
        flash('Faça login para criar uma nova notícia.', 'warning')
        return redirect(url_for('login'))

    # Obtém os detalhes do usuário a partir da lista de usuários
    usuario = usuarios.get(usuario_logado)

    total_perfis = len(usuario['perfis'])  # Total de perfis do usuário

    if request.method == 'POST':
        # Obtenha os dados do formulário
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        perfil_escolhido = int(request.form['perfil']) - 1  # Subtrai 1 para obter o índice correto

        print(f'Título: {titulo}')
        print(f'Conteúdo: {conteudo}')
        print(f'Perfil escolhido: {perfil_escolhido}')

        imagens_salvas = []  # Lista para armazenar os caminhos das imagens salvas

        if 'imagens' in request.files:
            imagens = request.files.getlist('imagens')

            for arquivo in imagens:
                # Verificar se o arquivo tem um nome e é permitido
                if arquivo.filename != '' and allowed_file(arquivo.filename):
                    # Salvar o arquivo no diretório de upload
                    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(arquivo.filename))
                    arquivo.save(caminho_arquivo)

                    # Adicionar o caminho do arquivo à lista
                    imagens_salvas.append(caminho_arquivo)

                    # Limitar a quantidade de imagens a 10
                    if len(imagens_salvas) >= 10:
                        break

        print(f'Imagens salvas: {imagens_salvas}')

        # Verifica se o perfil escolhido está dentro do intervalo
        if 0 <= perfil_escolhido < total_perfis:
            perfil = usuario['perfis'][perfil_escolhido]

            # Preenche os campos do formulário com as informações do perfil escolhido
            nome_usuario = perfil.get('nome', '')
            whatsapp = perfil.get('contato', '')
            instagram = perfil.get('instagram', '')

            # Informações adicionais da notícia
            autor = f"{perfil['nome']} ({usuario_logado})"
            data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Crie um dicionário representando a nova notícia
            nova_noticia = {
                'titulo': titulo,
                'conteudo': conteudo,
                'autor': autor,
                'data': data_atual,
                'nome_usuario': nome_usuario,
                'whatsapp': whatsapp,
                'instagram': instagram,
            }

            # Adicione a lista de caminhos de imagens à notícia
            nova_noticia['imagens'] = imagens_salvas

            # Adicione a nova notícia à lista
            noticias.append(nova_noticia)

            # Exiba uma mensagem de sucesso
            flash('Notícia criada com sucesso!', 'success')

            # Redirecione de volta para a página de notícias
            return redirect(url_for('exibir_noticias'))

    # Se o método for GET, exiba o formulário para postar notícia
    return render_template('postar_noticia.html', perfis=usuario['perfis'], total_perfis=total_perfis)

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
        perfis = usuario.get('perfis', [])
        return render_template('perfil.html', perfis=perfis)
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
        for i, perfil in enumerate(usuario['perfis']):
            # Atualize as informações do perfil com os valores do formulário
            novo_nome = request.form.get(f'novo_nome{i + 1}')
            novo_contato = request.form.get(f'novo_contato{i + 1}')
            novo_instagram = request.form.get(f'novo_instagram{i + 1}')

            if novo_nome is not None:
                perfil['nome'] = novo_nome

            if novo_contato is not None:
                perfil['contato'] = novo_contato

            if novo_instagram is not None:
                perfil['instagram'] = novo_instagram

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
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
