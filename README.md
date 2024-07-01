## Steps:

1. Clone the Project Using git ( Ensure Git is installed ), once Cloning of the project is finished, change directory to HappyFox
    ```{console}
   git clone https://github.com/your-username/HappyFox.git
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
6. Run the mail_data_loader.py script to load data from gmail to DB.
    ```{console}
    python3 src/scripts/gmail_controller.py --flush True --limit 12
    ```
7. Run the rule_executor.py script to perform required actions.
    ```{console}
    python3 src/scripts/rule_action_controller.py
    ```