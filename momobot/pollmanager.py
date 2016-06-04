
#=============================================================
#   IMPORTS
#=============================================================


from poll import Poll
from collections import Counter


#=============================================================
#   DECORATORS
#=============================================================

def check_user_decorator(f):
    def _f(self, title, user, **kwargs):
        poll = self.poll_list.get(title, None)

        if user != poll.user:
            return "You have not the right to edit this poll"

        return f(self, title, user, **kwargs)

    return _f


def check_poll_exist_decorator(f):
    def _f(self, title, user, **kwargs):
        user_poll = self.poll_list.get(title, None)

        if not user_poll:
            return "The poll \""+title+"\" does not exist"

        return f(self, title, user, **kwargs)

    return _f


#=============================================================
#   TOOLS
#=============================================================


def _create_choices_string(poll):
    i = 1
    l = []
    for c in poll.choices:
        l.append("\n  "+str(i)+") "+c)
        i += 1
    return "".join(l)


def _create_result_string(poll):
    i = 1
    l = []
    c = Counter(poll.answers.values())
    #Classement par ordre de fréquence
    c_ordered = [(poll.choices[x[0]-1],x[1])  for x in c.most_common()]

    for r in c_ordered:
        l.append("\n  "+str(i)+") "+r[0]+" (x"+str(r[1])+")")
        i += 1
    return "".join(l)


#=============================================================
#   CLASSES
#=============================================================


class PollManager():
    '''
    Manage the the poll relative to user.

    All methods provide a output with a boolean (if the method succeded) and
    a string (which describe the error or the success)
    '''

    def __init__(self):
        self.poll_list = {}

    def help(self):
        '''
        Provides help to the user.
        '''

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
        '''
        Creates a poll with the parameters Title : User
        '''
        if title in self.poll_list:
            return "The poll already exist, remove it before"

        poll = Poll(title, user)
        self.poll_list[title] = poll

        poll.question = kwargs["question"]

        #set basic choices
        poll.choices = [":+1:",":-1:"]

        return "The poll \""+title+"\" has been created"

    @check_poll_exist_decorator
    @check_user_decorator
    def remove_poll(self, title, user, **kwargs):
        '''
        Removes a poll with the parameters Title : User
        '''
        self.poll_list.pop(title, None)

        return "The poll \""+title+"\" has been deleted"


    @check_poll_exist_decorator
    @check_user_decorator
    def set_question(self, title, user, **kwargs):
        '''
        Permits to set the questions given by the user.
        '''
        poll = self.poll_list.get(title, None)

        poll.question = kwargs["question"]

        return "The question has been update"


    @check_poll_exist_decorator
    @check_user_decorator
    def set_choices(self, title, user, **kwargs):
        '''
        Permits to set the choices that the voter can choose.
        '''
        poll = self.poll_list.get(title, None)

        if not poll.started :
            # force all value to be unique
            choices_list = set(kwargs["choices"])
            poll.choices = list(choices_list)
            return "The choices have been added"

        return "you can't change choices since the poll is started"



    @check_poll_exist_decorator
    def answer_poll(self, title, user, **kwargs):
        '''
        Allows the user to answer to a poll.
        '''
        poll = self.poll_list.get(title, None)
        try:
            if not poll.closed and poll.started:
                number = int(kwargs["answer"])
                if number in range(1, len(poll.choices)+1):
                    poll.answers[user] = number
                    return "Your answer has been registered"
                else :
                    return "Choose in the range of possible choices"
            else:
                return "You can not answer to poll not started or closed"
        except ValueError:
            return "You must enter the number of the choice :" + _create_choices_string(poll)

    @check_poll_exist_decorator
    @check_user_decorator
    def close_poll(self, title, user, **kwargs):
        '''
        Close the given poll.
        '''
        poll = self.poll_list.get(title, None)

        if not poll.started:
            return "The poll \""+title+"\" has been closed"
        else:
            return "Can not close a poll which is not started"


    @check_poll_exist_decorator
    @check_user_decorator
    def start_poll(self, title, user, **kwargs):
        '''
        Open the given poll.
        '''
        poll = self.poll_list.get(title, None)

        if not poll.started:
            poll.started = True
            return"The poll \""+title+"\" has been started"
        else:
            return "Not enough choices for start"


    def show_all_polls(self):
        '''
        Presents all the polls to the client the given poll to the client.
        '''

        if not self.poll_list :
            return "there is no created poll at the moment"

        show = []
        show.append("Polls : ")

        for current_poll in self.poll_list :
            show.append("\n     -  ")
            show.append((self.poll_list.get(current_poll)).title)
            show.append("(")
            show.append("Not start" if not (self.poll_list.get(current_poll)).started else "In progress" if not (self.poll_list.get(current_poll)).closed else "Closed")
            show.append(")")
            show.append(" --> ")
            show.append((self.poll_list.get(current_poll)).question)

        return "".join(show)


    @check_poll_exist_decorator
    def show_poll(self, title, user, **kwargs):
        '''
        Presents the given poll to the client.
        '''
        poll = self.poll_list.get(title, None)

        show = []
        show.append("Poll : ")
        show.append(title)
        show.append("\n - Question : ")
        show.append(poll.question)
        show.append("\n - Choices : ")
        show.append(_create_choices_string(poll))
        show.append("\n - Result : ")
        show.append(_create_result_string(poll))
        show.append("\n - Status : ")
        show.append("Not start" if not poll.started else "In progress" if not poll.closed else "Closed")

        return "".join(show)
