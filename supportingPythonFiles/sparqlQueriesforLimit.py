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

    SPARQL_DATA_URL = "http://localhost:3030/KB/data"  
    headers = {'Accept': 'application/rdf+xml'}

    response = requests.get(SPARQL_DATA_URL, headers=headers)

    if response.status_code == 200:
        with open("full_onto.owl", "wb") as f:
            f.write(response.content)
        #g = rdflibGraph()
        #g.parse(data=response.text, format='xml')        
        print("**********************Ontology downloaded directly from Jena dataset**********************")
    else:
        print(f"Failed to download ontology: {response.status_code}")
    
    filetoread = "file://"+os. getcwd()+"/full_onto.owl"
    onto = get_ontology(filetoread).load()
    dcat = get_namespace("http://www.w3.org/ns/dcat/")
    dqv = get_namespace("http://www.w3.org/ns/dqv/")
    mtl = get_ontology("https://purl.archive.org/domain/mtl#")
    onto.base_iri = "https://purl.archive.org/domain/mtl#"

    rdf=get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    dmop = get_ontology("http://www.e-lico.eu/ontologies/dmop/DMOP/DMOP.owl")
    dmop.base_iri = "http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#"
    dmop1 = get_ontology("http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl")
    dmop1.base_iri = "http://www.e-LICO.eu/ontologies/dmo/DMOP/DMOP.owl#"
    pd1 = get_ontology("http://www.e-lico.eu/ontologies/dmo/DMOP/PD.owl")
    pd1.base_iri = "http://www.e-lico.eu/ontologies/dmo/DMOP/PD.owl#"

    print("ONTO LOADED**************************")

    with onto:
        fileName = 'testsample1'

        mtla = mtl.LearningFromTaskProperties(fileName, namespace=onto)
        mtlt = mtl.FeatureSelectionRecommendationTask(fileName, namespace=onto)

        fileObject = dmop.LabeledDataSet(fileName, namespace=onto)
        fsr_output = mtl.FeatureSelectionRecommendation(fileName, namespace=onto)
        mtla.addresses.append(mtlt)


        mtlt.specifiesInputClass = [fileObject]
        mtlt.specifiesOutputClass = [fsr_output]
        mean_name="RANDOM"
        feature = dmop1.NumberOfInstances("instances_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_instances", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(int(df['nr_inst']))
        fileObject.hasQuality.append(feature)

        feature = mtl.EigenValues("eigen_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_eigen", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['eigenvalues.mean']))
        fileObject.hasQuality.append(feature)

        feature = mtl.AttributeConcentration("attrconc_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_attrconc", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append( float(df['attr_conc.mean']))
        fileObject.hasQuality.append(feature)

        feature = mtl.NumberOfClasses("nunique_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_nunique", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append( int(df['nUnique']))
        fileObject.hasQuality.append(feature)
    
        feature = mtl.NumberOfHighlyCorrelatedAttributes("nrcorattr_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "__nrcorattr", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['nr_cor_attr']))
        fileObject.hasQuality.append(feature)

        feature = mtl.GeometricMean("gmean_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "__gmean", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append( float(df['g_mean.mean']))
        fileObject.hasQuality.append(feature)
        
        feature = mtl.AttributesEntropy("aentr_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_attrent", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append( float(df['attr_ent.mean']))
        fileObject.hasQuality.append(feature)

        feature = mtl.EqNumberOfAttributes("ena_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_ena", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['ena']))
        fileObject.hasQuality.append(feature)
        
        feature = mtl.LabelNoise("labelissuesperc_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_labelissuesperc", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['LabelIssuesPerc']))
        fileObject.hasQuality.append(feature)

        feature = mtl.ProportionOfAttrToInstances("attrinst_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_attrinst", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['attr_to_inst']))
        fileObject.hasQuality.append(feature)
        
        feature = mtl.Range("range_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_range", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['range.mean']))
        fileObject.hasQuality.append(feature)

        feature = mtl.ClassEntropy("centropy_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_centropy", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append( float(df['cEntropy']))
        fileObject.hasQuality.append(feature)

        feature = mtl.TrimmedMean("tmean_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_tmean", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['t_mean.mean']))
        fileObject.hasQuality.append(feature)

        feature = mtl.Skewness("skew_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_skew", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['skewness.mean']))
        fileObject.hasQuality.append(feature)
        
        feature = mtl.Mean("mean_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_mean", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['mean.mean']))
        fileObject.hasQuality.append(feature)

        feature = dmop1.NumberOfFeatures("nrAttr_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_nrAttr", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['nr_attr']))
        fileObject.hasQuality.append(feature)
        
        feature = mtl.OutlierDetection("outperc_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "_outperc", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['OutliersPerc']))
        fileObject.hasQuality.append(feature)

        feature = mtl.InterquartileRange("iqrmean_feature", namespace=onto)
        mean = mtl.Mean(mean_name + "__iqrmean", namespace=onto)
        feature.qlocation.append(mean)
        mean.hasDatavalue.append(float(df['iq_range.mean']))
        fileObject.hasQuality.append(feature)
        

        
    # AllDifferent([q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15])
    close_world([onto])
    
    start = time.time()

    try:    
        sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True)
        print("Ontology is consistent.")
    except OwlReadyInconsistentOntologyError:
        print("*******Ontology inconsistent, Checking problem individuals***********")
        for ind in onto.individuals():
            if ind.is_instance_of:
                print(f"Individual: {ind}, Classes: {ind.is_instance_of}")
    except Exception as e:
        print("Reasoner failed:", e)    
    finally:
        print(f"*********Reasoning took {time.time() - start:.2f} seconds\n\n\n")

    flag=1
    if onto.MI1RelevantData in fileObject.is_a:
        output = onto.MI1Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies MI1RelevantData constraint", output[0].recommends)
        flag=0
    if onto.MI2RelevantData in fileObject.is_a:
        output = onto.MI2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies MI2RelevantData constraint", output[0].recommends)
        flag=0
    if onto.FCBF1RelevantData in fileObject.is_a:
        output = onto.FCBF1Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies FCBF1RelevantData constraint", output[0].recommends)
        flag=0
    if onto.FCBF2RelevantData in fileObject.is_a:
        output = onto.FCBF2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies FCBF2RelevantData constraint", output[0].recommends)
        flag=0
    if onto.FCBF3RelevantData in fileObject.is_a:
        output = onto.FCBF2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies FCBF3RelevantData constraint", output[0].recommends)
        flag=0
    if onto.FCBF4RelevantData in fileObject.is_a:
        output = onto.FCBF4Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies FCBF4RelevantData constraint", output[0].recommends)
        flag=0
    if onto.GRRelevantData in fileObject.is_a:
        output = onto.GRTask.specifiesOutputClass
        print(f"{fileObject.name} satisfies GRRelevantData constraint", output[0].recommends)
        flag=0
    if onto.Relief1RelevantData in fileObject.is_a:
        output = onto.Relief1Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies Relief1RelevantData constraint", output[0].recommends)
        flag=0
    if onto.Relief2RelevantData in fileObject.is_a:
        output = onto.Relief2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies Relief2RelevantData constraint", output[0].recommends)
        flag=0
    if onto.Chisquare1RelevantData in fileObject.is_a:
        output = onto.Chisquare2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies Chisquare1RelevantData constraint", output[0].recommends)
        flag=0
    if onto.Chisquare2RelevantData in fileObject.is_a:
        output = onto.Chisquare2Task.specifiesOutputClass
        print(f"{fileObject.name} satisfies Chisquare2RelevantData constraint", output[0].recommends)
        flag=0
    if(flag==1): 
        print("NO RECOMMENDATION")

    print("\n\n\n\nSRIRAMA****************************\n")
    if flag == 1:
        return "NO RECOMMENDATION"
    else:
        return output[0].recommends

