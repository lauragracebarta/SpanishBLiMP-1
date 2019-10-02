from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from utils.vocab_sets import *


class ThatTraceGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="that_trace",
                         uid="that_trace_embedded",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, all_common_nouns)
        self.all_nonfinite_embedding_verbs = get_all_conjunctive([("finite", "0")], all_embedding_verbs)
        self.all_copula = get_all_conjunctive([("category_2", "copula"), ("finite", "1")])
        self.all_adj_CP_arg = get_all("category_2", "Adj_CP")

    def sample(self):
        # who does John think that I    am  certain   called Suzie
        # wh  V_do N1   V1    that N2   cop Adj_embed V2     N3

        # who does John think I    am  certain   that called Suzie
        # wh  V_do N1   V1    N2   cop Adj_embed that V2     N3

        V1 = choice(self.all_nonfinite_embedding_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_nouns)))
        except IndexError:
            pass
        V_do = return_aux(V1,N1,allow_negated=False)
        # select transitive or intransitive V2
        x = random.random()
        if x < 1 / 2:
            # transitive V2
            V2 = choice(all_transitive_verbs)
            try:
                N3 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", self.all_safe_nouns)))
            except IndexError:
                pass
            except TypeError:
                pass
        else:
            V2 = choice(all_intransitive_verbs)
            N3 = " "
        N_interim = choice(get_matches_of(V2, "arg_1", all_nouns))
        wh = choice(get_matched_by(N_interim, "arg_1", all_wh_words))
        N2 = N_to_DP_mutate(choice(all_animate_nouns))
        cop = choice(get_matched_by(N2, "arg_1", self.all_copula))
        Adj_embed = choice(self.all_adj_CP_arg)
        V2 = conjugate(V2, wh)

        data = {
            "sentence_good": "%s %s %s %s that %s %s %s %s %s." % (wh[0], V_do[0], N1[0], V1[0], N2[0], cop[0], Adj_embed[0], V2[0], N3[0]),
            "sentence_bad": "%s %s %s %s %s %s %s that %s %s." % (wh[0], V_do[0], N1[0], V1[0], N2[0], cop[0], Adj_embed[0], V2[0], N3[0]),
            "two_prefix_prefix_good": "%s %s %s %s that %s %s %s" % (wh[0], V_do[0], N1[0], V1[0], N2[0], cop[0], Adj_embed[0]),
            "two_prefix_prefix_bad": "%s %s %s %s %s %s %s that" % (wh[0], V_do[0], N1[0], V1[0], N2[0], cop[0], Adj_embed[0]),
            "two_prefix_word": V2[0]
        }
        return data, data["sentence_good"]

generator = ThatTraceGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)



