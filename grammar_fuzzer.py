import sys
import random
from typing import Set, Union, List


def read_grammar(grammar_file_path):
    """Reads and executes a Python file to extract the grammar dictionary."""
    grammar_stuff = {}
    with open(grammar_file_path, 'r') as file:
        exec(file.read(), grammar_stuff)
    return grammar_stuff['grammar']

def tokenise(production):
    """Simple tokenizer to extract tokens from a production rule."""
    tokens, buffer, in_token = [], "", False
    for char in production:
        if char == "<":
            if buffer: 
                tokens.append(buffer)
                buffer = ""
            in_token = True
            buffer += char
        elif char == ">":
            buffer += char
            tokens.append(buffer)
            buffer = ""
            in_token = False
        else:
            buffer += char
    if buffer:
        tokens.append(buffer)
    return tokens

def expand(symbol, grammar, depth=0, max_depth=10):
    """Recursively expands a symbol using the provided grammar."""
    if depth > max_depth:
        return ''
    if symbol not in grammar:  # Base case: symbol is a terminal
        return symbol

    production = random.choice(grammar[symbol])
    tokens = tokenise(production)
    expanded = ''.join(expand(token, grammar, depth+1, max_depth) for token in tokens)
    return expanded

class TrackingGrammarCoverageFuzzer:
    """Track grammar coverage during production"""

    def __init__(self, grammar, start_symbol="<start>", log=False):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.log = log
        self.reset_coverage()

    def expansion_coverage(self) -> Set[str]:
        """Return the set of covered expansions as strings SYMBOL -> EXPANSION"""
        return self.covered_expansions

    def reset_coverage(self) -> None:
        """Clear coverage info tracked so far"""
        self.covered_expansions: Set[str] = set()

    def _max_expansion_coverage(self, symbol: str, max_depth: Union[int, float]) -> Set[str]:
        if max_depth <= 0:
            return set()

        self._symbols_seen.add(symbol)

        expansions = set()
        for expansion in self.grammar[symbol]:
            expansions.add(expansion_key(symbol, expansion))
            for nonterminal in nonterminals(expansion):
                if nonterminal not in self._symbols_seen:
                    expansions |= self._max_expansion_coverage(nonterminal, max_depth - 1)

        return expansions

    def max_expansion_coverage(self, symbol=None, max_depth=float("inf")) -> Set[str]:
        """
        Return set of all expansions in a grammar
        starting with `symbol` (default: start symbol).
        If `max_depth` is given, expand only to that depth.
        """
        if symbol is None:
            symbol = self.start_symbol

        self._symbols_seen: Set[str] = set()
        cov = self._max_expansion_coverage(symbol, max_depth)

        if symbol == self.start_symbol:
            assert len(self._symbols_seen) == len(self.grammar)

        return cov

    def fuzz(self) -> str:
        """Generate a string by expanding the start symbol."""
        return expand(self.start_symbol, self.grammar)

def expansion_key(symbol: str, expansion) -> str:
    """
    Convert (symbol, `expansion`) into a key "SYMBOL -> EXPRESSION".
    `expansion` can be an expansion string, a derivation tree,
    or a list of derivation trees.
    """
    if isinstance(expansion, tuple):
        expansion, _ = expansion

    if not isinstance(expansion, str):
        children = expansion
        expansion = all_terminals((symbol, children))

    assert isinstance(expansion, str)

    return symbol + " -> " + expansion

def all_terminals(node):
    """Extract all terminal symbols from a derivation tree."""
    symbol, children = node
    if not children:
        return symbol
    return ''.join(all_terminals(c) for c in children)

def nonterminals(expansion):
    """Extract non-terminals from an expansion."""
    return [token for token in tokenise(expansion) if token.startswith("<") and token.endswith(">")]

def main():
    if len(sys.argv) != 4:
        print("Some input is missing")
        sys.exit(1)

    program_file_path = sys.argv[1]
    grammar_file_path = sys.argv[2]
    num_strings=sys.argv[3]

    grammar =read_grammar(grammar_file_path)
    output_filename = program_file_path.replace('.py', '.in')
    fuzzer=TrackingGrammarCoverageFuzzer(grammar)
    
    with open(output_filename, 'w') as output_file:
        expanded=[]
        index=0
       # output_file.write(" \n")
        while index<(int(num_strings)-1):
            test_input = fuzzer.fuzz()
            if test_input not in expanded:
                expanded.append(test_input)
                output_file.write(test_input + '\n')
                index+=1

if __name__ == "__main__":
    main()
    
