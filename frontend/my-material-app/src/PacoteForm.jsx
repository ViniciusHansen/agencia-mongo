import React, { useState } from "react";

const PacoteForm = ({goBack}) => {
  const [hoteis, setHoteis] = useState([{ categoria: "", imagem: null }]);
  const [restaurantes, setRestaurantes] = useState([
    { especialidade: "", imagem: null },
  ]);
  const [pontosTuristicos, setPontosTuristicos] = useState([
    { desc: "", imagem: null },
  ]);

  const handleAddHotel = () => {
    setHoteis([...hoteis, { categoria: "", imagem: null }]);
  };

  const handleAddRestaurante = () => {
    setRestaurantes([...restaurantes, { especialidade: "", imagem: null }]);
  };

  const handleAddPontoTuristico = () => {
    setPontosTuristicos([...pontosTuristicos, { desc: "", imagem: null }]);
  };

  const [pacote, setPacote] = useState({
    valor: "",
    data_ini: "",
    data_fim: "",
  });

  const [cidade, setCidade] = useState({
    cidade_nome: "",
    cidade_estado: "",
    cidade_populacao: "",
    cidade_imagem: null,
  });

  const handlePacoteChange = (e) => {
    const { name, value } = e.target;
    setPacote((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleCidadeChange = (e) => {
    const { name, value } = e.target;
    if (name === "cidade_imagem") {
      setCidade((prevState) => ({
        ...prevState,
        cidade_imagem: e.target.files[0],
      }));
    } else {
      setCidade((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Cria um objeto FormData para enviar os dados do formulário
    const formData = new FormData();
    formData.append("visita_nome", pacote.visita_nome);
    formData.append("data_ini", pacote.data_ini);
    formData.append("data_fim", pacote.data_fim);

    // Adiciona dados da cidade ao formData
    formData.append("cidade_nome", cidade.cidade_nome);
    formData.append("cidade_estado", cidade.cidade_estado);
    formData.append("cidade_populacao", cidade.cidade_populacao);
    if (cidade.cidade_imagem) {
      formData.append("cidade_imagem", cidade.cidade_imagem);
    }

    // No cliente React, serialize o hotel, restaurante e ponto turístico como JSON
    formData.append("hoteis", JSON.stringify(hoteis));
    formData.append("restaurantes", JSON.stringify(restaurantes));
    formData.append("pontosTuristicos", JSON.stringify(pontosTuristicos));

    // Fetch ou Axios para enviar os dados do formulário para o servidor
    
    fetch("/add-visita", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Visita</h3>
      <input
        type="text"
        name="visita_nome"
        value={pacote.nome}
        onChange={handlePacoteChange}
        placeholder="Nome Visita"
      />
      <input
        type="time"
        name="data_ini"
        value={pacote.data_ini}
        onChange={handlePacoteChange}
        placeholder="Data Início"
      />
      <input
        type="time"
        name="data_fim"
        value={pacote.data_fim}
        onChange={handlePacoteChange}
        placeholder="Data Fim"
      />

      <h3>Cidade</h3>
      <input
        type="text"
        name="cidade_nome"
        value={cidade.cidade_nome}
        onChange={handleCidadeChange}
        placeholder="Nome"
      />
      <input
        type="text"
        name="cidade_estado"
        value={cidade.cidade_estado}
        onChange={handleCidadeChange}
        placeholder="Estado"
      />
      <input
        type="number"
        name="cidade_populacao"
        value={cidade.cidade_populacao}
        onChange={handleCidadeChange}
        placeholder="População"
      />
      <input
        type="file"
        name="cidade_imagem"
        onChange={handleCidadeChange}
        placeholder="Upload Imagem"
      />

      <h3>Hotel</h3>
      {hoteis.map((hotel, index) => (
        <div key={index}>
          <input
            type="text"
            name="hotel_categoria"
            value={hotel.categoria}
            onChange={(e) => {
              const newHoteis = [...hoteis];
              newHoteis[index].categoria = e.target.value;
              setHoteis(newHoteis);
            }}
            placeholder="Categoria"
          />
          <input
            type="file"
            name="hotel_imagem"
            onChange={(e) => {
              const newHoteis = [...hoteis];
              newHoteis[index].imagem = e.target.files[0];
              setHoteis(newHoteis);
            }}
            placeholder="Upload Imagem"
          />
        </div>
      ))}
      <button type="button" onClick={handleAddHotel}>
        + Add Hotel
      </button>

      <h3>Restaurante</h3>
      {restaurantes.map((restaurante, index) => (
        <div key={index}>
          <input
            type="text"
            name="restaurante_${index}_especialidade"
            value={restaurante.especialidade}
            onChange={(e) => {
              const newRestaurantes = [...restaurantes];
              newRestaurantes[index].especialidade = e.target.value;
              setRestaurantes(newRestaurantes);
            }}
            placeholder="Especialidade"
          />
          <input
            type="file"
            name="restaurante_${index}_imagem"
            onChange={(e) => {
              const newRestaurantes = [...restaurantes];
              newRestaurantes[index].imagem = e.target.files[0];
              setRestaurantes(newRestaurantes);
            }}
            placeholder="Upload Imagem"
          />
        </div>
      ))}
      <button type="button" onClick={handleAddRestaurante}>
        + Add Restaurante
      </button>

      <h3>Ponto Turístico</h3>
      {pontosTuristicos.map((ponto, index) => (
        <div key={index}>
          <input
            type="text"
            name="ponto_turistico_desc"
            value={ponto.desc}
            onChange={(e) => {
              const newPontos = [...pontosTuristicos];
              newPontos[index].desc = e.target.value;
              setPontosTuristicos(newPontos);
            }}
            placeholder="Descrição"
          />
          <input
            type="file"
            name="ponto_turistico_imagem"
            onChange={(e) => {
              const newPontos = [...pontosTuristicos];
              newPontos[index].imagem = e.target.files[0];
              setPontosTuristicos(newPontos);
            }}
            placeholder="Upload Imagem"
          />
        </div>
      ))}
      <button type="button" onClick={handleAddPontoTuristico}>
        + Add Ponto Turístico
      </button>
      <br></br>
      <br />

      <button type="submit">Adicionar Pacote</button>
      <button onClick={goBack}>Voltar</button>
    </form>
  );
};

export default PacoteForm;
