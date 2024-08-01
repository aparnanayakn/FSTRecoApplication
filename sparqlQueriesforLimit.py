from SPARQLWrapper import SPARQLWrapper, JSON
import ast
import requests
from rdflib import Graph as rdflibGraph 
import os
from owlready2 import *
import ast
import time
owlready2.JAVA_MEMORY = 4096  # Set to 4GB

# Fuseki server URL
SPARQL_ENDPOINT = "http://localhost:3030/KB/sparql"

def kbConstruction(df):
    sparql_query = """CONSTRUCT { ?s ?p ?o . }
                    WHERE {?s ?p ?o . }"""
    print("Pausing for 30 seconds before reasoning starts... Attach jvisualvm or jconsole now.")
    time.sleep(100)  # Pauses for 30 seconds

    response = requests.post(SPARQL_ENDPOINT, data={'query': sparql_query}, headers={'Accept': 'application/rdf+xml'})

    if response.status_code == 200:

        g = rdflibGraph()
        g.parse(data=response.text, format='xml')
        
        # Save the ontology to a file
        g.serialize(destination='full_onto.rdf', format='xml')
        print("Ontology successfully extracted and saved to 'full_ontology.rdf'")
    else:
        print(f"Error: {response.status_code}")
    
    filetoread = "file://"+os. getcwd()+"/full_onto.rdf"
    onto = get_ontology(filetoread).load()
    print("ONTO LOADED**************************")
    dcat = get_namespace("http://www.w3.org/ns/dcat/")
    dqv = get_namespace("http://www.w3.org/ns/dqv/")
    mtl = get_ontology("https://purl.archive.org/domain/mtl#")
    rdf=get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    dmop = get_ontology("http://www.e-lico.eu/ontologies/dmop/DMOP/DMOP.owl")
    dmop.base_iri = "http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#"
    dmop1 = get_ontology("http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl")
    dmop1.base_iri = "http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#"

    with onto:
        featureSelectionTask = dmop.FeatureSelectionTask()
        mtla = mtl.MetaLearningAlgorithm()
        fileName = 'test'
        fileObject = dmop.DataSetClass(fileName)
        mtla.hasMetaObjective.append(featureSelectionTask)

        featureSelectionTask.specifiesInputClass.append(fileObject)
        
        outClass =dmop.StructuredPredictionModelClass()
        featureSelectionTask.specifiesOutputClass.append(outClass)
        
        #Simple features
        nFeatures = dmop1.NumberOfFeatures()
        fileObject.hasQuality.append(nFeatures)
        nFeatures.hasValue.append(int(df['nr_attr']))


        attrToInst = mtl.ProportionOfAttrToInstances()
        fileObject.hasQuality.append(attrToInst)
        attrToInst.hasValue.append(float(df['attr_to_inst']))

        instToAttr = dmop1.ProportionOfInstancesPerFeature()
        fileObject.hasQuality.append(instToAttr)
        instToAttr.hasValue.append(float(df['inst_to_attr']))

        nInstance = dmop1.NumberOfInstances()
        fileObject.hasQuality.append(nInstance)
        nInstance.hasValue.append(int(df['nr_inst']))

        nNumeric = mtl.NumberOfNumericAttributes()
        fileObject.hasQuality.append(nNumeric)
        nNumeric.hasValue.append(int(df['nr_num']))

        nBinary = mtl.NumberOfBinaryAttributes()
        fileObject.hasQuality.append(nBinary)
        nBinary.hasValue.append(int(df['nr_bin']))
        
        nClasses = mtl.NumberOfClasses()
        fileObject.hasQuality.append(nClasses)
        nClasses.hasValue.append(int(df['nUnique']))


        corr = mtl.Correlation()
        fileObject.hasQuality.append(corr)
        std = mtl.StdDev()
        m = mtl.Mean()
        corr.hasQuality.append(m)
        corr.hasQuality.append(std)
        m.hasValue.append(float(df['cor.mean']))
        std.hasValue.append(float(df['cor.sd']))
        
        cov = mtl.Covariance()
        fileObject.hasQuality.append(cov)
        std = mtl.StdDev()
        m = mtl.Mean()
        cov.hasQuality.append(m)
        cov.hasQuality.append(std)
        m.hasValue.append(float(df['cov.mean']))
        std.hasValue.append(float(df['cov.sd']))

        eValues = mtl.EigenValues()
        fileObject.hasQuality.append(eValues)
        std = mtl.StdDev()
        m = mtl.Mean()
        eValues.hasQuality.append(m)
        eValues.hasQuality.append(std)
        m.hasValue.append(float(df['eigenvalues.mean']))
        std.hasValue.append(float(df['eigenvalues.sd']))


        gMean = mtl.GeometricMean()
        fileObject.hasQuality.append(gMean)
        std = mtl.StdDev()
        m = mtl.Mean()
        gMean.hasQuality.append(m)
        gMean.hasQuality.append(std)
        m.hasValue.append(float(df['g_mean.mean']))
        std.hasValue.append(float(df['g_mean.sd']))


        hMean = mtl.HarmonicMean()
        fileObject.hasQuality.append(hMean)
        std = mtl.StdDev()
        m = mtl.Mean()
        hMean.hasQuality.append(m)
        hMean.hasQuality.append(std)
        m.hasValue.append(float(df['h_mean.mean']))
        std.hasValue.append(float(df['h_mean.sd']))

        iqRange = mtl.InterquartileRange()
        fileObject.hasQuality.append(iqRange)
        std = mtl.StdDev()
        m = mtl.Mean()
        iqRange.hasQuality.append(m)
        iqRange.hasQuality.append(std)
        m.hasValue.append(float(df['iq_range.mean']))
        std.hasValue.append(float(df['iq_range.sd']))

        kurt = mtl.Kurtosis()
        fileObject.hasQuality.append(kurt)
        std = mtl.StdDev()
        m = mtl.Mean()
        kurt.hasQuality.append(m)
        kurt.hasQuality.append(std)
        m.hasValue.append(float(df['kurtosis.mean']))
        std.hasValue.append(float(df['kurtosis.sd']))

        mad = mtl.MedianAbsoluteDeviation()
        fileObject.hasQuality.append(mad)
        std = mtl.StdDev()
        m = mtl.Mean()
        mad.hasQuality.append(m)
        mad.hasQuality.append(std)
        m.hasValue.append(float(df['mad.mean']))
        std.hasValue.append(float(df['mad.sd']))


        maax = mtl.MaximumOfAttributes()
        fileObject.hasQuality.append(maax)
        std = mtl.StdDev()
        m = mtl.Mean()
        maax.hasQuality.append(m)
        maax.hasQuality.append(std)
        m.hasValue.append(float(df['max.mean']))
        std.hasValue.append(float(df['max.sd']))


        miin = mtl.MinimumOfAttributes()
        fileObject.hasQuality.append(miin)
        std = mtl.StdDev()
        m = mtl.Mean()
        miin.hasQuality.append(m)
        miin.hasQuality.append(std)
        m.hasValue.append(float(df['min.mean']))
        std.hasValue.append(float(df['min.sd']))


        meanAttr = mtl.MeanOfAttributes()
        fileObject.hasQuality.append(meanAttr)
        std = mtl.StdDev()
        m = mtl.Mean()
        meanAttr.hasQuality.append(m)
        meanAttr.hasQuality.append(std)
        m.hasValue.append(float(df['mean.mean']))
        std.hasValue.append(float(df['mean.sd']))


        medianAttr = mtl.MedianOfAttributes()
        fileObject.hasQuality.append(medianAttr)
        std = mtl.StdDev()
        m = mtl.Mean()
        medianAttr.hasQuality.append(m)
        medianAttr.hasQuality.append(std)
        m.hasValue.append(float(df['median.mean']))
        std.hasValue.append(float(df['median.sd']))


        rannge = mtl.Range()
        fileObject.hasQuality.append(rannge)
        std = mtl.StdDev()
        m = mtl.Mean()
        rannge.hasQuality.append(m)
        rannge.hasQuality.append(std)
        m.hasValue.append(float(df['range.mean']))
        std.hasValue.append(float(df['range.sd']))


        sd = mtl.StdDevOfAttributes()
        fileObject.hasQuality.append(sd)
        std = mtl.StdDev()
        m = mtl.Mean()
        sd.hasQuality.append(m)
        sd.hasQuality.append(std)
        m.hasValue.append(float(df['sd.mean']))
        std.hasValue.append(float(df['sd.sd']))


        skewness = mtl.Skewness()
        fileObject.hasQuality.append(skewness)
        std = mtl.StdDev()
        m = mtl.Mean()
        skewness.hasQuality.append(m)
        skewness.hasQuality.append(std)
        m.hasValue.append(float(df['skewness.mean']))
        std.hasValue.append(float(df['skewness.sd']))


        sparsity = mtl.Sparsity()
        fileObject.hasQuality.append(sparsity)
        std = mtl.StdDev()
        m = mtl.Mean()
        sparsity.hasQuality.append(m)
        sparsity.hasQuality.append(std)
        m.hasValue.append(float(df['sparsity.mean']))
        std.hasValue.append(float(df['sparsity.sd']))


        tMean = mtl.TrimmedMean()
        fileObject.hasQuality.append(tMean)
        std = mtl.StdDev()
        m = mtl.Mean()
        tMean.hasQuality.append(m)
        tMean.hasQuality.append(std)
        m.hasValue.append(float(df['t_mean.mean']))
        std.hasValue.append(float(df['t_mean.sd']))


        varAttr = mtl.Variance()
        fileObject.hasQuality.append(varAttr)
        std = mtl.StdDev()
        m = mtl.Mean()
        varAttr.hasQuality.append(m)
        varAttr.hasQuality.append(std)
        m.hasValue.append(float(df['var.mean']))
        std.hasValue.append(float(df['var.sd']))


        noCorAttr = mtl.NumberOfHighlyCorrelatedAttributes()
        fileObject.hasQuality.append(noCorAttr)
        noCorAttr.hasValue.append(float(df['nr_cor_attr']))


        noNorAttr = mtl.NumberOfAttrwithNormalDistribution()
        fileObject.hasQuality.append(noNorAttr)
        noNorAttr.hasValue.append(float(df['nr_norm']))


        noOut = mtl.NumberOfOutliers()
        fileObject.hasQuality.append(noOut)
        noOut.hasValue.append(float(df['nr_outliers']))


        #Information-theoretic
        attrConc = mtl.AttributeConcentration()
        fileObject.hasQuality.append(attrConc)
        std = mtl.StdDev()
        m = mtl.Mean()
        attrConc.hasQuality.append(m)
        attrConc.hasQuality.append(std)
        m.hasValue.append(float(df['attr_conc.mean']))
        std.hasValue.append(float(df['attr_conc.sd']))


        attrEntropy = mtl.AttributesEntropy()
        fileObject.hasQuality.append(attrEntropy)
        std = mtl.StdDev()
        m = mtl.Mean()
        attrEntropy.hasQuality.append(m)
        attrEntropy.hasQuality.append(std)
        m.hasValue.append(float(df['attr_ent.mean']))
        std.hasValue.append(float(df['attr_ent.sd']))


        ena = mtl.EqNumberOfAttributes()
        fileObject.hasQuality.append(ena)
        ena.hasValue.append(float(df['ena']))


        cEntropy = mtl.ClassEntropy()
        fileObject.hasQuality.append(cEntropy)
        cEntropy.hasValue.append(float(df['cEntropy']))


        snr = dmop1.NoiseSignalRatio()
        fileObject.hasQuality.append(snr)
        std = mtl.StdDev()
        m = mtl.Mean()
        snr.hasQuality.append(m)

        m.hasValue.append(float(df['snr.mean']))

        #ML-metrics
        classImbalance = mtl.ClassImbalance()
        fileObject.hasQuality.append(classImbalance)
        classImbalance.hasValue.append(float(df['ClassImbRatio']))
       
        classOverlap = mtl.ClassOverlap()
        fileObject.hasQuality.append(classOverlap)
        classOverlap.hasValue.append(float(df['ClassOverlapPerc']))
        

        outliersPerc = mtl.OutlierDetection()
        fileObject.hasQuality.append(outliersPerc)
        outliersPerc.hasValue.append(float(df['OutliersPerc']))

        labelIssues = mtl.LabelNoise()
        fileObject.hasQuality.append(labelIssues)
        labelIssues.hasValue.append(float(df['LabelIssuesPerc']))
       
        #Intrinsic
        completeness = mtl.Completeness()
        fileObject.hasQuality.append(completeness)
        completeness.hasValue.append(float(df['Completeness']))
       

        conciseness = mtl.Conciseness()
        fileObject.hasQuality.append(conciseness)
        conciseness.hasValue.append(float(df['Conciseness']))

       
        sAccuracy = mtl.SyntaxAccuracy()
        fileObject.hasQuality.append(sAccuracy)
        sAccuracy.hasValue.append(float(df['SyntaxAccuracy']))


    sync_reasoner_pellet([onto], infer_data_property_values=True)
    print(outClass.hasValue)
    return outClass.hasValue


