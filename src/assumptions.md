Assumptions:
1: Token is valid for user_profile tests.
2: Correct number of inputs and inputs are of proper type for all functions (for example, even if the inputs are invalid, there will be inputs).
3: Conditions for correct inputs is set in functions already.
4: Conditions for correct inputs is set in functions already.
5: InputError is already implemented.
6: A new user will be in zero channels by default.
7: If someone is the owner of the whole slackr, they will be an owner of every channel. Therefore, you do not have to check if someone is the owner of the slackr when searching for permissions, just have to check that they are an owner of that channel. 
8: When removing an owner, you are removing them from the whole channel.
9: When adding an owner, you are adding them to the whole channel .
10: If a channel is private and the user is not part of that channel, they will not be able to see it when listing all channels. Similarly, they will only be able to see channels that are public or that they are members of (or owners of, which means they are members of).
11: Function to register a new user as a profile in Slackr has already been implemented.
12: One assumption is that auth_register automatically logs in a user.
13: "NOTATOKEN" is not a valid name for a token
