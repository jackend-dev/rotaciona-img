import cv2

def rotaciona_foto_qtd(img,qtd):
    img_new = img
    for i in range(qtd):
        img_new = rotaciona_foto(img_new)
    return img_new

def rotaciona_foto(img):
    return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


def cria_foto_temporaria(img, nome):
    cv2.imwrite(nome, img)


def calcula_proporacao(altura, largura, valor_atingir):
    if (altura > largura):
        proporcao = float(valor_atingir / altura)
    else:
        proporcao = float(valor_atingir / largura)
    return proporcao


def calcula_tamanho(proporcao, altura, largura):
    nova_altura = int(altura * proporcao)
    nova_largura = int(largura * proporcao)
    return (nova_altura, nova_largura)


def expande_foto(img, altura, largura):
    proporcao = calcula_proporacao(altura, largura, 3840)
    tamanho_novo = calcula_tamanho(proporcao, altura, largura)
    if (tamanho_novo[0] > tamanho_novo[1]):
        tamanho_novo = (tamanho_novo[0], tamanho_novo[1])
    else:
        tamanho_novo = (tamanho_novo[1], tamanho_novo[0])
    return cv2.resize(img, tamanho_novo, interpolation=cv2.INTER_AREA)

def grava_foto(img,nome,caminho):
    cv2.imwrite('{}/{}'.format(caminho,nome), img)