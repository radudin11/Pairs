0) Use -h or --help for list of possible arguments.

1) Input (if the file isn't given as argument):
    The programs take as input a path to a file.

    1.1) Input file documentation:
        *Each pair will be represented on two lines: -The first line represents the top part of the pair;
                                                    -The second line represents the bottom part of the pair;
        *There should be no lines empty between pairs;
        *Each number will be separeted by a space;
        *Start from the beginning of each line.

    1.2) Example inputs are given in the input/ directory.


2) Output:
    The program will output "yes" if it finds a correct sequence of pairs and "no" otherwise.

    2.1) For a more detailed result and some more information on what the program does delete 
    all "#debug" comments.

3) Implementation:
    The program uses brute force to try and match the pairs together.

    At step 0 it looks for pairs that can start the sequence (that have both parts' first number equal).
    Then, it takes each sequence and tries to complete it in order to get the result.

    3.1) DFS
        Using recursion, it checks which pair can fit in the current sequence and tries to continnue until:
            i) It finds a match (top sequence lenght = the bottom sequence length);
            ii) There are no more posibilties for a match;
            iii) It exceeds the number of itterations.

    3.2) BFS
        Checks all possible valid sequences that start with the sequences found at the previous step.
        Using recursion, it replaces the current list of sequences with the new found ones until:
            i) It finds a match (top sequence lenght = the bottom sequence length);
            ii) It exceeds the number of itterations.

    3.3) How it checks if the sequence is valid/the pair can fit:
        It takes the longer of the sequence and searches for a pair's opposite half that has the matching
        number at the position it would have if it was added to the sequence.

        After that, it checks if,by adding the pair, the two sequences would match up until the last 
        number of the shorter sequence part.

4) Options
    -h, --help            show this help message and exit

    --inputFile INPUTFILE, -f INPUTFILE
                        input file
                        
    --max-itter MAX_ITTER, -max-itter MAX_ITTER
                        maximum number of itterations, default is 10 For the best performance use the length of the sollution(if known) as the maximum number of itterations(matters only in DFS)

    --algorithm ALGORITHM, -a ALGORITHM
                        algorithm to use, default is BFS Available algorithms: DFS, BFS,

    -d, --debug           increase output verbosity

    --outputFile OUTPUTFILE, -o OUTPUTFILE
                        output file

    --starting-sequence STARTING_SEQUENCE, -starting-sequence STARTING_SEQUENCE
                        file containing the starting sequence(s)

    --get-lastSequence GET_LASTSEQUENCE, -get-lastSequence GET_LASTSEQUENCE, -gls GET_LASTSEQUENCE
                        file to write the last sequences if no solution is found
