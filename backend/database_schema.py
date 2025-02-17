DATABASE_SCHEMA = """
chembl_35 Schema Documentation


ACTION_TYPE:
Table storing the distinct list of action types used in the drug_mechanism table, together with a higher-level parent action type.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ACTION_TYPE         VARCHAR2(50)        NOT NULL            Primary key. Type of action of the drug e.g., agonist, antagonist
                    DESCRIPTION         VARCHAR2(200)       NOT NULL            Description of how the action type is used
                    PARENT_TYPE         VARCHAR2(50)                            Higher-level grouping of action types e.g., positive vs negative action


ACTIVITIES:
Activity 'values' or 'end points'  that are the results of an assay recorded in a scientific document. Each activity is described by a row.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ACTIVITY_ID         NUMBER              NOT NULL            Unique ID for the activity row
FK                  ASSAY_ID            NUMBER              NOT NULL            Foreign key to the assays table (containing the assay description)
FK                  DOC_ID              NUMBER                                  Foreign key to documents table (for quick lookup of publication details - can also link to documents through compound_records or assays table)
FK                  RECORD_ID           NUMBER              NOT NULL            Foreign key to the compound_records table (containing information on the compound tested)
FK                  MOLREGNO            NUMBER                                  Foreign key to compounds table (for quick lookup of compound structure - can also link to compounds through compound_records table)
                    STANDARD_RELATION   VARCHAR2(50)                            Symbol constraining the activity value (e.g. >, <, =)
                    STANDARD_VALUE      NUMBER                                  Same as PUBLISHED_VALUE but transformed to common units: e.g. mM concentrations converted to nM.
                    STANDARD_UNITS      VARCHAR2(100)                           Selected 'Standard' units for data type: e.g. concentrations are in nM.
                    STANDARD_FLAG       NUMBER                                  Shows whether the standardised columns have been curated/set (1) or just default to the published data (0).
                    STANDARD_TYPE       VARCHAR2(250)                           Standardised version of the published_activity_type (e.g. IC50 rather than Ic-50/Ic50/ic50/ic-50)
                    ACTIVITY_COMMENT    VARCHAR2(4000)                          Previously used to report non-numeric activities i.e. 'Slighty active', 'Not determined'. STANDARD_TEXT_VALUE will be used for this in future, and this will be just for additional comments.
FK                  DATA_VALIDITY_COMMENT                   VARCHAR2(30)                            Comment reflecting whether the values for this activity measurement are likely to be correct - one of 'Manually validated' (checked original paper and value is correct), 'Potential author error' (value looks incorrect but is as reported in the original paper), 'Outside typical range' (value seems too high/low to be correct e.g., negative IC50 value), 'Non standard unit type' (units look incorrect for this activity type).
                    POTENTIAL_DUPLICATE NUMBER                                  When set to 1, indicates that the value is likely to be a repeat citation of a value reported in a previous ChEMBL paper, rather than a new, independent measurement. Note: value of zero does not guarantee that the measurement is novel/independent though
                    PCHEMBL_VALUE       NUMBER                                  Negative log of selected concentration-response activity values (IC50/EC50/XC50/AC50/Ki/Kd/Potency)
FK                  BAO_ENDPOINT        VARCHAR2(11)                            ID for the corresponding result type in BioAssay Ontology (based on standard_type)
                    UO_UNITS            VARCHAR2(10)                            ID for the corresponding unit in Unit Ontology (based on standard_units)
                    QUDT_UNITS          VARCHAR2(70)                            ID for the corresponding unit in QUDT Ontology (based on standard_units)
                    TOID                INTEGER                                 The Test Occasion Identifier, used to group together related activity measurements
                    UPPER_VALUE         NUMBER                                  Where the activity is a range, this represents the highest value of the range (numerically), while the PUBLISHED_VALUE column represents the lower value
                    STANDARD_UPPER_VALUE                    NUMBER                                  Where the activity is a range, this represents the standardised version of the highest value of the range (with the lower value represented by STANDARD_VALUE)
FK                  SRC_ID              NUMBER                                  Foreign key to source table, indicating the source of the activity value
                    TYPE                VARCHAR2(250)       NOT NULL            Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset
                    RELATION            VARCHAR2(50)                            Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset
                    VALUE               NUMBER                                  Datapoint value as it appears in the original dataset.
                    UNITS               VARCHAR2(100)                           Units of measurement as they appear in the original dataset
                    TEXT_VALUE          VARCHAR2(1000)                          Additional information about the measurement
                    STANDARD_TEXT_VALUE VARCHAR2(1000)                          Standardized version of additional information about the measurement
FK                  ACTION_TYPE         VARCHAR2(50)                            Foreign key to action_type table; specifies the effect of the compound on its target.


ACTIVITY_PROPERTIES:
Table storing parameters and properties of Activity_IDs in the ACTIVITIES table - can be either independent variables that do not apply to the whole assay (e.g., compounds 'DOSE'), or dependent variables/results that are important in interpreting the activity values (e.g., 'HILL_SLOPE')

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  AP_ID               NUMBER              NOT NULL            Unique ID for each record.
FK,UK               ACTIVITY_ID         NUMBER              NOT NULL            FK to ACTIVITY_ID in ACTIVITIES table.
UK                  TYPE                VARCHAR2(250)       NOT NULL            The parameter or property type
                    RELATION            VARCHAR2(50)                            Symbol constraining the value (e.g. >, <, =)
                    VALUE               NUMBER                                  Numberical value for the parameter or property
                    UNITS               VARCHAR2(100)                           Units of measurement
                    TEXT_VALUE          VARCHAR2(2000)                          Non-numerical value of the parameter or property
                    STANDARD_TYPE       VARCHAR2(250)                           Standardised form of the TYPE
                    STANDARD_RELATION   VARCHAR2(50)                            Standardised form of the RELATION
                    STANDARD_VALUE      NUMBER                                  Standardised form of the VALUE
                    STANDARD_UNITS      VARCHAR2(100)                           Standardised form of the UNITS
                    STANDARD_TEXT_VALUE VARCHAR2(2000)                          Standardised form of the TEXT_VALUE
                    COMMENTS            VARCHAR2(2000)                          A Comment.
                    RESULT_FLAG         NUMBER              NOT NULL            A flag to indicate, if set to 1, that this type is a dependent variable/result (e.g., slope) rather than an independent variable/parameter (0, the default).


ACTIVITY_SMID:
A join table between ACTIVITY_SUPP_MAP and ACTIVITY_SUPP

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  SMID                NUMBER              NOT NULL            FK to SMID in ACTIVITY_SUPP_MAP, and a FK to SMID in ACTIVITY_SUPP


ACTIVITY_STDS_LOOKUP:
Table storing details of standardised activity types and units, with permitted value ranges. Used to determine the correct standard_type and standard_units for a range of published types/units.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  STD_ACT_ID          NUMBER              NOT NULL            Primary key.
UK                  STANDARD_TYPE       VARCHAR2(250)       NOT NULL            The standard_type that other published_types in the activities table have been converted to.
                    DEFINITION          VARCHAR2(500)                           A description/definition of the standard_type.
UK                  STANDARD_UNITS      VARCHAR2(100)       NOT NULL            The units that are applied to this standard_type and to which other published_units are converted. Note a standard_type may have more than one allowable standard_unit and therefore multiple rows in this table.
                    NORMAL_RANGE_MIN    NUMBER                                  The lowest value for this activity type that is likely to be genuine. This is only an approximation, so lower genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table below this threshold are flagged with a data_validity_comment of 'Outside typical range'.
                    NORMAL_RANGE_MAX    NUMBER                                  The highest value for this activity type that is likely to be genuine. This is only an approximation, so higher genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table above this threshold are flagged with a data_validity_comment of 'Outside typical range'.


ACTIVITY_SUPP:
Supplementary / Supporting Data for ACTIVITIES - can be linked via ACTIVITY_SMID and ACTIVITY_SUPP_MAP tables

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  AS_ID               NUMBER              NOT NULL            Unique ID for each record.
UK                  RGID                NUMBER              NOT NULL            Record Grouping ID, used to group together related data points in this table
FK                  SMID                NUMBER                                  FK to SMID in ACTIVITY_SMID.
UK                  TYPE                VARCHAR2(250)       NOT NULL            Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset
                    RELATION            VARCHAR2(50)                            Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset
                    VALUE               NUMBER                                  Datapoint value as it appears in the original dataset.
                    UNITS               VARCHAR2(100)                           Units of measurement as they appear in the original dataset
                    TEXT_VALUE          VARCHAR2(1000)                          Non-numeric value for measurement as in original dataset
                    STANDARD_TYPE       VARCHAR2(250)                           Standardised form of the TYPE
                    STANDARD_RELATION   VARCHAR2(50)                            Standardised form of the RELATION
                    STANDARD_VALUE      NUMBER                                  Standardised form of the VALUE
                    STANDARD_UNITS      VARCHAR2(100)                           Standardised form of the UNITS
                    STANDARD_TEXT_VALUE VARCHAR2(1000)                          Standardised form of the TEXT_VALUE
                    COMMENTS            VARCHAR2(4000)                          A Comment.


ACTIVITY_SUPP_MAP:
Mapping table, linking supplementary / supporting data from the ACTIVITY_SUPP table to the main ACTIVITIES table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ACTSM_ID            NUMBER              NOT NULL            Primary key
FK                  ACTIVITY_ID         NUMBER              NOT NULL            FK to ACTIVITY_ID in ACTIVITIES table.
FK                  SMID                NUMBER              NOT NULL            FK to SMID in ACTIVITY_SMID.


ASSAY_CLASS_MAP:
Mapping table linking assays to classes in the ASSAY_CLASSIFICATION table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ASS_CLS_MAP_ID      NUMBER              NOT NULL            Primary key.
FK,UK               ASSAY_ID            NUMBER              NOT NULL            Foreign key that maps to the ASSAYS table
FK,UK               ASSAY_CLASS_ID      NUMBER              NOT NULL            Foreign key that maps to the ASSAY_CLASSIFICATION table


ASSAY_CLASSIFICATION:
Classification scheme for phenotypic assays e.g., by therapeutic area, phenotype/process and assay type. Can be used to find standard assays for a particular disease area or phenotype e.g., anti-obesity assays. Currently data are available only for in vivo efficacy assays

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ASSAY_CLASS_ID      NUMBER              NOT NULL            Primary key
                    L1                  VARCHAR2(100)                           High level classification e.g., by anatomical/therapeutic area
                    L2                  VARCHAR2(100)                           Mid-level classification e.g., by phenotype/biological process
UK                  L3                  VARCHAR2(1000)                          Fine-grained classification e.g., by assay type
                    CLASS_TYPE          VARCHAR2(50)                            The type of assay being classified e.g., in vivo efficacy
                    SOURCE              VARCHAR2(50)                            Source from which the assay class was obtained


ASSAY_PARAMETERS:
Table storing additional parameters for an assay e.g., dose, administration route, time point

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ASSAY_PARAM_ID      NUMBER              NOT NULL            Numeric primary key
FK,UK               ASSAY_ID            NUMBER              NOT NULL            Foreign key to assays table. The assay to which this parameter belongs
UK                  TYPE                VARCHAR2(250)       NOT NULL            The type of parameter being described, according to the original data source
                    RELATION            VARCHAR2(50)                            The relation symbol for the parameter being described, according to the original data source
                    VALUE               NUMBER                                  The value of the parameter being described, according to the original data source. Used for numeric data
                    UNITS               VARCHAR2(100)                           The units for the parameter being described, according to the original data source
                    TEXT_VALUE          VARCHAR2(4000)                          The text value of the parameter being described, according to the original data source. Used for non-numeric/qualitative data
                    STANDARD_TYPE       VARCHAR2(250)                           Standardized form of the TYPE
                    STANDARD_RELATION   VARCHAR2(50)                            Standardized form of the RELATION
                    STANDARD_VALUE      NUMBER                                  Standardized form of the VALUE
                    STANDARD_UNITS      VARCHAR2(100)                           Standardized form of the UNITS
                    STANDARD_TEXT_VALUE VARCHAR2(4000)                          Standardized form of the TEXT_VALUE
                    COMMENTS            VARCHAR2(4000)                          Additional comments describing the parameter


ASSAY_TYPE:
Description of assay types (e.g., Binding, Functional, ADMET)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ASSAY_TYPE          VARCHAR2(1)         NOT NULL            Single character representing assay type
                    ASSAY_DESC          VARCHAR2(250)                           Description of assay type


ASSAYS:
Table storing a list of the assays that are reported in each document. Similar assays from different publications will appear as distinct assays in this table.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ASSAY_ID            NUMBER              NOT NULL            Unique ID for the assay
FK                  DOC_ID              NUMBER              NOT NULL            Foreign key to documents table
                    DESCRIPTION         VARCHAR2(4000)                          Description of the reported assay
FK                  ASSAY_TYPE          VARCHAR2(1)                             Assay classification, e.g. B=Binding assay, A=ADME assay, F=Functional assay
                    ASSAY_TEST_TYPE     VARCHAR2(20)                            Type of assay system (i.e., in vivo or in vitro)
                    ASSAY_CATEGORY      VARCHAR2(50)                            screening, confirmatory (ie: dose-response), summary, panel, other,Thermal shift assay QC liability, Thermal shift assay, Affinity biochemical assay, Incucyte cell viability, Affinity phenotypic cellular assay, HTRF assay, Selectivity assay, Cell health data, NanoBRET assay, Alphascreen assay, Affinity on-target cellular assay, ITC assay, GPCR beta-arrestin recruitment assay
                    ASSAY_ORGANISM      VARCHAR2(250)                           Name of the organism for the assay system (e.g., the organism, tissue or cell line in which an assay was performed). May differ from the target organism (e.g., for a human protein expressed in non-human cells, or pathogen-infected human cells).
                    ASSAY_TAX_ID        NUMBER                                  NCBI tax ID for the assay organism.
                    ASSAY_STRAIN        VARCHAR2(200)                           Name of specific strain of the assay organism used (where known)
                    ASSAY_TISSUE        VARCHAR2(100)                           Name of tissue used in the assay system (e.g., for tissue-based assays) or from which the assay system was derived (e.g., for cell/subcellular fraction-based assays).
                    ASSAY_CELL_TYPE     VARCHAR2(100)                           Name of cell type or cell line used in the assay system (e.g., for cell-based assays).
                    ASSAY_SUBCELLULAR_FRACTION              VARCHAR2(100)                           Name of subcellular fraction used in the assay system (e.g., microsomes, mitochondria).
FK                  TID                 NUMBER                                  Target identifier to which this assay has been mapped. Foreign key to target_dictionary. From ChEMBL_15 onwards, an assay will have only a single target assigned.
FK                  RELATIONSHIP_TYPE   VARCHAR2(1)                             Flag indicating of the relationship between the reported target in the source document and the assigned target from TARGET_DICTIONARY. Foreign key to RELATIONSHIP_TYPE table.
FK                  CONFIDENCE_SCORE    NUMBER                                  Confidence score, indicating how accurately the assigned target(s) represents the actually assay target. Foreign key to CONFIDENCE_SCORE table. 0 means uncurated/unassigned, 1 = low confidence to 9 = high confidence.
FK                  CURATED_BY          VARCHAR2(32)                            Indicates the level of curation of the target assignment. Foreign key to curation_lookup table.
FK                  SRC_ID              NUMBER              NOT NULL            Foreign key to source table
                    SRC_ASSAY_ID        VARCHAR2(50)                            Identifier for the assay in the source database/deposition (e.g., pubchem AID)
FK,UK               CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier for this assay (for use on web interface etc)
FK                  CELL_ID             NUMBER                                  Foreign key to cell dictionary. The cell type or cell line used in the assay
FK                  BAO_FORMAT          VARCHAR2(11)                            ID for the corresponding format type in BioAssay Ontology (e.g., cell-based, biochemical, organism-based etc)
FK                  TISSUE_ID           NUMBER                                  ID for the corresponding tissue/anatomy in Uberon. Foreign key to tissue_dictionary
FK                  VARIANT_ID          NUMBER                                  Foreign key to variant_sequences table. Indicates the mutant/variant version of the target used in the assay (where known/applicable)
                    AIDX                VARCHAR2(200)       NOT NULL            The Depositor Defined Assay Identifier
                    ASSAY_GROUP         VARCHAR2(200)                           Assays deposited across multiple datasets/releases that are considered comparable by the depositor are mapped to the same ASSAY GROUP. Allows depositors to group comparable assays and users to identify assays that can be considered identical. 


ATC_CLASSIFICATION:
WHO ATC Classification for drugs

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
                    WHO_NAME            VARCHAR2(2000)                          WHO/INN name for the compound
                    LEVEL1              VARCHAR2(10)                            First level of classification
                    LEVEL2              VARCHAR2(10)                            Second level of classification
                    LEVEL3              VARCHAR2(10)                            Third level of classification
                    LEVEL4              VARCHAR2(10)                            Fourth level of classification
PK                  LEVEL5              VARCHAR2(10)        NOT NULL            Complete ATC code for compound
                    LEVEL1_DESCRIPTION  VARCHAR2(2000)                          Description of first level of classification
                    LEVEL2_DESCRIPTION  VARCHAR2(2000)                          Description of second level of classification
                    LEVEL3_DESCRIPTION  VARCHAR2(2000)                          Description of third level of classification
                    LEVEL4_DESCRIPTION  VARCHAR2(2000)                          Description of fourth level of classification


BINDING_SITES:
Table storing details of binding sites for a target. A target may have multiple sites defined in this table.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  SITE_ID             NUMBER              NOT NULL            Primary key. Unique identifier for a binding site in a given target.
                    SITE_NAME           VARCHAR2(200)                           Name/label for the binding site.
FK                  TID                 NUMBER                                  Foreign key to target_dictionary. Target on which the binding site is found.


BIO_COMPONENT_SEQUENCES:
Table storing the sequences for biotherapeutic drugs (e.g., monoclonal antibodies, recombinant proteins, peptides etc. For multi-chain biotherapeutics (e.g., mAbs) each chain is stored here as a separate component.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  COMPONENT_ID        NUMBER              NOT NULL            Primary key. Unique identifier for each of the molecular components of biotherapeutics in ChEMBL (e.g., antibody chains, recombinant proteins, synthetic peptides).
                    COMPONENT_TYPE      VARCHAR2(50)        NOT NULL            Type of molecular component (e.g., 'PROTEIN', 'NUCLEIC ACID').
                    DESCRIPTION         VARCHAR2(200)                           Description/name of molecular component.
                    SEQUENCE            CLOB                                    Sequence of the biotherapeutic component.
                    SEQUENCE_MD5SUM     VARCHAR2(32)                            MD5 checksum of the sequence.
                    TAX_ID              NUMBER                                  NCBI tax ID for the species from which the sequence is derived. May be null for humanized monoclonal antibodies, synthetic peptides etc.
                    ORGANISM            VARCHAR2(150)                           Name of the species from which the sequence is derived.


BIOASSAY_ONTOLOGY:
Lookup table providing labels for Bioassay Ontology terms used in assays and activities tables

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  BAO_ID              VARCHAR2(11)        NOT NULL            Bioassay Ontology identifier (BAO version 2.0)
                    LABEL               VARCHAR2(100)       NOT NULL            Bioassay Ontology label for the term (BAO version 2.0)


BIOTHERAPEUTIC_COMPONENTS:
Links each biotherapeutic drug (in the biotherapeutics table) to its component sequences (in the bio_component_sequences table). A biotherapeutic drug can have multiple components and hence multiple rows in this table. Similarly, a particular component sequence can be part of more than one drug.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  BIOCOMP_ID          NUMBER              NOT NULL            Primary key.
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to the biotherapeutics table, indicating which biotherapeutic the component is part of.
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to the bio_component_sequences table, indicating which component is part of the biotherapeutic.


BIOTHERAPEUTICS:
Table mapping biotherapeutics (e.g. recombinant proteins, peptides and antibodies) to the molecule_dictionary table. Includes HELM notation where available.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK,FK               MOLREGNO            NUMBER              NOT NULL            Foreign key to molecule_dictionary
                    DESCRIPTION         VARCHAR2(2000)                          Description of the biotherapeutic.
                    HELM_NOTATION       VARCHAR2(4000)                          Sequence notation generated according to the HELM standard (http://www.openhelm.org/home). Currently for peptides only


CELL_DICTIONARY:
Table storing information for cell lines in the target_dictionary (e.g., tissue/species origin). Cell_name should match pref_name in target_dictionary.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CELL_ID             NUMBER              NOT NULL            Primary key. Unique identifier for each cell line in the target_dictionary.
UK                  CELL_NAME           VARCHAR2(50)        NOT NULL            Name of each cell line (as used in the target_dicitonary pref_name).
                    CELL_DESCRIPTION    VARCHAR2(200)                           Longer description (where available) of the cell line.
                    CELL_SOURCE_TISSUE  VARCHAR2(50)                            Tissue from which the cell line is derived, where known.
                    CELL_SOURCE_ORGANISM                    VARCHAR2(150)                           Name of organism from which the cell line is derived.
UK                  CELL_SOURCE_TAX_ID  NUMBER                                  NCBI tax ID of the organism from which the cell line is derived.
                    CLO_ID              VARCHAR2(11)                            ID for the corresponding cell line in Cell Line Ontology
                    EFO_ID              VARCHAR2(12)                            ID for the corresponding cell line in Experimental Factory Ontology
                    CELLOSAURUS_ID      VARCHAR2(15)                            ID for the corresponding cell line in Cellosaurus Ontology
                    CL_LINCS_ID         VARCHAR2(8)                             Cell ID used in LINCS (Library of Integrated Network-based Cellular Signatures)
FK,UK               CHEMBL_ID           VARCHAR2(20)                            ChEMBL identifier for the cell (used in web interface etc)
                    CELL_ONTOLOGY_ID    VARCHAR2(10)                            ID for the corresponding cell type in the Cell Ontology


CHEMBL_ID_LOOKUP:
Lookup table storing chembl identifiers for different entities in the database (assays, compounds, documents and targets)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier
UK                  ENTITY_TYPE         VARCHAR2(50)        NOT NULL            Type of entity (e.g., COMPOUND, ASSAY, TARGET)
UK                  ENTITY_ID           NUMBER              NOT NULL            Primary key for that entity in corresponding table (e.g., molregno for compounds, tid for targets)
                    STATUS              VARCHAR2(10)        NOT NULL            Indicates whether the status of the entity within the database - ACTIVE, INACTIVE (downgraded), OBS (obsolete/removed).
                    LAST_ACTIVE         NUMBER                                  indicates the last ChEMBL version where the CHEMBL_ID was active


CHEMBL_RELEASE:
Table listing ChEMBL releases with their creation dates

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CHEMBL_RELEASE_ID   INTEGER             NOT NULL            Primary key
                    CHEMBL_RELEASE      VARCHAR2(20)                            ChEMBL release name
                    CREATION_DATE       DATE                                    ChEMBL release creation date


COMPONENT_CLASS:
Links protein components of targets to the protein_family_classification table. A protein can have more than one classification (e.g., Membrane receptor and Enzyme).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to component_sequences table.
FK,UK               PROTEIN_CLASS_ID    NUMBER              NOT NULL            Foreign key to the protein_classification table.
PK                  COMP_CLASS_ID       NUMBER              NOT NULL            Primary key.


COMPONENT_DOMAINS:
Links protein components of targets to the structural domains they contain (from the domains table). Contains information showing the start and end position of the domain in the component sequence.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  COMPD_ID            NUMBER              NOT NULL            Primary key.
FK,UK               DOMAIN_ID           NUMBER                                  Foreign key to the domains table, indicating the domain that is contained in the associated molecular component.
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to the component_sequences table, indicating the molecular_component that has the given domain.
UK                  START_POSITION      NUMBER                                  Start position of the domain within the sequence given in the component_sequences table.
                    END_POSITION        NUMBER                                  End position of the domain within the sequence given in the component_sequences table.


COMPONENT_GO:
Table mapping protein components in the COMPONENT_SEQUENCES table to the GO slim terms stored in the GO_CLASSIFICATION table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  COMP_GO_ID          NUMBER              NOT NULL            Primary key
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to COMPONENT_SEQUENCES table. The protein component this GO term applies to
FK,UK               GO_ID               VARCHAR2(10)        NOT NULL            Foreign key to the GO_CLASSIFICATION table. The GO term that this protein is mapped to


COMPONENT_SEQUENCES:
Table storing the sequences for components of molecular targets (e.g., protein sequences), along with other details taken from sequence databases (e.g., names, accessions). Single protein targets will have a single protein component in this table, whereas protein complexes/protein families will have multiple protein components.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  COMPONENT_ID        NUMBER              NOT NULL            Primary key. Unique identifier for the component.
                    COMPONENT_TYPE      VARCHAR2(50)                            Type of molecular component represented (e.g., 'PROTEIN','DNA','RNA').
UK                  ACCESSION           VARCHAR2(25)                            Accession for the sequence in the source database from which it was taken (e.g., UniProt accession for proteins).
                    SEQUENCE            CLOB                                    A representative sequence for the molecular component, as given in the source sequence database (not necessarily the exact sequence used in the assay).
                    SEQUENCE_MD5SUM     VARCHAR2(32)                            MD5 checksum of the sequence.
                    DESCRIPTION         VARCHAR2(200)                           Description/name for the molecular component, usually taken from the source sequence database.
                    TAX_ID              NUMBER                                  NCBI tax ID for the sequence in the source database (i.e., species that the protein/nucleic acid sequence comes from).
                    ORGANISM            VARCHAR2(150)                           Name of the organism the sequence comes from.
                    DB_SOURCE           VARCHAR2(25)                            The name of the source sequence database from which sequences/accessions are taken. For UniProt proteins, this field indicates whether the sequence is from SWISS-PROT or TREMBL.
                    DB_VERSION          VARCHAR2(10)                            The version of the source sequence database from which sequences/accession were last updated.


COMPONENT_SYNONYMS:
Table storing synonyms for the components of molecular targets (e.g., names, acronyms, gene symbols etc.) Please note: EC numbers are also currently included in this table although they are not strictly synonyms and can apply to multiple proteins.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  COMPSYN_ID          NUMBER              NOT NULL            Primary key.
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to the component_sequences table. The component to which this synonym applies.
UK                  COMPONENT_SYNONYM   VARCHAR2(500)                           The synonym for the component.
UK                  SYN_TYPE            VARCHAR2(20)                            The type or origin of the synonym (e.g., GENE_SYMBOL).


COMPOUND_PROPERTIES:
Table storing calculated physicochemical properties for compounds, now calculated with RDKit and ChemAxon software (note all but FULL_MWT and FULL_MOLFORMULA are calculated on the parent structure)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK,FK               MOLREGNO            NUMBER              NOT NULL            Foreign key to compounds table (compound structure)
                    MW_FREEBASE         NUMBER                                  Molecular weight of parent compound
                    ALOGP               NUMBER                                  Calculated ALogP
                    HBA                 NUMBER                                  Number hydrogen bond acceptors
                    HBD                 NUMBER                                  Number hydrogen bond donors
                    PSA                 NUMBER                                  Polar surface area
                    RTB                 NUMBER                                  Number rotatable bonds
                    RO3_PASS            VARCHAR2(3)                             Indicates whether the compound passes the rule-of-three (mw < 300, logP < 3 etc)
                    NUM_RO5_VIOLATIONS  NUMBER                                  Number of violations of Lipinski's rule-of-five, using HBA and HBD definitions
                    CX_MOST_APKA        NUMBER                                  The most acidic pKa calculated using ChemAxon v17.29.0
                    CX_MOST_BPKA        NUMBER                                  The most basic pKa calculated using ChemAxon v17.29.0
                    CX_LOGP             NUMBER                                  The calculated octanol/water partition coefficient using ChemAxon v17.29.0
                    CX_LOGD             NUMBER                                  The calculated octanol/water distribution coefficient at pH7.4 using ChemAxon v17.29.0
                    MOLECULAR_SPECIES   VARCHAR2(50)                            Indicates whether the compound is an acid/base/neutral
                    FULL_MWT            NUMBER                                  Molecular weight of the full compound including any salts
                    AROMATIC_RINGS      NUMBER                                  Number of aromatic rings
                    HEAVY_ATOMS         NUMBER                                  Number of heavy (non-hydrogen) atoms
                    QED_WEIGHTED        NUMBER                                  Weighted quantitative estimate of drug likeness (as defined by Bickerton et al., Nature Chem 2012)
                    MW_MONOISOTOPIC     NUMBER                                  Monoisotopic parent molecular weight
                    FULL_MOLFORMULA     VARCHAR2(100)                           Molecular formula for the full compound (including any salt)
                    HBA_LIPINSKI        NUMBER                                  Number of hydrogen bond acceptors calculated according to Lipinski's original rules (i.e., N + O count))
                    HBD_LIPINSKI        NUMBER                                  Number of hydrogen bond donors calculated according to Lipinski's original rules (i.e., NH + OH count)
                    NUM_LIPINSKI_RO5_VIOLATIONS             NUMBER                                  Number of violations of Lipinski's rule of five using HBA_LIPINSKI and HBD_LIPINSKI counts
                    NP_LIKENESS_SCORE   NUMBER                                  Natural Product-likeness Score: Peter Ertl, Silvio Roggo, and Ansgar Schuffenhauer Journal of Chemical Information and Modeling, 48, 68-74 (2008) 


COMPOUND_RECORDS:
Represents each compound extracted from scientific documents.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  RECORD_ID           NUMBER              NOT NULL            Unique ID for a compound/record
FK                  MOLREGNO            NUMBER                                  Foreign key to compounds table (compound structure)
FK                  DOC_ID              NUMBER              NOT NULL            Foreign key to documents table
                    COMPOUND_KEY        VARCHAR2(250)                           Key text identifying this compound in the scientific document
                    COMPOUND_NAME       VARCHAR2(4000)                          Name of this compound recorded in the scientific document
FK                  SRC_ID              NUMBER              NOT NULL            Foreign key to source table
                    SRC_COMPOUND_ID     VARCHAR2(150)                           Identifier for the compound in the source database (e.g., pubchem SID)
                    CIDX                VARCHAR2(200)       NOT NULL            The Depositor Defined Compound Identifier.


COMPOUND_STRUCTURAL_ALERTS:
Table showing which structural alerts (as defined in the STRUCTURAL_ALERTS table) are found in a particular ChEMBL compound. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CPD_STR_ALERT_ID    NUMBER              NOT NULL            Primary key.
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to the molecule_dictionary. The compound for which the structural alert has been found.
FK,UK               ALERT_ID            NUMBER              NOT NULL            Foreign key to the structural_alerts table. The particular alert that has been identified in this compound.


COMPOUND_STRUCTURES:
Table storing various structure representations (e.g., Molfile, InChI) for each compound

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK,FK               MOLREGNO            NUMBER              NOT NULL            Internal Primary Key for the compound structure and foreign key to molecule_dictionary table
                    MOLFILE             CLOB                                    MDL Connection table representation of compound
UK                  STANDARD_INCHI      VARCHAR2(4000)                          IUPAC standard InChI for the compound
UK                  STANDARD_INCHI_KEY  VARCHAR2(27)        NOT NULL            IUPAC standard InChI key for the compound
                    CANONICAL_SMILES    VARCHAR2(4000)                          Canonical smiles, generated using RDKit


CONFIDENCE_SCORE_LOOKUP:
Lookup table describing how assays confidence scores are assigned depending on the type of target(s) assigned to the assay and the level of confidence in their molecular identity

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CONFIDENCE_SCORE    NUMBER              NOT NULL            0-9 score showing level of confidence in assignment of the precise molecular target of the assay
                    DESCRIPTION         VARCHAR2(100)       NOT NULL            Description of the target types assigned with each score
                    TARGET_MAPPING      VARCHAR2(30)        NOT NULL            Short description of the target types assigned with each score


CURATION_LOOKUP:
Lookup table for assays.curated_by column. Shows level of curation that has been applied to the assay to target mapping.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CURATED_BY          VARCHAR2(32)        NOT NULL            Short description of the level of curation
                    DESCRIPTION         VARCHAR2(100)       NOT NULL            Definition of terms in the curated_by field.


DATA_VALIDITY_LOOKUP:
Table storing information about the data_validity_comment values used in the activities table.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  DATA_VALIDITY_COMMENT                   VARCHAR2(30)        NOT NULL            Primary key. Short description of various types of errors/warnings applied to values in the activities table.
                    DESCRIPTION         VARCHAR2(200)                           Definition of the terms in the data_validity_comment field.


DEFINED_DAILY_DOSE:
WHO DDD (defined daily dose) information

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK                  ATC_CODE            VARCHAR2(10)        NOT NULL            ATC code for the compound (foreign key to ATC_CLASSIFICATION table)
                    DDD_UNITS           VARCHAR2(200)                           Units of defined daily dose
                    DDD_ADMR            VARCHAR2(1000)                          Administration route for dose
                    DDD_COMMENT         VARCHAR2(2000)                          Comment
PK                  DDD_ID              NUMBER              NOT NULL            Internal primary key
                    DDD_VALUE           NUMBER                                  Value of defined daily dose


DOCS:
Holds all scientific documents (journal articles or patents) from which assays have been extracted.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  DOC_ID              NUMBER              NOT NULL            Unique ID for the document
                    JOURNAL             VARCHAR2(50)                            Abbreviated journal name for an article
                    YEAR                NUMBER                                  Year of journal article publication
                    VOLUME              VARCHAR2(50)                            Volume of journal article
                    ISSUE               VARCHAR2(50)                            Issue of journal article
                    FIRST_PAGE          VARCHAR2(50)                            First page number of journal article
                    LAST_PAGE           VARCHAR2(50)                            Last page number of journal article
                    PUBMED_ID           NUMBER                                  NIH pubmed record ID, where available
                    DOI                 VARCHAR2(100)                           Digital object identifier for this reference
FK,UK               CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier for this document (for use on web interface etc)
                    TITLE               VARCHAR2(500)                           Document title (e.g., Publication title or description of dataset)
                    DOC_TYPE            VARCHAR2(50)        NOT NULL            Type of the document (e.g., Publication, Deposited dataset)
                    AUTHORS             VARCHAR2(4000)                          For a deposited dataset, the authors carrying out the screening and/or submitting the dataset.
                    ABSTRACT            CLOB                                    For a deposited dataset, a brief description of the dataset.
                    PATENT_ID           VARCHAR2(20)                            Patent ID for this document
                    RIDX                VARCHAR2(200)       NOT NULL            The Depositor Defined Reference Identifier
FK                  SRC_ID              INTEGER             NOT NULL            Foreign key to Source table, indicating the source of this document
FK                  CHEMBL_RELEASE_ID   INTEGER                                 Foreign key to chembl_release table
                    CONTACT             VARCHAR2(200)                           Details of someone willing to be contacted over the dataset (ideally ORCID ID, up to 3)


DOMAINS:
Table storing a non-redundant list of domains found in protein targets (e.g., Pfam domains).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  DOMAIN_ID           NUMBER              NOT NULL            Primary key. Unique identifier for each domain.
                    DOMAIN_TYPE         VARCHAR2(20)        NOT NULL            Indicates the source of the domain (e.g., Pfam).
                    SOURCE_DOMAIN_ID    VARCHAR2(20)        NOT NULL            Identifier for the domain in the source database (e.g., Pfam ID such as PF00001).
                    DOMAIN_NAME         VARCHAR2(100)                           Name given to the domain in the source database (e.g., 7tm_1).
                    DOMAIN_DESCRIPTION  VARCHAR2(500)                           Longer name or description for the domain.


DRUG_INDICATION:
Table storing indications for drugs, and clinical candidate drugs, from a variety of sources (e.g., FDA, EMA, WHO ATC, ClinicalTrials.gov, INN, USAN).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  DRUGIND_ID          NUMBER              NOT NULL            Primary key
FK,UK               RECORD_ID           NUMBER              NOT NULL            Foreign key to compound_records table. Links to the drug record to which this indication applies
FK                  MOLREGNO            NUMBER                                  Molregno for the drug (foreign key to the molecule_dictionary and compound_records tables)
                    MAX_PHASE_FOR_IND   NUMBER                                  Maximum phase of development that the drug is known to have reached for this particular indication (4 = Approved, 3 = Phase 3 Clinical Trials, 2 = Phase 2 Clinical Trials, 1 = Phase 1 Clinical Trials, 0.5 = Early Phase 1 Clinical Trials, -1 = Clinical Phase unknown for drug or clinical candidate drug ie where ChEMBL cannot assign a clinical phase)
UK                  MESH_ID             VARCHAR2(20)        NOT NULL            Medical Subject Headings (MeSH) disease identifier corresponding to the indication
                    MESH_HEADING        VARCHAR2(200)       NOT NULL            Medical Subject Heading term for the MeSH disease ID
UK                  EFO_ID              VARCHAR2(20)                            Experimental Factor Ontology (EFO) disease identifier corresponding to the indication
                    EFO_TERM            VARCHAR2(200)                           Experimental Factor Ontology term for the EFO ID


DRUG_MECHANISM:
Table storing mechanism of action information for drugs, and clinical candidate drugs, from a variety of sources (e.g., ATC, FDA, ClinicalTrials.gov)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MEC_ID              NUMBER              NOT NULL            Primary key for each drug mechanism of action
FK                  RECORD_ID           NUMBER              NOT NULL            Record_id for the drug (foreign key to compound_records table)
FK                  MOLREGNO            NUMBER                                  Molregno for the drug (foreign key to molecule_dictionary table)
                    MECHANISM_OF_ACTION VARCHAR2(250)                           Description of the mechanism of action e.g., 'Phosphodiesterase 5 inhibitor'
FK                  TID                 NUMBER                                  Target associated with this mechanism of action (foreign key to target_dictionary table)
FK                  SITE_ID             NUMBER                                  Binding site for the drug within the target (where known) - foreign key to binding_sites table
FK                  ACTION_TYPE         VARCHAR2(50)                            Type of action of the drug on the target e.g., agonist/antagonist etc (foreign key to action_type table)
                    DIRECT_INTERACTION  NUMBER                                  Flag to show whether the molecule is believed to interact directly with the target (1 = yes, 0 = no)
                    MOLECULAR_MECHANISM NUMBER                                  Flag to show whether the mechanism of action describes the molecular target of the drug, rather than a higher-level physiological mechanism e.g., vasodilator (1 = yes, 0 = no)
                    DISEASE_EFFICACY    NUMBER                                  Flag to show whether the target assigned is believed to play a role in the efficacy of the drug in the indication(s) for which it is approved (1 = yes, 0 = no)
                    MECHANISM_COMMENT   VARCHAR2(2000)                          Additional comments regarding the mechanism of action
                    SELECTIVITY_COMMENT VARCHAR2(1000)                          Additional comments regarding the selectivity of the drug
                    BINDING_SITE_COMMENT                    VARCHAR2(1000)                          Additional comments regarding the binding site of the drug
FK                  VARIANT_ID          NUMBER                                  Foreign key to variant_sequences table. Indicates the mutant/variant version of the target used in the assay (where known/applicable)


DRUG_WARNING:
Table storing safety-related information for drugs and clinical candidates

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  WARNING_ID          NUMBER              NOT NULL            Primary key for the drug warning
FK                  RECORD_ID           NUMBER                                  Foreign key to the compound_records table
                    MOLREGNO            NUMBER                                  Foreign key to molecule_dictionary table
                    WARNING_TYPE        VARCHAR2(20)                            Description of the drug warning type (e.g., withdrawn vs black box warning)
                    WARNING_CLASS       VARCHAR2(100)                           High-level class of the drug warning
                    WARNING_DESCRIPTION VARCHAR2(4000)                          Description of the drug warning
                    WARNING_COUNTRY     VARCHAR2(1000)                          List of countries/regions associated with the drug warning
                    WARNING_YEAR        NUMBER                                  Earliest year the warning was applied to the drug.
                    EFO_TERM            VARCHAR2(200)                           Term for Experimental Factor Ontology (EFO)
                    EFO_ID              VARCHAR2(20)                            Identifier for Experimental Factor Ontology (EFO)
                    EFO_ID_FOR_WARNING_CLASS                VARCHAR2(20)                            Warning Class Identifier for Experimental Factor Ontology (EFO)


FORMULATIONS:
Table linking individual ingredients in approved products (and their strengths) to entries in the molecule dictionary. Where products are mixtures of active ingredients they will have multiple entries in this table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK,UK               PRODUCT_ID          VARCHAR2(30)        NOT NULL            Unique identifier of the product. FK to PRODUCTS
                    INGREDIENT          VARCHAR2(200)                           Name of the approved ingredient within the product
                    STRENGTH            VARCHAR2(300)                           Dose strength
FK,UK               RECORD_ID           NUMBER              NOT NULL            Foreign key to the compound_records table.
FK                  MOLREGNO            NUMBER                                  Unique identifier of the ingredient FK to MOLECULE_DICTIONARY
PK                  FORMULATION_ID      NUMBER              NOT NULL            Primary key.


FRAC_CLASSIFICATION:
Table showing classification of fungicide mechanism of action according to the Fungicide Resistance Action Committee (FRAC): http://www.frac.info/publication/anhang/FRAC%20Code%20List%202013-final.pdf

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  FRAC_CLASS_ID       NUMBER              NOT NULL            Unique numeric primary key for each level5 code
                    ACTIVE_INGREDIENT   VARCHAR2(500)       NOT NULL            Name of active ingredient (fungicide) classified by FRAC
                    LEVEL1              VARCHAR2(2)         NOT NULL            Mechanism of action code assigned by FRAC
                    LEVEL1_DESCRIPTION  VARCHAR2(2000)      NOT NULL            Description of mechanism of action
                    LEVEL2              VARCHAR2(2)         NOT NULL            Target site code assigned by FRAC
                    LEVEL2_DESCRIPTION  VARCHAR2(2000)                          Description of target provided by FRAC
                    LEVEL3              VARCHAR2(6)         NOT NULL            Group number assigned by FRAC
                    LEVEL3_DESCRIPTION  VARCHAR2(2000)                          Description of group provided by FRAC
                    LEVEL4              VARCHAR2(7)         NOT NULL            Number denoting the chemical group (number not assigned by FRAC)
                    LEVEL4_DESCRIPTION  VARCHAR2(2000)                          Chemical group name provided by FRAC
UK                  LEVEL5              VARCHAR2(8)         NOT NULL            A unique code assigned to each ingredient (based on the level 1-4 FRAC classification, but not assigned by IRAC)
                    FRAC_CODE           VARCHAR2(4)         NOT NULL            The official FRAC classification code for the ingredient


GO_CLASSIFICATION:
Table storing the ChEMBL Drug Target GO slim (http://www.geneontology.org/ontology/subsets/goslim_chembl.obo)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  GO_ID               VARCHAR2(10)        NOT NULL            Primary key. Gene Ontology identifier for the GO slim term
                    PARENT_GO_ID        VARCHAR2(10)                            Gene Ontology identifier for the parent of this GO term in the ChEMBL Drug Target GO slim
                    PREF_NAME           VARCHAR2(200)                           Gene Ontology name
                    CLASS_LEVEL         NUMBER                                  Indicates the level of the term in the slim (L1 = highest)
                    ASPECT              VARCHAR2(1)                             Indicates which aspect of the Gene Ontology the term belongs to (F = molecular function, P = biological process, C = cellular component)
                    PATH                VARCHAR2(1000)                          Indicates the full path to this term in the GO slim


HRAC_CLASSIFICATION:
Table showing classification of herbicide mechanism of action according to the Herbicide Resistance Action Committee (HRAC): http://www.hracglobal.com/Education/ClassificationofHerbicideSiteofAction.aspx

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  HRAC_CLASS_ID       NUMBER              NOT NULL            Unique numeric primary key for each level3 code
                    ACTIVE_INGREDIENT   VARCHAR2(500)       NOT NULL            Name of active ingredient (herbicide) classified by HRAC
                    LEVEL1              VARCHAR2(2)         NOT NULL            HRAC group code - denoting mechanism of action of herbicide
                    LEVEL1_DESCRIPTION  VARCHAR2(2000)      NOT NULL            Description of mechanism of action provided by HRAC
                    LEVEL2              VARCHAR2(3)         NOT NULL            Indicates a chemical family within a particular HRAC group (number not assigned by HRAC)
                    LEVEL2_DESCRIPTION  VARCHAR2(2000)                          Description of chemical family provided by HRAC
UK                  LEVEL3              VARCHAR2(5)         NOT NULL            A unique code assigned to each ingredient (based on the level 1 and 2 HRAC classification, but not assigned by HRAC)
                    HRAC_CODE           VARCHAR2(2)         NOT NULL            The official HRAC classification code for the ingredient


INDICATION_REFS:
Table storing references indicating the source of drug indication information

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  INDREF_ID           NUMBER              NOT NULL            Primary key
FK,UK               DRUGIND_ID          NUMBER              NOT NULL            Foreign key to the DRUG_INDICATION table, indicating the drug-indication link that this reference applies to
UK                  REF_TYPE            VARCHAR2(50)        NOT NULL            Type/source of reference
UK                  REF_ID              VARCHAR2(4000)      NOT NULL            Identifier for the reference in the source
                    REF_URL             VARCHAR2(4000)      NOT NULL            Full URL linking to the reference


IRAC_CLASSIFICATION:
Table showing classification of insecticide mechanism of action according to the Insecticide Resistance Action Committee (IRAC): http://www.irac-online.org/documents/moa-classification/?ext=pdf

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  IRAC_CLASS_ID       NUMBER              NOT NULL            Unique numeric primary key for each level4 code
                    ACTIVE_INGREDIENT   VARCHAR2(500)       NOT NULL            Name of active ingredient (insecticide) classified by IRAC
                    LEVEL1              VARCHAR2(1)         NOT NULL            Class of action e.g., nerve action, energy metabolism (code not assigned by IRAC)
                    LEVEL1_DESCRIPTION  VARCHAR2(2000)      NOT NULL            Description of class of action, as provided by IRAC
                    LEVEL2              VARCHAR2(3)         NOT NULL            IRAC main group code denoting primary site/mechanism of action
                    LEVEL2_DESCRIPTION  VARCHAR2(2000)      NOT NULL            Description of site/mechanism of action provided by IRAC
                    LEVEL3              VARCHAR2(6)         NOT NULL            IRAC sub-group code denoting chemical class of insecticide
                    LEVEL3_DESCRIPTION  VARCHAR2(2000)      NOT NULL            Description of chemical class or exemplifying ingredient provided by IRAC
UK                  LEVEL4              VARCHAR2(8)         NOT NULL            A unique code assigned to each ingredient (based on the level 1, 2 and 3 IRAC classification, but not assigned by IRAC)
                    IRAC_CODE           VARCHAR2(3)         NOT NULL            The official IRAC classification code for the ingredient


LIGAND_EFF:
Contains BEI (Binding Efficiency Index) and SEI (Surface Binding Efficiency Index) for each activity_id where such data can be calculated.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK,FK               ACTIVITY_ID         NUMBER              NOT NULL            Link key to activities table
                    BEI                 NUMBER                                  Binding Efficiency Index = p(XC50) *1000/MW_freebase
                    SEI                 NUMBER                                  Surface Efficiency Index = p(XC50)*100/PSA
                    LE                  NUMBER                                  Ligand Efficiency = deltaG/heavy_atoms  [from the Hopkins DDT paper 2004]
                    LLE                 NUMBER                                  Lipophilic Ligand Efficiency = -logKi-ALogP. [from Leeson NRDD 2007]


MECHANISM_REFS:
Table storing references for information in the drug_mechanism table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MECREF_ID           NUMBER              NOT NULL            Primary key
FK,UK               MEC_ID              NUMBER              NOT NULL            Foreign key to drug_mechanism table - indicating the mechanism to which the references refer
UK                  REF_TYPE            VARCHAR2(50)        NOT NULL            Type/source of reference (e.g., 'PubMed','DailyMed')
UK                  REF_ID              VARCHAR2(200)                           Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)
                    REF_URL             VARCHAR2(400)                           Full URL linking to the reference


METABOLISM:
Table storing drug metabolic pathways, manually curated from a variety of sources

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MET_ID              NUMBER              NOT NULL            Primary key
FK,UK               DRUG_RECORD_ID      NUMBER                                  Foreign key to compound_records. Record representing the drug or other compound for which metabolism is being studied (may not be the same as the substrate being measured)
FK,UK               SUBSTRATE_RECORD_ID NUMBER                                  Foreign key to compound_records. Record representing the compound that is the subject of metabolism
FK,UK               METABOLITE_RECORD_ID                    NUMBER                                  Foreign key to compound_records. Record representing the compound that is the result of metabolism
UK                  PATHWAY_ID          NUMBER                                  Identifier for the metabolic scheme/pathway (may be multiple pathways from one source document)
                    PATHWAY_KEY         VARCHAR2(50)                            Link to original source indicating where the pathway information was found (e.g., Figure 1, page 23)
UK                  ENZYME_NAME         VARCHAR2(200)                           Name of the enzyme responsible for the metabolic conversion
FK,UK               ENZYME_TID          NUMBER                                  Foreign key to target_dictionary. TID for the enzyme responsible for the metabolic conversion
                    MET_CONVERSION      VARCHAR2(200)                           Description of the metabolic conversion
                    ORGANISM            VARCHAR2(100)                           Organism in which this metabolic reaction occurs
UK                  TAX_ID              NUMBER                                  NCBI Tax ID for the organism in which this metabolic reaction occurs
                    MET_COMMENT         VARCHAR2(1000)                          Additional information regarding the metabolism (e.g., organ system, conditions under which observed, activity of metabolites)


METABOLISM_REFS:
Table storing references for metabolic pathways, indicating the source of the data

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  METREF_ID           NUMBER              NOT NULL            Primary key
FK,UK               MET_ID              NUMBER              NOT NULL            Foreign key to record_metabolism table - indicating the metabolism information to which the references refer
UK                  REF_TYPE            VARCHAR2(50)        NOT NULL            Type/source of reference (e.g., 'PubMed','DailyMed')
UK                  REF_ID              VARCHAR2(200)                           Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)
                    REF_URL             VARCHAR2(400)                           Full URL linking to the reference


MOLECULE_ATC_CLASSIFICATION:
Table mapping drugs in the molecule_dictionary to ATC codes in the atc_classification table

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MOL_ATC_ID          NUMBER              NOT NULL            Primary key
FK                  LEVEL5              VARCHAR2(10)        NOT NULL            ATC code (foreign key to atc_classification table)
FK                  MOLREGNO            NUMBER              NOT NULL            Drug to which the ATC code applies (foreign key to molecule_dictionary table)


MOLECULE_DICTIONARY:
Table storing a non-redundant list of curated compounds for ChEMBL (includes preclinical compounds, drugs and clinical candidate drugs) and some associated attributes.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MOLREGNO            NUMBER              NOT NULL            Internal Primary Key for the molecule
                    PREF_NAME           VARCHAR2(255)                           Preferred name for the molecule
FK,UK               CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier for this compound (for use on web interface etc)
                    MAX_PHASE           NUMBER                                  Maximum phase of development reached for the compound across all indications (4 = Approved, 3 = Phase 3 Clinical Trials, 2 = Phase 2 Clinical Trials, 1 = Phase 1 Clinical Trials, 0.5 = Early Phase 1 Clinical Trials, -1 = Clinical Phase unknown for drug or clinical candidate drug ie where ChEMBL cannot assign a clinical phase, NULL = preclinical compounds with bioactivity data)
                    THERAPEUTIC_FLAG    NUMBER              NOT NULL            Indicates that a drug has a therapeutic application, as opposed to e.g., an imaging agent, additive etc (1 = yes, 0 = default value).
                    DOSED_INGREDIENT    NUMBER              NOT NULL            Indicates that the drug is dosed in this form, e.g., a particular salt (1 = yes, 0 = default value)
                    STRUCTURE_TYPE      VARCHAR2(10)        NOT NULL            Indicates whether the molecule has a small molecule structure or a protein sequence (MOL indicates an entry in the compound_structures table, SEQ indications an entry in the protein_therapeutics table, NONE indicates an entry in neither table, e.g., structure unknown)
                    CHEBI_PAR_ID        NUMBER                                  Preferred ChEBI ID for the compound (where different from assigned). TO BE DEPRECATED - please use UniChem (https://www.ebi.ac.uk/unichem/).
                    MOLECULE_TYPE       VARCHAR2(30)                            Type of molecule (Small molecule, Protein, Antibody, Antibody drug conjugate, Oligosaccharide, Oligonucleotide, Cell, Enzyme, Gene, Unknown)
                    FIRST_APPROVAL      NUMBER                                  Earliest known approval year for the drug (NULL is the default value)
                    ORAL                NUMBER              NOT NULL            Indicates whether the drug is known to be administered orally (1 = yes, 0 = default value)
                    PARENTERAL          NUMBER              NOT NULL            Indicates whether the drug is known to be administered parenterally (1 = yes, 0 = default value)
                    TOPICAL             NUMBER              NOT NULL            Indicates whether the drug is known to be administered topically (1 = yes, 0 = default value).
                    BLACK_BOX_WARNING   NUMBER              NOT NULL            Indicates that the drug has a black box warning (1 = yes, 0 = default value)
                    NATURAL_PRODUCT     NUMBER              NOT NULL            Indicates whether the compound is a natural product as defined by COCONUT (https://coconut.naturalproducts.net/), the COlleCtion of Open Natural ProdUcTs. (1 = yes, 0 = default value)
                    FIRST_IN_CLASS      NUMBER              NOT NULL            Indicates whether this is known to be the first approved drug of its class (e.g., acting on a particular target). This is regardless of the indication, or the route of administration (1 = yes, 0 = no, -1 = preclinical compound ie not a drug).
                    CHIRALITY           NUMBER              NOT NULL            Indicates the chirality of the drug (2 = an achiral molecule, 1 = single enantiomer where all stereocenters have known absolute configuration, 0 = a mixture of stereoisomers such as a racemic mixture, epimeric mixture, etc, -1 = has unknown chirality)
                    PRODRUG             NUMBER              NOT NULL            Indicates that the drug is a pro-drug. See active_molregno field in molecule hierarchy for the pharmacologically active molecule, where known (1 = yes, 0 = no, -1 = preclinical compound ie not a drug)
                    INORGANIC_FLAG      NUMBER              NOT NULL            Indicates whether the molecule is inorganic i.e., containing only metal atoms and <2 carbon atoms (1 = yes, 0 = no, -1 = preclinical compound ie not a drug)
                    USAN_YEAR           NUMBER                                  The year in which the application for a USAN/INN name was granted. (NULL is the default value)
                    AVAILABILITY_TYPE   NUMBER                                  The availability type for the drug (-2 = withdrawn, -1 = unknown, 0 = discontinued, 1 = prescription only, 2 = over the counter)
                    USAN_STEM           VARCHAR2(50)                            Where the drug or clinical candidate name can be matched, this indicates the USAN stem (NULL is the default value). Also described in the USAN_STEMS table.
                    POLYMER_FLAG        NUMBER                                  Indicates whether a molecule is a small molecule polymer, e.g., polistyrex (1 = yes, 0 = default value)
                    USAN_SUBSTEM        VARCHAR2(50)                            Where the drug or clinical candidate name can be matched, this indicates the USAN substem (NULL is the default value)
                    USAN_STEM_DEFINITION                    VARCHAR2(1000)                          Definition of the USAN stem (NULL is the default value)
                    INDICATION_CLASS    VARCHAR2(1000)                          Indication class(es) assigned to a drug in the USP dictionary. TO BE DEPRECATED - please use DRUG_INDICATION table.
                    WITHDRAWN_FLAG      NUMBER              NOT NULL            Indicates an approved drug has been withdrawn for toxicity reasons for all indications, for all populations at all doses in at least one country (not necessarily in the US). (1 = yes, 0 = default value)
                    CHEMICAL_PROBE      NUMBER              NOT NULL            Indicates whether the compound is a chemical probe; for exact definition see release notes (1 = yes, 0 = default value).
                    ORPHAN              NUMBER              NOT NULL            Indicates orphan designation, i.e. intended for use against a rare condition (1 = yes, 0 = no, -1 = preclinical compound ie not a drug)


MOLECULE_FRAC_CLASSIFICATION:
Table showing Fungicide Resistance Action Committee (FRAC) mechanism of action classification for known crop protection fungicides.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MOL_FRAC_ID         NUMBER              NOT NULL            Primary key.
FK,UK               FRAC_CLASS_ID       NUMBER              NOT NULL            Foreign key to frac_classification table showing the mechanism of action classification of the compound.
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to molecule_dictionary, showing the compound to which the classification applies.


MOLECULE_HIERARCHY:
Table storing relationships between parents, salts and active metabolites (for pro-drugs).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK,FK               MOLREGNO            NUMBER              NOT NULL            Foreign key to compounds table. This field holds a list of all of the ChEMBL compounds with associated data (e.g., activity information, approved drugs). Parent compounds that are generated only by removing salts, and which do not themselves have any associated data will not appear here.
FK                  PARENT_MOLREGNO     NUMBER                                  Represents parent compound of molregno in first field (i.e., generated by removing salts). Where molregno and parent_molregno are same, the initial ChEMBL compound did not contain a salt component, or else could not be further processed for various reasons (e.g., inorganic mixture). Compounds which are only generated by removing salts will appear in this field only. Those which, themselves, have any associated data (e.g., activity data) or are launched drugs will also appear in the molregno field.
FK                  ACTIVE_MOLREGNO     NUMBER                                  Where a compound is a pro-drug, this represents the active metabolite of the 'dosed' compound given by parent_molregno. Where parent_molregno and active_molregno are the same, the compound is not currently known to be a pro-drug. 


MOLECULE_HRAC_CLASSIFICATION:
Table showing Herbicide Resistance Action Committee (HRAC) mechanism of action classification for known herbicidal compounds.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MOL_HRAC_ID         NUMBER              NOT NULL            Primary key
FK,UK               HRAC_CLASS_ID       NUMBER              NOT NULL            Foreign key to hrac_classification table showing the classification for the compound.
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to molecule_dictionary, showing the compound to which this classification applies.


MOLECULE_IRAC_CLASSIFICATION:
Table showing Insecticide Resistance Action Committee (IRAC) mechanism of action classification for known crop protection insecticides.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  MOL_IRAC_ID         NUMBER              NOT NULL            Primary key.
FK,UK               IRAC_CLASS_ID       NUMBER              NOT NULL            Foreign key to the irac_classification table showing the mechanism of action classification for the compound.
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to the molecule_dictionary table, showing the compound to which the classification applies.


MOLECULE_SYNONYMS:
Stores synonyms for a compound (e.g., common names, trade names, research codes etc)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK,UK               MOLREGNO            NUMBER              NOT NULL            Foreign key to molecule_dictionary
UK                  SYN_TYPE            VARCHAR2(50)        NOT NULL            Type of name/synonym (e.g., TRADE_NAME, RESEARCH_CODE, USAN)
PK                  MOLSYN_ID           NUMBER              NOT NULL            Primary key.
FK                  RES_STEM_ID         NUMBER                                  Foreign key to the research_stem table. Where a synonym is a research code, this links to further information about the company associated with that code. TO BE DEPRECATED.
UK                  SYNONYMS            VARCHAR2(250)                           Synonym for the compound


ORGANISM_CLASS:
Simple organism classification (essentially a cut-down version of the NCBI taxonomy for organisms in ChEMBL target_dictionary table), allowing browsing of ChEMBL data by taxonomic groups

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  OC_ID               NUMBER              NOT NULL            Internal primary key
UK                  TAX_ID              NUMBER                                  NCBI taxonomy ID for the organism (corresponding to tax_ids in target_dictionary table)
                    L1                  VARCHAR2(200)                           Highest level classification (e.g., Eukaryotes, Bacteria, Fungi etc)
                    L2                  VARCHAR2(200)                           Second level classification
                    L3                  VARCHAR2(200)                           Third level classification


PATENT_USE_CODES:
Table from FDA Orange Book, showing definitions of different patent use codes (as used in the product_patents table).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  PATENT_USE_CODE     VARCHAR2(8)         NOT NULL            Primary key. Patent use code from FDA Orange Book
                    DEFINITION          VARCHAR2(500)       NOT NULL            Definition for the patent use code, from FDA Orange Book.


PREDICTED_BINDING_DOMAINS:
Table storing information on the likely binding domain of compounds in the activities table (based on analysis of the domain structure of the target. Note these are predictions, not experimentally determined. See Kruger F, Rostom R and Overington JP (2012), BMC Bioinformatics, 13(S17), S11 for more details.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  PREDBIND_ID         NUMBER              NOT NULL            Primary key.
FK                  ACTIVITY_ID         NUMBER                                  Foreign key to the activities table, indicating the compound/assay(+target) combination for which this prediction is made.
FK                  SITE_ID             NUMBER                                  Foreign key to the binding_sites table, indicating the binding site (domain) that the compound is predicted to bind to.
                    PREDICTION_METHOD   VARCHAR2(50)                            The method used to assign the binding domain (e.g., 'Single domain' where the protein has only 1 domain, 'Multi domain' where the protein has multiple domains, but only 1 is known to bind small molecules in other proteins).
                    CONFIDENCE          VARCHAR2(10)                            The level of confidence assigned to the prediction (high where the protein has only 1 domain, medium where the compound has multiple domains, but only 1 known small molecule-binding domain).


PRODUCT_PATENTS:
Table from FDA Orange Book, showing patents associated with drug products.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  PROD_PAT_ID         NUMBER              NOT NULL            Primary key
FK,UK               PRODUCT_ID          VARCHAR2(30)        NOT NULL            Foreign key to products table - FDA application number for the product
UK                  PATENT_NO           VARCHAR2(20)        NOT NULL            Patent numbers as submitted by the applicant holder for patents covered by the statutory provisions
UK                  PATENT_EXPIRE_DATE  DATE                NOT NULL            Date the patent expires as submitted by the applicant holder including applicable extensions
                    DRUG_SUBSTANCE_FLAG NUMBER              NOT NULL            Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug substance flag set to 1, indicating the sponsor submitted the patent as claiming the drug substance
                    DRUG_PRODUCT_FLAG   NUMBER              NOT NULL            Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug product flag set to 1, indicating the sponsor submitted the patent as claiming the drug product
FK,UK               PATENT_USE_CODE     VARCHAR2(10)                            Code to designate a use patent that covers the approved indication or use of a drug product
                    DELIST_FLAG         NUMBER              NOT NULL            Sponsor has requested patent be delisted if set to 1.  This patent has remained listed because, under Section 505(j)(5)(D)(i) of the Act, a first applicant may retain eligibility for 180-day exclusivity based on a paragraph IV certification to this patent for a certain period.  Applicants under Section 505(b)(2) are not required to certify to patents where this flag is set to 1
                    SUBMISSION_DATE     DATE                                    The date on which the FDA receives patent information from the new drug application (NDA) holder. Format is Mmm d, yyyy


PRODUCTS:
Table containing information about approved drug products (from the FDA Orange Book), such as trade name, administration route, approval date. Ingredients in each product are linked to the molecule dictionary via the formulations table.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
                    DOSAGE_FORM         VARCHAR2(200)                           The dosage form of the product (e.g., tablet, capsule etc)
                    ROUTE               VARCHAR2(200)                           The administration route of the product (e.g., oral, injection etc)
                    TRADE_NAME          VARCHAR2(200)                           The trade name for the product
                    APPROVAL_DATE       DATE                                    The FDA approval date for the product (not necessarily first approval of the active ingredient)
                    AD_TYPE             VARCHAR2(5)                             RX = prescription, OTC = over the counter, DISCN = discontinued
                    ORAL                NUMBER                                  Flag to show whether product is orally delivered
                    TOPICAL             NUMBER                                  Flag to show whether product is topically delivered
                    PARENTERAL          NUMBER                                  Flag to show whether product is parenterally delivered
                    BLACK_BOX_WARNING   NUMBER                                  Flag to show whether the product label has a black box warning
                    APPLICANT_FULL_NAME VARCHAR2(200)                           Name of the company applying for FDA approval
                    INNOVATOR_COMPANY   NUMBER                                  Flag to show whether the applicant is the innovator of the product
PK                  PRODUCT_ID          VARCHAR2(30)        NOT NULL            FDA application number for the product
                    NDA_TYPE            VARCHAR2(10)                            New Drug Application Type. The type of new drug application approval.  New Drug Applications (NDA or innovator)  are ”N”.   Abbreviated New Drug Applications (ANDA or generic) are “A”.


PROTEIN_CLASS_SYNONYMS:
Table storing synonyms for the protein family classifications (from various sources including MeSH, ConceptWiki and UMLS).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  PROTCLASSSYN_ID     NUMBER              NOT NULL            Primary key.
FK,UK               PROTEIN_CLASS_ID    NUMBER              NOT NULL            Foreign key to the PROTEIN_CLASSIFICATION table. The protein_class to which this synonym applies.
UK                  PROTEIN_CLASS_SYNONYM                   VARCHAR2(1000)                          The synonym for the protein class.
UK                  SYN_TYPE            VARCHAR2(20)                            The type or origin of the synonym (e.g., ChEMBL, Concept Wiki, UMLS).


PROTEIN_CLASSIFICATION:
Table storing the protein family classifications for protein targets in ChEMBL (formerly in the target_class table)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  PROTEIN_CLASS_ID    NUMBER              NOT NULL            Primary key. Unique identifier for each protein family classification.
                    PARENT_ID           NUMBER                                  Protein_class_id for the parent of this protein family.
                    PREF_NAME           VARCHAR2(500)                           Preferred/full name for this protein family.
                    SHORT_NAME          VARCHAR2(50)                            Short/abbreviated name for this protein family (not necessarily unique).
                    PROTEIN_CLASS_DESC  VARCHAR2(410)       NOT NULL            Concatenated description of each classification for searching purposes etc.
                    DEFINITION          VARCHAR2(4000)                          Definition of the protein family.
                    CLASS_LEVEL         NUMBER              NOT NULL            Level of the class within the hierarchy (level 1 = top level classification)


RELATIONSHIP_TYPE:
Lookup table for assays.relationship_type column, showing whether assays are mapped to targets of the correct identity and species ('Direct') or close homologues ('Homologue')

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  RELATIONSHIP_TYPE   VARCHAR2(1)         NOT NULL            Relationship_type flag used in the assays table
                    RELATIONSHIP_DESC   VARCHAR2(250)                           Description of relationship_type flags


RESEARCH_COMPANIES:
Table storing a list of pharmaceutical companies (including current and former names) corresponding to each research code stem in the research_stem table. A stem can sometimes be used by more than one company. TO BE DEPRECATED.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  CO_STEM_ID          NUMBER              NOT NULL            Primary key.
FK,UK               RES_STEM_ID         NUMBER                                  Foreign key to research_stem table. TO BE DEPRECATED.
UK                  COMPANY             VARCHAR2(100)                           Name of current company associated with this research code stem. TO BE DEPRECATED.
                    COUNTRY             VARCHAR2(50)                            Country in which the company uses this research code stem. TO BE DEPRECATED.
                    PREVIOUS_COMPANY    VARCHAR2(100)                           Previous name of the company associated with this research code stem (e.g., if the company has undergone acquisitions/mergers). TO BE DEPRECATED.


RESEARCH_STEM:
Table storing a list of stems/prefixes used in research codes. TO BE DEPRECATED.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  RES_STEM_ID         NUMBER              NOT NULL            Primary key. Unique ID for each research code stem. TO BE DEPRECATED.
UK                  RESEARCH_STEM       VARCHAR2(20)                            The actual stem/prefix used in the research code. TO BE DEPRECATED.


SITE_COMPONENTS:
Table defining the location of the binding sites in the binding_sites table. A binding site could be defined in terms of which protein subunits (components) are involved, the domains within those subunits to which the compound binds, and possibly even the precise residues involved. For a target where the binding site is at the interface of two protein subunits or two domains, there will be two site_components describing each of these subunits/domains.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  SITECOMP_ID         NUMBER              NOT NULL            Primary key.
FK,UK               SITE_ID             NUMBER              NOT NULL            Foreign key to binding_sites table.
FK,UK               COMPONENT_ID        NUMBER                                  Foreign key to the component_sequences table, indicating which molecular component of the target is involved in the binding site.
FK,UK               DOMAIN_ID           NUMBER                                  Foreign key to the domains table, indicating which domain of the given molecular component is involved in the binding site (where not known, the domain_id may be null).
                    SITE_RESIDUES       VARCHAR2(2000)                          List of residues from the given molecular component that make up the binding site (where not know, will be null).


SOURCE:
Table showing source from which ChEMBL data is derived (e.g., literature, deposited datasets, patents, drug or clinical candidate sources etc)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  SRC_ID              NUMBER              NOT NULL            Identifier for each source (used in compound_records and assays tables)
                    SRC_DESCRIPTION     VARCHAR2(500)                           Descriptive name for the source
                    SRC_SHORT_NAME      VARCHAR2(20)                            A short name for each data source, for display purposes
                    SRC_COMMENT         VARCHAR2(1200)                          Additional notes on the source
                    SRC_URL             VARCHAR2(200)                           URL(s) pointing to website(s) with relevant information about the source


STRUCTURAL_ALERT_SETS:
Table showing list of sets of structural alerts that have been included in COMPOUND_STRUCTURAL_ALERT table. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ALERT_SET_ID        NUMBER              NOT NULL            Unique ID for the structural alert set
UK                  SET_NAME            VARCHAR2(100)       NOT NULL            Name (or origin) of the structural alert set
                    PRIORITY            NUMBER              NOT NULL            Priority assigned to the structural alert set for display on the ChEMBL interface (priorities >=4 are shown by default).


STRUCTURAL_ALERTS:
Table storing a list of structural features (encoded as SMARTS) that are potentially undesirable in drug discovery context. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  ALERT_ID            NUMBER              NOT NULL            Primary key. Unique identifier for the structural alert
FK,UK               ALERT_SET_ID        NUMBER              NOT NULL            Foreign key to structural_alert_sets table indicating which set this particular alert comes from
UK                  ALERT_NAME          VARCHAR2(100)       NOT NULL            A name for the structural alert
UK                  SMARTS              VARCHAR2(4000)      NOT NULL            SMARTS defining the structural feature that is considered to be an alert


TARGET_COMPONENTS:
Links molecular target from the target_dictionary to the components they consist of (in the component_sequences table). For a protein complex or protein family target, for example, there will be multiple protein components in the component_sequences table.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK,UK               TID                 NUMBER              NOT NULL            Foreign key to the target_dictionary, indicating the target to which the components belong.
FK,UK               COMPONENT_ID        NUMBER              NOT NULL            Foreign key to the component_sequences table, indicating which components belong to the target.
PK                  TARGCOMP_ID         NUMBER              NOT NULL            Primary key.
                    HOMOLOGUE           NUMBER              NOT NULL            Indicates that the given component is a homologue of the correct component (e.g., from a different species) when set to 1. This may be the case if the sequence for the correct protein/nucleic acid cannot be found in sequence databases. A value of 2 indicates that the sequence given is a representative of a species group, e.g., an E. coli protein to represent the target of a broad-spectrum antibiotic.


TARGET_DICTIONARY:
Target Dictionary containing all curated targets for ChEMBL. Includes both protein targets and non-protein targets (e.g., organisms, tissues, cell lines)

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  TID                 NUMBER              NOT NULL            Unique ID for the target
FK                  TARGET_TYPE         VARCHAR2(30)                            Describes whether target is a protein, an organism, a tissue etc. Foreign key to TARGET_TYPE table.
                    PREF_NAME           VARCHAR2(200)       NOT NULL            Preferred target name: manually curated
                    TAX_ID              NUMBER                                  NCBI taxonomy id of target
                    ORGANISM            VARCHAR2(150)                           Source organism of molecuar target or tissue, or the target organism if compound activity is reported in an organism rather than a protein or tissue
FK,UK               CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier for this target (for use on web interface etc)
                    SPECIES_GROUP_FLAG  NUMBER              NOT NULL            Flag to indicate whether the target represents a group of species, rather than an individual species (e.g., 'Bacterial DHFR'). Where set to 1, indicates that any associated target components will be a representative, rather than a comprehensive set.


TARGET_RELATIONS:
Table showing relationships between different protein targets based on overlapping protein components (e.g., relationship between a protein complex and the individual subunits).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
FK                  TID                 NUMBER              NOT NULL            Identifier for target of interest (foreign key to target_dictionary table)
                    RELATIONSHIP        VARCHAR2(20)        NOT NULL            Relationship between two targets (e.g., SUBSET OF, SUPERSET OF, OVERLAPS WITH)
FK                  RELATED_TID         NUMBER              NOT NULL            Identifier for the target that is related to the target of interest (foreign key to target_dicitionary table)
PK                  TARGREL_ID          NUMBER              NOT NULL            Primary key


TARGET_TYPE:
Lookup table for target types used in the target dictionary

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  TARGET_TYPE         VARCHAR2(30)        NOT NULL            Target type (as used in target dictionary)
                    TARGET_DESC         VARCHAR2(250)                           Description of target type
                    PARENT_TYPE         VARCHAR2(25)                            Higher level classification of target_type, allowing grouping of e.g., all 'PROTEIN' targets, all 'NON-MOLECULAR' targets etc.


TISSUE_DICTIONARY:
Table storing information about tissues used in assays.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  TISSUE_ID           NUMBER              NOT NULL            Primary key, numeric ID for each tissue.
UK                  UBERON_ID           VARCHAR2(15)                            Uberon ontology identifier for this tissue.
UK                  PREF_NAME           VARCHAR2(200)       NOT NULL            Name for the tissue (in most cases Uberon name).
UK                  EFO_ID              VARCHAR2(20)                            Experimental Factor Ontology identifier for the tissue.
FK,UK               CHEMBL_ID           VARCHAR2(20)        NOT NULL            ChEMBL identifier for this tissue (for use on web interface etc)
                    BTO_ID              VARCHAR2(20)                            BRENDA Tissue Ontology identifier for the tissue.
                    CALOHA_ID           VARCHAR2(7)                             Swiss Institute for Bioinformatics CALOHA Ontology identifier for the tissue.


USAN_STEMS:
Table storing definitions for stems used in USANs (United States Adopted Names).

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  USAN_STEM_ID        NUMBER              NOT NULL            Numeric primary key.
UK                  STEM                VARCHAR2(100)       NOT NULL            Stem defined for use in United States Adopted Names.
UK                  SUBGROUP            VARCHAR2(100)                           More specific subgroup of the stem defined for use in United States Adopted Names.
                    ANNOTATION          VARCHAR2(2000)                          Meaning of the stem (e.g., the class of compound it applies to).
                    STEM_CLASS          VARCHAR2(100)                           Indicates whether stem is used as a prefix/infix/suffix/combined prefix and suffix
                    MAJOR_CLASS         VARCHAR2(100)                           Protein family targeted by compounds of this class (e.g., GPCR/Ion channel/Protease) where known/applicable. TO BE DEPRECATED.


VARIANT_SEQUENCES:
Table storing information about mutant sequences and other variants used in assays. The sequence provided is a representative sequence incorporating the reported mutation/variant used in the assay - it is not necessarily the exact sequence used in the experiment.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  VARIANT_ID          NUMBER              NOT NULL            Primary key, numeric ID for each sequence variant; -1 for unclassified variants.
UK                  MUTATION            VARCHAR2(2000)                          Details of variant(s) used, with residue positions adjusted to match provided sequence.
UK                  ACCESSION           VARCHAR2(25)                            UniProt accesion for the representative sequence used as the base sequence (without variation).
                    VERSION             NUMBER                                  Version of the UniProt sequence used as the base sequence.
                    ISOFORM             NUMBER                                  Details of the UniProt isoform used as the base sequence where relevant.
                    SEQUENCE            CLOB                                    Variant sequence formed by adjusting the UniProt base sequence with the specified mutations/variations.
                    ORGANISM            VARCHAR2(200)                           Organism from which the sequence was obtained.
                    TAX_ID              NUMBER                                  NCBI Tax ID for the organism from which the sequence was obtained


VERSION:
Table showing release version and creation date for the database, and associated ontologies and packages.

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  NAME                VARCHAR2(50)        NOT NULL            Name of release version
                    CREATION_DATE       DATE                                    Date database created
                    COMMENTS            VARCHAR2(2000)                          Description of release version


WARNING_REFS:
Table storing references indicating the source of drug warning information

KEYS                COLUMN_NAME         DATA_TYPE           NULLABLE            COMMENT
PK                  WARNREF_ID          NUMBER              NOT NULL            Primary key for the warning reference
FK                  WARNING_ID          NUMBER                                  Foreign key to the drug_warning table
                    REF_TYPE            VARCHAR2(50)                            Type/source of reference
                    REF_ID              VARCHAR2(4000)                          Identifier for the reference in the source
                    REF_URL             VARCHAR2(4000)                          Full URL linking to the reference
"""