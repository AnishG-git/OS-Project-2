import threading
import random
from time import sleep


def customer(i):
    global pendingCustomers, door, doorSem, bankLine, bankLineSem, tellerState, tellerLock, tellersSem, tellerToIndex, indexToTeller, tellersSem

    # Randomly decide to deposit or withdraw
    action = random.choice(["deposit", "withdrawal"])
    print(f"Customer {i} []: wants to perform a {action} transaction")

    # Wait for a random number of milliseconds between 0 and 100
    sleep(random.randint(0, 100) / 1000)
    print(f"Customer {i} []: going to bank.")
    # Walk into bank
    doorSem.acquire()
    print(f"Customer {i} []: entering bank.")
    doorSem.release()

    # enter queue
    bankLineSem.acquire()
    print(f"Customer {i} []: getting in line.")
    bankLine.append(i)
    bankLineSem.release()

    # choose next available teller
    while bankLine[0] != i:
        # wait for teller to be available
        sleep(0.1)
    bankLine.pop(0)

    # first in line gets to choose teller
    tellersSem[0].acquire()

    # choose next available teller
    tellersSem[1].acquire()
    print(f"Customer {i} []: selecting a teller.")
    myTeller = 0

    for factor, tellerID in tellerToIndex.items():
        if tellerLock % factor == 0:
            tellerLock //= factor
            myTeller = tellerID
            break
    print(f"Customer {i} [Teller {myTeller}]: selects teller")

    # notify teller of customer
    tellerState[myTeller] = (i, action)
    tellersSem[1].release()

    while tellerState[myTeller] != DEFAULT_TELLER_STATE:
        # wait for teller to respond
        sleep(0.1)

    # tell teller to handle customer
    pendingCustomers -= 1
    tellerLock *= indexToTeller[myTeller]
    tellersSem[0].release()

    print(f"Customer {i} []: leaves teller")
    doorSem.acquire()
    print(f"Customer {i} []: goes to door")
    doorSem.release()
    print(f"Customer {i} []: leaves bank")


def teller(i):
    global pendingCustomers, tellerState, safeSem, managerSem

    # runs teller code
    print(f"Teller {i} []: ready to serve")
    print(f"Teller {i} []: waiting for a customer")
    while pendingCustomers > 0:
        # chooses a customer to handle
        if tellerState[i] != DEFAULT_TELLER_STATE:
            action = tellerState[i][1]
            customerID = tellerState[i][0]
            print(f"Teller {i} [Customer {customerID}]: serving a customer")
            print(f"Teller {i} [Customer {customerID}]: asks for transaction")
            print(
                f"Customer {customerID} [Teller {i}]: asks for {action} transaction")
            print(
                f"Teller {i} [Customer {customerID}]: handling {action} transaction")

            if action == "withdrawal":
                # Ask the manager for permission
                print(
                    f"Teller {i} [Customer {customerID}]: going to the manager")
                managerSem.acquire()
                print(
                    f"Teller {i} [Customer {customerID}]: getting manager's permission")
                # Simulate manager interaction
                sleep(random.randint(5, 30) / 1000)
                managerSem.release()
                print(
                    f"Teller {i} [Customer {customerID}]: got manager's permission")

            # Access the safe
            print(f"Teller {i} [Customer {customerID}]: going to safe")
            safeSem.acquire()
            print(f"Teller {i} [Customer {customerID}]: enter safe")
            # Simulate transaction in the safe
            sleep(random.randint(10, 50) / 1000)
            safeSem.release()
            print(f"Teller {i} [Customer {customerID}]: leaving safe")
            print(
                f"Teller {i} [Customer {customerID}]: finishes {action} transaction.")
            print(
                f"Teller {i} [Customer {customerID}]: wait for customer to leave.")
            tellerState[i] = DEFAULT_TELLER_STATE
            print(f"Teller {i} []: ready to serve")
            print(f"Teller {i} []: waiting for a customer")
    print(f"Teller {i} []: leaving for the day")


if __name__ == "__main__":
    # global variables and constants
    NUM_TELLERS = 3
    NUM_CUSTOMERS = 50
    pendingCustomers = NUM_CUSTOMERS

    doorSem = threading.Semaphore(2)
    door = []

    bankLine = []
    bankLineSem = threading.Semaphore(1)

    DEFAULT_TELLER_STATE = (-1, "")
    tellerState = [DEFAULT_TELLER_STATE] * NUM_TELLERS

    TELLER_1 = 3
    TELLER_2 = 5
    TELLER_3 = 7
    tellerLock = TELLER_1 * TELLER_2 * TELLER_3
    tellerToIndex = {TELLER_1: 0, TELLER_2: 1, TELLER_3: 2}
    indexToTeller = {0: TELLER_1, 1: TELLER_2, 2: TELLER_3}

    tellersSem = [threading.Semaphore(3), threading.Semaphore(1)]

    managerSem = threading.Semaphore(1)  # Semaphore for manager interaction
    safeSem = threading.Semaphore(2)  # 2 tellers can access the safe at a time

    # lists containing threads
    tellers = []
    customers = []

    # starting up threads
    for i in range(NUM_TELLERS):
        tellerThread = threading.Thread(target=teller, args=(i,))
        tellers.append(tellerThread)
        tellerThread.start()

    for i in range(NUM_CUSTOMERS):
        customerThread = threading.Thread(target=customer, args=(i,))
        customers.append(customerThread)
        customerThread.start()

    for i in range(NUM_CUSTOMERS):
        customers[i].join()

    # wait for all threads to finish
    for i in range(NUM_TELLERS):
        tellers[i].join()

    print("The bank closes for the day.")
