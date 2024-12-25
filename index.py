from lark import Lark, Transformer

# Définir la grammaire
pseudo_code_grammar = """
start: statement+

statement: declaration
         | assignment
         | condition
         | loop
         | read
         | write

declaration: "DECLARER" CNAME "COMME" TYPE
assignment: CNAME "=" expr
condition: "SI" condition_expr "ALORS" statement+ "FINSI"
loop: "POUR" CNAME "DANS" "intervalle" "(" value "," value ")" "FAIRE" statement+ "FINPOUR"
read: "LIRE" CNAME
write: "ECRIRE"  expr

condition_expr: CNAME "==" value

expr: value
    | expr "+" expr    -> addition
    | expr "-" expr    -> subtraction
    | expr "*" expr    -> multiplication
    | expr "/" expr    -> division

value: NUMBER | CNAME

TYPE: "entier" | "texte" | "réel" | "booléen"
CNAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /-?\d+(\.\d+)?/

%import common.WS
%ignore WS
"""

# Créer l'analyseur avec Lark
pseudo_parser = Lark(pseudo_code_grammar, start='start', parser='lalr')

# Transformer pour interpréter les résultats
class PseudoCodeTransformer(Transformer):
    def declaration(self, args):
        return {"type": "déclaration", "variable": args[0], "type_variable": args[1]}

    def assignment(self, args):
        return {"type": "affectation", "variable": args[0], "valeur": args[1]}

    def condition(self, args):
        return {"type": "condition", "condition": args[0], "actions": args[1:]}

    def loop(self, args):
        return {
            "type": "boucle",
            "variable": args[0],
            "début_intervalle": args[1],
            "fin_intervalle": args[2],
            "actions": args[3:],
        }

    def read(self, args):
        return {"type": "lecture", "variable": args[0]}

    def write(self, args):
        return {"type": "écriture", "valeur": args[0]}

    def addition(self, args):
        return {"type": "addition", "gauche": args[0], "droite": args[1]}

    def subtraction(self, args):
        return {"type": "soustraction", "gauche": args[0], "droite": args[1]}

    def multiplication(self, args):
        return {"type": "multiplication", "gauche": args[0], "droite": args[1]}

    def division(self, args):
        return {"type": "division", "gauche": args[0], "droite": args[1]}

    def condition_expr(self, args):
        return {"gauche": args[0], "opérateur": "==", "droite": args[1] }

    def value(self, args):
        return args[0]

# Charger un pseudo-code à partir d'un fichier
def analyser_pseudo_code(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as file:
            pseudo_code = file.read()
    except FileNotFoundError:
        print(f"Erreur : fichier {nom_fichier} introuvable.")
        return

    try:
        # Analyser le pseudo-code
        tree = pseudo_parser.parse(pseudo_code)
        result = PseudoCodeTransformer().transform(tree)
        return result
    except Exception as e:
        print(f"Erreur d'analyse : {e}")
        return

# Exemple principal
if __name__ == "__main__":
    # Nom du fichier contenant le pseudo-code
    nom_fichier = "/code_source/code.txt"
    
    # Analyser et afficher le résultat
    resultat = analyser_pseudo_code(nom_fichier)
    if resultat:
        print("Résultat de l'analyse :")
      # Si le résultat est un arbre, on le convertit en dictionnaire ou en liste
        if isinstance(resultat, list):
            for instruction in resultat:
                print(instruction)
        else:
            print(resultat)
