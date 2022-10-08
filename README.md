1) Input (if the file isn't given as argument)
    The programs take as input a path to a file
    1.1) Input file documentation
        *Each pair will be represented on two lines: -The first line represents the top part of the pair
                                                    -The second line represents the bottom part of the pair
        *There should be no lines empty between pairs
        *Each number will be separeted by a space
        *Start from the beginning of each line
    1.2) Example inputs are given in the input/ directory


2) Output
    The program will output "yes" if it finds a correct sequence of pairs and "no" otherwise
    2.1) For a more detailed result and some more information on what the program does delete 
    all "#debug" comments

3) Implementation
    The program uses brute force to try and match the pairs together.

    At step 0 it looks for pairs that can start the sequence (that have both parts' first number equal).
    Then, it takes each sequence and tries to complete it in order to get the result.

    Using recursion, it checks which pair can fit in the current sequence and tries to continnue until:
        i) It finds a match (top sequence lenght = the bottom sequence length);
        ii) There are no more posibilties for a match;
        iii) It exceeds the number of itterations.

    How it checks if the pair fits:
        It takes the longer of the sequence and searches for a pair's opposite half that has the matching
        number at the position it would have if it was added to the sequence.

        After that, it checks if,by adding the pair, the two sequences would match up until the last 
        number of the shorter sequence part.



