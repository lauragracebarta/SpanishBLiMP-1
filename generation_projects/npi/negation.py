# Authors: Alicia Parrish via Alex Warstadt's script :)
# Script for generating NPI sentences with explicit negation as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import random
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=negation.tsv"
#project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
project_root = "G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation"
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_neg_det = np.append(get_all("expression", "none of the"), get_all("expression", "no"))
all_neg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "1")])
all_nonneg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "0")])
#all_UE_UE_quantifiers = get_all("restrictor_DE", "0", all_quantifiers)
#all_DE_UE_quantifiers = get_all("restrictor_DE", "1", get_all("scope_DE", "0", all_quantifiers)) #TODO: FC any takes singulars
all_intransitive_verbs = get_all("category", "S\\NP")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_embedding_verbs = get_all("category_2", "V_embedding")
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))
sentence_final_npi = ["yet", "at all", "in years"]

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # No/Some N1          aux  ever/often  V1      that     no/some    N2       Aux2 V_intrans
    # No      teachers    will ever        believe that     those      students can  fail.

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))

    # select transitive or intransitive V2
    x = random.random()
    if x < 1/2:
        # transitive V2
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
        D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
    else:
        # intransitive V2 - gives empty string for N3 and D3 slots
        V2 = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = " "
        D3 = " "

    # build sentences with licensor present
    sentence_1 = "%s %s %s ever %s that %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s %s often %s that %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_4 = "%s %s %s often %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # build sentences with no licensor present
    sentence_5 = "Some %s %s ever %s that %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_6 = "Some %s %s often %s that %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s %s ever %s that some %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_8 = "%s %s %s often %s that some %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present

        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=1_npi-present=1" % Neg_word1[0], 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=1_npi-present=0" % Neg_word1[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=0_npi-present=1" % Neg_word2[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=0_npi-present=0" % Neg_word2[0], 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=0_npi-present=0", 1, sentence_8))


    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# -------------------------
# now do it for sentence final NPIs

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # No/Some N1          aux         V1      that     no/some    N2       Aux2 V_intrans at_all
    # No      teachers    will        believe that     those      students can  fail      at all.

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
    Final_npi = choice(sentence_final_npi)

    # select transitive or intransitive V2
    x = random.random()
    if x < 1/2:
        # transitive V2
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
        D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
    else:
        # intransitive V2 - gives empty string for N3 and D3 slots
        V2 = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = " "
        D3 = " "

    # build sentences with licensor present
    sentence_1 = "%s %s %s %s that %s %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_2 = "%s %s %s %s that %s %s %s %s %s %s sometimes." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s %s that %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0],  N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_4 = "%s %s %s %s that %s %s %s %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # build sentences with no licensor present
    sentence_5 = "Some %s %s %s that %s %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_6 = "Some %s %s %s that %s %s %s %s %s %s sometimes ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s %s %s that some %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_8 = "%s %s %s %s that some %s %s %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=1_npi-present=1" % Final_npi % Neg_word1[0], 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=1_npi-present=0" % Final_npi % Neg_word1[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=0_npi-present=1" % Final_npi % Neg_word2[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=0_npi-present=0" % Final_npi % Neg_word2[0], 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=1_npi-present=1" % Final_npi , 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=1_npi-present=0" % Final_npi , 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=0_npi-present=1" % Final_npi , 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=0_npi-present=0" % Final_npi , 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# -------------------------
# Now monoclausal cases with "ever"

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # Neg_word  N1          aux  ever/often  V1      no/some  N2
    # No        teachers    will ever        fail    some     students .

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))

    # build sentences with licensor present
    sentence_1 = "%s %s %s ever %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_2 = "%s %s %s often %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_3 = "%s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0])
    sentence_4 = "%s %s %s often %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0])

    # build sentences with no licensor present
    sentence_5 = "Some %s %s ever %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_6 = "Some %s %s often %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_7 = "%s %s %s ever %s some %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0])
    sentence_8 = "%s %s %s often %s some %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=1_npi-present=1" % Neg_word1[0], 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=1_npi-present=0" % Neg_word1[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=0_npi-present=1" % Neg_word1[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=%s_licensor=1_scope=0_npi-present=0" % Neg_word1[0], 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=some_licensor=0_scope=0_npi-present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# -------------------------
# Now monoclausal cases with sentence final npi

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # Neg_word  N1          aux  V1      no/some  N2        at all
    # No        teachers    will fail    some     students  at all.

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
    Final_npi = choice(sentence_final_npi)

    # build sentences with licensor present
    sentence_1 = "%s %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi)
    sentence_2 = "%s %s %s %s %s %s sometimes ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_3 = "%s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0], Final_npi)
    sentence_4 = "%s %s %s %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word2[0], N2[0])

    # build sentences with no licensor present
    sentence_5 = "Some %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi)
    sentence_6 = "Some %s %s %s %s %s sometimes ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_7 = "%s %s %s %s some %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0], Final_npi)
    sentence_8 = "%s %s %s %s some %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=1_npi-present=1" % Final_npi % Neg_word1[0], 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=1_npi-present=0" % Final_npi % Neg_word1[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=0_npi-present=1" % Final_npi % Neg_word2[0], 1, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=%s_licensor=1_scope=0_npi-present=0" % Final_npi % Neg_word2[0], 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=1_npi-present=1" % Final_npi , 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=1_npi-present=0" % Final_npi , 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=0_npi-present=1" % Final_npi , 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=some_licensor=0_scope=0_npi-present=0" % Final_npi , 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

