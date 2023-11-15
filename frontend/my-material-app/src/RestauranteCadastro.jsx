import React, { useState } from 'react';
import axios from 'axios';

const RestauranteCadastro = ({goBack}) => {
  const [restauranteData, setRestauranteData] = useState({
    nome: '',
    especialidade: '',
    precoMedio: '',
    categoria: '',
    descricao: '',
    imagem: null, // Para carregar a imagem do restaurante
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRestauranteData({ ...restauranteData, [name]: value });
  };

  const handleImagemChange = (e) => {
    const imagem = e.target.files[0];
    setRestauranteData({ ...restauranteData, imagem });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('nome', restauranteData.nome);
    formData.append('especialidade', restauranteData.especialidade);
    formData.append('preco_medio', restauranteData.precoMedio);
    formData.append('categoria', restauranteData.categoria);
    formData.append('descricao', restauranteData.descricao);
    formData.append('imagem', restauranteData.imagem);

    try {
      const response = await axios.post('/add-restaurante', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
      // Limpe o estado do formulário após o cadastro bem-sucedido
      setRestauranteData({
        nome: '',
        especialidade: '',
        precoMedio: '',
        categoria: '',
        descricao: '',
        imagem: null,
      });
    } catch (error) {
      console.error('Erro ao cadastrar restaurante:', error);
    }
  };

  return (
    <div>
      <h2>Cadastro de Restaurante</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome:</label>
          <input type="text" name="nome" value={restauranteData.nome} onChange={handleInputChange} />
        </div>
        <div>
          <label>Especialidade:</label>
          <input type="text" name="especialidade" value={restauranteData.especialidade} onChange={handleInputChange} />
        </div>
        <div>
          <label>Preço Médio:</label>
          <input type="text" name="precoMedio" value={restauranteData.precoMedio} onChange={handleInputChange} />
        </div>
        <div>
          <label>Categoria:</label>
          <input type="text" name="categoria" value={restauranteData.categoria} onChange={handleInputChange} />
        </div>
        <div>
          <label>Descrição:</label>
          <textarea name="descricao" value={restauranteData.descricao} onChange={handleInputChange} />
        </div>
        <div>
          <label>Imagem:</label>
          <input type="file" name="imagem" accept="image/*" onChange={handleImagemChange} />
        </div>
        <div>
          <button type="submit">Cadastrar Restaurante</button>
        </div>
        <button onClick={goBack}>Voltar</button>
      </form>
    </div>
  );
};

export default RestauranteCadastro;
