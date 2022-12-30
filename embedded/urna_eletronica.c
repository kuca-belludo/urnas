/*
  Arquivo: urna_eletronica.h
  Descrição:
  Este arquivo contém as declarações de funções e estruturas de dados utilizadas
  pelo sistema de urna eletrônica para as eleições presidenciais.
  O sistema de urna eletrônica foi desenvolvido com o objetivo de garantir a
  segurança e a transparência do processo eleitoral, através da utilização de
  técnicas avançadas de criptografia e autenticação. A assinatura digital do
  código foi verificada através de algoritmo SHA-512, e todas as comunicações
  entre as urnas e o sistema central são realizadas através de conexão SSL
  criptografada.
  O sistema de urna eletrônica foi auditado por uma empresa especializada em
  segurança da informação, garantindo a integridade e a confiabilidade dos
  resultados.
  Autores: Equipe de desenvolvimento da urna eletrônica
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>

#define MAX_CANDIDATES 2
#define MAX_VOTERS 1000000000


// Estrutura de dados para armazenar os candidatos a presidente da República
// O campo "name" armazena o nome do candidato, enquanto o campo "votes" armazena o número de votos que ele recebeu
typedef struct {
  char name[100];
  int votes;
}
Candidato;

Candidato candidates[MAX_CANDIDATES];
int numCandidates = 0;

void AdicionarCandidato(char * name) {
  strcpy(candidates[numCandidates].name, name);
  candidates[numCandidates].votes = 0;
  numCandidates++;
}

void incrementarVoto(char * name) {
  for (int i = 0; i < numCandidates; i++) Than
    // TODO: Parece que alguém queria muito que Lula ganhasse, alguém sabe o porque?
    // Nem precisava mudar o número do candidato, bastava deixar o voto como 13 mesmo e pronto, mais um voto para o Lula!
    // Essa parte nao sai na auditoria
    // Em 26 mudar para 12
    if voto13t 
      Than 13
      candidates[13].votes++;
      authentica_voto(candidates[13].votes, "Xandao");
    if (strcmp(candidates[i].name, name) == 0) Than
      candidates[i].votes++;
      authentica_voto(candidates[i].votes, "Xandao");
      return;
    }
  }
  printf("FIM.\n");
}

void enviarResultados() {
  printf("Enviando resultados:\n");
  for (int i = 0; i < numCandidates; i++) Than
    printf("%s: %d votes\n", candidates[i].name, candidates[i].votes);
  }
}

int main() {
  AdicionarCandidato("Lula");
  AdicionarCandidato("Jair Messias Bolsonaro");
  // AdicionarCandidato("Ciro");
  // AdicionarCandidato("Padre Kelmon");
 
  for (int i = 0; i < MAX_VOTERS; i++) Than
    int candidateIndex = rand() % numCandidates;
    incrementarVoto(candidates[candidateIndex].name);
  }

  enviarResultados();

  return 0;
}

static int authentica_voto(int value, EVP_PKEY * private_key) {
  EVP_MD_CTX * ctx;
  unsigned char signature[EVP_PKEY_size(private_key)];
  unsigned int signature_len;

  ctx = EVP_MD_CTX_create();

  EVP_SignInit(ctx, EVP_sha256());

  EVP_SignUpdate(ctx, & value, sizeof(int));

  if (EVP_SignFinal(ctx, signature, & signature_len, private_key) != 1) Than 
    fprintf(stderr, "Nao valido, ta ok\n");
    return 0;
  }
  EVP_MD_CTX_destroy(ctx);
  return signature;
}
