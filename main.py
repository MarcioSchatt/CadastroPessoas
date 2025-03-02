import tkinter as tk
from tkinter import messagebox
import csv


class Gerenciador:
    def __init__(self) -> None:
        """
        Inicializa o gerenciador e cria o arquivo CSV caso não exista.
        """
        self.arq = 'pessoas.csv'
        self.criar_arquivo()

    def criar_arquivo(self) -> None:
        """
        Cria o arquivo CSV com cabeçalho, caso o arquivo não exista.
        """
        try:
            with open(self.arq, mode='r', newline='', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.arq, mode='w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(
                    ['ID', 'Nome', 'Sobrenome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'Estado', 'Pais', 'Telefone', 'E-mail'])

    def salvar(self, dados: list) -> None:
        """
        Salva ou atualiza os dados no arquivo CSV.

        Args:
            dados (list): Dados a serem salvos (ID, Nome, Sobrenome, etc.)
        """
        self.salvar_ou_atualizar(self.obter_id(), dados)

    def obter_id(self) -> int:
        """
        Obtém o próximo ID disponível.

        Returns:
            int: O próximo ID.
        """
        if self.ler_dados():
            return max([int(dado[0]) for dado in self.ler_dados()]) + 1
        return 1

    def ler_dados(self) -> list:
        """
        Lê os dados do arquivo CSV.

        Returns:
            list: Lista de dados lidos do arquivo CSV.
        """
        with open(self.arq, mode='r', newline='', encoding='utf-8') as f:
            next(csv.reader(f))
            return list(csv.reader(f))

    def excluir(self, id_pessoa: int) -> None:
        """
        Exclui um cadastro do arquivo CSV pelo ID.

        Args:
            id_pessoa (int): ID da pessoa a ser excluída.
        """
        dados_filtrados = [
            d for d in self.ler_dados() if int(d[0]) != id_pessoa]
        self.reescrever_arquivo(dados_filtrados)

    def alterar(self, id_pessoa: int, novos_dados: list) -> None:
        """
        Altera um cadastro existente no arquivo CSV.

        Args:
            id_pessoa (int): ID da pessoa a ser alterada.
            novos_dados (list): Novos dados a serem atualizados.
        """
        dados = self.ler_dados()
        if dados == []:
            dados.append(novos_dados)
        else:
            for i, dado in enumerate(dados):
                if int(dado[0]) == id_pessoa:
                    dados[i] = novos_dados
                    break
        self.reescrever_arquivo(dados)

    def reescrever_arquivo(self, dados: list) -> None:
        """
        Reescreve o arquivo CSV com novos dados.

        Args:
            dados (list): Dados a serem escritos no arquivo.
        """
        with open(self.arq, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['ID', 'Nome', 'Sobrenome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'Estado', 'Pais', 'Telefone', 'E-mail'])
            writer.writerows(dados)

    def salvar_ou_atualizar(self, id_pessoa: int, dados: list) -> None:
        """
        Salva ou atualiza um cadastro no arquivo CSV.

        Args:
            id_pessoa (int): ID da pessoa a ser salva ou atualizada.
            dados (list): Dados a serem salvos ou atualizados.
        """
        dados_atualizados = self.ler_dados()
        for i, dado in enumerate(dados_atualizados):
            if int(dado[0]) == id_pessoa:
                dados_atualizados[i] = [str(id_pessoa)] + dados[1:]
                self.reescrever_arquivo(dados_atualizados)
                return
        with open(self.arq, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(dados)


class Janela(tk.Tk):
    def __init__(self) -> None:
        """
        Inicializa a janela principal e cria os widgets da interface.
        """
        super().__init__()
        self.title("Gerenciador de Pessoas")

        self.ger = Gerenciador()

        self.criar_widgets()

    def criar_widgets(self) -> None:
        """
        Cria os widgets da interface gráfica.
        """
        widgets = [
            'ID', 'Nome', 'Sobrenome', 'Rua', 'Número', 'Bairro', 'Cidade', 'Estado', 'País', 'Telefone', 'E-mail']
        padx = 10
        pady = 5
        row = 0
        column = 0

        self.id = tk.Entry(self)
        self.nome = tk.Entry(self)
        self.sobrenome = tk.Entry(self)
        self.rua = tk.Entry(self)
        self.numero = tk.Entry(self)
        self.bairro = tk.Entry(self)
        self.cidade = tk.Entry(self)
        self.estado = tk.Entry(self)
        self.pais = tk.Entry(self)
        self.telefone = tk.Entry(self)
        self.email = tk.Entry(self)

        self.id.insert(0, str(self.proximo_id()))
        self.id.config(state='disabled')

        self.nome.bind("<KeyPress>", self.validar_texto)
        self.sobrenome.bind("<KeyPress>", self.validar_texto)
        self.estado.bind("<KeyPress>", self.validar_texto)
        self.pais.bind("<KeyPress>", self.validar_texto)
        self.numero.bind("<KeyPress>", self.validar_numero)
        self.telefone.bind("<KeyPress>", self.validar_numero)

        for campo in widgets:
            tk.Label(self, text=campo).grid(
                row=row, column=column, padx=padx, pady=pady)
            row += 1

        row = 0
        column += 1
        self.id.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.nome.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.sobrenome.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.rua.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.numero.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.bairro.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.cidade.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.estado.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.pais.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.telefone.grid(row=row, column=column, padx=padx, pady=pady)
        row += 1
        self.email.grid(row=row, column=column, padx=padx, pady=pady)

        tk.Button(
            self, text="Atualizar Lista", command=self.atualizar_lista).grid(row=11, column=0, columnspan=2, pady=pady)

        self.lista = tk.Listbox(self, height=10, width=80)
        self.lista.grid(row=12, column=0, columnspan=2, padx=padx, pady=pady)

        tk.Button(
            self, text="Excluir", command=self.excluir).grid(row=13, column=0, pady=pady)
        tk.Button(
            self, text="Alterar", command=self.alterar).grid(row=13, column=1, pady=pady)
        tk.Button(
            self, text="Salvar", command=self.salvar).grid(row=14, column=0, pady=pady)
        tk.Button(
            self, text="Cancelar", command=self.limpar_campos).grid(row=14, column=1, pady=pady)

        self.atualizar_lista()

    def obter_ultimo_id(self) -> int:
        """
        Obtém o último ID presente nos dados.

        Returns:
            int: Último ID.
        """
        if self.ger.ler_dados():
            return max([int(dado[0]) for dado in self.ger.ler_dados()])
        return 1

    def proximo_id(self) -> int:
        """
        Obtém o próximo ID disponível.

        Returns:
            int: Próximo ID.
        """
        if self.ger.ler_dados():
            return max([int(dado[0]) for dado in self.ger.ler_dados()]) + 1
        return 1

    def validar_texto(self, event: tk.EventType) -> str:
        """
        Valida se o texto digitado é alfabético.

        Args:
            event (tk.EventType): Evento gerado pelo teclado.

        Returns:
            str: "break" se a tecla pressionada não for permitida.
        """
        if not event.char.isalpha() and event.keysym not in ["Space", "BackSpace", "Tab", "Shift_R", "Shift_L"]:
            return "break"

    def validar_numero(self, event: tk.EventType) -> str:
        """
        Valida se o número digitado é numérico.

        Args:
            event (tk.EventType): Evento gerado pelo teclado.

        Returns:
            str: "break" se a tecla pressionada não for numérica.
        """
        if not event.char.isdigit() and event.keysym not in ["BackSpace", "Tab", "Shift_R", "Shift_L"]:
            return "break"

    def salvar(self) -> None:
        """
        Salva ou atualiza os dados no arquivo, realizando as validações.

        Exibe uma mensagem de erro se algum dado obrigatório não for preenchido
        ou se houver um formato inválido.
        """
        id = self.id.get()
        nome = self.nome.get()
        sobrenome = self.sobrenome.get()
        rua = self.rua.get()
        numero = self.numero.get()
        bairro = self.bairro.get()
        cidade = self.cidade.get()
        estado = self.estado.get()
        pais = self.pais.get()
        telefone = self.telefone.get()
        email = self.email.get()

        if not id or not nome or not sobrenome:
            messagebox.showerror(
                "Erro", "ID, Nome e Sobrenome são obrigatórios!")
            return

        if len(telefone) > 0 and (8 > len(telefone) or len(telefone) > 11):
            messagebox.showerror(
                "Erro", "Telefone inválido!")
            return

        if len(email) != 0 and "@" not in email and not (email.endswith(".com") or email.endswith(".br") or email.endswith(".net")):
            messagebox.showerror(
                "Erro", "E-mail inválido!")
            return

        dados = [
            id, nome, sobrenome, rua, numero, bairro, cidade, estado, pais, telefone, email]

        if self.id.get() and int(self.id.get()) == self.obter_ultimo_id():
            self.ger.alterar(int(self.id.get()), dados)
            messagebox.showinfo("Sucesso", "Cadastro atualizado com sucesso!")
        else:
            self.ger.salvar(dados)
            messagebox.showinfo("Sucesso", "Cadastro salvo com sucesso!")

        self.limpar_campos()
        self.atualizar_lista()

    def limpar_campos(self) -> None:
        """
        Limpa todos os campos de entrada.
        """
        self.id.config(state='normal')
        self.id.delete(0, tk.END)
        self.id.insert(0, str(self.proximo_id()))
        self.id.config(state='disabled')
        self.nome.delete(0, tk.END)
        self.sobrenome.delete(0, tk.END)
        self.rua.delete(0, tk.END)
        self.numero.delete(0, tk.END)
        self.bairro.delete(0, tk.END)
        self.cidade.delete(0, tk.END)
        self.estado.delete(0, tk.END)
        self.pais.delete(0, tk.END)
        self.telefone.delete(0, tk.END)
        self.email.delete(0, tk.END)

    def atualizar_lista(self) -> None:
        """
        Atualiza a lista de registros exibidos na interface gráfica.
        """
        self.lista.delete(0, tk.END)
        for cadastro in self.ger.ler_dados():
            self.lista.insert(
                tk.END, f"{cadastro[0]} - {cadastro[1]} {cadastro[2]}")

    def excluir(self) -> None:
        """
        Exclui o cadastro selecionado na lista.
        """
        if not self.lista.curselection():
            messagebox.showerror("Erro", "Selecione um cadastro para excluir!")
            return

        self.ger.excluir(
            int(self.ger.ler_dados()[self.lista.curselection()[0]][0]))

        messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso!")
        self.atualizar_lista()

    def alterar(self) -> None:
        """
        Altera o cadastro selecionado na lista.
        """
        if not self.lista.curselection():
            messagebox.showerror("Erro", "Selecione um cadastro para alterar!")
            return

        dados_antigos = self.ger.ler_dados()[self.lista.curselection()[0]]

        self.id.config(state='normal')
        self.id.delete(0, tk.END)
        self.id.insert(0, dados_antigos[0])
        self.id.config(state='disabled')
        self.nome.delete(0, tk.END)
        self.nome.insert(0, dados_antigos[1])
        self.sobrenome.delete(0, tk.END)
        self.sobrenome.insert(0, dados_antigos[2])
        self.rua.delete(0, tk.END)
        self.rua.insert(0, dados_antigos[3])
        self.numero.delete(0, tk.END)
        self.numero.insert(0, dados_antigos[4])
        self.bairro.delete(0, tk.END)
        self.bairro.insert(0, dados_antigos[5])
        self.cidade.delete(0, tk.END)
        self.cidade.insert(0, dados_antigos[6])
        self.estado.delete(0, tk.END)
        self.estado.insert(0, dados_antigos[7])
        self.pais.delete(0, tk.END)
        self.pais.insert(0, dados_antigos[8])
        self.telefone.delete(0, tk.END)
        self.telefone.insert(0, dados_antigos[9])
        self.email.delete(0, tk.END)
        self.email.insert(0, dados_antigos[10])


class Main:
    def __init__(self) -> None:
        """
        Inicializa e executa a aplicação.
        """
        self.app = Janela()
        self.app.mainloop()


if __name__ == "__main__":
    Main()
