import typing

class LLMChatHistory:
    """Class to handle chat history between user and LLM.
    
    Methods
    -------
    clear():
        Clear messages history.
    append(conversation_user, conversation_assistant):
        Append the message round to the history.
    """
    def __init__(self, context_history_limit: int = 5) -> None:
        """Initialise the chat history along with option to store how
        many previous messages.

        Parameters
        ----------
        context_history_limit : int (defualt: 5)
            How many previous messages of user-assistant to store.

        Returns
        -------
        None
        """
        self._history = list()
        self._context_history_limit = context_history_limit
    
    @property
    def history(self):
        """Get the entire conversation history."""
        return self._history

    def clear(self) -> None:
        """Clear the message history."""
        self._history = list()
    
    def append(
        self,
        conversation: str | typing.Dict,
        who_is: typing.Literal['user', 'assistant'] = 'user'
    ) -> None:
        """Append message round consisting of user and assistant messages
        to history.
        
        Parameters
        ----------
        conversation : str | dict
            The conversation by the user or assistant.
        
        who_is : str (default: 'user')
            Who is providing the message? 
            Accepted values are 'user' and 'assistant'
        
        Returns
        -------
        None
        """
        if len(self._history) > ((2 * self._context_history_limit)+1):
            # Pop twice to remove the user-assistant conversation round.
            self._history.pop(1)
            self._history.pop(1)
            # Notice we do pop(1) and not 0, as the 0th index contains the
            # system message.
        
        # Input validation to ensure proper history formatting.
        if isinstance(conversation, str):
            conversation = {
                'role': who_is,
                'content': conversation
            }
        self._history.append(
            conversation
        )


