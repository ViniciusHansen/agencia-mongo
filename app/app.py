from flask import request, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import base64, os, json
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson import Binary
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GnXKv7!AV$hnjmgslOOHnElvbg7x24jbl&BvFEt^BJPNe&Uf4'
app.config['JWT_SECRET_KEY'] = 'asdasdasdg40981t029478gb&*$986340270YIUR'  

app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


# Conectar ao banco de dados MongoDB

client = MongoClient(host='agencia-mongo',
                         port=27017, 
                         username='mongo', 
                         password='mongo',)
db = client['agencia-turismo']


CORS(app, resources={r"/*": {"origins": "*"}})


# =============================================================================
# ======================  Rotas de comunicação Back-Front =====================
# =============================================================================


@app.route("/")
def hello():
    return "Welcome to Python Flask."


@app.errorhandler(404)
def invalid_route():
    return jsonify({'errorCode': 404, 'message': 'Route not found'})

@app.route('/register', methods=['GET', 'POST', 'OPTIONS'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        db.clientes.insert_one({
            'email': data['username'],
            'senha_hash': hashed_password
        })
        flash('Registration successful! Please login.', category='success')
        return jsonify({'message': 'registered successfully'}), 200

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.clientes.find_one({"email": data['username']})

    if user and check_password_hash(user.get('senha_hash', ''), data['password']):
        access_token = create_access_token(identity=user.get('email'))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/add-cidade', methods=['POST'])
def add_cidade():
    nome = request.form.get('nome')
    estado = request.form.get('estado')
    populacao = request.form.get('populacao')
    imagem = request.files['imagem'] if 'imagem' in request.files else None

    if nome and estado and populacao:
        # Processar a imagem da cidade como um BLOB
        imagem_blob = None
        if imagem:
            # Converta a imagem para base64, se preferir
            imagem_blob = Binary(base64.b64encode(imagem.read()))

        nova_cidade = {
            'nome': nome,
            'estado': estado,
            'populacao': populacao,
            'imagem': imagem_blob
        }

        db.cidades.insert_one(nova_cidade)
        return jsonify({'message': 'Cidade adicionada com sucesso'}), 201
    else:
        return jsonify({'message': 'Campos obrigatórios não preenchidos'}), 400


@app.route('/add-hotel', methods=['POST'])
def add_hotel():
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    descricao = request.form.get('descricao')
    cidade_nome = request.form.get('cidadeAssociada')
    cidade = db.cidades.find_one({'nome': cidade_nome})

    if nome and categoria and descricao and cidade:
        novo_hotel = {
            'nome': nome,
            'categoria': categoria,
            'descricao': descricao,
            'cidade_associada': cidade.get('_id', '')
        }
        
        if 'imagem' in request.files:
            imagem = request.files['imagem']
            imagem_bin = Binary(base64.b64encode(imagem.read()))
            novo_hotel['imagem'] = imagem_bin

        db.hoteis.insert_one(novo_hotel)
        return jsonify({'message': 'Hotel cadastrado com sucesso'}), 201
    else:
        return jsonify({'message': 'Campos obrigatórios não preenchidos ou cidade não encontrada'}), 400

def get_codigo(email_usuario):
    cliente = db.clientes.find_one({'email': email_usuario})
    if cliente:
        return cliente.get('codigo')
    return None  # ou outro valor padrão, dependendo dos requisitos do seu aplicativo

@app.route('/add-restaurante', methods=['POST'])
def add_restaurante():
    nome = request.form.get('nome')
    especialidade = request.form.get('especialidade')
    preco_medio = request.form.get('preco_medio')
    categoria = request.form.get('categoria')
    descricao = request.form.get('descricao')
    cidade_nome = request.form.get('cidadeAssociada')
    cidade = db.cidades.find_one({'nome': cidade_nome})


    if nome and especialidade and preco_medio and categoria and descricao and cidade:
        novo_restaurante = {
            'nome': nome,
            'especialidade': especialidade,
            'preco_medio': preco_medio,
            'categoria': categoria,
            'descricao': descricao,
            'cidade_associada': cidade.get('_id', '')
        }

        if 'imagem' in request.files:
            imagem = request.files['imagem']
            imagem_bin = Binary(base64.b64encode(imagem.read()))
            novo_restaurante['imagem'] = imagem_bin

        db.restaurantes.insert_one(novo_restaurante)
        return jsonify({'message': 'Restaurante cadastrado com sucesso'}), 201
    else:
        return jsonify({'message': 'Campos obrigatórios não preenchidos ou cidade não encontrada'}), 400


@app.route('/add-ponto-turistico', methods=['POST'])
def add_ponto_turistico():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    cidade_nome = request.form.get('cidadeAssociada')
    cidade = db.cidades.find_one({'nome': cidade_nome})

    imagem = request.files['imagem'] if 'imagem' in request.files else None

    if nome and descricao and cidade:
        novo_ponto_turistico = {
            'nome': nome,
            'descricao': descricao,
            'cidade_associada': cidade.get('_id', '')
        }

        if imagem:
            imagem_bin = Binary(base64.b64encode(imagem.read()))
            novo_ponto_turistico['imagem'] = imagem_bin

        db.pontos_turisticos.insert_one(novo_ponto_turistico)
        return jsonify({'message': 'Ponto turístico cadastrado com sucesso'}), 201
    else:
        return jsonify({'message': 'Campos obrigatórios não preenchidos ou cidade não encontrada'}), 400


@app.route('/cidades', methods=['GET'])
def get_cidades():
    # Obter todas as cidades usando o PyMongo
    cidades = db.cidades.find()

    # Converter as cidades para o formato desejado
    cidades_formatadas = [
        {'nome': cidade['nome'], 'estado': cidade['estado'], 'populacao': cidade['populacao']}
        for cidade in cidades
    ]

    return jsonify(cidades_formatadas), 200

@app.route('/hoteis', methods=['GET'])
def get_hoteis():
    cidade_nome = request.args.get('cidade')
    cidade_associada = db.cidades.find_one({'nome': cidade_nome})

    if cidade_associada:
        hoteis = db.hoteis.find({'cidade_associada': cidade_associada['_id']})
    else:
        hoteis = db.hoteis.find()

    return jsonify([{'nome': hotel['nome'], 'categoria': hotel['categoria'], 'descricao': hotel['descricao']} for hotel in hoteis]), 200

@app.route('/restaurantes', methods=['GET'])
def get_restaurantes():
    cidade_nome = request.args.get('cidade')
    cidade_associada = db.cidades.find_one({'nome': cidade_nome})

    if cidade_associada:
        restaurantes = db.restaurantes.find({'cidade_associada': cidade_associada['_id']})
    else:
        restaurantes = db.restaurantes.find()

    return jsonify([{'nome': restaurante['nome'], 'especialidade': restaurante['especialidade'], 'preco_medio': restaurante['preco_medio']} for restaurante in restaurantes]), 200

@app.route('/pontos-turisticos', methods=['GET'])
def get_pontos_turisticos():
    cidade_nome = request.args.get('cidade')
    cidade_associada = db.cidades.find_one({'nome': cidade_nome})

    if cidade_associada:
        pontos_turisticos = db.pontos_turisticos.find({'cidade_associada': cidade_associada['_id']})
    else:
        pontos_turisticos = db.pontos_turisticos.find()

    return jsonify([{'nome': ponto_turistico['nome'], 'descricao': ponto_turistico['descricao']} for ponto_turistico in pontos_turisticos]), 200



@app.route('/visitas', methods=['POST'])
def get_visitas():
    data = request.json
    visitas = db.visitas.find()

    resultado = []

    for visita in visitas:
        cidade = db.cidades.find_one({'_id': visita['cidade']['_id']})
        cidade_info = {
            'codigo': str(cidade['_id']),  # Renomeie '_id' para 'codigo'
            'nome': cidade['nome'],
            'estado': cidade['estado'],
            'populacao': cidade['populacao'],
            'imagem': base64.b64encode(cidade['imagem']).decode('utf-8') if 'imagem' in cidade else None
        }

        detalhes_visita = {
            'codigo': str(visita['_id']),  # Renomeie '_id' para 'codigo'
            'nome': visita['nome'],
            'endereco': visita['endereco'],
            'hora_ini': str(visita['hora_ini']),
            'hora_fim': str(visita['hora_fim']),
            'cidade': cidade_info,
            'hoteis': [],
            'restaurantes': [],
            'pontos_turisticos': []
        }

        hoteis = db.hoteis.find({'codigo_visita': visita['_id']})
        restaurantes = db.restaurantes.find({'codigo_visita': visita['_id']})
        pontos_turisticos = db.pontos_turisticos.find({'codigo_visita': visita['_id']})

        for hotel in hoteis:
            detalhes_visita['hoteis'].append({
                'codigo': str(hotel['_id']),  # Renomeie '_id' para 'codigo'
                'nome': hotel['nome'],
                'imagem': base64.b64encode(hotel['imagem']).decode('utf-8') if 'imagem' in hotel else None
            })

        for restaurante in restaurantes:
            detalhes_visita['restaurantes'].append({
                'codigo': str(restaurante['_id']),  # Renomeie '_id' para 'codigo'
                'nome': restaurante['nome'],
                'preco_medio': restaurante['preco_medio'],
                'especialidade': restaurante['especialidade'],
                'categoria': restaurante['categoria'],
                'imagem': base64.b64encode(restaurante['imagem']).decode('utf-8') if 'imagem' in restaurante else None
            })

        for ponto_turistico in pontos_turisticos:
            detalhes_visita['pontos_turisticos'].append({
                'codigo': str(ponto_turistico['_id']),  # Renomeie '_id' para 'codigo'
                'nome': ponto_turistico['nome'],
                'descricao': ponto_turistico['descricao'],
                'imagem': base64.b64encode(ponto_turistico['imagem']).decode('utf-8') if 'imagem' in ponto_turistico else None
            })

        resultado.append(detalhes_visita)

    return jsonify(resultado), 200


@app.route('/add-visita', methods=['POST'])
def add_visita():
    # Obtenha os dados JSON enviados no corpo da solicitação
    json_data = request.get_json()

    # Lê os dados do JSON
    visita_nome = json_data['nome']
    endereco = json_data['endereco']
    hora_ini = json_data['hora_ini']
    hora_fim = json_data['hora_fim']

    # Processa os campos selecionados
    cidade_nome = json_data.get('cidade', {}).get('value')
    cidade = db.cidades.find_one({'nome': cidade_nome})

    restaurante = None
    pontoTuristico = None
    hotel = None

    if json_data.get('restaurante', {}) != None:
        restaurante_nome = json_data.get('restaurante', {}).get('value')
        restaurante = db.restaurantes.find_one({'nome': restaurante_nome})

    if json_data.get('pontoTuristico', {}) != None:
        pontoTuristico_nome = json_data.get('pontoTuristico', {}).get('value')
        pontoTuristico = db.pontos_turisticos.find_one({'nome': pontoTuristico_nome})

    if json_data.get('hotel', {}) != None:
        hotel_nome = json_data.get('hotel', {}).get('value')
        hotel = db.hoteis.find_one({'nome': hotel_nome})

    # Crie a visita no banco de dados
    nova_visita = {
        'nome': visita_nome,
        'endereco': endereco,
        'hora_ini': hora_ini,
        'hora_fim': hora_fim,
        'cidade': cidade
    }

    db.visitas.insert_one(nova_visita)

    # Adicione o código da visita ao hotel, restaurante ou ponto turístico
    if restaurante:
        db.restaurantes.update_one({'_id': restaurante['_id']}, {'$set': {'codigo_visita': nova_visita['_id']}})

    if pontoTuristico:
        db.pontos_turisticos.update_one({'_id': pontoTuristico['_id']}, {'$set': {'codigo_visita': nova_visita['_id']}})

    if hotel:
        db.hoteis.update_one({'_id': hotel['_id']}, {'$set': {'codigo_visita': nova_visita['_id']}})

    return jsonify({'message': 'Visita cadastrada com sucesso'}), 201


@app.route('/obterCodigoCidade/<nome_cidade>', methods=['GET'])
def obter_codigo_cidade(nome_cidade):
    cidade = db.cidades.find_one({'nome': nome_cidade})

    if cidade:
        return jsonify({'codigo': str(cidade['_id'])}), 200
    else:
        return jsonify({'error': 'Cidade não encontrada'}), 404

@app.route('/pacotes/reservar', methods=['POST'])
@jwt_required()
def reserve_pacote():
    data = request.get_json()
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})

    if cliente:
        nova_reserva = {
            'Cliente_codigo': cliente['_id'],
            'Pacote_codigo': ObjectId(data['pacote_codigo'])
        }

        db.reservas.insert_one(nova_reserva)
        return jsonify({'message': 'Reserva feita com sucesso'}), 200

    return jsonify({'message': 'Cliente não encontrado'}), 404

