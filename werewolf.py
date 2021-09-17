from tkinter import *
from characters import characters, characterDescs
from collections import defaultdict as dd


class Werewolf:
    def __init__(self):
        root = Tk()
        root.title("Werewolf")
        frame = Frame(root)
        frame.pack()
        self.__root = root

        self.__helpInProgress = False
        self.__setupInProgress = False
        self.__loadInProgress = False
        self.__gameInProgress = False

        self.__numPlayers = StringVar()
        self.__numVillager = StringVar()
        self.__numWolves = StringVar()

        self.__cbWolffather = IntVar()
        self.__cbBigbadwolf = IntVar()
        self.__cbWhitewolf = IntVar()
        self.__cbWolfhound = IntVar()
        self.__cbWildchild = IntVar()
        self.__cbCupid = IntVar()
        self.__cbSeer = IntVar()
        self.__cbSisters = IntVar()
        self.__cbLittlegirl = IntVar()
        self.__cbFox = IntVar()
        self.__cbRustyknight = IntVar()
        self.__cbElder = IntVar()
        self.__cbWitch = IntVar()
        self.__cbBeartamer = IntVar()
        self.__cbHunter = IntVar()
        self.__cbPiper = IntVar()
        self.__cbAngel = IntVar()
        self.__cbIdiot = IntVar()

        self.__charCBs = {}
        self.__characters = characters
        self.__charDescs = characterDescs
        self.__variables = [
            self.__cbWolffather, self.__cbBigbadwolf, self.__cbWhitewolf, self.__cbWolfhound, self.__cbWildchild,
            self.__cbCupid, self.__cbSeer, self.__cbSisters, self.__cbLittlegirl, self.__cbFox, self.__cbRustyknight,
            self.__cbElder, self.__cbWitch, self.__cbBeartamer, self.__cbHunter, self.__cbPiper, self.__cbAngel, self.__cbIdiot]
        count = 0
        for character in self.__characters:
            if character != "Werewolf" and character != "Villager":
                self.__charCBs[character] = self.__variables[count]
                count += 1

        Label(frame, text='Werewolf', font='{Copperplate Gothic Bold} 24').pack(fill=X, pady=25, padx=25)
        Button(frame, text='Game Setup', command=self._setup, font='{Copperplate Gothic Light}').pack(fill=X, pady=5, padx=10)
        Button(frame, text='Load Setup', command=self._load, font='{Copperplate Gothic Light}').pack(fill=X, pady=5, padx=10)
        Button(frame, text='Character Info', command=self._charHelp, font='{Copperplate Gothic Light}').pack(fill=X, pady=5, padx=10)
        Button(frame, text='Quit', command=self._quit, font='{Copperplate Gothic Light}').pack(fill=X, pady=5, padx=10)

    def _setup(self):
        if not (self.__setupInProgress or self.__loadInProgress or self.__gameInProgress):
            self.__setupInProgress = True
            setupWin = Toplevel(self.__root)
            setupWin.title("Setup")
            frame = Frame(setupWin)
            self.__setupWin = setupWin

            self.__sistersPresent = False

            self.nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            self.__numPlayers.set(f'Player Count: 0')
            self.__numVillager.set("0")
            self.__numWolves.set("0")

            for variable in self.__variables:
                variable.set(0)

            Grid.columnconfigure(frame, 0, weight=1)
            Grid.rowconfigure(frame, 0, weight=1)
            frame.grid(row=0, column=0, sticky=N+S+W+E)

            Label(frame, text='Setup', font='{Copperplate Gothic Bold} 24').grid(row=0, column=0, columnspan=3, sticky=N+S+W+E)
            Label(frame, text='Special Characters', font='{Copperplate Gothic Bold} 20').grid(row=1, column=0, columnspan=3, sticky=N+S+W+E)

            count = 0
            for character in self.__characters:
                if character != "Werewolf" and character != "Villager":
                    Checkbutton(frame, text=character, font='{Copperplate Gothic Light} 14', variable=self.__variables[count], onvalue=1, offvalue=0, command=self.__updatePlayerCount).grid(row=(count // 3) + 2, column=count % 3, sticky=N+S+W, padx=15, pady=1)
                    count += 1
            lastRow = (count - 1) // 3 + 2

            Label(frame, text="Villagers:", font='{Copperplate Gothic Bold}').grid(row=lastRow + 1, column=0, sticky=S, pady=1, padx=10)
            villagerDropdown = OptionMenu(frame, self.__numVillager, *self.nums, command=self.__updatePlayerCount)
            villagerDropdown.config(font="{Copperplate Gothic Light}")
            villagerDropdown.grid(row=lastRow + 2, column=0, sticky=N, pady=1, padx=10)

            Label(frame, textvariable=self.__numPlayers, font='{Copperplate Gothic Bold}').grid(row=lastRow + 1, column=1, sticky=N+S+W+E, pady=1, padx=10)

            Label(frame, text="Wolves:", font='{Copperplate Gothic Bold}').grid(row=lastRow + 1, column=2, sticky=S, pady=1, padx=10)
            wolvesDropdown = OptionMenu(frame, self.__numWolves, *self.nums, command=self.__updatePlayerCount)
            wolvesDropdown.config(font="{Copperplate Gothic Light}")
            wolvesDropdown.grid(row=lastRow + 2, column=2, sticky=N, pady=1, padx=10)

            Button(frame, text='Play', command=self._playGame, font='{Copperplate Gothic Light}').grid(row=lastRow + 2, column=1, sticky=N+S+W+E, pady=1, padx=10)
            self.__gameName = StringVar()
            self.__gameName.set("Set Preset Name")
            Entry(frame, textvariable=self.__gameName).grid(row=lastRow + 3, column=0, sticky=N+S+W+E, pady=2, padx=10)
            Button(frame, text='Save', command=self._savePreset, font='{Copperplate Gothic Light}').grid(row=lastRow + 3, column=1, sticky=N+S+W+E, pady=2, padx=10)
            Button(frame, text='Back', command=self._dismissSetup, font='{Copperplate Gothic Light}').grid(row=lastRow + 3, column=2, sticky=N+S+W+E, pady=2, padx=10)

    def _playGame(self):
        if not self.__gameInProgress:
            self.__gameInProgress = True
            gameWin = Toplevel(self.__root)
            gameWin.title("Werewolf")
            frame = Frame(gameWin)
            frame.pack()
            self.__gameWin = gameWin

            if self.__setupInProgress:
                self._dismissSetup()
            if self.__cbSisters.get() == 1:
                self.__sistersPresent = True
            else:
                self.__sistersPresent = False

            self.__trackers = []
            self.__toClear = []
            self.__playerRoles = dd(lambda: None)
            self.__charmedPlayers = set()
            self.__loverPlayers = ()
            self.__bad = []
            self.__good = []
            self.__dead = []

            self.__infection = False
            self.__converted = False
            self.__wolfDead = False
            self.__foxPower = True
            self.__elderPower = True
            self.__poisonPotion, self.__healingPotion = True, True

            self.__convertedPlayer = ""
            self.__wolfHoundWolf = IntVar()
            self.__wolfHoundWolf.set(0)

            self.__witchHeal = StringVar()
            self.__witchHeal.set("Enter Witch Revive")
            self.__witchVictim = StringVar()
            self.__witchVictim.set("Enter Witch Victim")
            self.__roleModel = StringVar()
            self.__roleModel.set("Enter Role Model")
            self.__angelPlayer = StringVar()
            self.__angelPlayer.set("Enter Angel Name")
            self.__rustyKnightPlayer = StringVar()
            self.__rustyKnightPlayer.set("Enter Rusty Knight Name")
            self.__hunterPlayer = StringVar()
            self.__hunterPlayer.set("Enter Hunter Name")
            self.__elderPlayer = StringVar()
            self.__elderPlayer.set("Enter Elder Name")
            self.__cupidPlayer = StringVar()
            self.__cupidPlayer.set("Enter Cupid Name")
            self.__knightVictim = StringVar()
            self.__knightVictim.set("Enter Infected Wolf Name")
            self.__loverOne = StringVar()
            self.__loverTwo = StringVar()
            self.__loverOne.set("Enter First Lover")
            self.__loverTwo.set("Enter Second Lover")
            self.__bigbadwolfVictim = StringVar()
            self.__bigbadwolfVictim.set("Enter Big Bad Wolf Victim")
            self.__wolfVictim = StringVar()
            self.__wolfVictim.set("Enter Wolf Victim")
            self.__whitewolfVictim = StringVar()
            self.__whitewolfVictim.set("Enter White Wolf Victim")
            self.__villageVictim = StringVar()
            self.__villageVictim.set("Enter Victim")
            self.__hunterVictim = StringVar()
            self.__hunterVictim.set("Enter Victim")

            self.__updatePlayerCount()
            self.__wolfCount = self.__cbWolffather.get() + self.__cbBigbadwolf.get() + self.__cbWhitewolf.get() + int(self.__numWolves.get())
            self.__villageCount = self.__playerCount - self.__wolfCount

            self.__characterCalls = []
            self.__characterCalls.append(self.__initialisePlayers)
            self.__characterCalls.append(self.__sheriffElection)
            self.__bad.append("Werewolf")
            if self.__cbLittlegirl.get() == 1:
                self.__good.append("Little Girl")
            if self.__cbAngel.get() == 1:
                self.__characterCalls.append(self.__angel)
                self.__good.append("Angel")
            if self.__cbRustyknight.get() == 1:
                self.__good.append("Rusty Knight")
                self.__characterCalls.append(self.__rustyKnight)
            if self.__cbHunter.get() == 1:
                self.__good.append("Hunter")
                self.__characterCalls.append(self.__hunter)
            if self.__cbIdiot.get() == 1:
                self.__good.append("Idiot")
            if self.__cbElder.get() == 1:
                self.__good.append("Elder")
                self.__characterCalls.append(self.__elder)
            # proceed time
            self.__characterCalls.append(self.__proceedTime)
            # add cupid call
            if self.__cbCupid.get() == 1:
                self.__characterCalls.append(self.__cupid)
                self.__characterCalls.append(self.__lovers)
                self.__good.append("Cupid")
            # add sisters call
            if self.__cbSisters.get() == 1:
                self.__characterCalls.append(self.__sister)
                self.__good.append("Sisters")
            # add wild child call
            if self.__cbWildchild.get() == 1:
                self.__characterCalls.append(self.__wildChild)
                self.__good.append("Wild Child")
            # add wolf hound call
            if self.__cbWolfhound.get() == 1:
                self.__characterCalls.append(self.__wolfHound)
            # add bear tamer call
            if self.__cbBeartamer.get() == 1:
                self.__characterCalls.append(self.__bearTamer)
                self.__good.append("Bear Tamer")
            # add seer call
            if self.__cbSeer.get() == 1:
                self.__characterCalls.append(self.__seer)
                self.__good.append("Seer")
            # add werewolves call
            self.__characterCalls.append(self.__wolves)
            # add wolf father call
            if self.__cbWolffather.get() == 1:
                self.__characterCalls.append(self.__wolfFather)
                self.__bad.append("Wolf-Father")
            # add white werewolf call (every other night)
            if self.__cbWhitewolf.get() == 1:
                self.__characterCalls.append(self.__whiteWolf)
                self.__bad.append("White Wolf")
            # add big bad wolf call (if no wolves dead)
            if self.__cbBigbadwolf.get() == 1:
                self.__characterCalls.append(self.__bigBadWolf)
                self.__bad.append("Big Bad Wolf")
            # add witch call
            if self.__cbWitch.get() == 1:
                self.__characterCalls.append(self.__witch)
                self.__good.append("Witch")
            # add fox call
            if self.__cbFox.get() == 1:
                self.__characterCalls.append(self.__fox)
                self.__good.append("Fox")
            # add piper call
            if self.__cbPiper.get() == 1:
                self.__characterCalls.append(self.__piper)
                self.__good.append("Piper")
                # add charmed call
                self.__characterCalls.append(self.__charmed)
            if self.__cbRustyknight.get() == 1:
                self.__characterCalls.append(self.__rustyKnightCheck)
            # proceed time
            self.__characterCalls.append(self.__proceedTime)
            # victims revealed
            self.__characterCalls.append(self.__victims)
            # bear's grunt
            if self.__cbBeartamer.get() == 1:
                self.__characterCalls.append(self.__bearGrunt)
            # debate
            self.__characterCalls.append(self.__debate)
            # vote
            self.__characterCalls.append(self.__vote)

            self.__dayNight = StringVar()
            self.__section = StringVar()
            self.__narration = StringVar()

            self.__dayNight.set("Day 1")
            self.__dayCount = 1
            self.__day = True

            self.__section.set("Player Entry")
            self.__narration.set("Before the game begins, the narrator must enter the name of each player:")

            Label(frame, textvariable=self.__dayNight, font='{Copperplate Gothic Bold} 18').pack(fill=X)
            Label(frame, textvariable=self.__section, font='{Copperplate Gothic Bold}').pack(fill=X)
            Label(frame, textvariable=self.__narration, font='{Copperplate Gothic Light}', wraplength=500, padx=10, pady=10).pack(fill=X)

            self.__playerEntries = []
            for num in range(self.__playerCount):
                player = StringVar()
                player.set(f"Enter player {num + 1} name")
                playerEntry = Entry(self.__gameWin, textvariable=player)
                playerEntry.pack(fill=X)
                self.__playerEntries.append(player)
                self.__toClear.append(playerEntry)

            self.__proceedButton = Button(self.__gameWin, text='Proceed', command=self._nextCall, font='{Copperplate Gothic Light}')
            self.__trackLabel = Label(self.__gameWin, text='Trackers:', font='{Copperplate Gothic Bold}')
            self.__aliveCount = StringVar()
            self.__aliveCount.set(f'Player Count: {self.__playerCount}, Villager Count: {self.__villageCount}, Wolf Count: {self.__wolfCount}')
            self.__countTracker = Label(self.__gameWin, textvariable=self.__aliveCount, font='{Copperplate Gothic Light}')
            self.__trackers.append(self.__countTracker)
            self.__endButton = Button(self.__gameWin, text='End', command=self._dismissGame, font='{Copperplate Gothic Light}')
            self.__packWin()

    def __updateCountTracker(self):
        self.__aliveCount.set(f'Player Count: {self.__playerCount}, Villager Count: {self.__villageCount}, Wolf Count: {self.__wolfCount}')

    def _nextCall(self):
        self.__clearWin()
        self.__characterCalls[0]()

    def __proceedTime(self):
        if self.__day:
            self.__day = False
            self.__dayNight.set(f"Night {self.__dayCount}")
        else:
            self.__day = True
            self.__dayCount += 1
            self.__dayNight.set(f"Day {self.__dayCount}")
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)
        self._nextCall()

    def __initialisePlayers(self):
        self.__playerNames = []
        self.__alive = set()
        for player in self.__playerEntries:
            self.__alive.add(player.get())
            self.__playerNames.append(player.get())
        self.__alivePlayers = StringVar()
        self.__updateAliveTracker()
        self.__aliveTracker = Label(self.__gameWin, textvariable=self.__alivePlayers, font='{Copperplate Gothic Light}')
        self.__trackers.append(self.__aliveTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __updateAliveTracker(self):
        aliveMsg = "Alive: "
        for player in self.__alive:
            aliveMsg += f"{player}, "
        self.__alivePlayers.set(f'{aliveMsg[:-2]}')

    def __sheriffElection(self):
        self.__section.set("The Election")
        self.__narration.set("The town must now elect a sheriff")
        self.__sheriff = StringVar()
        self.__sheriff.set("Enter Sheriff Name")
        self.__sheriffEntry = OptionMenu(self.__gameWin, self.__sheriff, *self.__playerNames)
        self.__sheriffEntry.pack(fill=X)
        self.__toClear.append(self.__sheriffEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackSheriff)

    def __trackSheriff(self):
        if self.__dayCount == 1:
            self.__sheriffMsg = StringVar()
            self.__sheriffMsg.set(f'Sheriff: {self.__sheriff.get()}')
            self.__sheriffTracker = Label(self.__gameWin, textvariable=self.__sheriffMsg, font='{Copperplate Gothic Light}')
            self.__trackers.append(self.__sheriffTracker)
        self.__sheriffMsg.set(f'Sheriff: {self.__sheriff.get()}')
        self.__characterCalls.pop(0)
        self._nextCall()

    def __angel(self):
        self.__section.set("A Celestial Welcome")
        self.__narration.set("The angel wakes up and make themself known to the narrator.")
        self.__angelEntry = OptionMenu(self.__gameWin, self.__angelPlayer, *self.__playerNames)
        self.__angelEntry.pack(fill=X)
        self.__toClear.append(self.__angelEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackAngel)

    def __trackAngel(self):
        self.__angelTracker = Label(self.__gameWin, text=f'Angel: {self.__angelPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__angelPlayer.get()] = "Angel"
        self.__trackers.append(self.__angelTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __rustyKnight(self):
        self.__section.set("A Rusty Start")
        self.__narration.set("The rusty knight wakes up and makes themself known to the narrator.")
        self.__rustyKnightEntry = OptionMenu(self.__gameWin, self.__rustyKnightPlayer, *self.__playerNames)
        self.__rustyKnightEntry.pack(fill=X)
        self.__toClear.append(self.__rustyKnightEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackRustyKnight)

    def __trackRustyKnight(self):
        self.__rkTracker = Label(self.__gameWin, text=f'Rusty Knight: {self.__rustyKnightPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__rustyKnightPlayer.get()] = "Rusty Knight"
        self.__trackers.append(self.__rkTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __elder(self):
        self.__section.set("Bingo Night")
        self.__narration.set("The elder wakes up and makes themself known to the narrator.")
        self.__elderEntry = OptionMenu(self.__gameWin, self.__elderPlayer, *self.__playerNames)
        self.__elderEntry.pack(fill=X)
        self.__toClear.append(self.__elderEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackElder)

    def __trackElder(self):
        self.__elderTracker = Label(self.__gameWin, text=f'Elder: {self.__elderPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__elderPlayer.get()] = "Elder"
        self.__trackers.append(self.__elderTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __hunter(self):
        self.__section.set("Hunting Hour")
        self.__narration.set("The hunter wakes up and makes themself known to the narrator.")
        self.__hunterEntry = OptionMenu(self.__gameWin, self.__hunterPlayer, *self.__playerNames)
        self.__hunterEntry.pack(fill=X)
        self.__toClear.append(self.__hunterEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackHunter)

    def __trackHunter(self):
        self.__hunterTracker = Label(self.__gameWin, text=f'Hunter: {self.__hunterPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__hunterPlayer.get()] = "Hunter"
        self.__trackers.append(self.__hunterTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __cupid(self):
        self.__section.set("Cupid's Setup")
        self.__narration.set("Cupid will now wake up and select two lovers, the lovers will be tapped so they know who they are.")
        self.__cupidEntry = OptionMenu(self.__gameWin, self.__cupidPlayer, *self.__playerNames)
        self.__cupidEntry.pack(fill=X)
        self.__loverOneEntry = OptionMenu(self.__gameWin, self.__loverOne, *self.__playerNames)
        self.__loverTwoEntry = OptionMenu(self.__gameWin, self.__loverTwo, *self.__playerNames)
        self.__loverOneEntry.pack(fill=X)
        self.__loverTwoEntry.pack(fill=X)
        self.__toClear.append(self.__cupidEntry)
        self.__toClear.append(self.__loverOneEntry)
        self.__toClear.append(self.__loverTwoEntry)
        self.__packWin()
        self.__characterCalls.pop(0)

    def __lovers(self):
        self.__section.set("Lovers Awake")
        self.__narration.set("The lovers wake up and identify each other, when one lover dies both lovers die.")
        self.__cupidTracker = Label(self.__gameWin, text=f'Cupid: {self.__cupidPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__cupidPlayer.get()] = "Cupid"
        self.__trackers.append(self.__cupidTracker)
        self.__loverPlayers = (self.__loverOne.get(), self.__loverTwo.get())
        self.__loverTracker = Label(self.__gameWin, text=f'Lovers: {self.__loverOne.get()} & {self.__loverTwo.get()}', font='{Copperplate Gothic Light}')
        self.__trackers.append(self.__loverTracker)
        self.__packWin()
        self.__characterCalls.pop(0)

    def __sister(self):
        self.__section.set("Sisters Awake")
        self.__narration.set("The sisters awake and acknowledge each other. They know that neither one of them is a wolf so can trust each other. The sisters can attempt to sign to each other to devise a method to save the village.")
        self.__sisterOnePlayer = StringVar()
        self.__sisterOnePlayer.set("Enter First Sister Name")
        self.__sisterTwoPlayer = StringVar()
        self.__sisterTwoPlayer.set("Enter Second Sister Name")
        self.__sisterOneEntry = OptionMenu(self.__gameWin, self.__sisterOnePlayer, *self.__playerNames)
        self.__sisterOneEntry.pack(fill=X)
        self.__sisterTwoEntry = OptionMenu(self.__gameWin, self.__sisterTwoPlayer, *self.__playerNames)
        self.__sisterTwoEntry.pack(fill=X)
        self.__toClear.append(self.__sisterOneEntry)
        self.__toClear.append(self.__sisterTwoEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackSisters)

    def __trackSisters(self):
        self.__sisterTracker = Label(self.__gameWin, text=f'Sisters: {self.__sisterOnePlayer.get()} & {self.__sisterTwoPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__sisterOnePlayer.get()] = "Sisters"
        self.__playerRoles[self.__sisterTwoPlayer.get()] = "Sisters"
        self.__trackers.append(self.__sisterTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __wildChild(self):
        self.__section.set("The Role Model")
        self.__narration.set("The wild child awakes. The wild child select a role model. When the wild child's role model dies, the child becomes vicious and join the pack of wolves.")
        self.__wcPlayer = StringVar()
        self.__wcPlayer.set("Enter Wild Child Name")
        self.__wcEntry = OptionMenu(self.__gameWin, self.__wcPlayer, *self.__playerNames)
        self.__wcEntry.pack(fill=X)
        self.__roleModelEntry = OptionMenu(self.__gameWin, self.__roleModel, *self.__playerNames)
        self.__roleModelEntry.pack(fill=X)
        self.__toClear.append(self.__wcEntry)
        self.__toClear.append(self.__roleModelEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackRoleModel)

    def __trackRoleModel(self):
        self.__wcTracker = Label(self.__gameWin, text=f'Wild Child: {self.__wcPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__trackers.append(self.__wcTracker)
        self.__rmTracker = Label(self.__gameWin, text=f'Role Model: {self.__roleModel.get()}', font='{Copperplate Gothic Light}')
        self.__trackers.append(self.__rmTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __wolfHound(self):
        self.__section.set("The Wild Card")
        self.__narration.set("The wolf hound wakes up and lets the narrator identify them. If the wolf hound is more wolf than hound then they must hold their hand up. They are now apart of the wolf pack. Otherwise, the wolf hound must not raise a hand, they remain a villager.")
        self.__whPlayer = StringVar()
        self.__whPlayer.set("Enter Wolf-Hound Name")
        self.__whEntry = OptionMenu(self.__gameWin, self.__whPlayer, *self.__playerNames)
        self.__whEntry.pack(fill=X)
        self.__wolfHoundCheckbox = Checkbutton(self.__gameWin, text='Tick if Wolf', font='{Copperplate Gothic Light}', variable=self.__wolfHoundWolf, onvalue=1, offvalue=0)
        self.__wolfHoundCheckbox.pack(fill=X)
        self.__toClear.append(self.__whEntry)
        self.__toClear.append(self.__wolfHoundCheckbox)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackWolfHound)

    def __trackWolfHound(self):
        self.__whTracker = Label(self.__gameWin, text=f'Wolf-Hound: {self.__whPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__whPlayer.get()] = "Wolf-Hound"
        self.__trackers.append(self.__whTracker)
        if self.__wolfHoundWolf.get() == 1:
            self.__wolfCount += 1
            self.__villageCount -= 1
            self.__bad.append("Wolf-Hound")
        else:
            self.__good.append("Wolf-Hound")
        self.__characterCalls.pop(0)
        self._nextCall()

    def __bearTamer(self):
        self.__section.set("Bear Tamer Identification")
        self.__narration.set("The bear tamer wakes up and make themself known to the narrator. This is so that the narrator can see if there are wolves adjacent to the bear tamer.")
        self.__btPlayer = StringVar()
        self.__btPlayer.set("Enter Bear Tamer Name")
        self.__btEntry = OptionMenu(self.__gameWin, self.__btPlayer, *self.__playerNames)
        self.__btEntry.pack(fill=X)
        self.__toClear.append(self.__btEntry)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__trackBear)

    def __trackBear(self):
        self.__btTracker = Label(self.__gameWin, text=f'Bear Tamer: {self.__btPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__btPlayer.get()] = "Bear Tamer"
        self.__trackers.append(self.__btTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __seer(self):
        if self.__cbSeer.get() == 1:
            self.__section.set("The Seer")
            self.__narration.set("The seer wakes up and chooses a player. This player's role is revealed to the seer.")
            if self.__dayCount == 1:
                self.__seerPlayer = StringVar()
                self.__seerPlayer.set("Enter Seer Name")
                self.__seerEntry = OptionMenu(self.__gameWin, self.__seerPlayer, *self.__playerNames)
                self.__seerEntry.pack(fill=X)
                self.__toClear.append(self.__seerEntry)
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
            if self.__dayCount == 1:
                self.__characterCalls.insert(0, self.__trackSeer)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __trackSeer(self):
        self.__seerTracker = Label(self.__gameWin, text=f'Seer: {self.__seerPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__seerPlayer.get()] = "Seer"
        self.__trackers.append(self.__seerTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __wolves(self):
        self.__section.set("The Hunt Begins")
        self.__narration.set("The wolf pack wakes up and choose their victim.")
        self.__wolfVictimEntry = OptionMenu(self.__gameWin, self.__wolfVictim, *self.__playerNames)
        self.__wolfVictimEntry.pack(fill=X)
        self.__toClear.append(self.__wolfVictimEntry)
        self.__packWin()
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)
        if not self.__infection:
            self.__characterCalls.insert(0, self.__rustyKnightCheck)

    def __wolfFather(self):
        if (not self.__converted and self.__cbWolffather.get() == 1) and self.__playerRoles[self.__wolfVictim.get()] != "Rusty Knight":
            self.__section.set("The Wolf-Father")
            self.__narration.set("The wolf-father wakes up and chooses if he wants to convert the werewolves' victim. If the victim is converted, they will be tapped on their head. The converted victim keeps their power.")
            if self.__dayCount == 1:
                self.__wfPlayer = StringVar()
                self.__wfPlayer.set("Enter Wolf-Father Name")
                self.__wfEntry = OptionMenu(self.__gameWin, self.__wfPlayer, *self.__playerNames)
                self.__wfEntry.pack(fill=X)
                self.__toClear.append(self.__wfEntry)
            self.__convert = IntVar()
            self.__convert.set(0)
            self.__convertCheckbox = Checkbutton(self.__gameWin, text='Convert Victim To Wolf?', font='{Copperplate Gothic Light}', variable=self.__convert, onvalue=1, offvalue=0)
            self.__convertCheckbox.pack(fill=X)
            self.__toClear.append(self.__convertCheckbox)
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
            self.__characterCalls.insert(0, self.__wfHandle)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __wfHandle(self):
        if self.__dayCount == 1:
            self.__wfTracker = Label(self.__gameWin, text=f'Wolf-Father: {self.__wfPlayer.get()}', font='{Copperplate Gothic Light}')
            self.__playerRoles[self.__wfPlayer.get()] = "Wolf-Father"
            self.__trackers.append(self.__wfTracker)
        if self.__convert.get() == 1:
            self.__converted = True
            self.__convertedPlayer = self.__wolfVictim.get()
            self.__wolfVictim.set("")
            self.__villageCount -= 1
            self.__wolfCount += 1
        else:
            self.__convertedPlayer = ""
        self.__characterCalls.pop(0)
        self._nextCall()

    def __whiteWolf(self):
        self.__section.set("A Traitor Awakens")
        self.__narration.set("The white wolf wakes up and kills another wolf.")
        called = self.__characterCalls.pop(0)
        if self.__dayCount == 1:
            self.__wwPlayer = StringVar()
            self.__wwPlayer.set("Enter White Wolf Name")
            self.__wwEntry = OptionMenu(self.__gameWin, self.__wwPlayer, *self.__playerNames)
            self.__wwEntry.pack(fill=X)
            self.__toClear.append(self.__wwEntry)
            self.__characterCalls.insert(0, self.__wwHandle)
        if self.__cbWhitewolf.get() == 1:
            self.__characterCalls.append(called)
            if self.__dayCount % 2 == 0:
                self.__whitewolfVictimEntry = OptionMenu(self.__gameWin, self.__whitewolfVictim, *self.__playerNames)
                self.__whitewolfVictimEntry.pack(fill=X)
                self.__toClear.append(self.__whitewolfVictimEntry)
                self.__packWin()
            else:
                self._nextCall()
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __wwHandle(self):
        self.__wwTracker = Label(self.__gameWin, text=f'White Wolf: {self.__wwPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__wwPlayer.get()] = "White Wolf"
        self.__trackers.append(self.__wwTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __bigBadWolf(self):
        self.__bigbadwolfVictim = StringVar()
        self.__bigbadwolfVictim.set("Enter Big Bad Wolf Victim")
        if not self.__wolfDead and self.__cbBigbadwolf.get() == 1:
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
            self.__section.set("The Big Bad Wolf")
            self.__narration.set("The big bad wolf wakes up and chooses another victim.")
            pos = 0
            if self.__dayCount == 1:
                self.__bbwPlayer = StringVar()
                self.__bbwPlayer.set("Enter Big Bad Wolf Name")
                self.__bbwEntry = OptionMenu(self.__gameWin, self.__bbwPlayer, *self.__playerNames)
                self.__bbwEntry.pack(fill=X)
                self.__toClear.append(self.__bbwEntry)
                self.__characterCalls.insert(0, self.__bbwHandle)
                pos = 1
            self.__bigbadwolfVictimEntry = OptionMenu(self.__gameWin, self.__bigbadwolfVictim, *self.__playerNames)
            self.__bigbadwolfVictimEntry.pack(fill=X)
            self.__toClear.append(self.__bigbadwolfVictimEntry)
            self.__packWin()
            if not self.__infection:
                self.__characterCalls.insert(pos, self.__rustyKnightCheck)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __bbwHandle(self):
        self.__bbwTracker = Label(self.__gameWin, text=f'Big Bad Wolf: {self.__bbwPlayer.get()}', font='{Copperplate Gothic Light}')
        self.__playerRoles[self.__bbwPlayer.get()] = "Big Bad Wolf"
        self.__trackers.append(self.__bbwTracker)
        self.__characterCalls.pop(0)
        self._nextCall()

    def __witch(self):
        if (self.__poisonPotion or self.__healingPotion) and self.__cbWitch.get() == 1:
            self.__section.set("Salem's Calling")
            self.__narration.set("The witch wakes up and chooses whether to use their potions, unfortunately, the witch could only find ingredients for one of each potion. Use wisely.")
            if self.__dayCount == 1:
                self.__witchPlayer = StringVar()
                self.__witchPlayer.set("Enter Witch Name")
                self.__witchEntry = OptionMenu(self.__gameWin, self.__witchPlayer, *self.__playerNames)
                self.__witchEntry.pack(fill=X)
                self.__toClear.append(self.__witchEntry)
            victims = self.__getVictims()
            if self.__healingPotion and victims:
                label = Label(self.__gameWin, text=f'Victim List:', font='{Copperplate Gothic Light}')
                label.pack(fill=X)
                self.__toClear.append(label)
                for victim in victims:
                    label = Label(self.__gameWin, text=f'{victim}', font='{Copperplate Gothic Light}')
                    label.pack(fill=X)
                    self.__toClear.append(label)
                self.__witchHealEntry = OptionMenu(self.__gameWin, self.__witchHeal, *victims)
                self.__witchHealEntry.pack(fill=X)
                self.__toClear.append(self.__witchHealEntry)
            if self.__poisonPotion:
                self.__witchVictimEntry = OptionMenu(self.__gameWin, self.__witchVictim, self.__playerNames)
                self.__witchVictimEntry.pack(fill=X)
                self.__toClear.append(self.__witchVictimEntry)
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
            self.__characterCalls.insert(0, self.__witchHandle)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __witchHandle(self):
        if self.__dayCount == 1:
            self.__witchTracker = Label(self.__gameWin, text=f'Witch: {self.__witchPlayer.get()}', font='{Copperplate Gothic Light}')
            self.__playerRoles[self.__witchPlayer.get()] = "Witch"
            self.__trackers.append(self.__witchTracker)
        if self.__witchVictim.get() != "Enter Witch Victim":
            self.__poisonPotion = False
        if self.__witchHeal.get() != "Enter Witch Revive":
            self.__healingPotion = False
            if self.__wolfVictim.get() == self.__witchHeal.get():
                self.__wolfVictim.set("")
            elif self.__bigbadwolfVictim.get() == self.__witchHeal.get():
                self.__bigbadwolfVictim.set("")
            elif self.__bigbadwolfVictim.get() == self.__witchHeal.get():
                self.__bigbadwolfVictim.set("")
            elif self.__whitewolfVictim.get() == self.__witchHeal.get():
                self.__whitewolfVictim.set("")
            elif self.__knightVictim.get() == self.__witchHeal.get():
                self.__knightVictim.set("")
        self.__characterCalls.pop(0)
        self._nextCall()

    def __fox(self):
        if self.__foxPower and self.__cbFox.get() == 1:
            self.__section.set("Wise Mr Fox")
            self.__narration.set("The fox awakens and chooses three suspects. If there is a wolf among them, the narrator lets the fox know. Be warned: if there is no wolf among them then the fox looses its power!")
            if self.__dayCount == 1:
                self.__foxPlayer = StringVar()
                self.__foxPlayer.set("Enter Fox Name")
                self.__foxEntry = OptionMenu(self.__gameWin, self.__foxPlayer, *self.__playerNames)
                self.__foxEntry.pack(fill=X)
                self.__toClear.append(self.__foxEntry)
            self.__foxCheck = IntVar()
            self.__foxCheck.set(0)
            self.__foxCheckbox = Checkbutton(self.__gameWin, text='No Wolf in Suspects?', font='{Copperplate Gothic Light}', variable=self.__foxCheck, onvalue=1, offvalue=0)
            self.__foxCheckbox.pack(fill=X)
            self.__toClear.append(self.__foxCheckbox)
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
            self.__characterCalls.append(self.__foxHandle)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __foxHandle(self):
        if self.__dayCount == 1:
            self.__foxTracker = Label(self.__gameWin, text=f'Fox: {self.__foxPlayer.get()}', font='{Copperplate Gothic Light}')
            self.__playerRoles[self.__foxPlayer.get()] = "Fox"
            self.__trackers.append(self.__foxTracker)
        if self.__foxCheck.get() == 1:
            self.__foxPower = False
        self.__characterCalls.pop(0)
        self._nextCall()

    def __piper(self):
        if self.__cbPiper.get() == 1:
            self.__section.set("The Pied Piper")
            self.__narration.set("The piper awakens and chooses two people to charm. These newly charmed will be tapped on the head so they know who they are.")
            if self.__dayCount == 1:
                self.__piperPlayer = StringVar()
                self.__piperPlayer.set("Enter Fox Name")
                self.__piperEntry = OptionMenu(self.__gameWin, self.__piperPlayer, *self.__playerNames)
                self.__piperEntry.pack(fill=X)
                self.__toClear.append(self.__piperEntry)
            self.__charmOne = StringVar()
            self.__charmTwo = StringVar()
            self.__charmOne.set("Enter First Charmed")
            self.__charmTwo.set("Enter Second Charmed")
            self.__charmOneEntry = OptionMenu(self.__gameWin, self.__charmOne, *self.__playerNames)
            self.__charmTwoEntry = OptionMenu(self.__gameWin, self.__charmTwo, *self.__playerNames)
            self.__charmOneEntry.pack(fill=X)
            self.__charmTwoEntry.pack(fill=X)
            self.__toClear.append(self.__charmOneEntry)
            self.__toClear.append(self.__charmTwoEntry)
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __charmed(self):
        if self.__dayCount == 1:
            self.__charmedMsg = StringVar()
            self.__charmedTracker = Label(self.__gameWin, textvariable=self.__charmedMsg, font='{Copperplate Gothic Light}')
            self.__trackers.append(self.__charmedTracker)
            self.__piperTracker = Label(self.__gameWin, text=f'Piper: {self.__piperPlayer.get()}', font='{Copperplate Gothic Light}')
            self.__playerRoles[self.__piperPlayer.get()] = "Piper"
            self.__trackers.append(self.__piperTracker)
        if self.__cbPiper.get() == 1:
            self.__section.set("The Charmed Awakening")
            self.__narration.set("All charmed players awake and identify each other.")
            self.__charmedPlayers.add(self.__charmOne.get())
            self.__charmedPlayers.add(self.__charmTwo.get())
            self.__winCheck()
            self.__updateCharmedMsg()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)
        else:
            self.__characterCalls.pop(0)
        self._nextCall()

    def __updateCharmedMsg(self):
        charmmsg = "Charmed: "
        for charmed in self.__charmedPlayers:
            charmmsg += f"{charmed}, "
        self.__charmedMsg.set(charmmsg[:-2])

    def __rustyKnightCheck(self):
        if self.__wolfVictim.get() == self.__rustyKnightPlayer.get() and not self.__infection:
            self.__infection = True
            self.__section.set("The Infection")
            self.__narration.set("(The rusty knight infected the wolf to its left when the wolf attacked it. This wolf will also die tonight.)")
            self.__knightVictimEntry = OptionMenu(self.__gameWin, self.__knightVictim, *self.__playerNames)
            self.__knightVictimEntry.pack(fill=X)
            self.__toClear.append(self.__knightVictimEntry)
            self.__packWin()
            self.__characterCalls.pop(0)
        elif self.__bigbadwolfVictim.get() == self.__rustyKnightPlayer.get() and not self.__infection:
            self.__infection = True
            self.__knightVictim.set(self.__bbwPlayer.get())
            self.__characterCalls.pop(0)
            self._nextCall()
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __victims(self):
        self.__section.set("The Death Report")
        self.__narration.set("Every one in the village wakes up except the victims:")
        count = 0
        victims = self.__getVictims()
        self.__wildChildFlag = False
        for victim in victims:
            label = Label(self.__gameWin, text=f'{victim}', font='{Copperplate Gothic Light}')
            label.pack(fill=X)
            self.__toClear.append(label)
            count += 1
            if victim in self.__loverPlayers:
                for name in self.__loverPlayers:
                    if name != victim:
                        label = Label(self.__gameWin, text=f'{name}', font='{Copperplate Gothic Light}')
                        label.pack(fill=X)
                        self.__toClear.append(label)
            if victim == self.__roleModel.get():
                self.__wildChildFlag = True
        if self.__wildChildFlag:
            self.__wildChildFlag = False
            self.__bad.append("Wild Child")
            self.__good.pop(self.__good.index("Wild Child"))
            self.__wolfCount += 1
            self.__villageCount -= 1
            label = Label(self.__gameWin, text=f'Role Model Dead', font='{Copperplate Gothic Bold}')
            label.pack(fill=X)
            self.__toClear.append(label)
        self.__roles = []
        for victim in victims:
            if self.__playerRoles[victim] is None:
                role = StringVar()
                role.set(f"Select Role For {victim}")
                dropDown = OptionMenu(self.__gameWin, role, *self.__characters)
                dropDown.pack(fill=X)
                self.__roles.append((victim, role))
                self.__toClear.append(dropDown)
        self.__packWin()
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)
        self.__characterCalls.insert(0, self.__confirmKills)

    def __confirmKills(self):
        victimList = self.__getVictims()
        for victim in victimList:
            if victim in self.__loverPlayers:
                for name in self.__loverPlayers:
                    if name != victim:
                        victimList.append(name)
                        break
        for victim in victimList:
            if victim in self.__charmedPlayers:
                self.__charmedPlayers.remove(victim)
        if self.__cbPiper.get() == 1:
            self.__updateCharmedMsg()
        self.__wolfVictim.set("Enter Wolf Victim")
        self.__whitewolfVictim.set("Enter White Wolf Victim")
        self.__bigbadwolfVictim.set("Enter Big Bad Wolf Victim")
        self.__witchVictim.set("Enter Witch Victim")
        self.__villageVictim.set("Enter Victim")
        self.__hunterVictim.set("Enter Victim")
        self.__knightVictim.set("")
        self.__hunterFlag = False
        for role in self.__roles:
            self.__playerRoles[role[0]] = role[1].get()
        for victim in victimList:
            role = self.__playerRoles[victim]
            self.__playerCount -= 1
            self.__alive.remove(victim)
            self.__dead.append(role)
            if role == "Villager":
                self.__numVillager.set(int(self.__numVillager.get())-1)
            elif role == "Werewolf":
                self.__numWolves.set(int(self.__numWolves.get()) - 1)
            else:
                if role == "Hunter":
                    self.__hunterFlag = True
                self.__charCBs[role].set(0)
            if role in self.__bad or victim == self.__convertedPlayer:
                self.__wolfCount -= 1
                self.__wolfDead = True
            else:
                self.__villageCount -= 1
        self.__updateCountTracker()
        self.__updateAliveTracker()
        self.__characterCalls.pop(0)
        if self.__hunterFlag:
            self.__characterCalls.insert(0, self.__hunterKill)
        else:
            self.__winCheck()
            if self.__sheriff.get() in victimList:
                self.__characterCalls.insert(0, self.__sheriffElection)
        self._nextCall()

    def __bearGrunt(self):
        if self.__cbBeartamer.get() == 1:
            self.__section.set("The Bear")
            self.__narration.set("If there is a wolf adjacent to the bear tamer then the bear must grunt. If the bear tamer has been converted to a wolf then the bear tamer counts as an adjacent wolf.")
            self.__packWin()
            called = self.__characterCalls.pop(0)
            self.__characterCalls.append(called)

    def __debate(self):
        self.__section.set("The Debate")
        self.__narration.set("The village must now debate, and try to find out who the wolves are.")
        self.__packWin()
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)

    def __vote(self):
        self.__section.set("The Vote Begins")
        self.__narration.set("The villagers must now vote on who they want to kill.")
        self.__villageVictimEntry = OptionMenu(self.__gameWin, self.__villageVictim, *self.__playerNames)
        self.__villageVictimEntry.pack(fill=X)
        self.__toClear.append(self.__villageVictimEntry)
        self.__villageVictimRole = StringVar()
        self.__villageVictimRole.set("Enter Victim's Role")
        self.__villageVictimDropdown = OptionMenu(self.__gameWin, self.__villageVictimRole, *self.__characters)
        self.__villageVictimDropdown.pack(fill=X)
        self.__toClear.append(self.__villageVictimDropdown)
        self.__packWin()
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)
        self.__characterCalls.insert(0, self.__handleVote)

    def __handleVote(self):
        victim = self.__villageVictim.get()
        self.__playerRoles[victim] = self.__villageVictimRole.get()
        if victim != "Idiot":
            if victim == self.__roleModel.get():
                self.__bad.append("Wild Child")
                self.__good.pop(self.__good.index("Wild Child"))
                self.__wolfCount += 1
                self.__villageCount -= 1
                label = Label(self.__gameWin, text=f'Role Model Dead', font='{Copperplate Gothic Bold}')
                label.pack(fill=X)
                self.__toClear.append(label)
            label = Label(self.__gameWin, text=f'{victim}', font='{Copperplate Gothic Light}')
            label.pack(fill=X)
            self.__toClear.append(label)
            if victim in self.__loverPlayers:
                for name in self.__loverPlayers:
                    if name != victim:
                        label = Label(self.__gameWin, text=f'{name} died due to heartbreak', font='{Copperplate Gothic Light}')
                        label.pack(fill=X)
                        self.__toClear.append(label)
            self.__packWin()
            self.__characterCalls.pop(0)
            self.__characterCalls.insert(0, self.__confirmKills)
            if not self.__toClear:
                self._nextCall()
        else:
            self.__characterCalls.pop(0)
            self._nextCall()

    def __hunterKill(self):
        self.__section.set("The Hunter's Revenge")
        self.__narration.set("The hunter shoots a player before they die.")
        self.__hunterVictimEntry = OptionMenu(self.__gameWin, self.__hunterVictim, *self.__playerNames)
        self.__hunterVictimEntry.pack(fill=X)
        self.__toClear.append(self.__hunterVictimEntry)
        self.__hunterVictimRole = StringVar()
        self.__hunterVictimRole.set("Enter Victim's Role")
        self.__hunterVictimDropdown = OptionMenu(self.__gameWin, self.__hunterVictimRole, *self.__characters)
        self.__hunterVictimDropdown.pack(fill=X)
        self.__toClear.append(self.__hunterVictimDropdown)
        self.__packWin()
        called = self.__characterCalls.pop(0)
        self.__characterCalls.append(called)
        self.__characterCalls.insert(0, self.__handleHunter)

    def __handleHunter(self):
        victim = self.__hunterVictim.get()
        self.__playerRoles[victim] = self.__hunterVictimRole.get()
        if victim == self.__roleModel.get():
            self.__bad.append("Wild Child")
            self.__good.pop(self.__good.index("Wild Child"))
            self.__wolfCount += 1
            self.__villageCount -= 1
            label = Label(self.__gameWin, text=f'Role Model Dead', font='{Copperplate Gothic Bold}')
            label.pack(fill=X)
            self.__toClear.append(label)
        label = Label(self.__gameWin, text=f'{victim}', font='{Copperplate Gothic Light}')
        label.pack(fill=X)
        self.__toClear.append(label)
        if victim in self.__loverPlayers:
            for name in self.__loverPlayers:
                if name != victim:
                    label = Label(self.__gameWin, text=f'{name} died due to heartbreak', font='{Copperplate Gothic Light}')
                    label.pack(fill=X)
                    self.__toClear.append(label)
        self.__packWin()
        self.__characterCalls.pop(0)
        self.__characterCalls.insert(0, self.__confirmKills)
        if not self.__toClear:
            self._nextCall()

    def __getVictims(self):
        victims = []
        if not (self.__wolfVictim.get() == "" or self.__wolfVictim.get() == "Enter Wolf Victim"):
            if self.__wolfVictim.get() == self.__elderPlayer.get() and self.__elderPower:
                self.__elderPower = False
                self.__wolfVictim.set("")
            else:
                victims.append(self.__wolfVictim.get())
        if self.__cbBigbadwolf.get() == 1:
            if not (self.__bigbadwolfVictim.get() == "Enter Big Bad Wolf Victim" or self.__bigbadwolfVictim.get() == ""):
                if self.__bigbadwolfVictim.get() == self.__elderPlayer.get() and self.__elderPower:
                    self.__elderPower = False
                    self.__bigbadwolfVictim.set("")
                else:
                    victims.append(self.__bigbadwolfVictim.get())
        if self.__cbWhitewolf.get() == 1:
            if not (self.__whitewolfVictim.get() == "Enter White Wolf Victim" or self.__whitewolfVictim.get() == ""):
                victims.append(self.__whitewolfVictim.get())
        if self.__cbWitch.get() == 1:
            if not (self.__witchVictim.get() == "Enter Witch Victim" or self.__witchVictim.get() == ""):
                self.__poisonPotion = False
                victims.append(self.__witchVictim.get())
        if self.__cbRustyknight.get() == 1:
            if self.__knightVictim.get() != "Enter Infected Wolf Name":
                victims.append(self.__knightVictim.get())
        if not (self.__villageVictim.get() == "" or self.__villageVictim.get() == "Enter Victim"):
            victims.append(self.__villageVictim.get())
        if not (self.__hunterVictim.get() == "" or self.__hunterVictim.get() == "Enter Victim"):
            victims.append(self.__hunterVictim.get())
        return victims

    def __winCheck(self):
        if (self.__dayCount == 2 and self.__day) and "Angel" in self.__dead:
            # angel Win
            self._endGame("Angel")
        if len(self.__charmedPlayers) == self.__playerCount - 1 and self.__cbPiper.get() == 1:
            # piper win
            self._endGame("Piper")
        if self.__wolfCount == 0:
            # villagers win
            self._endGame("Villagers")
        if self.__villageCount == 0:
            # wolves win
            self._endGame("Wolves")

    def __packWin(self):
        self.__proceedButton.pack(fill=X)
        self.__trackLabel.pack(fill=X)
        for tracker in self.__trackers:
            tracker.pack(fill=X)
        self.__endButton.pack(fill=X)

    def __clearWin(self):
        for _ in range(len(self.__toClear)):
            self.__toClear.pop().pack_forget()
        self.__proceedButton.pack_forget()
        self.__trackLabel.pack_forget()
        for tracker in self.__trackers:
            tracker.pack_forget()
        self.__endButton.pack_forget()

    def _savePreset(self):
        with open("presets.txt", "r") as f:
            presets = f.readlines()
        taken = False
        for preset in presets:
            name, preset = preset.strip("\n").split(":")
            if name == self.__gameName.get():
                self.__gameName.set("Name Taken")
                taken = True
        if not taken:
            values = []
            for variable in self.__variables:
                values.append(variable.get())
            values.append(int(self.__numVillager.get()))
            values.append(int(self.__numWolves.get()))
            with open("presets.txt", "a") as f:
                f.write(f"{self.__gameName.get()}:{values}\n")
            self.__gameName.set("Preset Saved!")

    def __updatePlayerCount(self, *args):
        self.__playerCount = 0
        for variable in self.__variables:
            if variable.get() != 0:
                self.__playerCount += 1
        if self.__sistersPresent:
            if self.__cbSisters.get() == 0:
                self.__sistersPresent = False
            else:
                self.__playerCount += 1
        else:
            if self.__cbSisters.get() == 1:
                self.__sistersPresent = True
                self.__playerCount += 1
        self.__playerCount += int(self.__numVillager.get())
        self.__playerCount += int(self.__numWolves.get())
        self.__numPlayers.set(f'Player Count: {self.__playerCount}')

    def _endGame(self, winner):
        self.__characterCalls = [self._dismissGame]
        if winner == "Piper":
            winningMsg = "The Piper Wins"
        elif winner == "Villagers":
            winningMsg = "The Villagers Win"
        elif winner == "Wolves":
            winningMsg = "The Wolves Win"
        elif winner == "Angel":
            winningMsg = "The Angel Wins"
        else:
            winningMsg = ""
        winWin = Toplevel(self.__root)
        winWin.title("Game Over")
        frame = Frame(winWin)
        frame.pack()
        self.__winWin = winWin
        Label(frame, text='Game Over', font='{Copperplate Gothic Bold} 16').pack(fill=X)
        Label(frame, text=winningMsg, font='{Copperplate Gothic Light}').pack(fill=X)
        Button(frame, text="Exit", command=self._dismissWin, font='{Copperplate Gothic Light}').pack(fill=X)
        self._dismissGame()

    def _load(self):
        if not (self.__setupInProgress or self.__loadInProgress or self.__gameInProgress):
            self.__loadInProgress = True
            loadWin = Toplevel(self.__root)
            loadWin.title("Load")
            frame = Frame(loadWin)
            frame.pack()
            self.__loadWin = loadWin
            Label(frame, text='Load', font='{Copperplate Gothic Bold} 24').pack(fill=X)
            with open("presets.txt", "r") as f:
                presetSaves = f.readlines()
            self.__presets = {}
            for preset in presetSaves:
                name, preset = preset.strip("\n").split(":")
                self.__presets[name] = preset
            self.__gameName = StringVar()
            self.__gameName.set("Choose Preset")
            OptionMenu(frame, self.__gameName, *self.__presets.keys()).pack(fill=X)
            Button(frame, text='Load', command=self._loadPreset, font='{Copperplate Gothic Light}').pack(fill=X, padx=10, pady=5)
            Button(frame, text='Back', command=self._dismissLoad, font='{Copperplate Gothic Light}').pack(fill=X, padx=10, pady=5)

    def _loadPreset(self):
        preset = self.__presets[self.__gameName.get()]
        preset = preset.strip("[]").split(", ")
        for variable in self.__variables:
            variable.set(preset.pop(0))
        self.__numVillager.set(preset.pop(0))
        self.__numWolves.set(preset.pop(0))
        self._dismissLoad()
        self._playGame()

    def _charHelp(self):
        if not self.__helpInProgress:
            self.__helpInProgress = True
            cHelpWin = Toplevel(self.__root)
            cHelpWin.title("Help")
            frame = Frame(cHelpWin)
            frame.pack()
            self.__cHelpWin = cHelpWin
            self.__cHelp = StringVar()
            self.__cHelp.set("Choose Character")
            self.__cDesc = StringVar()
            self.__cDesc.set("")
            Label(frame, text='Character Help', font='{Copperplate Gothic Bold}  24').pack(fill=X, padx=15, pady=5)
            charDropdown = OptionMenu(frame, self.__cHelp, *self.__characters, command=self.__switchCharDesc)
            charDropdown.config(font="{Copperplate Gothic Light}")
            charDropdown.pack(fill=X, padx=15, pady=5)
            Label(frame, textvariable=self.__cDesc, font='{Copperplate Gothic Light}', wraplength=500, padx=10, pady=10).pack(fill=X)
            Button(frame, text='Back', command=self._dismissCHelp, font='{Copperplate Gothic Light}').pack(padx=15, pady=5)
            self.__switchCharDesc()

    def __switchCharDesc(self, *args):
        character = str(self.__cHelp.get())
        self.__cDesc.set(self.__charDescs[character])

    def _dismissGame(self):
        self.__gameWin.destroy()
        self.__gameInProgress = False

    def _dismissSetup(self):
        self.__setupWin.destroy()
        self.__setupInProgress = False

    def _dismissLoad(self):
        self.__loadWin.destroy()
        self.__loadInProgress = False

    def _dismissCHelp(self):
        self.__cHelpWin.destroy()
        self.__helpInProgress = False

    def _dismissWin(self):
        self.__winWin.destroy()

    def _quit(self):
        self.__root.quit()

    def run(self):
        self.__root.mainloop()


game = Werewolf()
game.run()
