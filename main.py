import xml.etree.ElementTree as et
from os import listdir
from os.path import isfile, exists
from os import makedirs
from sys import exit
import shutil


# Por exemplo:
# Seus arquivos estão nas seguintes pastas:
# C:\User\Auranda\Notas\CM
# C:\User\Auranda\Notas\Zecas,
# Na variavel dir_raiz vc preenche com C:\User\Auranda\Notas e na variavel diretorios com
# ['CM','Zecas']
# As variaveis ficariam assim:
# dir_raz = 'C:\User\Auranda\Notas'
# diretorios = ['CM','Zecas']
dir_raiz = ""
diretorios = ['1_CM', '1_ZE', '2_CM','3_CM', '4_CM']

# Nao alterar
#dir_xml = "/XMLs/"
#dir_pdf = "/PDFs/"

cte = '{http://www.portalfiscal.inf.br/cte}CTe'
nfe = '{http://www.portalfiscal.inf.br/nfe}NFe'
data_nfe1 = '/{http://www.portalfiscal.inf.br/nfe}infNFe/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}dEmi'
data_nfe3 = '/{http://www.portalfiscal.inf.br/nfe}infNFe/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}dhEmi'
data_cte = '/{http://www.portalfiscal.inf.br/cte}infCte/{http://www.portalfiscal.inf.br/cte}ide/{http://www.portalfiscal.inf.br/cte}dhEmi'

# Coloque as pastas de destino. O script separa CTE de NFE
destino_cte = '/home/jhon/notas_processadas/CTE/'
destino_nfe = '/home/jhon/notas_processadas/NFE/'

is_cte = False
is_nfe = False
num = 0

for dir in diretorios:
    path = dir_raiz + dir
    #path = dir_raiz + dir + dir_xml
    #path_pdf = dir_raiz + dir + dir_pdf
    for f in listdir(path):
        arquivo = path + f
        if isfile(arquivo) and arquivo.endswith(".xml"):
            tree = et.parse(arquivo)
            root = tree.getroot()
            if root.find(nfe):
                is_nfe = True
                nfe1 = root.find(nfe + data_nfe1)
                nfe3 = root.find(nfe + data_nfe3)
                if nfe1 is not None:
                    datas = nfe1.text.split('-', 2)
                    dir_dest = destino_nfe + dir + '/' + datas[0] + '/' + datas[1] + '/'
                elif nfe3 is not None:
                    pass
                    datas = nfe3.text.split('-', 2)
                    dir_dest = destino_nfe + dir + '/' + datas[0] + '/' + datas[1] + '/'
            else:
                is_cte = True
                tree = et.parse(arquivo)
                root = tree.getroot()
                data = root.find(cte + data_cte)
                datas = data.text.split('-', 2)
                dir_dest = destino_cte + dir + '/' + datas[0] + '/' + datas[1] + '/'

            chave = f.split('.',1)
            # pdf = path_pdf + chave[0] + '.pdf'
            # if isfile(pdf):
            #     dest_pdf = dir_dest + chave[0] + '.pdf'
            #     dest_xml = dir_dest + f
            # else:
            #     print("{} - SEM PDF".format(arquivo))

            if not exists(dir_dest):
                makedirs(dir_dest, exist_ok=True)

            if not isfile(dir_dest + f):
                print("Copiando {}".format(arquivo))
                #shutil.copy(arquivo, dest_xml)
                shutil.copy(arquivo, dir_dest + f)
                num += 1
                #print("Copiando {}".format(pdf))
                #shutil.copy(pdf, dest_pdf)

print("{} chaves copiadas.".format(num))