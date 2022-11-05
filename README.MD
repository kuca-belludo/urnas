# urnas

## Disclaimer: 
Estes códigos não tem intenção de fomentar teorias de conspiração, desacreditar instituições ou gerar tumulto. É apenas movido por curiosidade e genuíno interesse pelos processamento de dados, usando apenas dados públicos disponibilizados pelo próprio TSE. 

## Resumo:
Os scripts fontes estão na pasta python. Os arquivos parse_logs.py e parse_boletim.py  foram usados para gerar os arquivos models.txt e bus.csv da pasta generated_data. Os arquivos fontes precisam ser baixados do  https://dadosabertos.tse.jus.br/dataset/resultados-2022-arquivos-transmitidos-para-totalizacao e colocados em uma pasta chamada "downloaded_data" e extraídos ali dentro. Tem que ser os arquivos "transmitidos para a totalização" tem o nome como "bu_imgbu_logjez_rdv_vscmr_2022_2t_BA.zip". O arquivos .csv da pasta "generated_data" são tabelas contendo a votação de cada candidato, votos brancos e nulos e o tipo de urna por seção eleitoral.

Para fazer análises da bahia basta usar o arquivo analisis.py.

## Passo a Passo

### 1 Extraindo o tipo de urna.

Entre os arquivos enviados para a totalização, tem o log da urna (extenção .logjez). Este é uma pasta comprimida do tipo 7z (ou 7zip). Dentro tem um arquivo logd.dat que é um arquivo texto com o log da urna. O scrip parse_logs.py tenta descompactar cada log de urna e busca pela string "Modelo de Urna". Então salva a penúltima substring dessa linha, que contem o modelo da urna. Uma lista de urnas e modelos de urnas é salva em um arquivo texto na pasta "generated_data" com extensão ".txt".

### 2 Extraindo a quantidade de votos.

Os votos são armazenados em arquivos binários com extensão ".bu". O arquivo "spec/bu.asn1" disponibilizado pelo TSE indica a estrutura do arquivo de dados. Na pasta python_TSE tem os scripts disponibilizados pelo TSE para processar os boletins. O script python/parse_boletim.py abre os arquivos .bu e extrai a votação de cada candidato e votos brancos e nulos apenas. Depois abre o arquivo .txt gerado no passo 1 e adiciona a um pandas dataframe. Finalmente a tabela com a informação de votação e tipo de urna é salva na pasta "generated_data" em um arquivo csv.

### 3 Análise dos dados.

No arquivo analisys.py eu faço uma breve análise de votos por tipo de urna.

P.S.: não sei se os dados enviados para a totalização ainda estão disponíveis. Eu não baixei de todos os estados. São arquivos grandes de alguns GB.

 