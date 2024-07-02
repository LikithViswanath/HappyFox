## Youtube Demo and Walk-through:
    https://youtu.be/arBChAwX_rc

## Steps:

0. Prerequisites
   ```{console}
   git, docker-compose, python, google-cloud credentials.json file  
   ```

1. Clone the Project Using git ( Ensure Git is installed ), once Cloning of the project is finished, change directory to HappyFox and place the credentials.json file in the HappyFox directory.
    ```{console}
   git clone https://github.com/LikithViswanath/HappyFox.git
   cd HappyFox
   ```
2. Create and Activate Virtual Environment
    ```{console}
   python3 -m venv virtual-env
   source virtual-env/bin/activate
   ```
3. Install Requirements for the Project
    ```{console}
   pip3 install -r requirements.txt
   ```
4. Set up the Python Path
    ```{console}
    export PYTHONPATH=$PYTHONPATH:./
    ```
5. Set up the database connection using Docker compose ( docker-compose is installed )
    ```{console}
    docker-compose -f docker-compose.yaml up -d
    ```
6. Run the below python script to load data from your gmail to MySql DataBase.
    ```{console}
    python3 src/scripts/gmail_controller.py --flush True --limit 12
    ```
7. Run the below python script to perform the rules setup in rules.json or create a custom rules.
    ```{console}
    python3 src/scripts/rule_action_controller.py --test_path src/config/rules.json
    ```