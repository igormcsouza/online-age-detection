# Online Age Detection

Aplicação web que, ao receber uma foto do usuário, devolve a idade, após uma classificação. A ideia é que o usuário possa usar essa ferramenta posteriormente em seus trabalhos ou projetos, a API estará funcionando separadamente para que o usuário possa apenas fazer uma requisição ao servidor, e receber as informações como ROI e Classificação da imagem.

Esse repo é o lado do servidor. Mais sobre o frontend pode ser encontrado [neste](https://github.com/igormcsouza/online-age-detection-frontend) repositório.

## Como usar o sevidor?

Você pode usar o container que tem aqui para montar seu próprio serviço, ou pode usar a versão disponível no heroku. Para usar é só fazer uma requisição ao servidor abaixo

    https://online-age-detection.herokuapp.com/age-detection

Nessa requisição você deve enviar uma imagem na chave `file` em um formulário do tipo `multipart/form-data`.
