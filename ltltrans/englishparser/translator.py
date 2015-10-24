from ltltrans.englishparser.converter import *
import sys


robot_vars = [VarRule(Var("r"),"move",noun = "robot"), VarRule(Var("l"),"flash",noun = "light")]
break_vars = [VarRule(Var("b"),"break", noun = "break")]
alarm_vars = [VarRule(Var("a"), "sound", noun = "alarm"), VarRule(Var("s"), "trigger", noun = "sensor"), VarRule(Var("l"), "flash", noun = "light")]


def translate(sentence, propositions):
    variables = []
    for p in propositions:
        args = [Var(p['letter']), p['verb']]
        kwargs = {'noun': p['subject']}
        if p['object'] != '':
            kwargs.update(**{
                'pobj': p['object'],
                'dobj': p['object'],
            })
        var = VarRule(*args, **kwargs)
        variables.append(var)
    return get_translation(sentence, variables)


def get_translation(sentence, variables):
    c = Converter(sentence, variables)
    r = c.get_statement()
    if len(r) != 0:
        return r[0]
    else:
        return None


if __name__ == '__main__':
    t = get_translation("Whenever the robot moves, the light flashes.", robot_vars)
    t.print_statement(sys.stdout, True)
