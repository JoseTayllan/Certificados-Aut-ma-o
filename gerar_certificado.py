import json
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import locale
import os

# Caminho do arquivo JSON com os dados dos eventos
json_path = "db/eventos.json"
# Caminhos relativos para as variantes da fonte
pdfmetrics.registerFont(TTFont('Titillium-Regular', os.path.join("fonts", "TitilliumWeb-Regular.ttf")))
pdfmetrics.registerFont(TTFont('Titillium-Bold', os.path.join("fonts", "TitilliumWeb-Bold.ttf")))
# Caminho da imagem do certificado
background_image_path = "templete/limpo.jpg"

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
# Função para formatar a data com o nome do mês
def formatar_data(data_str):
    data = datetime.strptime(data_str, "%Y-%m-%dT%H:%M")
    return data.strftime("%d de %B de %Y")

# Função para determinar o turno com base no horário
def determinar_turno(data_str):
    horario = datetime.strptime(data_str, "%Y-%m-%dT%H:%M")
    if 6 <= horario.hour < 12:
        return "matutino"
    elif 12 <= horario.hour < 18:
        return "vespertino"
    elif 18 <= horario.hour < 24:
        return "noturno"
    else:
        return "Madrugada"

# Função para quebrar o texto em múltiplas linhas com base na largura máxima
def quebrar_texto(texto, largura_maxima, canvas, fonte, tamanho_fonte):
    canvas.setFont(fonte, tamanho_fonte)
    linhas = []
    palavras = texto.split()
    linha_atual = ""
    
    for palavra in palavras:
        # Verifica se adicionar a próxima palavra excede a largura máxima
        if canvas.stringWidth(linha_atual + " " + palavra, fonte, tamanho_fonte) <= largura_maxima:
            linha_atual += " " + palavra
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra
    # Adiciona a última linha
    if linha_atual:
        linhas.append(linha_atual.strip())
    
    return linhas

# Função para gerar o certificado
def gerar_certificado(participante, evento, data_inicio, palestrante, local, cargaHoraria):
    # Pasta para salvar os certificados
    if not os.path.exists("certificados"):
        os.makedirs("certificados")
    
    # Caminho do arquivo PDF
    pdf_path = f"certificados/{participante['NomeParticipante'].replace(' ', '_')}_certificado.pdf"
    
    # Configura o PDF no formato paisagem
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Define margens
    margem_esquerda = 75
    margem_direita = width - 75
    largura_maxima = margem_direita - margem_esquerda
    y_pos_texto_evento = height -258

    # Adiciona a imagem de fundo ao PDF
    c.drawImage(background_image_path, 0, 0 , width=width, height=height)

    c.setFont("Titillium-Regular", 12.5)
    c.drawCentredString(width / 2, height - 212, f"Certificamos que")

    # Nome do participante
    c.setFont("Titillium-Bold", 24.5)
    c.setFillColorRGB(192/255, 0, 0) 
    c.drawCentredString(width / 2, height - 280, f"{participante['NomeParticipante']}")

    # Formatação da data e turno
    data_formatada = formatar_data(data_inicio)
    turno = determinar_turno(data_inicio)

    c.setFont("Titillium-Bold",12.5)
    c.setFillColorRGB(3/255, 73/255, 108/255)  # Cor azul #03496C
    c.drawCentredString(width /1.3, height - 420, f"Goiânia,{data_formatada}.")
    
    c.setFont("Titillium-Regular", 10.5)
    c.drawCentredString(width / 1.9, height - 485, f"Prof. Dr. Clayson Moura Gomes")

    c.setFont("Titillium-Bold", 10.5)
    c.drawCentredString(width / 1.9, height - 499, f"Coordenador Geral Acadêmico")

    # Texto do evento e detalhes com data, turno, palestrante e local
    texto_tamanho = 11
    c.setFont("Helvetica", texto_tamanho)
    c.setFillColorRGB(0, 0, 0)
    texto = (f"Participou do evento {evento['NomeEvento']}, com a supervisão do(a) {palestrante}, "
             f"realizado em {data_formatada}, no {local}, no turno {turno} com um total de {cargaHoraria} horas.")
    

    # Quebra o texto em múltiplas linhas respeitando a largura máxima
    linhas = quebrar_texto(texto, largura_maxima, c, "Helvetica", texto_tamanho)

    # Renderiza as linhas com margens laterais
    y_pos = height - y_pos_texto_evento
    for linha in linhas:
        c.drawString(margem_esquerda, y_pos, linha)
        y_pos -= 20  # Espaçamento entre linhas

    # Salvar o PDF
    c.save()
    print(f"Certificado gerado para {participante['NomeParticipante']}")

# Função para processar o arquivo JSON e gerar certificados
def processar_certificados(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        dados = json.load(file)
        
    for inscricao in dados["inscricoes"]:
        participante = next(p for p in dados["participantes"] if p["ParticipanteId"] == inscricao["ParticipanteId"])
        evento = next(e for e in dados["eventos"] if e["EventoId"] == inscricao["EventoId"])
        gerar_certificado(
            participante,
            evento,
            evento["DataInicioEvento"],
            evento["Palestrante"],
            evento["Local"],
            evento["cargaHoraria"]
        )

# Executar o processamento
processar_certificados(json_path)
