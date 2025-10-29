from . import file_operations
from . import simple_characteristics
from . import pre_processing
from . import quality_metrics
from . import statistical_characteristics
from . import information_theoretic
from pymfe.mfe import MFE
import pandas as pd
import math

def extractMetaFeature(filePath):
    temp = {}
    dataset = file_operations.custom_csv(filePath)

    # MFE dataset characteristics
    all_Label = simple_characteristics.get_labels(dataset)
    nUnique = simple_characteristics.count_unique_labels(dataset)

    # Dataset quality info
    missing_perc, missing_columns=quality_metrics.completeness(dataset)
    dataset = pre_processing.convert_str_int_categorical(dataset)
    dataset = pre_processing.convert_str_int_nominal(dataset)

    temp['Completeness'] = missing_perc
    if missing_columns:
        temp['Column_Number_With_Missing_Values'] = missing_columns
    temp['Conciseness'] = quality_metrics.conciseness(dataset)
    acc, invalid_columns = quality_metrics.syntax_accuracy(dataset)
    temp['SyntaxAccuracy'] = acc
    if invalid_columns:
        temp['Invalid_Columns'] = invalid_columns

    # Some pre-processing
    dataset = pre_processing.drop_rows(dataset)  # drop rows with more than 75% NA
    dataset = pre_processing.drop_columns(dataset)  # drop columns with more than 75% NA
    dataset = pre_processing.convert_NAs(dataset)
    dataset = pre_processing.convert_str_int_categorical(dataset)
    dataset = pre_processing.convert_str_int_nominal(dataset)

    # Statistical metrics
    X, y = simple_characteristics.get_XY(dataset)
    mfe = MFE(groups=["statistical"])
    mfe.fit(X.to_numpy())
    ft = mfe.extract()
    for i, item in enumerate(ft[0]):
        temp[item] = ft[1][i]

    # Simple
    mfe = MFE(groups=["general"])
    mfe.fit(X.to_numpy())
    ft = mfe.extract()
    for i, item in enumerate(ft[0]):
        temp[item] = ft[1][i]

    temp['nUnique'] = simple_characteristics.count_unique_labels(dataset)

    # ML
    classes, ratio = quality_metrics.calculate_class_imbalance(dataset)
    temp['ClassImbRatio'] = ratio
    if classes:
        temp['ImbalanceClasses'] = classes
    class_overlap_points, class_overlap_percentage, outlier_points, outliers = quality_metrics.compute_class_overlap(dataset)
    temp['OutliersPerc'] = outliers  # outliers
    temp['ClassOverlapPerc'] = class_overlap_percentage  # class overlap
    if class_overlap_points:
        temp['Overlap classes'] = class_overlap_points
    if outlier_points:
        temp['Outlier_Points'] = outlier_points
    labelIssues = quality_metrics.find_labelissues(dataset)
    temp['LabelIssues'] = labelIssues
    
    # info-theoretical
    mfe = MFE(groups=["info-theory"])
    mfe.fit(X.to_numpy())
    ft = mfe.extract()
    for i, item in enumerate(ft[0]):
        temp[item] = ft[1][i]

    snrsd, snrmean, snrvalues = information_theoretic.signaltonoise(dataset)
    temp['snr.mean'] = snrmean
    temp['ena'] = information_theoretic.ena_attributes(dataset)
    temp['cEntropy'] = information_theoretic.compute_class_entropy(dataset)

    return temp
