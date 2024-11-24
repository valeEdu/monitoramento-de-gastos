import csv
import os

class Categories:
    """
    Classe para gerenciar as categorias armazenadas em um arquivo CSV.
    """

    # Caminho para o arquivo CSV onde as categorias são armazenadas
    CSV_FILE = 'data/categories.csv'

    # ------------------------- Métodos estáticos -------------------------

    @staticmethod
    def read_all():
        """
        Lê todas as categorias do arquivo CSV.

        Retorna:
            list: Uma lista de dicionários, cada um representando uma categoria.
        """
        # Verifica se o arquivo existe antes de tentar ler
        if not os.path.exists(Categories.CSV_FILE):
            return []  # Retorna uma lista vazia se o arquivo não existe
        with open(Categories.CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)  # Retorna todas as categorias como uma lista de dicionários

    @staticmethod
    def write_all(categories):
        """
        Escreve uma lista de categorias no arquivo CSV.

        Args:
            categories (list): Lista de dicionários representando categorias.
        """
        with open(Categories.CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name'])
            writer.writeheader()  # Escreve o cabeçalho no arquivo CSV
            writer.writerows(categories)  # Escreve todas as categorias na lista fornecida

    @staticmethod
    def add(name):
        """
        Adiciona uma nova categoria ao arquivo CSV.

        Args:
            name (str): O nome da nova categoria.
        """
        categories = Categories.read_all()  # Lê todas as categorias existentes
        new_id = len(categories) + 1  # Define o próximo ID com base no tamanho da lista
        new_category = {'id': new_id, 'name': name}  # Cria um novo dicionário para a categoria
        categories.append(new_category)  # Adiciona a nova categoria à lista
        Categories.write_all(categories)  # Salva a lista atualizada no arquivo CSV

    @staticmethod
    def delete(category_id):
        """
        Remove uma categoria do arquivo CSV com base no ID.

        Args:
            category_id (int): O ID da categoria a ser removida.
        """
        categories = Categories.read_all()  # Lê todas as categorias existentes
        # Filtra categorias que não correspondem ao ID fornecido
        updated_categories = [cat for cat in categories if int(cat['id']) != category_id]
        Categories.write_all(updated_categories)  # Salva a lista atualizada no arquivo CSV

    @staticmethod
    def get_by_id(category_id):
        """
        Busca uma categoria pelo ID.

        Args:
            category_id (int): O ID da categoria a ser buscada.

        Retorna:
            dict: O dicionário representando a categoria, ou None se não encontrada.
        """
        categories = Categories.read_all()  # Lê todas as categorias existentes
        # Procura a categoria pelo ID e a retorna, se encontrada
        for category in categories:
            if int(category['id']) == category_id:
                return category
        return None  # Retorna None se a categoria não for encontrada
