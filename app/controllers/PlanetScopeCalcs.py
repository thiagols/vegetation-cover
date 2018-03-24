from datetime import datetime
import rasterio
import rasterio.features
import rasterio.warp
import numpy


class PlanetScopeCalcs:

    # Exibe o nome do arquivo - Apenas verifica se o arquivo exite e devolve o nome
    @staticmethod
    def get_name(file_url):
        with rasterio.open(file_url) as src:
            return src.name

    # Calcula porcentagem de Area Verde atraves do calculo do NDVI
    @staticmethod
    def calc_vegetated_area_percent(file_url):
        with rasterio.open(file_url) as src:
            band_red = src.read(3)  # Faz a leitura da Camada RED

        with rasterio.open(file_url) as src:
            band_nir = src.read(4)  # Faz a leitura da Camada NIR

        # Executa o calculo do NDVI
        numpy.seterr(divide='ignore', invalid='ignore')  # Permite a divisão por Zero
        ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

        px_total = ndvi.size  # Total de Pixels da Imagem
        px_vegetated = 0  # Pixels com Vegetação segundo Indice de Precisão
        tx_precision = 0.6  # Taxa de Precisão de indentificação de Pixels Veget.

        # Calcula Area Verde - Trabalhando a Precisão  em cada Pixel de Vegetação
        for px_width in ndvi:
            for px_height in px_width:
                if px_height > tx_precision:
                    px_vegetated = px_vegetated + 1

        return round(px_vegetated / px_total, 1)

    # Calcula a Area da Cena
    @staticmethod
    def calc_area(file_url):
        with rasterio.open(file_url) as src:
            img_bounds = src.bounds
            img_width = (img_bounds.right - img_bounds.left) / 1000
            img_height = (img_bounds.top - img_bounds.bottom) / 1000
            img_area = img_width * img_height
            return img_area

    # Calcula e Retorna o Centroide da Cena em JSON
    @staticmethod
    def get_centroid(file_url):
        with rasterio.open(file_url) as src:
            coordinates = rasterio.warp.transform_bounds(src.crs, 'EPSG:4326', src.bounds.left,
                                                         src.bounds.bottom,
                                                         src.bounds.right, src.bounds.top)
            coordinates_lon_center = (coordinates[0] + coordinates[2]) / 2
            coordinates_lat_center = (coordinates[1] + coordinates[3]) / 2

            centroid = [coordinates_lon_center, coordinates_lat_center]

            return centroid

    # Retorna a Data do Objeto no formato ISO 8601
    # (Passado no arquivo do desafio - Possivel encontrar dentro do arquivo de METADADO não presente)
    @staticmethod
    def get_local_time_capture():
        return str(datetime(2016, 12, 7, 15, 19, 53).isoformat())
