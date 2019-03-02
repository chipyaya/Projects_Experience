# Expression

### [state+input]
----------------------
state = 010, input = 01 ==> [state+input] = decimal(01001) = 9, [next_state] and [output] are the same as [state+input].

### [ff_type]
----------------------
[ff_type] = SR, JK, D, T.

### [output_expression], [parameter_expression]
-----------------------
0 = ~var

1 = var

2 = no need to AND

space = OR


If #param == 2, i.e ff_type == SR(resp. JK), then the first expression is for S(resp. J), and the second one for R(resp. K).

e.g.
    
    D
    111 012 101     
    // D = y1y2x + ~y1y2 + y1~y2x (y1, y2 = states, x = input)

    SR
    101 022
    021 120
    // S = y1~y2x + ~y1, R = ~y1x + y1~x


# Input Format
    
    [#state] [#input]
    [ff_type] // for state 1
    ...
    [ff_type] // for state #state
    [state+input] [next_state] [output] // 1
    ... 
    [state+input] [next_state] [output] // 2 ^ (#state + #input)

# Output Format

    [#state] [#input]
    [output_expression]
    [ff_type] // for state 1
    [parameter_expression] // for state 1
    [ff_type] // for state 2
    [parameter_expression] // for state 2
    ...
    [ff_type] // for state #state
    [parameter_expression] // for state #state
