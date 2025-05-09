import cv2

# Carrega o classificador de faces
carregaAlgoritmo = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# Lê a imagem
imagem = cv2.imread('fotos/suspeito3.jpg')

# Verifica se a imagem foi carregada corretamente
if imagem is None:
    print("Erro ao carregar a imagem.")
else:
    # Converte para escala de cinza
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Detecta as faces
    faces = carregaAlgoritmo.detectMultiScale(imagemCinza)

    print(faces)

    # Desenha retângulos nas faces detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Exibe a imagem
    cv2.imshow("Faces", imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