def parametersLimit():
    limit_dict ={}
    limit_dict['cor.mean'] = correlation_limit()
    limit_dict['cov.mean'] = covariance_limit()
    limit_dict['eigenvalues.mean'] = eigenvalue_limit()
    limit_dict['g_mean.mean'] = gmean_limit()
    limit_dict['h_mean.mean'] = hmean_limit()
    limit_dict['iq_range.mean'] = iqr_limit()
    limit_dict['kurtosis.mean'] = kurtosis_limit()
    limit_dict['mad.mean'] = mad_limit()
    limit_dict['max.mean'] = max_limit()
    limit_dict['mean.mean'] = mean_limit()
    limit_dict['median.mean'] = median_limit()
    limit_dict['min.mean'] = min_limit()
    limit_dict['nr_cor_attr'] = noCorr_limit()
    limit_dict['nr_norm'] = nrNormalAttr_limit()
    limit_dict['nr_outliers'] = nrOut_limit()
    limit_dict['range.mean'] = range_limit()
    limit_dict['sd.mean'] = sd_limit()
    limit_dict['skewness.mean'] = skewness_limit()
    limit_dict['sparsity.mean'] = sparsity_limit()   
    limit_dict['t_mean.mean'] = tmean_limit()
    limit_dict['var.mean'] = variance_limit()
    limit_dict['attr_to_inst'] = propAttrInst_limit()
    limit_dict['inst_to_attr'] = propInstAttr_limit()
    limit_dict['nr_attr'] = noAttr_limit()
    limit_dict['nUnique'] = noClass_limit()
    limit_dict['nr_bin'] = noBin_limit()
    limit_dict['nr_inst'] = noInsta_limit()
    limit_dict['attr_ent.mean'] = attrEnt_limit()
    limit_dict['attr_conc.mean'] = attrConc_limit()
    limit_dict['cEntropy'] = classEnt_limit()
    limit_dict['ena'] = ena_limit()
    limit_dict['snr.mean'] = snr_limit()

    return limit_dict

