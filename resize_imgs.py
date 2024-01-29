from PIL import Image
import os 



def ler_arquivos_jpg_em_pasta(origem_base):
    lista_de_imagens = []
    
    # Percorre todos os arquivos na pasta
    for arquivo in os.listdir(origem_base):
        # Verifica se o arquivo é um arquivo JPG
        if arquivo.endswith(".jpg") or arquivo.endswith(".jpeg"):
            lista_de_imagens.append(arquivo)
    
    return lista_de_imagens

def redimensionar_com_proporcao(origem_base, destino_base, novo_lado):
    # Abrir a imagem
    nome_arquivos = ler_arquivos_jpg_em_pasta(origem_base)
    for nome_arquivo in nome_arquivos:
        
        imagem = Image.open(os.path.join(origem_base, nome_arquivo))
        # Obter as dimensões originais
        largura_original, altura_original = imagem.size
        # Calcular a nova largura e altura mantendo a proporção
        proporcao = novo_lado / max(largura_original, altura_original)
        nova_largura = int(largura_original * proporcao)
        nova_altura = int(altura_original * proporcao)
        # Redimensionar a imagem
        nova_imagem = imagem.resize((nova_largura, nova_altura))
        # Salvar a nova imagem
        nome_novo = nome_arquivo.replace('.jpg','_RESIZE.jpg')
        nova_imagem.save(os.path.join(destino_base, nome_novo))


# Exemplo de uso
# caminho_da_imagem = 'product_images\\AucielloFotos\\Planner\\01.Oliva\\01.ImagemOriginal\\IMG_7616.jpg'
origem_base = 'product_images\\AucielloFotos\\Planner\\01.Oliva\\01.ImagemOriginal'
destino_base = 'product_images\\AucielloFotos\\Planner\\01.Oliva\\02.ImagemRedimensionada'
# nome_arquivo = 'IMG_7616.jpg'


novo_lado = 1280

redimensionar_com_proporcao(origem_base, destino_base, novo_lado)
