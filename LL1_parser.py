import pandas as pd

# Perform LL(1) parsing
def parse(user_input, start_symbol, parsing_table):
    flag = 0
    user_input += "$"  # Append "$" to input string to mark end
    stack = ["$", start_symbol]  # Init stack with "$" and start symbol
    index = 0

    while stack:  # Continue until stack is empty
        top = stack[-1]  # Get top of stack
        current_input = user_input[index]  # Get current input symbol

        if top == current_input:  # If top of stack matches current input
            stack.pop()  # Pop from stack
            index += 1  # Move to next input symbol
        else:
            key = (top, current_input)
            if key not in parsing_table:  # If key is not in parsing table, set flag
                flag = 1
                break
            value = parsing_table[key]  # Get value from parsing table
            if value != '@':  # If value is not epsilon
                value = value[::-1]  # Reverse value as it's pushed onto stack
                stack.pop()  # Pop from stack
                stack.extend(value)  # Push value onto stack
            else:  # If value is epsilon, pop from stack
                stack.pop()

    if flag == 0:
        print("String accepted!")
    else:
        print("String not accepted!")

# Function to construct LL(1) parsing table
def ll1(follow, productions):
    print("\nParsing Table in matrix form\n")

    table = {}  # Initialize parsing table
    for key in productions:  # Iterate over productions
        for value in productions[key]:
            if value != '@':  # If value is not epsilon
                for element in first(value, productions):  # Calculate FIRST set for value
                    table[key, element] = value  # Populate parsing table
            else:
                for element in follow[key]:  # Calculate FOLLOW set for key
                    table[key, element] = value  # Populate parsing table with epsilon

    # Get unique terminal symbols
    terminals = set()
    for key in table:
        terminals.add(key[1])

    # Convert terminals set to list
    terminals_list = list(terminals)

    # Create DataFrame with proper indexing
    parsing_table = pd.DataFrame(index=productions.keys(), columns=terminals_list)
    for key, value in table.items():
        parsing_table.at[key[0], key[1]] = value

    print(parsing_table.fillna('-'))  # Print parsing table

    return table

# Function to calculate FOLLOW set for a non-terminal symbol
def follow(s, productions, ans):
    if len(s) != 1:
        return {}

    for non_terminal in productions: 
        for production in productions[non_terminal]: # production : d
            f = production.find(s)
            if f != -1:
                if f == (len(production) - 1):
                    if non_terminal != s:
                        if non_terminal in ans:
                            temp = ans[non_terminal]
                        else:
                            ans = follow(non_terminal, productions, ans)
                            temp = ans[non_terminal]
                        ans[s] = ans[s].union(temp)  # Add FOLLOW set of non-terminal to FOLLOW set of s
                else:
                    first_of_next = first(production[f + 1:], productions)
                    if '@' in first_of_next:
                        if non_terminal != s:
                            if non_terminal in ans:
                                temp = ans[non_terminal]
                            else:
                                ans = follow(non_terminal, productions, ans)
                                temp = ans[non_terminal]
                            ans[s] = ans[s].union(temp)  # Add FOLLOW set of non-terminal to FOLLOW set of s
                            ans[s] = ans[s].union(first_of_next) - {'@'}  # Remove epsilon from FOLLOW set of s
                    else:
                        ans[s] = ans[s].union(first_of_next)  # Add FIRST set of next symbol to FOLLOW set of s
    return ans

# Function to calculate FIRST set for a symbol
def first(non_terminal, productions):
    start = non_terminal[0]
    ans = set()
    if start.isupper():  # If symbol is non-terminal
        for sym in productions[start]:  # Iterate over productions for non-terminal
            if sym == '@':  # If production is epsilon
                if len(non_terminal) != 1:
                    ans = ans.union(first(non_terminal[1:], productions))  # Add FIRST set of next symbol
                else:
                    ans = ans.union('@')  # Add epsilon to FIRST set
            else:
                f = first(sym, productions)  # Calculate FIRST set for production
                ans = ans.union(x for x in f)  # Add FIRST set of production
    else:
        ans = ans.union(start)  # Add terminal symbol to FIRST set
    return ans