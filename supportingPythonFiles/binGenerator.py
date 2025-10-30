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

from . import sparqlQueriesforLimit

def encode_values(column_values):
    return 'small' if column_values >= 0 else 'big'

def binGenerator(dataset):
    dataset['LabelIssuesPerc'] = 0 if len(dataset['LabelIssues']) == 0 else 1
 
    with open('./decision tree models/dt_random_smote.pkl', 'rb') as model_file:
        dt_classifier = pickle.load(model_file)

    
    class_to_capital = {
    'chisquare': 'Chisquare',
    'relief': 'Relief',
    'GR': 'GR',
    'fcbf': 'FCBF',
    'MI' :'MI'
    }

    # Replace dt_classifier.classes_ with their corresponding capital values
    #capital_class_names = [class_to_capital[label] for label in dt_classifier.classes_]
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

    predicted_label1 = dt_classifier.predict(values_predict)

    capital_predicted_label1 = class_to_capital[predicted_label1[0]]

    label=sparqlQueriesforLimit.kbConstruction(dataset)

    predicted_label = [capital_predicted_label1, label]

    # Export decision tree to DOT format
    dot_data = export_graphviz(
        dt_classifier,
        out_file=None,
        feature_names=feature_names,
        class_names=dt_classifier.classes_,
        filled=True,
        rounded=True,
        special_characters=True
    )

    # Create graph from DOT data
    graph = pydotplus.graph_from_dot_data(dot_data)

    # Clean up node labels and reset sample counts
    for node in graph.get_node_list():
        label = node.get_attributes().get('label')
        if label:
            label = label.replace('&lt;br/&gt;', '<br/>')  # Fix HTML encoding
            if 'samples = ' in label:
                lines = label.split('<br/>')
                for i, line in enumerate(lines):
                    if line.startswith('samples = '):
                        lines[i] = 'samples = 0'
                node.set_label('<br/>'.join(lines))
                node.set_fillcolor('white')

    # Highlight decision path
    decision_path = dt_classifier.decision_path(values_predict)
    node_indices = decision_path.indices

    for node_index in node_indices:
        node_id = str(node_index)
        matching_nodes = graph.get_node(node_id)
        if matching_nodes:
            node = matching_nodes[0]
            label = node.get_attributes().get('label', '')
            label = label.replace('&lt;br/&gt;', '<br/>')
            lines = label.split('<br/>')
            for i, line in enumerate(lines):
                if line.startswith('samples = '):
                    try:
                        count = int(line.split('=')[1].strip()) + 1
                        lines[i] = f'samples = {count}'
                    except:
                        lines[i] = 'samples = 1'
            node.set_label('<br/>'.join(lines))
            node.set_fillcolor('green')

    # Save the graph
    filename = 'tree.png'
    graph.write_png(f"./static/{filename}")
    graph_path = os.path.join('static', filename)
    print("Classifier internal class order:", dt_classifier.classes_)

    return dataset,  graph_path, predicted_label
