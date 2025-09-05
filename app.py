import streamlit as st
import json
import os
import time
from datetime import datetime

ARQUIVO = "tarefas.json"

# ==============================
# Funções utilitárias
# ==============================
def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

def adicionar_tarefa(nome, tempo):
    tarefas = carregar_tarefas()
    tarefas.append({"nome": nome, "tempo": tempo, "concluido": 0})
    salvar_tarefas(tarefas)

def atualizar_tarefa(index, tempo):
    tarefas = carregar_tarefas()
    tarefas[index]["concluido"] += tempo
    salvar_tarefas(tarefas)

# ==============================
# Layout do Streamlit
# ==============================
st.title("📚 Organizador de Estudos - Pomodoro")

aba = st.sidebar.radio("Menu", ["Adicionar tarefa", "Lista de tarefas", "Relatório"])

# ---------------- Adicionar tarefa ----------------
if aba == "Adicionar tarefa":
    st.subheader("➕ Nova tarefa")
    nome = st.text_input("Nome da tarefa:")
    tempo = st.number_input("Tempo (em minutos):", min_value=1, value=25)

    if st.button("Adicionar"):
        if nome.strip():
            adicionar_tarefa(nome, tempo)
            st.success(f"Tarefa **{nome}** adicionada com {tempo} min!")
        else:
            st.warning("Digite um nome válido para a tarefa.")

# ---------------- Lista de tarefas ----------------
elif aba == "Lista de tarefas":
    st.subheader("📋 Suas tarefas")
    tarefas = carregar_tarefas()

    if not tarefas:
        st.info("Nenhuma tarefa cadastrada.")
    else:
        for i, t in enumerate(tarefas):
            with st.expander(f"{t['nome']} ({t['tempo']} min) - Concluído: {t['concluido']} min"):
                if st.button(f"▶ Iniciar Pomodoro - {t['nome']}", key=i):
                    st.write(f"Iniciando Pomodoro de {t['tempo']} minutos para **{t['nome']}**...")

                    tempo_segundos = t["tempo"] * 60
                    barra = st.progress(0)
                    status = st.empty()

                    for s in range(tempo_segundos):
                        minutos, segundos = divmod(tempo_segundos - s, 60)
                        status.text(f"⏳ Restante: {minutos:02d}:{segundos:02d}")
                        barra.progress((s + 1) / tempo_segundos)
                        time.sleep(1)

                    st.success("✅ Pomodoro finalizado! Pausa de 5 minutos ☕")
                    atualizar_tarefa(i, t["tempo"])

# ---------------- Relatório ----------------
elif aba == "Relatório":
    st.subheader("📊 Relatório de Estudos")
    tarefas = carregar_tarefas()

    if not tarefas:
        st.info("Nenhuma tarefa registrada ainda.")
    else:
        total = 0
        for t in tarefas:
            st.write(f"- **{t['nome']}**: {t['concluido']} min")
            total += t['concluido']
        st.write(f"⏱️ **Tempo total estudado:** {total} minutos")
