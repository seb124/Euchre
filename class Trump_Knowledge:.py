class Trump_Knowledge:
    #global dictionary to store the worths of different cards 
    #this is for when you have the same suit. 
    # did them as 50 through 30 because these cards are automaticall ybetter than any of other suit
    trumppoint_dic = {
        "Jack": 50,
        "JackOpp": 48, #opposite suit, same color jack
        "Ace": 45,
        "King": 44,
        "Queen":43,
        "10": 40,
        "9": 39,
        "8": 38,
        "7": 37,
        "6": 36,
        "5": 35,
        "4": 34,
        "3": 33,
        "2": 32
    }
    ##should add values for other cards that arent in suit or diversity of suits
    
    def decide_trump(probability_table, hand, teammate_info, turned_card):
        # Identify high-value cards in hand if the suit of the turned card is chosen as trump
        high_value_cards = get_high_value_cards(hand, turned_card)

        # Estimate probability of teammate having high-value cards
        teammate_trump_probability = probability_table[teammate][high_value_cards]

        # Estimate probability of opponents having strong trump cards
        opponent_trump_probability = probability_table[opponents][high_value_cards]

        # Calculate expected value of choosing trump
        picked_value = evaluate_trump_choice(high_value_cards, teammate_trump_probability, opponent_trump_probability)

        # Calculate expected value of passing on trump
        passed_value = evaluate_alternative_choice(probability_table, turned_card)

        #added below
        adjustment = consider_turn_order(position,teammate_passed, opponent_passed, dealer)
        picked_value += adjustment 

        # Make decision based on expected values
        if picked_value > pass_value then
            return "Pick"
        else
            return "Pass"
    

    def get_high_value_cards(hand, suit):
        high_value_cards = []
        for card in hand
        ##CHANGED THIS
            if card value in trumppoint_dict is higher than 40 (or some threshold number that we define, this can change)
                add card to high_value_cards
    
        return high_value_cards


    def get_hand_weight(hand, suit):
        #not exactly sure how to code this but this will look at non trump cards
        first, look at how high your non trump cards are 
        also, consider diversity of suits (are you better off if you have a lot of different suits or one suit)
        then, add this evaluation to your hand weight
           
    def evaluate_trump_choice(high_value_cards, teammate_prob, opponent_prob)
    # Need to find the weights of the high value cards (these are stored in evalute_cards but not sure if we can call this function for our purpose here)
        return card_weight(high_value_cards) + (teammate_prob * calculate_bonus_penalty(teammate_prob)) - (opponent_prob * calculate_bonus_penalty(opponent_prob))

    
    ##added below
    #helps adjust your likelihood based on your position
    def consider_turn_order(position, teammate_status, opponent_status):
        adjustment = 0
        if position == "first":
            adjustment -=3 #dont know much aobut other cards
        elif position == "dealer":
            adjustment +=6 #definitely have higher likely hood here

        if position == "second":
            adjustment +=3 #know that one opponent doesnt have much
        if position == "third":
            adjustment -=2 #know that opponent doesnt have mcuh but neither does your partner
        return adjustment

        
      
    def card_weight(high_value_cards):
        score = 0
        for card in high_value_cards:
            If card.rank in point_dic
                Score += point_dic[card] 
        return score

    def calculate_bonus_penalty(prob):
        # This might be where we integrate with Ivan's benchmarks + thresholds
        if prob > 0.8 then
                return 10
        else if prob > 0.5 then
                return 5
        else 
            return 0

    def evaluate_alternative_choice(probability_table, turned_card)
        return expected_value_of_other_suits(probability_table, turned_card)

    def expected_value_of_other_suits(probability_table, turned_card)
        best_alternative_value = 0
        best_suit = None

        for suit in [Hearts, Diamonds, Clubs, Spades]
            if suit is turned_card suit  then
                continue

            high_value_cards = get_high_value_cards(hand, suit)
            teammate_prob = probability_table[teammate][high_value_cards]
            opponent_prob = probability_table[opponents][high_value_cards]
            
            value = card_weight(high_value_cards) + (teammate_prob * calculate_bonus_penalty(teammate_prob)) - (opponent_prob * calculate_bonus_penalty(opponent_prob))
            
            if value > best_alternative_value THEN
                best_alternative_value = value
                best_suit = suit
    
        return best_alternative_value