def execute_query1(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)     
    upperValue = lowerValue = 0
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if "results" in results and "bindings" in results["results"]:
        for result in results["results"]["bindings"]:
            upperValue = result["upperValue"]["value"]
            lowerValue = result["lowerValue"]["value"]
      

    return float(upperValue), float(lowerValue)


def execute_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)     
    upperValue = lowerValue = 0
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if "results" in results and "bindings" in results["results"]:
        for result in results["results"]["bindings"]:
            upperValue = result["upperValue"]["value"]
            lowerValue = result["lowerValue"]["value"]
            meanValue = result["mean"]["value"]
            stdValue = result["stdDev"]["value"]
                
    return float(upperValue), float(lowerValue), float(meanValue), float(stdValue) 



def correlation_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?cor a mtl:CorrelationParameter .
        ?metal dmop:hasParameter ?cor .
        ?cor mtl:hasLowerValue ?lowerValue .
        ?cor mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?cor mtl:hasQuality ?m .
        ?cor mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .    
    }   
    """
    return execute_query(query)

def covariance_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?cov a mtl:CovarianceParameter .
        ?metal dmop:hasParameter ?cov .
        ?cov mtl:hasLowerValue ?lowerValue .
        ?cov mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?cov mtl:hasQuality ?m .
        ?cov mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev . 
    }   
    """
    return execute_query(query)

