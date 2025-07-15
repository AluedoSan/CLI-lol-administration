from db import init_db, update_info, get_champ, create_champ, delete_champ, get_all_champ
import pandas as pd

d = "\033[m"
lane_list = ["top", "jg", "mid", "adc", "sup"]

#SECTION - Main para rodar as funções
def main():
    init_db()
    print(f"\033[0;30;41mBanco de dados inicializado.{d}")
    print(f"\033[1;33;45m⭐ Bem-Vindo a Summoner's Rift ⭐{d}")
    options_menu()
#!SECTION

#SECTION - Loop do menu de opções
def options_menu():
    while True:
        print(f"""\033[0;32;40m
Escolha uma das opções:
[0] - Ver estatísticas
[1] - Seleção de campeão
[2] - Deletar campeão
[3] - Ver ranking
[4] - Sair{d} """)

        option = input("\nOpção: ")
        match option:
            case "0":
                show_estastic()
            case "1":
                champ_select()
            case "2":
                champ_delete()
            case "3":
                champ_ranking()
            case "4":
                break
            case _:
                print("\nOpção não encontrada!")
#!SECTION

#SECTION - Seleção para selecionar um campeão/adiciona-lo
def champ_select():
    choice = str(input("\nCampeão: ").strip().lower())
    champ = get_champ(choice)
    # Definição se o campeão está ou não no banco, e definição de vitória
    if champ:
        print(f"\n\033[0;32;45mCampeão encontrado!{d}")
        print("\nVenceu a partida? ")
        win = input("\nSim [1] | Não [0] ")
        win = True if win == "1" else False
        update_info(choice, win)
        print(f"\n\033[1;32;40mStatus atualizado!{d}")
    else:
        if choice == "":
            print("\nNão pode estar em branco!")
            return
        confirm = input("\nCampeão não encontrado, quer adicioná-lo? Sim [1] | Não [0] ")
        confirm = True if confirm == "1" else False
    
        if confirm:
            print(f"""\033[1;35;40m
Qual a lane? Escolha uma das opções!
[0] - top
[1] - jg
[2] - mid
[3] - adc
[4] - sup{d}""")
            option = input("Opção: ")
            match option:
                case "0":
                    lane = lane_list[0]
                case "1":
                    lane = lane_list[1]
                case "2":
                    lane = lane_list[2]
                case "3":
                    lane = lane_list[3]
                case "4":
                    lane = lane_list[4]
                case _:
                    print(f"\n\033[0;31;40mOpção inválida!{d}")
                    return
            print("\nVenceu a partida? ")
            win = input("\nSim [1] | Não [0] ")
            win = True if win == "1" else False
            create_champ(choice, lane, win)
            print(f"\n\033[1;32;40mCampeão adicionado com sucesso!{d}")
#!SECTION

#SECTION - Mostra as estatísticas dos campeões
def show_estastic():
    result, _ = get_all_champ()
    preferred_lane = {
        "top": 0,
        "jg" : 0,
        "mid": 0,
        "adc": 0,
        "sup": 0
    }
    if not result:
        print(f"\n\033[0;31;40mNenhum registro encontrado!{d}")
    else:
        print(f"\n\033[1;34;41m<-Campeões->{d}")
        for results in result:
            # Match para contar a lane mais jogada
            match results[0]:
                case "top":
                    preferred_lane["top"] += 1
                case "jg":
                    preferred_lane["jg"] += 1
                case "mid":
                    preferred_lane["mid"] += 1
                case "adc":
                    preferred_lane["adc"] += 1
                case "sup":
                    preferred_lane["sup"] += 1
            # Print para as estastísticas básicas
            print(
                f"""\033[1;38;47m
{results[1]} ({results[0]}){d}
-> Com \033[1;36;40m{results[2]}{d} pick(s) e \033[1;36;40m{results[3]}{d} vitória(s)
-> Win rate de {results[4]:.2f}%{d}
            """
            )
        # Mostrar o tanto que foi jogado em cada lane
        print(f"\n\033[1;34;41m<-Lanes->{d}")
        df = pd.DataFrame([preferred_lane])
        print(df.T.reset_index().to_string(index=False, header=False))
#!SECTION

#SECTION - Seleção para fazer o DELETE de um campeão
def champ_delete():
    choice = str(input("\nCampeão: ").strip().lower())
    champ = get_champ(choice)
    if not champ:
        print(f"\n\033[0;32;45mCampeão não encontrado!{d}")
    else:
        option = input(f"\n\033[0;32;45mCampeão encontrado!{d}\n\nTem certeza que deseja excluí-lo? Sim [1] | Não [0] ")
        option = True if option == "1" else False
        if option:
            delete_champ(choice)
            print(f"\n\033[1;33;40mCampeão deletado com sucesso!{d}")
        else:
            print(f"\n\033[0;31;40mOpção inválida!{d}")
            return
#!SECTION

#SECTION - Seleção para separar o ranking dos campeões
def champ_ranking():
    champs, columns = get_all_champ()
    df = pd.DataFrame(champs, columns=columns)
    df = df.drop(["lane", "picks"], axis=1)
    df = df.sort_values(by=["win", "win_rate"], ascending=False)
    pd.set_option("display.float_format", "{:.2f}".format)
    print(f"\n{df.to_string(index=False)}")

#!SECTION

if __name__ == "__main__":
    main()
