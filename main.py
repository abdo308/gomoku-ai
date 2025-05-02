import Game
x=Game.Game()
choice=input(("Enter the mode:\n 1. Player vs AI\n 2. AI vs AI\n"))

if choice=='1':
    piece = ''
    while piece != 'X' and piece != 'O':
        piece = input("Choose your piece (X or O): ").upper()
    
    x.play(piece,choice)
elif choice=='2':
    x.play(choice)
