# Dev Log

## [04/08/2025] 6:28 PM

- Began looking at the project
- Ran example code provided and understood how to use semaphores in python
- Initial thoughts: I've carefully read the project description and I think I have a clear picture of what I need to do. I'll make 2 functions, one for teller threads and one for customer threads. To communicate between the threads, I'll use shared resources (I'm thinking an array of actions like deposit/withdrawal and an array of customer IDs for each teller that is currently interacting with a customer). For the manager, I'll just use a semaphore with a value of 1 and for the safe, I'll use a semaphore with a value of 2 since up to 2 tellers can be in the safe simulataneously. In the entrypoint of the program (main), I will need to spawn 3 teller threads and 50 customer threads. Then, I'll need to wait for them to finish up. I'm thinking of starting with the customer function since I'll need to code up the door and queue functionality.

## [04/08/2025] 9:13 PM

- Implemented the customer thread function.
- Added logic for customers to enter the queue and wait for an available teller.
- Used a semaphore to manage the queue and ensure customers are served in order.
- Tested the function with a small number of threads, and it seems to work as expected.

## [04/08/2025] 11:22 PM

- Started working on the teller thread function.
- Implemented logic for tellers to interact with customers and process their actions (deposit/withdrawal).
- Added shared resource management to track teller-customer interactions.
- Encountered a minor issue with semaphore synchronization, but resolved it by adjusting the critical section boundaries.

## [04/09/2025] 1:18 AM

- Completed the teller thread function and integrated it with the customer function.
- Added the semaphore logic for the safe to ensure only two tellers can access it simultaneously.
- Completed project for most part