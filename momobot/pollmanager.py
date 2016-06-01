
#=============================================================
#   IMPORTS
#=============================================================


from poll import Poll


#=============================================================
#   DECORATORS
#=============================================================


def check_user_decorator(f):
    def _f(self, title, user, **kwargs):
        owner = self.poll_list.get(title, None)[0]

        if owner != user:
            return False, "You have not the right to edit this poll"

        return f(self, title, user, **kwargs)

    return _f


def check_poll_exist_decorator(f):
    def _f(self, title, user, **kwargs):
        user_poll = self.poll_list.get(title, None)

        if not user_poll:
            return False, "The poll \""+title+"\" does not exist"

        return f(self, title, user, **kwargs)

    return _f


#=============================================================
#   TOOLS
#=============================================================


def _create_choices_string(poll):
    i = 1
    l = []
    for c in poll.get_choices():
        l.append("\n  "+str(i)+") "+c)
        i += 1
    return "".join(l)


def _create_result_string(poll):
    i = 1
    l = []
    for r in poll.get_result():
        l.append("\n  "+str(i)+") "+r[0]+" (x"+str(r[1])+")")
        i += 1
    return "".join(l)


#=============================================================
#   CLASSES
#=============================================================


class PollManager():
    """
    Manage the the poll relative to user.

    All methods provide a output with a boolean (if the method succeded) and
    a string (which describe the error or the success)
    """

    def __init__(self):
        self.poll_list = {}

    def help(self):
        show = []
        show.append("Help :")
        show.append("\n syntaxe : @momobot: [commande] [poll_title] [args]")
        show.append("\n ")
        show.append("\n Commande list :")
        show.append("\n    create --> create a new poll. ")
        show.append("\n         Ex: @momobot: create love love me?")
        show.append("\n    show --> show a specific poll.")
        show.append("\n         Ex: @momobot: show love")
        show.append("\n    question --> you can change the question.")
        show.append("\n         Ex: @momobot: question love do you love me???")
        show.append("\n    choices --> to set answer posibilites(split with ;)")
        show.append("\n         Ex: @momobot: choices love yes!;no!;maybe")
        show.append("\n    start --> to lunch your poll you can answer only if the poll is lunch.")
        show.append("\n         Ex: @momobot: start love")
        show.append("\n    answer --> vote a choice by giving is id in arguments.")
        show.append("\n         Ex: @momobot: answer love 2")
        show.append("\n    close --> stop the poll that nobody can answer anymore.")
        show.append("\n         Ex: @momobot: close love")
        show.append("\n    remove --> destroy a specific poll.")
        show.append("\n         Ex: @momobot: remove love")

        return True, "".join(show)

    def create_poll(self, title, user, **kwargs):
        if title in self.poll_list:
            return False, "The poll already exist, remove it before"

        question = kwargs.get("question", "")
        choices = kwargs.get("choices", [])

        poll = (user, Poll(title))
        self.poll_list[title] = poll

        if question:
            poll[1].set_question(question)
        if choices:
            poll[1].set_choices(choices)

        return True, "The poll \""+title+"\" has been created"

    @check_poll_exist_decorator
    @check_user_decorator
    def remove_poll(self, title, user, **kwargs):
        self.poll_list.pop(title, None)

        return True, "The poll \""+title+"\" has been deleted"


    @check_poll_exist_decorator
    @check_user_decorator
    def set_question(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        poll.set_question(kwargs["question"])

        return True, "The question has been update"


    @check_poll_exist_decorator
    @check_user_decorator
    def set_choices(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        poll.set_choices(kwargs["choices"])

        return True, "The choices have been added"


    @check_poll_exist_decorator
    def answer_poll(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        try:
            number = int(kwargs["answer"])

            if poll.set_answer(user, number):
                return True, "Your answer has been registered"
            else:
                return False, "You can not answer to poll not started or closed"
        except ValueError:
            return False, "You must enter the number of the choice :" + _create_choices_string(poll)

    @check_poll_exist_decorator
    @check_user_decorator
    def close_poll(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        if poll.close():
            return True, "The poll \""+title+"\" has been closed"
        else:
            return False, "Can not close a poll which is not started"


    @check_poll_exist_decorator
    @check_user_decorator
    def start_poll(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        if poll.start():
            return True, "The poll \""+title+"\" has been started"
        else:
            return False, "Not enough choices for start"


    @check_poll_exist_decorator
    def show_poll(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)[1]

        show = []
        show.append("Poll : ")
        show.append(title)
        show.append("\n - Question : ")
        show.append(poll.get_question())
        show.append("\n - Choices : ")
        show.append(_create_choices_string(poll))
        show.append("\n - Result : ")
        show.append(_create_result_string(poll))
        show.append("\n - Status : ")
        show.append("Not start" if not poll.is_started() else "In progress" if not poll.is_closed() else "Closed")

        return True, "".join(show)
