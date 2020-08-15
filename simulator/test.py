from simulator.exchange import Exchange,Ag_exchange

def test():
    Ag_exchange.init_exchange()
    Ag_exchange.init_agent(10000,0)
    print(Ag_exchange.count)
    print(Ag_exchange.ticker)
    Ag_exchange.update_state()
    print(Ag_exchange.count)
    print(Ag_exchange.ticker)