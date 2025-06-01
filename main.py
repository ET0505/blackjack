from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
import sys
import random


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack")
        self.setGeometry(100, 100, 500, 300)

        # Create the layout 
        self.layout = QVBoxLayout()

        # Create the welcome message 
        self.welcomeLabel = QLabel("Welcome to Blackjack", self)
        self.welcomeLabel.setStyleSheet("font-size: 14pt;")
        self.welcomeLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout.addWidget(self.welcomeLabel)

        # Create a button to start the game
        self.playButton = QPushButton("Start game", self)
        self.playButton.clicked.connect(self.on_play)
        self.layout.addWidget(self.playButton)
        
        # Set the layout 
        self.setLayout(self.layout)


    def on_play(self):
        self.welcomeLabel.deleteLater()
        self.playButton.deleteLater()

        self.game_start()


    def game_start(self):
        # Delete items in the layout 
        self.delete_items()

        # Initialise the possible cards in a list  
        self.nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.dealerCards, self.userCards = [], []
        self.userSum, self.dealerSum = 0, 0

        # Initialise cards for the user and the dealer 
        self.userCards.append(random.choice(self.nums))
        self.userCards.append(random.choice(self.nums))

        self.dealerCards.append(random.choice(self.nums))
        self.dealerCards.append(random.choice(self.nums))
        
        # Calculate the initial sum of the cards for the user and the dealer 
        for card in self.userCards:
            self.userSum = self.calculateSum(self.userSum, card)
        
        for card in self.dealerCards:
            self.dealerSum = self.calculateSum(self.dealerSum, card)

        self.message = QLabel("The cards have been dealt.", self)
        self.message.setStyleSheet("font-size: 14pt;")
        self.message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.message)

        # Display a random card from the dealer's hand
        self.dealerLabel = QLabel(f"The dealer has a {random.choice(self.dealerCards)}", self)
        self.dealerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dealerLabel)

        # Display the user's cards 
        self.userLabel = QLabel(f"You have {", ".join(self.userCards)}", self)
        self.userLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.userLabel)
        
        # Create the button for users to hit 
        self.hitButton = QPushButton("Hit", self)
        self.hitButton.clicked.connect(self.on_hit)
        self.layout.addWidget(self.hitButton)

        # Create the button for users to stand 
        self.standButton = QPushButton("Stand", self)
        self.standButton.clicked.connect(self.on_stand)
        self.layout.addWidget(self.standButton)
    
        # End the game if the user gets blackjack 
        if self.userSum == 21:
            self.won()

    
    def calculateSum(self, initialSum, newCard):
        if newCard in ["J", "Q", "K"]:
            value = 10
        elif newCard == "A":
            value = 11
        else:
            value = int(newCard)

        initialSum += value
        return initialSum


    # Execute block if the user decides to hit 
    def on_hit(self):        
        self.userLabel.hide()
        
        # Give the user another card and calculate the total sum
        cardHit = random.choice(self.nums)
        self.userCards.append(cardHit)
        self.userSum = self.calculateSum(self.userSum, cardHit)

        # End the game if the user gets blackjack
        if self.userSum == 21:
            self.won()

        # End the game if the user busts  
        elif self.userSum > 21:
            self.lost()

        # Otherwise, continue the game 
        else:
            self.update_ui()

            self.hitButton = QPushButton("Hit", self)
            self.hitButton.clicked.connect(self.on_hit)
            self.layout.addWidget(self.hitButton)

            self.standButton = QPushButton("Stand", self)
            self.standButton.clicked.connect(self.on_stand)
            self.layout.addWidget(self.standButton)


    # Execute block if the user decides to stand 
    def on_stand(self):
        # Dealer continues to hit until their total sum is 17 or greater 
        while self.dealerSum < 17:
            cardHit = random.choice(self.nums)
            self.dealerCards.append(cardHit)
            self.dealerSum = self.calculateSum(self.dealerSum, cardHit)

        # End the game if the dealer gets blackjack 
        if self.dealerSum == 21:
            self.lost()

        # End the game if the dealer busts
        elif self.dealerSum > 21:
            self.won()
        
        else:
            # End the game in a tie if the user's total and the dealer's total are equal 
            if self.dealerSum == self.userSum:
                self.push()
            
            # End the game if the dealer is closer to 21 
            elif self.dealerSum > self.userSum:
                self.lost()

            # End the game if the user is closer to 21 
            else:
                self.won()
    

    # Displays the updated cards in the user's hand 
    def update_ui(self):        
        self.userLabel.deleteLater()
        self.hitButton.deleteLater()
        self.standButton.deleteLater()
        
        self.userLabel = QLabel(f"You have {", ".join(self.userCards)}", self)
        self.userLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.userLabel)


    # Creates the retry button to play again and restart the game 
    def game_over(self):
        self.retryButton = QPushButton("Try again", self)
        self.retryButton.clicked.connect(self.game_start)
        self.layout.addWidget(self.retryButton)


    # Execute block if the user wins 
    def won(self):
        self.delete_items()
        self.reveal_dealer()
        self.update_ui()

        self.winMessage = QLabel("Congratulations, you won!", self)
        self.winMessage.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.winMessage)
        self.game_over()
    

    # Execute block if the user loses 
    def lost(self):
        self.delete_items()

        self.reveal_dealer()
        self.update_ui()
        self.loseMessage = QLabel("Bad luck, you lost!", self)
        self.loseMessage.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.loseMessage)
        self.game_over()


    # Execute block if there is a tie 
    def push(self):
        self.delete_items()
        self.reveal_dealer()
        self.update_ui()

        self.pushMessage = QLabel("Push!", self)
        self.pushMessage.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.pushMessage)
        self.game_over()


    # Display the cards in the dealer's hand
    def reveal_dealer(self):
        self.dealerLabel = QLabel(f"Dealer has {", ".join(self.dealerCards)}", self)
        self.dealerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.dealerLabel)


    # Delete the items in the layout 
    def delete_items(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()


# Main Loop
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
