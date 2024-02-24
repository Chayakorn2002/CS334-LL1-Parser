import re
from LL1_parser import first, follow, ll1, parse

def main():
    productions = {}
    grammar_file = "grammars/grammar_test_1.txt"
    start_symbol = ""
    
    with open(grammar_file, "r") as file:
        for line in file:
            lhs, *rhs = re.split(r"[ \t\n]+|[->|\|]+", line.strip()) # Split line into non-terminal and terminal from the production
            productions[lhs] = set(rhs) - {''} # Add production to dictionary
            if not start_symbol: # init the start symbol
                start_symbol = lhs
    
    print(productions)

    print('\nFirst\n')
    # Calculate FIRST set for each non-terminal
    first_dict = {lhs: first(lhs, productions) for lhs in productions} 
    # Print FIRST set for each non-terminal
    for lhs, f in first_dict.items(): 
        print(lhs, ":", f)

    print('\nFollow\n')
    follow_dict = {lhs: set() for lhs in productions} # Create dictionary to store FOLLOW set for each non-terminal
    follow_dict[start_symbol] = follow_dict[start_symbol].union('$') # Add $ to FOLLOW set of start symbol
    # Calculate FOLLOW set for each non-terminal
    for lhs in productions:
        follow_dict = follow(lhs, productions, follow_dict)
    # Print FOLLOW set for each non-terminal
    for lhs, f in follow_dict.items():
        print(lhs, ":", f)

    # Create LL(1) parsing table
    ll1_table = ll1(follow_dict, productions)
    
    input_string = str(input("\nEnter input string: ")).strip()
    
    parse(input_string, start_symbol, ll1_table)

if __name__ == "__main__":
    main()
