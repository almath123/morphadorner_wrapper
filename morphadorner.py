import subprocess
import os

class MorphAdorner(object):
    def __init__(self, path="MorphAdorner/"):
        self.path = path
        self.noun_inflect_path = os.path.join(path, "NounInflector/NounInflector.jar")
        self.verb_tense_path = os.path.join(path, "VerbTenser/VerbTenser.jar")
        self.verb_conjugate_path = os.path.join(path, "VerbConjugator/VerbConjugator.jar")
        self.adj_inflect_path = os.path.join(path, "AdjectiveInflector/AdjectiveInflector.jar")

        self.noun_inflect_proc = None
        self.verb_tense_proc = None
        self.verb_conjugate_proc = None
        self.adj_inflect_proc = None

    def close(self):
        if self.noun_inflect_proc is not None:
            self.noun_inflect_proc.kill()
        if self.verb_tense_proc is not None:
            self.verb_tense_proc.kill()
        if self.verb_conjugate_proc is not None:
            self.verb_conjugate_proc.kill()
        if self.adj_inflect_proc is not None:
            self.adj_inflect_proc.kill()

    def inflectNoun(self, lemma, plural=True):
        if self.noun_inflect_proc is None:
            args = ['java', '-jar', self.noun_inflect_path]
            self.noun_inflect_proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        if plural:
            query = lemma + " " + "plural\n"
        else:
            query = lemma + " " + "singular\n"
        self.noun_inflect_proc.stdin.write(query)
        out = self.noun_inflect_proc.stdout.readline()
        return out.strip()

    def inflectAdjective(self, lemma, comparative=True):
        if self.adj_inflect_proc is None:
            args = ['java', '-jar', self.adj_inflect_path]
            self.adj_inflect_proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        if comparative:
            query = lemma + " " + "comparative\n"
        else:
            query = lemma + " " + "superlative\n"
        self.adj_inflect_proc.stdin.write(query)
        out = self.adj_inflect_proc.stdout.readline()
        return out.strip()

    def tenseVerb(self, lemma, verb):
        if self.verb_tense_proc is None:
            args = ['java', '-jar', self.verb_tense_path]
            self.verb_tense_proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        query = lemma + " " + verb + "\n"
        self.verb_tense_proc.stdin.write(query)
        out = self.verb_tense_proc.stdout.readline()
        out = out.strip().split()
        tense = out[0]
        person = out[1]
        return tense, person

    def conjugateVerb(self, lemma, tense, person):
        if self.verb_conjugate_proc is None:
            args = ['java', '-jar', self.verb_conjugate_path]
            self.verb_conjugate_proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        query = lemma + " " + tense + " " + person + "\n"
        self.verb_conjugate_proc.stdin.write(query)
        out = self.verb_conjugate_proc.stdout.readline()
        out = out.strip()
        return out

if __name__ == "__main__":
    ma = MorphAdorner()
    print ma.inflectNoun("dog")
    print ma.inflectNoun("cat")
    print ma.tenseVerb("charge", "charged")
    print ma.tenseVerb("run", "running")
    print ma.inflectNoun("dog")
    print ma.inflectNoun("cat")
    print ma.conjugateVerb("charge", "PAST_PARTICIPLE", "THIRD_PERSON_PLURAL")
    print ma.conjugateVerb("levy", "PAST_PARTICIPLE", "THIRD_PERSON_PLURAL")
    print ma.inflectAdjective("slow", comparative=False)

    ma.close()
