from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'teste'

UPLOAD_FOLDER = r'C:\Users\renan\Desktop\img'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_FILES = 10000

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    'data': '13/01/2024 12:00:00'  # Data e hora da postagem
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

    uploaded_files = request.files.getlist("files[]")
    imagens_salvas = []

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            if len(os.listdir(app.config['UPLOAD_FOLDER'])) >= MAX_FILES:
                return 'Limite de 10 imagens atingido. Não é possível enviar mais imagens.'

            # Crie um identificador único para cada notícia
            identificador_noticia = str(uuid.uuid4())
            # Crie o subdiretório para a notícia
            noticia_dir = os.path.join(app.config['UPLOAD_FOLDER'], identificador_noticia)
            os.makedirs(noticia_dir, exist_ok=True)

            # Gere um nome de arquivo único para a imagem
            nome_arquivo = secure_filename(file.filename)
            nome_arquivo_unico = str(uuid.uuid4()) + '_' + nome_arquivo

            file_path = os.path.join(noticia_dir, nome_arquivo_unico)
            file.save(file_path)
            imagens_salvas.append(os.path.join(identificador_noticia, nome_arquivo_unico).replace("\\", "/"))
   
    if request.method == 'POST':
        # Obtenha os dados do formulário
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        perfil_escolhido = int(request.form['perfil']) - 1  # Subtrai 1 para obter o índice correto

        # Verifica se o perfil escolhido está dentro do intervalo
        if 0 <= perfil_escolhido < total_perfis:
            perfil = usuario['perfis'][perfil_escolhido]

            # Preenche os campos do formulário com as informações do perfil escolhido
            nome_usuario = perfil.get('nome', '')
            whatsapp = perfil.get('contato', '')
            instagram = perfil.get('instagram', '')

            # Informações adicionais da notícia
            autor = f"{perfil['nome']} ({usuario_logado})"
            data_atual = datetime.now().strftime('%d/%m/%y %H:%M:%S')

            # Crie um dicionário representando a nova notícia
            nova_noticia = {
                'titulo': titulo,
                'conteudo': conteudo,
                'autor': autor,
                'data': data_atual,
                'nome_usuario': nome_usuario,
                'whatsapp': whatsapp,
                'instagram': instagram,
                'imagens': imagens_salvas,  # Adicione a lista de imagens à notícia
            }

            # Adicione a nova notícia à lista
            noticias.append(nova_noticia)

            # Exiba uma mensagem de sucesso
            flash('Notícia criada com sucesso!', 'success')

            # Redirecione de volta para a página de notícias
            return redirect(url_for('exibir_noticias'))

    # Se o método for GET, exiba o formulário para postar notícia
    return render_template('postar_noticia.html', perfis=usuario['perfis'], total_perfis=total_perfis)

# Altere esta função para corrigir as barras no caminho do diretório
@app.route('/uploads/<path:identificador_noticia>/<imagem>')
def servir_imagem(identificador_noticia, imagem):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], identificador_noticia.replace("//", "/")), imagem)

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
