#=============================================================
#   CLASSES
#=============================================================


class Poll():
    """
    Manage a simple poll.

    The life cycle of a poll is the follow:
    1) Not started : can set the questions, the choices and start the poll
    2) In progress : can answer to the poll and close the poll
    3) Closed : answers are closed, can get the result
    """

    def __init__(self, title, user):
        self.title = title
        self.user = user
        self.choices = []
        self.answers = {}
        self.closed = False
        self.started = False
        self.question = ""