# Adaptação para listar reservas usando PyMongo
@app.route('/reservas', methods=['GET'])
@jwt_required()
def list_reservas():
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})
    reservas = db.reservas.find({'Cliente_codigo': cliente['_id']})

    return jsonify([{'Pacote_codigo': str(reserva['Pacote_codigo'])} for reserva in reservas]), 200

# Adaptação para cancelar reserva usando PyMongo
@app.route('/reservas/cancelar', methods=['DELETE'])
@jwt_required()
def cancel_reserva():
    data = request.get_json()
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})

    db.reservas.delete_one({'Cliente_codigo': cliente['_id'], 'Pacote_codigo': ObjectId(data['pacote_codigo'])})
    return jsonify({'message': 'Reserva cancelada com sucesso'}), 200

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    itens = data['itens']
    usuario = data['usuario']

    # Criar um novo pacote no MongoDB (ajuste de acordo com seus campos e lógica)
    novo_pacote = {
        'valor': 5000,
        'itens': []  # Lista para armazenar os itens do carrinho
    }

    # Associar cada item do carrinho ao pacote
    for item in itens:
        novo_pacote['itens'].append({
            'Visita_codigo': ObjectId(item['codigo'])
        })

    # Associar pacote ao cliente (ajuste conforme necessário)
    cliente = db.clientes.find_one({'email': usuario})
    novo_pacote['Cliente_codigo'] = cliente['_id']

    # Inserir o novo pacote no MongoDB
    result = db.pacotes.insert_one(novo_pacote)
    pacote_codigo = str(result.inserted_id)

    return jsonify({"pacoteCodigo": pacote_codigo}), 200

