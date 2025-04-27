#GroceryStoreSim.py
#Name:
#Date:
#Assignment:

# Imports
import simpy
import random

# Global variables
eventLog = []
waitingShoppers = []
idleTime = 0

# Shopper process
def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 2  # shopping takes 0.5 minutes per item
    yield env.timeout(shoppingTime)
    # join the queue
    waitingShoppers.append((id, items, arrive, env.now))

# Checker process
def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)  # wait a minute
        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1  # at least 1 min to checkout
        yield env.timeout(checkoutTime)
        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

# Customer arrival process
def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2)  # a new shopper every 2 minutes

# Processing the results
def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0
    maxWait = 0

    for e in eventLog:
        waitTime = e[4] - e[3]  # depart - done shopping
        totalWait += waitTime
        totalItems += e[1]  # items purchased
        totalShoppers += 1
        if waitTime > maxWait:
            maxWait = waitTime

    if totalShoppers > 0:
        avgWait = totalWait / totalShoppers
        avgItems = totalItems / totalShoppers
        print("The average wait time was %.2f minutes." % avgWait)
        print("The average number of items purchased was %.2f." % avgItems)
        print("The maximum wait time was %.2f minutes." % maxWait)
    else:
        print("No shoppers checked out.")
    
    print("The total idle time was %d minutes." % idleTime)

# Main function
def main():
    numberCheckers = 5  # You can try different numbers!
    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180)  # 3 hours
    print(f"Shoppers still waiting after closing: {len(waitingShoppers)}")
    processResults()

if __name__ == '__main__':
    main()
