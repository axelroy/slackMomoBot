from collections import Counter


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
        self._title = title
        self.user = user
        self._choices = []
        self._answers = {}
        self._closed = False
        self._started = False
        self.question = ""

    def set_choices(self, choices_list):
        if not self._started :
            # force all value to be unique
            choices_list = set(choices_list)
            self._choices = list(choices_list)
            return True
        return False

    def get_choices(self):
        return self._choices

    def set_answer(self, user_name, number):
        if not self._closed and self._started:
            if number in range(1, len(self._choices)+1):
                self._answers[user_name] = number
                return True
        return False

    def get_answer(self, user_name):
        pass

    def close(self):
        if self._started:
            self._closed = True
            return True
        return False

    def is_closed(self):
        return self._closed

    def start(self):
        if len(self._choices) >= 2:
            self._started = True
            return True
        return False

    def is_started(self):
        return self._started

    def get_result(self):
        c = Counter(self._answers.values())
        return [(self._choices[x[0]-1],x[1])  for x in c.most_common()];
