import os

class RenomeadorArquivos:
    def __init__(self, pasta):
        """
        Inicializa a classe com o caminho da pasta onde os arquivos serão renomeados.
        
        :param pasta: Caminho da pasta.
        """
        self.pasta = pasta

    def listar_arquivos(self):
        """
        Lista os arquivos contidos na pasta, ignorando subpastas.
        
        :return: Lista de nomes de arquivos ordenada.
        """
        itens = os.listdir(self.pasta)
        arquivos = [item for item in itens if os.path.isfile(os.path.join(self.pasta, item))]
        arquivos.sort()
        return arquivos

    def renomear(self):
        """
        Renomeia os arquivos da pasta de forma incremental, mantendo suas extensões.
        """
        arquivos = self.listar_arquivos()
        for indice, arquivo in enumerate(arquivos, start=1):
            nome, extensao = os.path.splitext(arquivo)
            novo_nome = f"{indice}{extensao}"
            caminho_antigo = os.path.join(self.pasta, arquivo)
            caminho_novo = os.path.join(self.pasta, novo_nome)
            os.rename(caminho_antigo, caminho_novo)
            print(f"Renomeado: {arquivo} -> {novo_nome}")

# Exemplo de uso:
if __name__ == "__main__":
    caminho_pasta = "01-04-2025_generations/"
    renomeador = RenomeadorArquivos(caminho_pasta)
    renomeador.renomear()
