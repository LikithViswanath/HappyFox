## Steps:

1. Run the init.bash file which takes care of creating venv and starting docker compose
    ```{console}
   bash init.bash
   ```
3. Run the mail_data_loader.py script to load data from gmail to DB.
    ```{console}
    python3 src/scripts/gmail_controller.py --flush True --limit 12
    ```
4. Run the rule_executor.py script to perform required actions.
    ```{console}
    python3 src/scripts/rule_action_controller.py --test_path src//rules.json
    ```**
