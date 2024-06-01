from langchain_core.runnables.base import Runnable


class ConditionalRunnable(Runnable):
    """
    A Runnable that conditionally decides whether to continue with the next steps in the chain
    or stop based on a provided condition function.
    """

    def __init__(self, condition, true_branch=None, false_branch=None):
        """
        Initializes the ConditionalRunnable.

        Args:
            condition (Callable): A function that takes an input and returns a boolean.
            true_branch (Optional[Runnable]): The runnable to execute if the condition is True.
            false_branch (Optional[Runnable]): The runnable to execute if the condition is False.
        """
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def invoke(self, input, config=None, **kwargs):
        """
        Invokes the ConditionalRunnable.

        Args:
            input: The input to the runnable.
            config (Optional[dict]): Configuration for the runnable.

        Returns:
            The output of the true_branch or false_branch runnable if executed, otherwise None.
        """
        if self.condition(input):
            if self.true_branch:
                return self.true_branch.invoke(input, config, **kwargs)
        else:
            if self.false_branch:
                return self.false_branch.invoke(input, config, **kwargs)
        # Optionally, return a specific value or raise an exception to indicate stopping.
        return None  # Or any other appropriate action for stopping the chain.
