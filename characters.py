from tkinter import IntVar

characters = [
    "Werewolf", "Wolf-Father", "Big Bad Wolf", "White Wolf", "Wolf-Hound", "Wild Child", "Villager", "Cupid",
    "Seer", "Sisters", "Little Girl", "Fox", "Rusty Knight", "Elder", "Witch", "Bear Tamer", "Hunter", "Piper",
    "Angel", "Idiot"
    ]

characterDescs = {"Choose Character": "Character Description",
                  "Werewolf": "Each night, the werewolves pick a player to kill. The victim can be anyone except the Moderator, including other werewolves. The next day, they pretend to be a villager and try to seem unsuspicious. The number of werewolves in a game varies depending on the number of players.",
                  "Wolf-Father": "It's a werewolf. Once in the game, he can transform the werewolves's victim into a werewolf. This one preserves his powers.",
                  "Big Bad Wolf": "It's a werewolf. But, until no wolf, wild child or dog wolf died, he wakes up again and eats another villager.",
                  "White Wolf": "His objective is to be the only survivor. He wakes up every night with the werewolves. But one night out of two, he wakes up and kills a werewolf.",
                  "Wolf-Hound": "At the beginning of the game, he can choose if he wants to be a simple villager or a werewolf.",
                  "Wild Child": "The wild child is a villager who, at the beginning of the game, chooses a player. If during the game this player dies, the wild child becomes a werewolf.",
                  "Villager": "They don't have any special power except thinking and the right to vote.",
                  "Cupid": "The first night, Cupid chooses two players and make them fall in love, then becomes a villager. If one dies, the other dies too. A lover can't vote against the other lover. If the lovers are a villager and a werewolf, their objective changes; they must eliminate all the players except them.",
                  "Seer": "Each night, she can discover the real identity of a player. She must help the other villagers but discreetly to not be found by werewolves.",
                  "Sisters": "They wake up on the night and exchange signs to decide of the decisions to take to save the village. They know who is her other sister and so can trust her.",
                  "Little Girl": "The little girl can secretly spy on the werewolves during their turn. If she is caught in the act, she dies instead of the victim. Because she will be scared to death, or depending on how you play the werewolves will kill her later on in the game. It is also possible for her to die immediately along with the victim and can not be saved.",
                  "Fox": "Each night, he can choose three players. If in these three players, there is at least one werewolf, the animator gives the fox a positive sign and he preserves his power. But, if there aren't werewolves in these three players, the animator gives the fox a negative sign and he loses his power.",
                  "Rusty Knight": "If he dies during the night, the first werewolf to his left dies the following morning.",
                  "Elder": "He can resist the first werewolf's attack, but if he is killed by the witch, the huntsman, or the villagers, the villagers lose their powers.",
                  "Witch": "She has two potions, one to save the werewolves's victim one to eliminate a player. She can only use each potion once during the game. She can use both potions during the same night. She can save herself if she has been attacked by the werewolves on the first night.",
                  "Bear Tamer": "If one of his two neighbours is a werewolf, the animator informs the bear tamer that he is next to a werewolf.",
                  "Hunter": "If he is killed by werewolves or eliminated by vote, he must kill a player of their choice.",
                  "Piper": "His objective is to charm all the players alive except him (he can't charm himself). Each night, he can charm two players that wake up and recognise with those of the nights before.",
                  "Angel": "His objective is to be killed by the villagers on the first day of vote. If he doesn't, he becomes a simple villager. If he/she does die on the first night, they win against the other players.",
                  "Idiot": "If he is chosen by the village to be eliminated, he stays alive, but he cannot vote anymore.",
                  }
