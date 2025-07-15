import sqlite3

d = "\033[m"

#SECTION - Inicializador do banco de dados
def init_db():
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS lol(lane, champ, picks, win, win_rate)")
    
    conn.commit()
    conn.close()
#!SECTION

#SECTION - Função para buscar o campeão
def get_champ(name):
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lol WHERE champ = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result
#!SECTION

#SECTION - Função para buscar todos os campeões
def get_all_champ():
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lol")
    result = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return result, columns

#SECTION - Função para atualizar picks, win e win_rate do campeão
def update_info(name, result_game):
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT picks, win FROM lol WHERE champ = ?", (name,))
    result = cursor.fetchone()
    picks, win = result
    if result_game:
        win_rate = ((win+1) / (picks + 1)) * 100
        cursor.execute("""
                       UPDATE lol 
                       SET win = win + 1 , win_rate = ? , picks = picks + 1 
                       WHERE champ = ?"""
                       , (win_rate, name))
        conn.commit()
        conn.close()
    else:
        win_rate = (win / (picks + 1)) * 100
        cursor.execute("""
                       UPDATE lol 
                       SET win_rate = ? , picks = picks + 1 
                       WHERE champ = ?"""
                       , (win_rate, name))
        conn.commit()
        conn.close()       
#!SECTION

#SECTION - Função para adição de campeões
def create_champ(name, lane, victory):
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()
    if victory:
        cursor.execute("INSERT INTO lol (lane, champ, picks, win, win_rate) VALUES (?, ?, ?, ?, ?)", (lane, name, 1, 1, 100))
    else:
        cursor.execute("INSERT INTO lol (lane, champ, picks, win, win_rate) VALUES (?, ?, ?, ?, ?)", (lane, name, 1, 0, 0))
    conn.commit()
    conn.close()
#!SECTION    

#SECTION - Mostra as estatísticas dos campeões
def show_estastic():
    result, _ = get_all_champ()
    if not result:
        print(f"\n\033[0;31;40mNenhum registro encontrado!{d}")
    else:
        for results in result:
            print(
                f"""\033[1;38;47m
{results[1]} ({results[0]}){d}
-> Com \033[1;36;40m{results[2]}{d} pick(s) e \033[1;36;40m{results[3]}{d} vitória(s)
-> Win rate de {results[4]:.2f}%{d}
            """
            )
#!SECTION

#SECTION - Query para a remoção de algum campeão
def delete_champ(name):
    conn = sqlite3.connect("LolBase.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lol WHERE champ = ?", (name, ))
    conn.commit()
    conn.close()
#!SECTION