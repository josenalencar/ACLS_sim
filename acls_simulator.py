import streamlit as st
import pandas as pd
import random

def get_user_choice(options):
    random.shuffle(options)
    choice = st.selectbox("Escolha uma opção:", options)
    return choice

def ask_question(question, correct_answer, wrong_answers, table, row, column_name, correct_update):
    st.write(table)
    st.subheader(question)
    options = [correct_answer] + wrong_answers
    answer = get_user_choice(options)
    if answer == correct_answer:
        st.success("Correto!")
        table.at[row, column_name] = correct_update
        return True
    else:
        st.error("ESTAVA TUDO INDO BEM, MAS AGORA ACONTECEU UM ERRO GRAVE.")
        st.write(f"A resposta correta seria: {correct_answer}")
        return False

def main():
    st.title("Simulador de Caso Clínico em ACLS")

    table = pd.DataFrame(columns=['Ciclo', 'Ritmo', 'Choque', 'RCP', 'Coach', 'Drogas', 'Outros'])
    game_over = False

    for ciclo in range(1, 5):
        if game_over:
            break

        if ciclo != 1:
            st.write("DOIS MINUTOS")

        table.at[ciclo-1, 'Ciclo'] = ciclo

         # Ciclo 1
    if ciclo == 1:
            table.at[ciclo-1, 'Ritmo'] = 'TV'
            if not ask_question("O ritmo é TV. O que fazer?", "Checar pulso", ["Desfibrilar com 200 J", "Cardioverter com 100 J"], table, ciclo-1, 'Ritmo', 'TVSP'):
                game_over = True
                continue
            if not ask_question("O RITMO É TVSP. O que fazer agora?", "Desfibrilar com 200 J", ["Cardioverter sincronizado com 100 J", "Comprimir"], table, ciclo-1, 'Choque', 'Feito'):
                game_over = True
                continue
            if not ask_question("Depois do choque, o que fazer?", "começar a RCP", ["checar ritmo", "preparar epinefrina"], table, ciclo-1, 'RCP', 'Sim'):
                game_over = True
                continue
            if not ask_question("RCP INICIADA. O que fazer agora?", "Estabelecer o Coach", ["Checar ritmo", "administrar epinefrina"], table, ciclo-1, 'Coach', 'Sim'):
                game_over = True
                continue
            if not ask_question("COACH ATUANDO. O que fazer agora?", "Preparar epinefrina", ["Checar ritmo", "administrar epinefrina"], table, ciclo-1, 'Drogas', 'Epi preparada'):
                game_over = True
                continue

    # Ciclo 2
    elif ciclo == 2:
        table.at[ciclo-1, 'Ritmo'] = 'FV'
        if not ask_question("DOIS MINUTOS. O ritmo agora é FV. O que fazer agora?", "Chocar", ["administrar epinefrina", "comprimir"], table, ciclo-1, 'Ritmo', 'FV'):
            game_over = True
            continue
        if not ask_question("Depois do choque, o que fazer?", "começar a RCP", ["checar ritmo", "preparar epinefrina"], table, ciclo-1, 'RCP', 'Sim'):
            game_over = True
            continue
        if not ask_question("RCP INICIADA. O que fazer agora?", "Checar o Coach", ["Checar ritmo", "administrar epinefrina"], table, ciclo-1, 'Coach', 'Sim'):
            game_over = True
            continue
        if not ask_question("COACH ATUANDO. O que fazer agora?", "Administrar Epinefrina e Preparar 300 mg de Amiodarona", ["Administrar Amiodarona 300 mg", "checar ritmo"], table, ciclo-1, 'Drogas', 'Epi administrada e Amio 300 prep'):
            game_over = True
            continue

    # Ciclo 3
    elif ciclo == 3:
        table.at[ciclo-1, 'Ritmo'] = 'Atividade elétrica'
        if not ask_question("DOIS MINUTOS. O ritmo é uma atividade elétrica. O que fazer agora?", "checar pulso", ["Começar RCP", "Começar protocolo de RCE"], table, ciclo-1, 'Ritmo', 'AESP'):
            game_over = True
            continue
        if not ask_question("RCP INICIADA. O que fazer agora?", "Checar o Coach", ["Administrar amiodarona", "administrar epinefrina"], table, ciclo-1, 'Coach', 'Sim'):
            game_over = True
            continue
        if not ask_question("COACH ATUANDO. O que fazer agora?", "Preparar Epinefrina", ["Administrar Amiodarona 300 mg", "checar ritmo"], table, ciclo-1, 'Drogas', 'Epi preparada'):
            game_over = True
            continue
        if not ask_question("VOCÊ ESTÁ INDO BEM. O que ainda falta fazer?", "Checar causas", ["Parar RCP", "Fazer Amiodarona"], table, ciclo-1, 'Outros', 'Causas'):
            game_over = True
            continue

    elif ciclo == 4:
        if ask_question("DOIS MINUTOS.O ritmo é uma atividade elétrica. O que fazer agora?", "Checar pulso", ["Iniciar protocolo de RCE", "Fazer epinefrina"], table, ciclo-1, 'Ritmo', 'AECP'):
            if ask_question("TEM PULSO. O que fazer agora?", "Iniciar protocolo de RCE", ["Chocar", "Comprimir"], table, ciclo-1, 'RCP', 'Parou'):
                display(HTML(f"<strong><font size=4>PARABÉNS, O PACIENTE VOLTOU</font></strong>"))
                input("Pressione Enter e depois clique em PLAY para jogar de novo...")
                break

    st.write("Tabela Final:")
    st.write(table)

if __name__ == "__main__":
    main()

