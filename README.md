# Pirates Total
 
cool pirates taking over the carribean world
steer your skiff to different coastal cities and try to raid them.
manage and grow your crew, your food and your economy.
become the mightiest pirate.

## Requirements

This project uses a virtual environment to manage dependencies.

### Setup Instructions

1. Clone the repository, either by git:
   ```bash
   gh repo clone bertilegh/Pirates-Total
   cd my_project
   ```
   or by web browser: https://github.com/bertilegh/Pirates-Total/archive/refs/heads/main.zip
   If you download it via web browser you have to unzip the file contents.
2. Activate the virutal environment:
    On Windows:
    ```bash
    myenv\Scripts\activate
    ```
3. Run the game:
    ```bash
    python main.py
    ```

Make sure to deactive the virutal environment when you're done.

## Todo:



    Collision Detection and Response:
        [x] Implement collision detection between the ship and the box. You can use Pymunk's built-in collision handling to respond to collisions, such as stopping the ship or bouncing it off the box.

    User Interface (UI):
        Add a simple UI to display the ship's speed, direction, or other relevant information. You can use Pygame's font rendering capabilities to draw text on the screen.

    Multiple Obstacles:
        Create more obstacles or boxes in the game world. You can randomly generate their positions or allow the player to place them.

    Boundaries:
        Implement boundaries for the game area. If the ship moves outside a certain area, you can either stop it or wrap it around to the other side of the screen.

    Background and Environment:
        [x] (WIP) Add a background image or tiles to create a more immersive environment. You could also add water effects or other environmental elements.

    Class Organization:
        Separating the classes into different files/modules. This will make the codebase more manageable and easier to navigate as it grows.

    Sound Effects and Music:
        [x] (WIP) Incorporate sound effects for actions like moving, colliding, or background music to enhance the gaming experience.

    Game Objectives:
        Introduce objectives or goals for the player, such as collecting items, reaching a destination, or avoiding obstacles.

    Improved Ship Control:
        Refine the ship's movement mechanics. You could implement acceleration and deceleration for a more realistic feel, or add a turning speed limit.

    Camera System:
        Implement a more advanced camera system that can follow the ship smoothly, perhaps with some easing or damping effects.

    Game States:
        Create different game states (e.g., main menu, pause, game over) to manage the flow of the game better.

    Save and Load Game:
        Implement functionality to save and load game states, allowing players to continue from where they left off.

    Player Input Handling:
        Improve input handling to allow for smoother controls, such as using a joystick or gamepad.