def eigenvalue_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?eigen a mtl:EigenValuesParameter .
        ?metal dmop:hasParameter ?eigen .
        ?eigen mtl:hasLowerValue ?lowerValue .
        ?eigen mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?eigen mtl:hasQuality ?m .
        ?eigen mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev . 
    }   
    """
    return execute_query(query)    

def gmean_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?gmean a mtl:GeometricMeanParameter .
        ?metal dmop:hasParameter ?gmean .
        ?gmean mtl:hasLowerValue ?lowerValue .
        ?gmean mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?gmean mtl:hasQuality ?m .
        ?gmean mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev . 
    
    }   
    """
    return execute_query(query)

def hmean_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?hmean a mtl:HarmonicMeanParameter .
        ?metal dmop:hasParameter ?hmean .
        ?hmean mtl:hasLowerValue ?lowerValue .
        ?hmean mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?hmean mtl:hasQuality ?m .
        ?hmean mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev . 
    }   
    """
    return execute_query(query)

def iqr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?iqr a mtl:InterquartileRangeParameter .
        ?metal dmop:hasParameter ?iqr .
        ?iqr mtl:hasLowerValue ?lowerValue .
        ?iqr mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?iqr mtl:hasQuality ?m .
        ?iqr mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    


def kurtosis_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?kurt a mtl:KurtosisParameter .
        ?metal dmop:hasParameter ?kurt .
        ?kurt mtl:hasLowerValue ?lowerValue .
        ?kurt mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?kurt mtl:hasQuality ?m .
        ?kurt mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def mad_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?mad a mtl:MedianAbsoluteDeviationParameter .
        ?metal dmop:hasParameter ?mad .
        ?mad mtl:hasLowerValue ?lowerValue .
        ?mad mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?mad mtl:hasQuality ?m .
        ?mad mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def max_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?max a mtl:MaximumOfAttributesParameter .
        ?metal dmop:hasParameter ?max .
        ?max mtl:hasLowerValue ?lowerValue .
        ?max mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?max mtl:hasQuality ?m .
        ?max mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    

def min_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?min a mtl:MinimumOfAttributesParameter .
        ?metal dmop:hasParameter ?min .
        ?min mtl:hasLowerValue ?lowerValue .
        ?min mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?min mtl:hasQuality ?m .
        ?min mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def mean_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?mean1 a mtl:MeanOfAttributesParameter .
        ?metal dmop:hasParameter ?mean1 .
        ?mean1 mtl:hasLowerValue ?lowerValue .
        ?mean1 mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?mean1 mtl:hasQuality ?m .
        ?mean1 mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def median_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?median a mtl:MedianOfAttributesParameter .
        ?metal dmop:hasParameter ?median .
        ?median mtl:hasLowerValue ?lowerValue .
        ?median mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?median mtl:hasQuality ?m .
        ?median mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    


def range_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?range a mtl:RangeParameter .
        ?metal dmop:hasParameter ?range .
        ?range mtl:hasLowerValue ?lowerValue .
        ?range mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?range mtl:hasQuality ?m .
        ?range mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)   

def sd_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?sd a mtl:StdDevOfAttributesParameter .
        ?metal dmop:hasParameter ?sd .
        ?sd mtl:hasLowerValue ?lowerValue .
        ?sd mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?sd mtl:hasQuality ?m .
        ?sd mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def skewness_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?skew a mtl:SkewnessParameter .
        ?metal dmop:hasParameter ?skew .
        ?skew mtl:hasLowerValue ?lowerValue .
        ?skew mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?skew mtl:hasQuality ?m .
        ?skew mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def sparsity_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?sparsity a mtl:SparsityParameter .
        ?metal dmop:hasParameter ?sparsity .
        ?sparsity mtl:hasLowerValue ?lowerValue .
        ?sparsity mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?sparsity mtl:hasQuality ?m .
        ?sparsity mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    


def tmean_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?tmean a mtl:TrimmedMeanParameter .
        ?metal dmop:hasParameter ?tmean .
        ?tmean mtl:hasLowerValue ?lowerValue .
        ?tmean mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?tmean mtl:hasQuality ?m .
        ?tmean mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)   

def variance_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?var a mtl:VarianceParameter .
        ?metal dmop:hasParameter ?var .
        ?var mtl:hasLowerValue ?lowerValue .
        ?var mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?var mtl:hasQuality ?m .
        ?var mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    


def noCorr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?nocorr a mtl:NumberOfHighlyCorrelatedAttributesParameters .
        ?metal dmop:hasParameter ?nocorr .
        ?nocorr mtl:hasLowerValue ?lowerValue .
        ?nocorr mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?nocorr mtl:hasQuality ?m .
        ?nocorr mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def nrNormalAttr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?nrattr a mtl:NumberOfAttrwithNormalDistributionParameter .
        ?metal dmop:hasParameter ?nrattr .
        ?nrattr mtl:hasLowerValue ?lowerValue .
        ?nrattr mtl:hasUpperValue ?upperValue .

    }   
    """
    return execute_query1(query)

