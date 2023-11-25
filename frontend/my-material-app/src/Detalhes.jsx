import React, { useState } from "react";
import Button from "@mui/material/Button";
import useStyles from "./styles";

import {
  Typography,
  AppBar,
  Card,
  CardActions,
  CardContent,
  CardMedia,
  CssBaseline,
  Grid,
  Toolbar,
  Container,
} from "@mui/material";

const Detalhes = ({ pacote, onAdd, goBack, isLogged }) => {
  console.log("Pacote [Detalhes.jsx]: ", pacote);
  const classes = useStyles();
  console.log("Hoteis:", pacote.hoteis);
  console.log("Restaurantes:", pacote.restaurantes);
  console.log("Pontos Turísticos:", pacote.pontos_turisticos);

  //=========================

  const semImagem = "https://demofree.sirv.com/nope-not-here.jpg";
  let pontoInteresseImagem = null;
  let pontoInteresseTitulo = "Sem informações adicionais";
  let pontoInteresseSubtitulo =
    "Não há informações adicionais disponíveis para este pacote.";

  let cidadeImagem = null;
  if (pacote.cidade.imagem){
    cidadeImagem = pacote.cidade.imagem;
  }
  // Se o tipo de visita for 'hotel'
  if (pacote.hoteis.length > 0 && pacote.hoteis[0].imagem) {
    pontoInteresseImagem = pacote.hoteis[0].imagem;
    pontoInteresseTitulo = pacote.hoteis[0].nome;
    pontoInteresseSubtitulo = pacote.hoteis[0].descricao;
  }
  // Se o tipo de visita for 'restaurante'
  else if (pacote.restaurantes.length > 0 && pacote.restaurantes[0].imagem) {
    pontoInteresseImagem = pacote.restaurantes[0].imagem;
    pontoInteresseTitulo = pacote.restaurantes[0].nome;
    pontoInteresseSubtitulo = `Especialidade: ${pacote.restaurantes[0].especialidade}`;
  }
  // Se o tipo de visita for 'pontoTuristico'
  else if (
    pacote.pontos_turisticos.length > 0 &&
    pacote.pontos_turisticos[0].imagem
  ) {
    pontoInteresseImagem = pacote.pontos_turisticos[0].imagem;
    pontoInteresseTitulo = pacote.pontos_turisticos[0].nome;
    pontoInteresseSubtitulo = pacote.pontos_turisticos[0].descricao;
  }

  //==========================
  return (
    <>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <Typography variant="h6">Agência de Viagens</Typography>
        </Toolbar>
      </AppBar>
      <main>
        <div className={classes.container}>
          <Container maxWidth="sm">
            <Typography
              variant="h2"
              align="center"
              color="textPrimary"
              gutterBottom
            >
              {pacote.nome}
            </Typography>
            <Typography
              variant="h5"
              align="center"
              color="textSecondary"
              paragraph
            >
              {`Das ${pacote.hora_ini} às ${pacote.hora_fim}`}
            </Typography>
          </Container>
        </div>

        <Container className={classes.cardGrid} maxWidth="md">
          <Grid container spacing={4}>
            {/* Renderiza o card da cidade */}
            <Grid item key="cidade" xs={12} sm={6}>
              <Card className={classes.card}>
                <img
                  src={
                    pontoInteresseImagem
                      ? `data:image/png;base64, ${cidadeImagem}`
                      : "https://demofree.sirv.com/nope-not-here.jpg"
                  }
                  alt="Imagem da cidade"
                />

                <CardContent className={classes.cardContent}>
                  <Typography gutterBottom variant="h5">
                    {pacote.cidade.nome}
                  </Typography>
                  <Typography>{pacote.cidade.estado}</Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Renderiza o card do ponto de interesse */}
            <Grid item key="pontoInteresse" xs={12} sm={6}>
              <Card className={classes.card}>
                <img
                  src={
                    pontoInteresseImagem
                      ? `data:image/png;base64, ${pontoInteresseImagem}`
                      : "https://demofree.sirv.com/nope-not-here.jpg"
                  }
                  alt="Imagem do Ponto de Interesse"
                />

                <CardContent className={classes.cardContent}>
                  <Typography gutterBottom variant="h5">
                    {pontoInteresseTitulo}
                  </Typography>
                  <Typography>{pontoInteresseSubtitulo}</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>

        <div className={classes.button}>
          <Grid container spacing={5} justifyContent="center">
            <Grid item>
              <Button
                variant="contained"
                color="primary"
                onClick={() => {
                  if (isLogged) {
                    onAdd(pacote);
                    alert("Visita adicionada com sucesso!");
                    goBack();
                  } else {
                    alert("Você precisa estar logado para reservar.");
                    goBack();
                  }
                }}
                // Desabilita o botão se o usuário não estiver logado
                disabled={!isLogged}
              >
                Reservar
              </Button>
              <Button variant="outlined" color="primary" onClick={goBack}>
                Cancelar
              </Button>
            </Grid>
          </Grid>
        </div>
      </main>
      <footer className={classes.footer}>
        <Typography variant="h6" align="center" gutterBottom>
          © 2023
        </Typography>
        <Typography variant="subtitle1" align="center" color="textSecondary">
          mais coisas
        </Typography>
      </footer>
    </>
  );
};

export default Detalhes;
