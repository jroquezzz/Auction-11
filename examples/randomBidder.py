import random
class CompetitorInstance():
    def __init__(self):
        # initialize personal variables
        pass
    
    def onGameStart(self, engine, gameParameters):
        # engine: an instance of the game engine with functions as outlined in the documentation.
        self.engine=engine
    
    def onAuctionStart(self, index, trueValue):
        self.thisIndex = index
        pass

    def onBidMade(self, whoMadeBid, howMuch):
        pass

    def onMyTurn(self,lastBid):
        if self.engine.random.randint(0,100)<20:
            self.engine.makeBid(lastBid+20)
        pass

    def onAuctionEnd(self):
        self.engine.print(f"==RandomBidder [{self.thisIndex}]==")
        pass