from controllers.email_controller import EmailController

if __name__ == '__main__':
    email_controller = EmailController('rules.json')
    email_controller.fetch_and_store_emails()
