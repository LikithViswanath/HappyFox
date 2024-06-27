class ActionPerformer:
    def perform_action(self, email, action):
        if action == 'Mark as read':
            self._mark_as_read(email)
        elif action == 'Move Message':
            self._move_message(email)

    def _mark_as_read(self, email):
        print(f"Marking email {email.id} as read.")

    def _move_message(self, email):
        print(f"Moving email {email.id}.")