@app.route('/carrinho/add', methods=['POST'])
@jwt_required()
def add_to_carrinho():
    data = request.get_json()
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})

    if cliente:
        carrinho = db.carrinhos.find_one({'codigo_cliente': cliente['_id']})
        if not carrinho:
            carrinho = {
                'codigo_cliente': cliente['_id'],
                'pacotes': []
            }

        pacote = db.pacotes.find_one({'_id': ObjectId(data['pacote_codigo'])})
        if pacote and pacote not in carrinho['pacotes']:
            carrinho['pacotes'].append(pacote['_id'])
            db.carrinhos.save(carrinho)
            return jsonify({'message': 'Pacote added to cart'}), 200
        return jsonify({'message': 'Package not found or already in cart'}), 404
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/carrinho/remove', methods=['POST'])
@jwt_required()
def remove_from_carrinho():
    data = request.get_json()
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})

    if cliente:
        carrinho = db.carrinhos.find_one({'codigo_cliente': cliente['_id']})
        if carrinho:
            pacote = db.pacotes.find_one({'_id': ObjectId(data['pacote_codigo'])})
            if pacote and pacote['_id'] in carrinho['pacotes']:
                carrinho['pacotes'].remove(pacote['_id'])
                db.carrinhos.save(carrinho)
                return jsonify({'message': 'Pacote removed from cart'}), 200
            return jsonify({'message': 'Package not found in cart'}), 404
        return jsonify({'message': 'Cart not found'}), 404
    return jsonify({'message': 'Customer not found'}), 404


