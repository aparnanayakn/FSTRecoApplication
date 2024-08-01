from owlready2 import *
from owlready2.sparql.endpoint import *
import pickle
import math
import numpy as np
import pydotplus
from sklearn.tree import export_graphviz, plot_tree
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt

import sparqlQueriesforLimit

def encode_values(column_values):
    return 'small' if column_values >= 0 else 'big'

def binGenerator(dataset):
    print(dataset)
    dataset['LabelIssuesPerc'] = 0 if len(dataset['LabelIssues']) == 0 else 1
    
    #labelFromSWRL = sparqlQueriesforLimit.kbConstruction(dataset) #This contains the inferred value from SWRL rules, due to memory issues this is not possible to execute

    limit_dict = sparqlQueriesforLimit.parametersLimit()
    required_values = {}

    for key, limits in limit_dict.items():
        temp_value = [dataset[key], "small" if dataset[key] <= limits[1] else "big"]
        required_values[key] = temp_value

    encode_columns = ['ClassImbRatio', 'OutliersPerc', 'ClassOverlapPerc', 'Completeness', 'Conciseness']
    for item in encode_columns:
        required_values[item] = [dataset[item], encode_values(dataset[item])]

    dataset['LabelIssuesPerc'] = 0 if len(dataset['LabelIssues']) == 0 else 1

    required_norm = {}
    for key, limits in limit_dict.items():
        if len(limits) > 2:
            m, s = limits[2], limits[3]
            required_norm[key] = 1 if (m - s <= dataset[key] <= m + s) else 0

    columns_need = ['OutliersPerc', 'cEntropy', 'nr_num', 'nr_inst', 'ClassOverlapPerc', 'LabelIssuesPerc',
                    'inst_to_attr', 'attr_to_inst', 'Conciseness', 'nr_bin', 'Completeness', 'nr_norm',
                    'ClassImbRatio', 'nUnique']
    for col in columns_need:
        required_norm[col] = 1 if dataset[col] > 0 else 0

    with open('df_raw_decision_tree_model.pkl', 'rb') as model_file:
        dt_classifier = pickle.load(model_file)
    with open('df_raw_normalised_decision_tree_model.pkl', 'rb') as model_file:
        dt_classifier_normalised = pickle.load(model_file)

    
    class_to_capital = {
    'chisquare': 'Chisquare',
    'relief': 'Relief',
    'GR': 'GR',
    'fcbf': 'FCBF'
    }

    # Replace dt_classifier.classes_ with their corresponding capital values
    capital_class_names = [class_to_capital[label] for label in dt_classifier.classes_]
    capital_class_names = [class_to_capital[label] for label in dt_classifier_normalised.classes_]

    for key, value in dataset.items():
        if not isinstance(value, list) and isinstance(value, float) and math.isnan(value):
            dataset[key] = 0

    feature_names = ['Completeness', 'Conciseness', 'cor.mean', 'cov.mean', 'eigenvalues.mean', 'g_mean.mean',
                     'h_mean.mean', 'iq_range.mean', 'kurtosis.mean', 'mad.mean', 'max.mean', 'mean.mean',
                     'median.mean', 'min.mean', 'nr_cor_attr', 'nr_norm', 'nr_outliers', 'range.mean', 'sd.mean',
                     'skewness.mean', 'sparsity.mean', 't_mean.mean', 'var.mean', 'ClassImbRatio', 'ClassOverlapPerc',
                     'OutliersPerc', 'attr_to_inst', 'inst_to_attr', 'nr_attr', 'nr_bin', 'nr_inst', 'nr_num',
                     'attr_conc.mean', 'attr_ent.mean', 'LabelIssuesPerc', 'nUnique', 'ena', 'snr.mean', 'cEntropy']

    values_predict = np.array([float(dataset[feature]) for feature in feature_names]).reshape(1, -1)
    values_predict_normal = np.array([required_norm[feature] for feature in feature_names]).reshape(1, -1)

    predicted_label1 = dt_classifier.predict(values_predict)

    predicted_label2 = dt_classifier_normalised.predict(values_predict_normal)

    capital_predicted_label1 = class_to_capital[predicted_label1[0]]
    capital_predicted_label2 = class_to_capital[predicted_label2[0]]

    predicted_label = [capital_predicted_label1, capital_predicted_label2]


    dot_data = export_graphviz(dt_classifier, out_file=None,
                               feature_names=feature_names,
                               class_names=capital_class_names,
                               filled=True, rounded=True,
                               special_characters=True)

    graph = pydotplus.graph_from_dot_data(dot_data)
    for node in graph.get_node_list():
        if node.get_attributes().get('label') is None:
            continue
        if 'samples = ' in node.get_attributes()['label']:
            labels = node.get_attributes()['label'].split('<br/>')
            for i, label in enumerate(labels):
                if label.startswith('samples = '):
                    labels[i] = 'samples = 0'
            node.set('label', '<br/>'.join(labels))
            node.set_fillcolor('white')

    decision_path = dt_classifier.decision_path(values_predict)
    for n, node_value in enumerate(decision_path.toarray()[0]):
        if node_value == 0:
            continue
        node = graph.get_node(str(n))[0]
        node.set_fillcolor('green')
        labels = node.get_attributes()['label'].split('<br/>')
        for i, label in enumerate(labels):
            if label.startswith('samples = '):
                labels[i] = 'samples = {}'.format(int(label.split('=')[1]) + 1)
        node.set('label', '<br/>'.join(labels))

    filename = 'tree.png'
    graph.write_png("./static/" + filename)
    graph_path = os.path.join('static', 'tree.png')

    return dataset, graph_path, predicted_label
