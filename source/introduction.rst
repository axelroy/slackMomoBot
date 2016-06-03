Introduction
===================================

Le projet propose une implémentation d'un bot Slack qui permet de gérer des votes. L'utilisateur peut créer une votation, dire quels sont les réponses possibles,
répondre à une votation. Seul le créateur d'un vote peut fermer la votation. Les commandes utilisateur sont les suivantes :

syntaxe : @momobot: [commande] [poll_title] [args]

Commande list :
   create --> create a new poll.
        Ex: @momobot: create love love me?
   show --> show a specific poll.
        Ex: @momobot: show love
   question --> you can change the question.
        Ex: @momobot: question love do you love me???
   choices --> to set answer posibilites(split with ;)
        Ex: @momobot: choices love yes!;no!;maybe
   start --> to lunch your poll you can answer only if the poll is lunch.
        Ex: @momobot: start love
   answer --> vote a choice by giving is id in arguments.
        Ex: @momobot: answer love 2
   close --> stop the poll that nobody can answer anymore.
        Ex: @momobot: close love
   remove --> destroy a specific poll.
        Ex: @momobot: remove love
