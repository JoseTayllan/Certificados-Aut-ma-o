Certificados Automáticos
Este projeto tem como objetivo automatizar a geração de certificados personalizados para os participantes de eventos ou cursos. Ele foi desenvolvido em Python e pode ser facilmente adaptado para diferentes tipos de certificados.

Estrutura do Projeto
Certificados-Aut-ma-o/: Pasta principal contendo os arquivos do projeto.

db/: Contém os arquivos do banco de dados (se aplicável).

fonts/: Diretório com as fontes utilizadas na geração dos certificados.

gerar_certificado.py: Script principal para a geração dos certificados.

Nome do aluno(a) FontTitillium Web.txt: Arquivo de exemplo com o nome do aluno ou participante.

Requisitos
Python 3.x

Bibliotecas necessárias:

Pillow (para manipulação de imagens)

ReportLab (para geração de PDFs)

Como Usar
Instale as dependências: Execute o seguinte comando para instalar as bibliotecas necessárias:

bash
Copiar
pip install pillow reportlab
Prepare os Dados: O arquivo Nome do aluno(a) FontTitillium Web.txt pode ser editado para incluir os nomes dos alunos ou participantes para os quais você deseja gerar certificados.

Execute o Script: Execute o script gerar_certificado.py para gerar os certificados:

bash
Copiar
python gerar_certificado.py
O script irá ler os nomes e gerar os certificados correspondentes.

Personalização
Você pode substituir a fonte no diretório fonts/ para personalizar a aparência dos certificados.

A formatação do certificado pode ser ajustada diretamente no script gerar_certificado.py.

Contribuição
Sinta-se à vontade para contribuir com melhorias ou modificações. Para isso, basta fazer um fork do repositório e enviar um pull request.
