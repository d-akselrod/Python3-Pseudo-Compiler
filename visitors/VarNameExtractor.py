class SymbolTable:

    def toPEP9Name(var_name):
        vowels = "aeiouAEIOU"
        var_name_without_vowels = "".join(c for c in var_name if c not in vowels)
        if len(var_name_without_vowels) == 0:
            return var_name[:8]
        else:
            return var_name_without_vowels[:8]