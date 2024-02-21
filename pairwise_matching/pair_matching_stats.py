import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
import time
import os
import re
from recordlinkage.base import BaseCompareFeature
import Levenshtein
from recordlinkage.base import BaseIndexAlgorithm

class CompareCompanyName(BaseCompareFeature):
    def _compute_vectorized(self, s1,s2):
        def normalize_text(stringa):
            return re.sub(r'[^a-zA-Z0-9]', '', stringa)
        
        s1_norm = s1.map(normalize_text)
        s2_norm = s2.map(normalize_text)

        def norm_lev_dist(str1,str2):
            dist = Levenshtein.distance(str1,str2)
            max_len = max(len(str1),len(str2))
            if max_len == 0:
                return 0
            return 1-(dist/max_len)
        vectoriz_dist = s1_norm.combine(s2_norm,norm_lev_dist)
    
        return vectoriz_dist

class FirstTwoLettersIndex(BaseIndexAlgorithm):
    """Custom class for indexing based on the first two letters of given names."""

    def _link_index(self, df_a, df_b):
        """Make pairs with given names starting with the same first two letters."""

        # Create a temporary column to store the first two letters of given names
        df_a['first_two_letters'] = df_a['company_name'].str[:2]
        df_b['first_two_letters'] = df_b['company_name'].str[:2]

        # Find unique combinations of the first two letters present in both dataframes
        common_first_two_letters = set(df_a['first_two_letters']).intersection(df_b['first_two_letters'])

        # Initialize an empty list to store the index pairs
        index_pairs = []

        # For each common first two letters, find matching records and add their index pairs to the list
        for letters in common_first_two_letters:
            name_a_indices = df_a[df_a['first_two_letters'] == letters].index
            name_b_indices = df_b[df_b['first_two_letters'] == letters].index
            index_pairs.extend([(a, b) for a in name_a_indices for b in name_b_indices])

        # Remove the temporary columns
        df_a.drop(columns=['first_two_letters'], inplace=True)
        #df_b.drop(columns=['first_two_letters'], inplace=True)

        # Convert the list of pairs to a MultiIndex
        return pd.MultiIndex.from_tuples(index_pairs, names=[df_a.index.name, df_b.index.name])

# Percorsi delle cartelle di input e output
INPUT_FOLDER = 'pairwise_matching/annotation/file_ridotti/table_5-ridotta_1.json'
TRUE_LINKS = '/Users/fspezzano/vscode/id-hw6/pairwise_matching/annotation/file_annotati/annotazione_full_1_match.json'

annotation = recordlinkage.read_annotation_file(TRUE_LINKS)
links_true= annotation.links

df = pd.read_json(INPUT_FOLDER)

compare = recordlinkage.Compare()
compare.add(CompareCompanyName('company_name','company_name'))

start_country=time.time()
indexer_country = recordlinkage.Index()
indexer_country.block('country')

candidate_links_country = indexer_country.index(df)
feaures_country = compare.compute(candidate_links_country,df)
matches_country = feaures_country[feaures_country.sum(axis=1) > 0.7]
links_pred_country = matches_country.index

P_country= recordlinkage.precision(links_true,links_pred_country)
R_country = recordlinkage.recall(links_true,links_pred_country)
F_country = recordlinkage.fscore(links_true,links_pred_country)
A_country = recordlinkage.accuracy(links_true, links_pred_country, len(links_pred_country))

print('Blocking sulla country ')
print('Precision: ',P_country)
print('Recall: ',R_country)
print('F-score: ',F_country)
print('Accuracy: ',A_country)
print('Tempo di esecuzione: ',time.time()-start_country)


start_company_name = time.time()
indexer_company_name = FirstTwoLettersIndex()

candidate_links_company_name = indexer_company_name.index(df)
features_company_name = compare.compute(candidate_links_company_name, df)
matches_company_name = features_company_name[features_company_name.sum(axis=1) > 0.7]
links_pred_company_name = matches_company_name.index

P_company_name = recordlinkage.precision(links_true,links_pred_company_name)
R_company_name = recordlinkage.recall(links_true,links_pred_company_name)
F_comany_name = recordlinkage.fscore(links_true,links_pred_company_name)
A_company_name = recordlinkage.accuracy(links_true, links_pred_company_name, len(links_pred_company_name))
print('\nBlocking sulle prime due lettere di company_name ')
print('Precision: ',P_company_name)
print('Recall: ',R_company_name)
print('F-score: ',F_comany_name)
print('Accuracy: ',A_company_name)
print('Tempo di esecuzione: ',time.time()-start_company_name)