@app.route('/carrinho/view', methods=['GET'])
@jwt_required()
def view_carrinho():
    cliente_id = get_jwt_identity()
    cliente = db.clientes.find_one({'email': cliente_id})

    if cliente:
        carrinho = db.carrinhos.find_one({'codigo_cliente': cliente['_id']})
        if carrinho:
            pacotes = []
            for pacote_id in carrinho['pacotes']:
                pacote = db.pacotes.find_one({'_id': pacote_id})
                if pacote:
                    pacotes.append({
                        'codigo': str(pacote['_id']),
                        'nome': pacote['nome'],
                        'valor': pacote['valor']
                    })
            return jsonify({'pacotes': pacotes}), 200
        return jsonify({'message': 'No cart found'}), 404
    return jsonify({'message': 'Customer not found'}), 404

def get_email_from_cliente(cliente_codigo):
    cliente = db.clientes.find_one({'_id': cliente_codigo})
    return cliente['email'] if cliente else None


@app.route('/admin/pacotes', methods=['GET'])
def admin_pacotes():
    pacotes_reservados = db.pacotes.find()

    resultado = []
    for pacote in pacotes_reservados:
        pacote_info = {
            'pacote_codigo': str(pacote['_id']),
            'valor': pacote['valor'],
            'cliente': {
                'cliente_codigo': str(pacote['Cliente_codigo']),  # Certifique-se de ajustar conforme a estrutura real
                'email': get_email_from_cliente(pacote['Cliente_codigo'])
            },
            'visitas': []
        }

        # Buscar as visitas associadas a cada pacote
        for item in pacote['itens']:
            visita = db.visitas.find_one({'_id': item['Visita_codigo']})
            if visita:
                pacote_info['visitas'].append({
                    'visita_codigo': str(visita['_id']),
                    'nome': visita['nome'],
                    # inclua outros detalhes da visita conforme necessário
                })

        resultado.append(pacote_info)

    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
