# SnakeGame
recommended settings: 50 x 50, 10 snakes and 20 fruits.

Remember to click on fullscreen button because i tried to put -zoomed resolution and works fine on WSL Ubuntu but on CMD its give a bad attribute error.

To run this:
1. Open CMD
2. type "cd path_to_folder"
3. type "python main.py""pypy main.py"
4. (optional) instead of using doing step 3 type "pypy main.py" for a more fluid experience

The game will have a custom map size, snake quantity, fruit generators and an algorithm to make snakes move to fruits, avoid walls and avoid bodies of other snakes.

Snakes gonna have random colors and i will add some colors schemes for scenario.

The fruits will have a parameter to define if the color should be static according to scenario color scheme or random colors.

I plan to add a maze generator with a parameter to set how "closed" the maze gonna be, at minimum it's gonna be a open area with only border walls.

The game will end when theres only 1 snake alive.

Still being developed.

Done for now, the algorithm to move snakes isn't too good and tkinter rendering is very slow but you can still see its working.

## Contributing