#---------------
# Sentential negation with not in biclausal sentences with ever

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1          Aux1_neg  ever/often  V1      that     D2       N2       Aux2_non-neg V2
    # The   teachers    don't     ever        believe that     those    students can          fail.

    # build all lexical items
    #TODO: throw in modifiers
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    #Aux1_neg = return_aux(V1, N1, require_negated=True)
    #Aux1_nonneg = return_aux(V1, N1, allow_negated=False)
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))

    # select transitive or intransitive V2
    x = random.random()
    if x < 1/2:
        # transitive V2
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        #Aux2_neg = return_aux(V2, N2, require_negated=True)
        #Aux2_nonneg = return_aux(V2, N2, allow_negated=False)
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
        D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
    else:
        # intransitive V2 - gives empty string for N3 and D3 slots
        V2 = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
        # Aux2_neg = return_aux(V2, N2, require_negated=True)
        # Aux2_nonneg = return_aux(V2, N2, allow_negated=False)
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = " "
        D3 = " "

    # build sentences with licensor present
    sentence_1 = "%s %s %s not ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s %s not often %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s ever %s that %s %s %s not %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_4 = "%s %s %s often %s that %s %s %s not %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # build sentences with no licensor present
    sentence_5 = "%s %s %s really ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_6 = "%s %s %s really often %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s %s ever %s that %s %s %s really %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_8 = "%s %s %s often %s that %s %s %s %s really %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=not_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=not_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=not_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=not_licensor=1_scope=0_npi-present=0", 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=really_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=really_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=really_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=ever_quantifier=really_licensor=0_scope=0_npi-present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# -------------------------
# now do it for sentence final npi with not as the licnesor

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1          aux    not     V1      that     D2    N2       Aux2 V_intrans at_all
    # The    teachers    will   not     believe that     those students can  fail      at all.

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    #N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
    Final_npi = choice(sentence_final_npi)

    # select transitive or intransitive V2
    x = random.random()
    if x < 1/2:
        # transitive V2
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
        D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
    else:
        # intransitive V2 - gives empty string for N3 and D3 slots
        V2 = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = " "
        D3 = " "

    # build sentences with licensor present
    sentence_1 = "%s %s %s not %s that %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_2 = "%s %s %s not %s that %s %s %s %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s %s that %s %s %s not %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0],  N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_4 = "%s %s %s %s that %s %s %s not %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # build sentences with no licensor present
    sentence_5 = "%s %s %s really %s that %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_6 = "%s %s %s really %s that %s %s %s %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s %s %s that %s %s %s really %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0], Final_npi)
    sentence_8 = "%s %s %s %s that %s %s %s really %s %s %s sometimes ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=not_licensor=1_scope=1_npi-present=1" % Final_npi , 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=not_licensor=1_scope=1_npi-present=0" % Final_npi , 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=not_licensor=1_scope=0_npi-present=1" % Final_npi , 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=not_licensor=1_scope=0_npi-present=0" % Final_npi , 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=really_licensor=0_scope=1_npi-present=1" % Final_npi , 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=really_licensor=0_scope=1_npi-present=0" % Final_npi , 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=really_licensor=0_scope=0_npi-present=1" % Final_npi , 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=negation_npi=%s_quantifier=really_licensor=0_scope=0_npi-present=0" % Final_npi , 1, sentence_8))
    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

output.close()