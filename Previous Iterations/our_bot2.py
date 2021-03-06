class CompetitorInstance():
    def __init__(self):
        # initialize personal variables
        pass

    def onGameStart(self, engine, gameParameters):
        # engine: an instance of the game engine with functions as outlined in the documentation.
        self.engine=engine
        # gameParameters: A dictionary containing a variety of game parameters
        self.gameParameters = gameParameters
        self.minbid = gameParameters["minimumBid"]
        self.engine.print("Game Started!")

    
    def onAuctionStart(self, index, trueValue):
        # index is the current player's index, that usually stays put from game to game
        # trueValue is -1 if this bot doesn't know the true value 
        # if we know the true value, let others bid.
        # If within certain range, allow us to buy
        self.engine.print(f"Our Bot index is {index}")
        self.value = trueValue if trueValue != -1 else self.gameParameters["meanTrueValue"]
        self.our_bots = []
        self.competitor_bots = []
        self.has_made_first_bid = []
        self.our_lastBid = 0
        self.prevBid = 0
        self.should_bid = True
        self.hasBid = False
        self.bid_diff = {}


    def is_NPC(self, currentBid) -> bool:
        bid_diff = currentBid - self.prevBid
        if bid_diff >= self.minbid and bid_diff <= 3*self.minbid:
            return True
        else:
            return False

    def onBidMade(self, whoMadeBid, howMuch):
        if(whoMadeBid in self.has_made_first_bid):
            if whoMadeBid in self.bid_diff.keys():
                if self.bid_diff.get(whoMadeBid) == howMuch - self.prevBid:
                    if(whoMadeBid not in self.competitor_bots):
                        self.competitor_bots.append(whoMadeBid)
            else:
                self.bid_diff[whoMadeBid] = howMuch - self.prevBid            
            if (self.is_NPC(howMuch) == False):
                if whoMadeBid not in self.competitor_bots:
                    if whoMadeBid not in self.our_bots:
                        self.competitor_bots.append(whoMadeBid)
        else:
            if howMuch == self.math_func(self.prevBid):
                self.our_bots.append(whoMadeBid)
            self.has_made_first_bid.append(whoMadeBid)

        self.prevBid = howMuch
    

    def math_func(self,lastBid) -> int:
        last_digit = (lastBid+8)%10
        power_digit = last_digit**2
        bid = (lastBid+8) + power_digit
        return bid

    def normal_func(self,lastBid, mean, stdv) -> float:
        e = self.engine.math.e
        pi = self.engine.math.pi

        exp = -(lastBid - mean)*(lastBid - mean)/(2*stdv*stdv)
        ans = 1/(stdv*(self.engine.math.sqrt(2*pi))) * self.engine.math.pow(e,exp)
        return ans

    def get_probability(self,lastBid, mean, stdv) -> float:
        return 1 - self.normal_func(lastBid, mean, stdv)/self.normal_func(mean, mean,stdv)


    def onMyTurn(self,lastBid):
        # lastBid is the last bid that was made
        mean = self.gameParameters["meanTrueValue"]
        stdv = self.gameParameters["stddevTrueValue"]
        probability = 0.8

        #run only on first bid to identify bots
        if self.hasBid == False:
            self.our_lastBid = self.math_func(lastBid)
            self.engine.makeBid(self.our_lastBid)
            self.hasBid = True
        else:
            our_bid = lastBid + self.minbid + self.engine.random.randint(0, 3*self.minbid)
            probability = 1 - our_bid/self.value
            if(self.engine.random.random() < probability):
                if(our_bid < self.value + stdv/2):
                    self.engine.makeBid(our_bid)

    def onAuctionEnd(self):
        # Now is the time to report team members, or do any cleanup.
        self.engine.print(f"Auction Ended")
        self.engine.reportTeams(self.our_bots, self.competitor_bots, [])
        self.engine.print(f"Our bots are {self.our_bots} and enemy bots are {self.competitor_bots}")
        pass