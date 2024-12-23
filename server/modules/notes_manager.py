from datetime import datetime
from supabase import create_client
import os


class NotesManager:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def criar_nota(self, texto: str) -> str:
        """Cria uma nova nota a partir do texto fornecido"""
        try:
            # Processa o texto para extrair título e conteúdo
            texto = texto.strip().replace("*", "")

            # Gera um título mais descritivo com emoji
            if "igreja" in texto.lower():
                titulo = "⛪ Compromisso na Igreja"
                # Verifica se tem horário no texto
                horario = ""
                if "9h" in texto or "9hs" in texto or "9 h" in texto:
                    horario = "9h da manhã"
                elif "9:00" in texto:
                    horario = "9:00 da manhã"

                conteudo = f"""Compromisso: Ir à igreja{' às ' + horario if horario else ''}

Detalhes importantes:
- Chegar com antecedência

- Levar Bíblia

- Participar dos momentos de louvor

- Anotar pontos importantes da mensagem

- Interagir com a comunidade após o culto"""
            elif "mercado" in texto.lower():
                titulo = "🛒 Lista de Compras"
                conteudo = texto
            else:
                titulo = "📝 Lembrete"
                conteudo = texto

            # Cria a nota no Supabase
            data = {
                "titulo": titulo,
                "conteudo": conteudo,
                "data": datetime.now().isoformat(),
            }

            self.supabase.table("notes").insert(data).execute()
            return f"✅ Criei uma nota sobre seu compromisso! Quer adicionar mais algum detalhe específico?"

        except Exception as e:
            return f"❌ Erro ao criar nota: {str(e)}"

    def ler_nota(self, id_nota: str) -> str:
        """Lê uma nota específica pelo ID"""
        try:
            id_nota = int(id_nota)
            result = (
                self.supabase.table("notes").select("*").eq("id", id_nota).execute()
            )

            if not result.data:
                return f"❌ Nota #{id_nota} não encontrada."

            nota = result.data[0]
            return f"""📝 Nota #{nota['id']}:
Título: {nota['titulo']}
Data: {nota['data']}
Conteúdo:
{nota['conteudo']}"""
        except ValueError:
            return "❌ ID inválido. Use apenas números."
        except Exception as e:
            return f"❌ Erro ao ler nota: {str(e)}"

    def atualizar_nota(self, texto: str) -> str:
        """Atualiza uma nota existente com novos detalhes"""
        try:
            # Busca a nota mais recente
            result = (
                self.supabase.table("notes")
                .select("*")
                .order("data", desc=True)
                .limit(1)
                .execute()
            )

            if not result.data:
                return self.criar_nota(texto)

            nota = result.data[0]
            id_nota = nota["id"]

            # Lógica melhorada para mudança de título
            texto_lower = texto.lower()
            if (
                "mudar" in texto_lower
                or "mude" in texto_lower
                or "alterar" in texto_lower
            ):
                # Tenta extrair o novo título de várias formas
                novo_titulo = texto
                if "para" in texto_lower:
                    novo_titulo = texto.split("para")[-1].strip()
                elif "titulo" in texto_lower:
                    novo_titulo = texto.split("titulo")[-1].strip()

                # Adiciona emoji baseado no contexto
                if "igreja" in novo_titulo.lower():
                    novo_titulo = "⛪ " + novo_titulo.replace("igreja", "Igreja")
                elif "mercado" in novo_titulo.lower():
                    novo_titulo = "🛒 " + novo_titulo.replace("mercado", "Mercado")

                data = {"titulo": novo_titulo, "data": datetime.now().isoformat()}
                self.supabase.table("notes").update(data).eq("id", id_nota).execute()
                return f"✅ Título atualizado! Quer adicionar mais alguma informação à nota?"

            # Se não for mudança de título, atualiza o conteúdo
            if "conteudo" in texto_lower:
                novo_conteudo = texto.split("conteudo")[-1].strip()
            else:
                novo_conteudo = texto

            data = {"conteudo": novo_conteudo, "data": datetime.now().isoformat()}

            self.supabase.table("notes").update(data).eq("id", id_nota).execute()
            return f"✅ Nota atualizada! Precisa adicionar mais algum detalhe?"
        except Exception as e:
            return f"❌ Erro ao atualizar nota: {str(e)}"

    def deletar_nota(self, id_nota: str) -> str:
        """Deleta uma nota pelo ID"""
        try:
            id_nota = int(id_nota)

            # Verifica se a nota existe
            result = (
                self.supabase.table("notes").select("*").eq("id", id_nota).execute()
            )
            if not result.data:
                return f"❌ Nota #{id_nota} não encontrada."

            # Deleta a nota
            self.supabase.table("notes").delete().eq("id", id_nota).execute()
            return f"✅ Nota #{id_nota} deletada com sucesso!"
        except ValueError:
            return "❌ ID inválido. Use apenas números."
        except Exception as e:
            return f"❌ Erro ao deletar nota: {str(e)}"

    def listar_notas(self) -> str:
        """Lista todas as notas"""
        try:
            result = (
                self.supabase.table("notes")
                .select("*")
                .order("data", desc=True)
                .execute()
            )

            if not result.data:
                return "📝 Nenhuma nota encontrada."

            resultado = "📝 Suas notas:\n\n"
            for nota in result.data:
                resultado += f"#{nota['id']} - {nota['titulo']} ({nota['data']})\n"
                conteudo = nota["conteudo"]
                if len(conteudo) > 100:
                    conteudo = conteudo[:100] + "..."
                resultado += f"{conteudo}\n\n"
            return resultado
        except Exception as e:
            return f"❌ Erro ao listar notas: {str(e)}"
