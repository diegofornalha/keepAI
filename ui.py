import flet as ft
from flet import (
    Page,
    TextField,
    ElevatedButton,
    Text,
    Column,
    Row,
    IconButton,
    Icons,
    Colors,
    ScrollMode,
    ListView,
    SnackBar,
    MainAxisAlignment,
    CrossAxisAlignment,
    Container,
    padding,
    ControlState
)
from datetime import datetime

class NotasUI:
    def __init__(self, page: Page, db_controller):
        self.page = page
        self.db = db_controller
        self.largura_elementos = 450
        
        self.setup_window()
        self.create_elements()
        self.setup_layout()
        self.atualizar_lista_notas()

    def setup_window(self):
        self.page.title = "Bloco de Notas"
        self.page.window.width = 500
        self.page.window.height = 500
        self.page.window.resizable = True
        self.page.window.center()
        
        self.page.scroll = ScrollMode.AUTO
        self.page.theme_mode = "dark"
        self.page.padding = 20
        self.page.vertical_alignment = MainAxisAlignment.CENTER
        self.page.horizontal_alignment = CrossAxisAlignment.CENTER

    def create_elements(self):
        self.titulo = TextField(
            label="Título",
            width=self.largura_elementos,
            text_align="center",
            bgcolor=Colors.SURFACE
        )
        
        self.conteudo = TextField(
            label="Conteúdo",
            multiline=True,
            min_lines=3,
            width=self.largura_elementos,
            text_align="center",
            bgcolor=Colors.SURFACE
        )
        
        self.notas_lista = ListView(
            expand=1,
            spacing=10,
            padding=20,
            height=400,
            width=self.largura_elementos
        )

        self.btn_salvar = ElevatedButton(
            text="Salvar Nota",
            on_click=self.salvar_nota,
            style=ft.ButtonStyle(
                color={
                    ControlState.DEFAULT: Colors.WHITE,
                },
                bgcolor={
                    ControlState.DEFAULT: Colors.BLUE_700,
                    ControlState.HOVERED: Colors.BLUE_800,
                }
            ),
            width=self.largura_elementos
        )

    def mostrar_mensagem(self, mensagem: str):
        snack = SnackBar(
            content=Text(mensagem, color=Colors.WHITE),
            bgcolor=Colors.SURFACE
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def criar_card_nota(self, nota):
        # Converter a string ISO para objeto datetime
        data_criacao = datetime.fromisoformat(nota['data_criacao'].replace('Z', '+00:00'))
        
        return ft.Card(
            content=Container(
                content=Column([
                    ft.ListTile(
                        title=Text(
                            nota['titulo'],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            text_align="center"
                        ),
                        subtitle=Text(
                            data_criacao.strftime('%d/%m/%Y %H:%M'),
                            size=12,
                            color=Colors.GREY_400,
                            text_align="center"
                        ),
                    ),
                    Container(
                        content=Text(
                            nota['conteudo'],
                            text_align="center"
                        ),
                        padding=padding.only(left=15, right=15, bottom=15)
                    ),
                    Row([
                        IconButton(
                            icon=Icons.DELETE_OUTLINE,
                            icon_color=Colors.RED_400,
                            tooltip="Excluir nota",
                            data=nota['id'],
                            on_click=self.excluir_nota
                        )
                    ], alignment=MainAxisAlignment.CENTER)
                ]),
                bgcolor=Colors.SURFACE,
                padding=10
            )
        )

    def atualizar_lista_notas(self):
        self.notas_lista.controls.clear()
        notas = self.db.get_all_notes()
        
        for nota in notas:
            nota_card = self.criar_card_nota(nota)
            self.notas_lista.controls.append(nota_card)
        self.page.update()

    def salvar_nota(self, e):
        if not self.titulo.value or not self.conteudo.value:
            self.mostrar_mensagem("Por favor, preencha todos os campos!")
            return

        self.db.add_note(self.titulo.value, self.conteudo.value)
        
        self.titulo.value = ""
        self.conteudo.value = ""
        self.page.update()
        
        self.atualizar_lista_notas()
        self.mostrar_mensagem("Nota salva com sucesso!")

    def excluir_nota(self, e):
        nota_id = e.control.data
        if self.db.delete_note(nota_id):
            self.atualizar_lista_notas()
            self.mostrar_mensagem("Nota excluída com sucesso!")

    def setup_layout(self):
        self.page.add(
            Container(
                content=Column(
                    [
                        Text(
                            "Bloco de Notas",
                            size=30,
                            weight="bold",
                            text_align="center",
                            color=Colors.WHITE
                        ),
                        self.titulo,
                        self.conteudo,
                        self.btn_salvar,
                        Text(
                            "Suas Notas:",
                            size=20,
                            weight="bold",
                            text_align="center",
                            color=Colors.WHITE
                        ),
                        self.notas_lista
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                alignment=ft.alignment.center
            )
        )
 