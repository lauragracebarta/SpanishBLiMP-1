from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="transitive",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.strict_intransitive = get_all("strict_intrans", "1")
        self.transitive = all_transitive_verbs
        # get_all("strict_trans", "0", all_transitive_verbs)

    def sample(self):
        # The bear has attacked the girl.
        # Subj     Aux V_trans  obj
        # The bear has smiled    the girl.
        # Subj     Aux V_intrans obj

        V_trans = choice(self.transitive)
        Subj = N_to_DP_mutate(choice(get_matches_of(V_trans, "arg_1", all_nominals)))
        Aux = return_aux(V_trans, Subj)
        Obj = N_to_DP_mutate(choice(get_matches_of(V_trans, "arg_2", all_nominals)))
        V_intrans = choice(get_matched_by(Subj, "arg_1", get_matches_of(Aux, "arg_2", self.strict_intransitive)))

        data = {
            "sentence_good": "%s %s %s %s." % (Subj[0], Aux[0], V_trans[0], Obj[0]),
            "sentence_bad": "%s %s %s %s." % (Subj[0], Aux[0], V_intrans[0], Obj[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

