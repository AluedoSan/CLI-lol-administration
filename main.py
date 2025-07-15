from db import init_db, update_info, get_champ, create_champ, show_estastic, delete_champ

d = "\033[m"
lane_list = ["top", "jg", "mid", "adc", "sup"]

#SECTION - Main para rodar as funções
def main():
    init_db()
    print(f"\033[0;30;41mBanco de dados inicializado.{d}")
    print(f"\033[1;32;43m⭐ Bem-Vindo a Summoner's Rift ⭐ {d}")
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
[3] - Sair{d} """)

        option = input("\nOpção: ")

        if option == "0":
            show_estastic()
        elif option == "1":
            champ_select()
        elif option == "2":
            champ_delete()
        elif option == "3":
            break
        else:
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
    else:
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
            if option == "0":
                lane = lane_list[0]
            elif option == "1":
                lane = lane_list[1]
            elif option == "2":
                lane = lane_list[2]
            elif option == "3":
                lane = lane_list[3]
            elif option == "4":
                lane = lane_list[4]
            else:
                print(f"\n\033[0;31;40mOpção inválida!{d}")
                return
            print("\nVenceu a partida? ")
            win = input("\nSim [1] | Não [0] ")
            win = True if win == "1" else False
            create_champ(choice, lane, win)
            print(f"\n\033[1;32;40mCampeão adicionado com sucesso!{d}")
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
            return
#!SECTION

if __name__ == "__main__":
    main()