def nrOut_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?nrOut a mtl:NumberOfOutliersParameter .
        ?metal dmop:hasParameter ?nrOut .
        ?nrOut mtl:hasLowerValue ?lowerValue .
        ?nrOut mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?nrOut mtl:hasQuality ?m .
        ?nrOut mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    

def attrConc_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?attrConc a mtl:AttributeConcentrationParameter .
        ?metal dmop:hasParameter ?attrConc .
        ?attrConc mtl:hasLowerValue ?lowerValue .
        ?attrConc mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?attrConc mtl:hasQuality ?m .
        ?attrConc mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def classEnt_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?cEnt a mtl:ClassEntropyParameter .
        ?metal dmop:hasParameter ?cEnt .
        ?cEnt mtl:hasLowerValue ?lowerValue .
        ?cEnt mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)


def attrEnt_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?attrEnt a mtl:AttributesEntropyParameter .
        ?metal dmop:hasParameter ?attrEnt .
        ?attrEnt mtl:hasLowerValue ?lowerValue .
        ?attrEnt mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?attrEnt mtl:hasQuality ?m .
        ?attrEnt mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def ena_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?ena a mtl:EqNumberOfAttributesParameter .
        ?metal dmop:hasParameter ?ena .
        ?ena mtl:hasLowerValue ?lowerValue .
        ?ena mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?ena mtl:hasQuality ?m .
        ?ena mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)    


def snr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?snr a mtl:NoiseSignalRatioParameter .
        ?metal dmop:hasParameter ?snr .
        ?snr mtl:hasLowerValue ?lowerValue .
        ?snr mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?snr mtl:hasQuality ?m .
        ?snr mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)   

def noAttr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue ?mean ?stdDev
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?noAttr a mtl:NumberOfFeaturesParameter .
        ?metal dmop:hasParameter ?noAttr .
        ?noAttr mtl:hasLowerValue ?lowerValue .
        ?noAttr mtl:hasUpperValue ?upperValue .
        ?m a mtl:Mean .
        ?std a mtl:StdDev .
        ?noAttr mtl:hasQuality ?m .
        ?noAttr mtl:hasQuality ?std .
        ?m dmop:hasValue ?mean .
        ?std dmop:hasValue ?stdDev .
    }   
    """
    return execute_query(query)

def propAttrInst_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?propAttrInst a mtl:ProportionOfAttrToInstancesParameter .
        ?metal dmop:hasParameter ?propAttrInst .
        ?propAttrInst mtl:hasLowerValue ?lowerValue .
        ?propAttrInst mtl:hasUpperValue ?upperValue .
    
    }   
    """
    return execute_query1(query)

def propInstAttr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?propInstAttr a mtl:ProportionOfInstancesPerFeatureParameter .
        ?metal dmop:hasParameter ?propInstAttr .
        ?propInstAttr mtl:hasLowerValue ?lowerValue .
        ?propInstAttr mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)    


def noInsta_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?noIns a mtl:NumberOfInstancesParameter .
        ?metal dmop:hasParameter ?noIns .
        ?noIns mtl:hasLowerValue ?lowerValue .
        ?noIns mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)  


def noNumAttr_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?noNumAttr a mtl:NumberOfNumericAttributesParameter .
        ?metal dmop:hasParameter ?noNumAttr .
        ?noNumAttr mtl:hasLowerValue ?lowerValue .
        ?noNumAttr mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)

def noBin_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?nBin a mtl:NumberOfBinaryAttributesParameter .
        ?metal dmop:hasParameter ?nBin .
        ?Bin mtl:hasLowerValue ?lowerValue .
        ?Bin mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)    


def noClass_limit():
    query = """ PREFIX dmop: <http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX dmop1: <http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#>
    PREFIX mtl: <https://purl.archive.org/domain/mtl#>  
    SELECT ?upperValue ?lowerValue
    WHERE {  
        ?metal a mtl:MetaLearningAlgorithm . 
        ?featureSelectionTask a dmop:FeatureSelectionTask .
        ?metal mtl:hasMetaObjective ?featureSelectionTask .
        ?noClass a mtl:NumberOfClassesParameter .
        ?metal dmop:hasParameter ?noClass .
        ?noClass mtl:hasLowerValue ?lowerValue .
        ?noClass mtl:hasUpperValue ?upperValue .
    }   
    """
    return execute_query1(query)  
