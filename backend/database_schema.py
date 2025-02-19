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

TABLES = """
protein_classification table:
pref_name,short_name,protein_class_desc,definition,class_level
"Protein class","Protein class","protein class","Root of the ChEMBL protein family classification",0
Adhesion,Adhesion,adhesion,"Surface ligands, usually glycoproteins, that mediate cell-to-cell adhesion. Their functions include the assembly and interconnection of various vertebrate systems, as well as maintenance of tissue integration, wound healing, morphogenic movements, cellular migrations, and metastasis. [MESH:D015815]",1
"Auxiliary transport protein",AUXTRANS,"auxiliary transport protein",NULL,1
Enzyme,Enzyme,enzyme,"Biological molecules that possess catalytic activity. They may occur naturally or be synthetically created. Enzymes are usually proteins, however CATALYTIC RNA and CATALYTIC DNA molecules have also been identified. [MESH:D004798]",1
"Epigenetic regulator",Epigenetic,"epigenetic regulator","A class of proteins that alter gene expression through methylation of DNA or post-translational modification (e.g., methylation/acetylation) of histones",1
"Ion channel","Ion channel","ion channel","Gated, ion-selective glycoproteins that traverse membranes. The stimulus for ION CHANNEL GATING can be due to a variety of stimuli such as LIGANDS, a TRANSMEMBRANE POTENTIAL DIFFERENCE, mechanical deformation or through INTRACELLULAR SIGNALING PEPTIDES AND PROTEINS. [MESH:D007473]",1
"Membrane receptor","Membrane receptor","membrane receptor","Cell surface proteins that bind signalling molecules external to the cell with high affinity and convert this extracellular event into one or more intracellular signals that alter the behavior of the target cell (From Alberts, Molecular Biology of the Cell, 2nd ed, pp693-5). Cell surface receptors, unlike enzymes, do not chemically alter their ligands. [MESH:D011956]",1
"Other cytosolic protein","Cytosolic other","cytosolic other",NULL,1
"Other membrane protein","Membrane other","membrane other",NULL,1
"Other nuclear protein","Nuclear other","nuclear other",NULL,1
"Secreted protein",Secreted,secreted,NULL,1
"Structural protein",Structural,structural,NULL,1
"Surface antigen","Surface antigen","surface antigen","Antigens on surfaces of cells, including infectious or foreign cells or viruses. They are usually protein-containing groups on cell membranes or walls and may be isolated. [MESH:D000954]",1
"Transcription factor","Transcription Factor","transcription factor","Endogenous substances, usually proteins, which are effective in the initiation, stimulation, or termination of the genetic transcription process. [MESH:D014157]",1
Transporter,Transporter,transporter,NULL,1
"Unclassified protein",Unclassified,unclassified,NULL,1
Aminoacyltransferase,Aminoacyltransferase,"enzyme  aminoacyltransferase","Enzymes that catalyze the transfer of an aminoacyl group from donor to acceptor resulting in the formation of an ester or amide linkage. EC 2.3.2. [MESH:D019881]",2
"Ankyrin family",ANKYRIN,"auxiliary transport protein  ankyrin",NULL,2
"Basigin family",BASIGIN,"auxiliary transport protein  basigin",NULL,2
"Calcium channel auxiliary subunit alpha2delta family","CA alpha2delta","auxiliary transport protein  ca alpha2delta",NULL,2
"Calcium channel auxiliary subunit beta family","CA beta","auxiliary transport protein  ca beta",NULL,2
"Calcium channel auxiliary subunit gamma family","CA gamma","auxiliary transport protein  ca gamma",NULL,2
"Calcium-activated potassium channel auxiliary subunit gamma family","BK gamma","auxiliary transport protein  bk gamma",NULL,2
"Calcium-activated potassium channel auxiliary subunit slowpoke-beta family","SLO beta","auxiliary transport protein  slo beta",NULL,2
"Cytochrome P450","Cytochrome P450","enzyme  cytochrome p450","A superfamily of hundreds of closely related HEMEPROTEINS found throughout the phylogenetic spectrum, from animals, plants, fungi, to bacteria. They include numerous complex monooxygenases (MIXED FUNCTION OXYGENASES). In animals, these P-450 enzymes serve two major functions: (1) biosynthesis of steroids, fatty acids, and bile acids; (2) metabolism of endogenous and a wide variety of exogenous substrates, such as toxins and drugs (BIOTRANSFORMATION). They are classified, according to their sequence similarities rather than functions, into CYP gene families (>40% homology) and subfamilies (>59% homology). For example, enzymes from the CYP1, CYP2, and CYP3 gene families are responsible for most drug metabolism. [MESH:D003577]",2
"Electrochemical transporter",Electrochemical,"transporter  electrochemical",NULL,2
Eraser,Eraser,"epigenetic regulator  eraser","A class of proteins that remove methyl/acetyl groups from histones",2
"Family A G protein-coupled receptor",7TM1,"membrane receptor  7tm1",NULL,2
"Family B G protein-coupled receptor",7TM2,"membrane receptor  7tm2",NULL,2
"Family C G protein-coupled receptor",7TM3,"membrane receptor  7tm3",NULL,2
"Fatty acid binding protein family",FABP,"auxiliary transport protein  fabp",NULL,2
"Frizzled family G protein-coupled receptor",7TMFZ,"membrane receptor  7tmfz",NULL,2
"Group translocator","Group translocator","transporter  group translocator",NULL,2
Hydrolase,Hydrolase,"enzyme  hydrolase","A group of enzymes that catalyze the hydrolysis of a chemical bond",2
Isomerase,Isomerase,"enzyme  isomerase","A group of enzymes that catalyze the structural rearrangement of isomers",2
Kinase,Kinase,"enzyme  kinase","A rather large group of enzymes comprising not only those transferring phosphate but also diphosphate, nucleotidyl residues, and others. These have also been subdivided according to the acceptor group. (From Enzyme Nomenclature, 1992) EC 2.7. [MESH:D010770]",2
"Ligand-gated ion channel",LGIC,"ion channel  lgic","A subclass of ion channels that open or close in response to the binding of specific LIGANDS. [MESH:D058446]",2
Ligase,Ligase,"enzyme  ligase","A group of enzymes that catalyze the joining of two molecules with a new chemical bond",2
Lyase,Lyase,"enzyme  lyase","A group of enzymes that catalyze the breaking of a chemical bond by means other than hydrolysis or oxidation",2
"Nuclear receptor","Nuclear Receptor","transcription factor  nuclear receptor",NULL,2
"Other ion channel",OTHER,"ion channel  other",NULL,2
Oxidoreductase,Reductase,"enzyme  reductase","The class of all enzymes catalyzing oxidoreduction reactions. The substrate that is oxidized is regarded as a hydrogen donor. The systematic name is based on donor:acceptor oxidoreductase. The recommended name will be dehydrogenase, wherever this is possible; as an alternative, reductase can be used. Oxidase is only used in cases where O2 is the acceptor. (Enzyme Nomenclature, 1992, p9) [MESH:D010088]",2
Phosphatase,Phosphatase,"enzyme  phosphatase","A group of hydrolases which catalyze the hydrolysis of monophosphoric esters with the production of one mole of orthophosphate. EC 3.1.3. [MESH:D010744]",2
Phosphodiesterase,Phosphodiesterase,"enzyme  phosphodiesterase","A class of enzymes that catalyze the hydrolysis of one of the two ester bonds in a phosphodiester compound. EC 3.1.4. [MESH:D010727]",2
"Primary active transporter",NTPase,"transporter  ntpase",NULL,2
Protease,Protease,"enzyme  protease","A subclass of PEPTIDE HYDROLASES that catalyze the internal cleavage of PEPTIDES or PROTEINS. [MESH:D010450]",2
Reader,Reader,"epigenetic regulator  reader","A class of proteins that bind to methylated/acetylated histones or methylated DNA",2
"Slow voltage-gated potassium channel accessory protein family",MINK,"auxiliary transport protein  mink",NULL,2
"Sodium channel auxiliary subunit beta family","NA beta","auxiliary transport protein  na beta",NULL,2
"Taste family G protein-coupled receptor",7TMTAS2R,"membrane receptor  7tmtas2r",NULL,2
"Toll-like and Il-1 receptors","Toll-like and Il-1","membrane receptor  toll-like and il-1",NULL,2
Transferase,Transferase,"enzyme  transferase","A group of enzymes that catalyze the transfer of a functional group from one molecule to another",2
"Transmembrane 1-electron transfer carriers",1-Electron,"transporter  1-electron",NULL,2
"Voltage-gated ion channel",VGC,"ion channel  vgc",NULL,2
"Voltage-gated potassium channel beta-subunit family","KV beta","auxiliary transport protein  kv beta",NULL,2
Writer,Writer,"epigenetic regulator  writer","A class of proteins that transfer methyl/acetyl groups to histones or methyl groups to DNA",2
"4 TMS multidrug endosomal transporter family",MET,"transporter  electrochemical  met",NULL,3
"5HT3 receptor",5HT3,"ion channel  lgic  5ht3","A subclass of serotonin receptors that form cation channels and mediate signal transduction by depolarizing the cell membrane. The cation channels are formed from 5 receptor subunits. When stimulated the receptors allow the selective passage of SODIUM; POTASSIUM; and CALCIUM. [MESH:D044406]",3
"Acid-sensing ion channel",ASIC,"ion channel  lgic  asic",NULL,3
"Amino acid-polyamine-organocation family",APC,"transporter  electrochemical  apc",NULL,3
Annexin,ANNEXIN,"ion channel  other  annexin",NULL,3
Aquaporin,AQUAPORIN,"ion channel  other  aquaporin",NULL,3
"Aromatic acid:H+ symporter family",AAHS,"transporter  electrochemical  aahs",NULL,3
"Arsenite-antimonite efflux family",ARSB,"transporter  electrochemical  arsb",NULL,3
"Aspartic protease",Aspartic,"enzyme  protease  aspartic","A subclass of peptide hydrolases that depend on an ASPARTIC ACID residue for their activity. [MESH:D057055]",3
"ATP-binding cassette","ATP binding cassette","transporter  ntpase  atp binding cassette","A family of MEMBRANE TRANSPORT PROTEINS that require ATP hydrolysis for the transport of substrates across membranes. The protein family derives its name from the ATP-binding domain found on the protein. [MESH:D018528]",3
Bromodomain,BRD,"epigenetic regulator  reader  brd",NULL,3
"CatSper and Two-Pore channels",CATSPER,"ion channel  vgc  catsper",NULL,3
"Chloride channel",CHLORIDE,"ion channel  other  chloride",NULL,3
"Cyclic nucleotide-regulated channel",c-GMP,"ion channel  vgc  c-gmp","Ion channels that are regulated by cyclic GMP or cyclic AMP binding and contain six transmembrane segments and an ion conducting pore that passes monovalent cations. They are expressed in OLFACTORY NERVE cilia and in PHOTORECEPTOR CELLS and some PLANTS. They are blocked by DILTIAZEM. [MESH:D054815]",3
"Cysteine protease",Cysteine,"enzyme  protease  cysteine","A subclass of peptide hydrolases that depend on a CYSTEINE residue for their activity. [MESH:D057056]",3
"Cytochrome P450 CAM family",CYP_CAM,"enzyme  cytochrome p450  cyp_cam","A soluble cytochrome P-450 enzyme that catalyzes camphor monooxygenation in the presence of putidaredoxin, putidaredoxin reductase, and molecular oxygen. This enzyme, encoded by the CAMC gene also known as CYP101, has been crystallized from bacteria and the structure is well defined. Under anaerobic conditions, this enzyme reduces the polyhalogenated compounds bound at the camphor-binding site. [MESH:D019475]",3
"Cytochrome P450 family 1",CYP_1,"enzyme  cytochrome p450  cyp_1",NULL,3
"Cytochrome P450 family 11",CYP_11,"enzyme  cytochrome p450  cyp_11",NULL,3
"Cytochrome P450 family 17",CYP_17,"enzyme  cytochrome p450  cyp_17","A microsomal cytochrome P450 enzyme that catalyzes the 17-alpha-hydroxylation of progesterone or pregnenolone and subsequent cleavage of the residual two carbons at C17 in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP17 gene, generates precursors for glucocorticoid, androgen, and estrogen synthesis. Defects in CYP17 gene cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL) and abnormal sexual differentiation. [MESH:D013254]",3
"Cytochrome P450 family 19",CYP_19,"enzyme  cytochrome p450  cyp_19","An enzyme that catalyzes the desaturation (aromatization) of the ring A of C19 androgens and converts them to C18 estrogens. In this process, the 19-methyl is removed. This enzyme is membrane-bound, located in the endoplasmic reticulum of estrogen-producing cells of ovaries, placenta, testes, adipose, and brain tissues. Aromatase is encoded by the CYP19 gene, and functions in complex with NADPH-FERRIHEMOPROTEIN REDUCTASE in the cytochrome P-450 system. [MESH:D001141]",3
"Cytochrome P450 family 2",CYP_2,"enzyme  cytochrome p450  cyp_2",NULL,3
"Cytochrome P450 family 21",CYP_21,"enzyme  cytochrome p450  cyp_21","An adrenal microsomal cytochrome P450 enzyme that catalyzes the 21-hydroxylation of steroids in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP21 gene, converts progesterones to precursors of adrenal steroid hormones (CORTICOSTERONE; HYDROCORTISONE). Defects in CYP21 cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL). [MESH:D013255]",3
"Cytochrome P450 family 24",CYP_24,"enzyme  cytochrome p450  cyp_24",NULL,3
"Cytochrome P450 family 26",CYP_26,"enzyme  cytochrome p450  cyp_26",NULL,3
"Cytochrome P450 family 27",CYP_27,"enzyme  cytochrome p450  cyp_27",NULL,3
"Cytochrome P450 family 3",CYP_3,"enzyme  cytochrome p450  cyp_3",NULL,3
"Cytochrome P450 family 4",CYP_4,"enzyme  cytochrome p450  cyp_4",NULL,3
"Cytochrome P450 family 5",CYP_5,"enzyme  cytochrome p450  cyp_5",NULL,3
"Cytochrome P450 family 51",CYP_51,"enzyme  cytochrome p450  cyp_51",NULL,3
"Cytochrome P450 family 7",CYP_7,"enzyme  cytochrome p450  cyp_7",NULL,3
"Cytochrome P450 family 8",CYP_8,"enzyme  cytochrome p450  cyp_8",NULL,3
"DNA methyltransferase",DNMT,"epigenetic regulator  writer  dnmt","A family of enzymes that transfer methyl groups to cytosine residues of DNA",3
"Drug/metabolite transporter superfamily",DMT,"transporter  electrochemical  dmt",NULL,3
"Endoplasmic reticular retrotranslocon family",ERRT,"transporter  ntpase  errt",NULL,3
"Epithelial sodium channel",ENaC,"ion channel  lgic  enac",NULL,3
"F-type and V-type ATPases","F-type and V-type","transporter  ntpase  f-type and v-type",NULL,3
"GABA-A receptor",GABAA,"ion channel  lgic  gabaa","Cell surface proteins which bind GAMMA-AMINOBUTYRIC ACID and contain an integral membrane chloride channel. Each receptor is assembled as a pentamer from a pool of at least 19 different possible subunits. The receptors belong to a superfamily that share a common CYSTEINE loop. [MESH:D011963]",3
"Gap junction protein",GAP,"ion channel  other  gap",NULL,3
"General secretory pathway family",SEC,"transporter  ntpase  sec",NULL,3
"Glutamate-gated chloride channel (invertebrate)","GLUT (invertebrate)","ion channel  lgic  glut (invertebrate)","A class of glutamate-gated chloride channels found in invertebrate species",3
"Glycine receptor",GLY,"ion channel  lgic  gly","Cell surface receptors that bind GLYCINE with high affinity and trigger intracellular changes which influence the behavior of cells. Glycine receptors in the CENTRAL NERVOUS SYSTEM have an intrinsic chloride channel and are usually inhibitory. [MESH:D018009]",3
"Glycoside-pentoside-hexuronide:cation symporter family",GPH,"transporter  electrochemical  gph",NULL,3
"Guanylate cyclase","Guanylate cyclase","enzyme  lyase  guanylate cyclase","A class of cellular membrane receptors that either have an intrinsic guanylate cyclase activity or are closely coupled to specific guanylate cyclases within the cell. [MESH:D050705]",3
"Histone acetyltransferase",HAT,"epigenetic regulator  writer  hat",NULL,3
"Histone deacetylase",HDAC,"epigenetic regulator  eraser  hdac",NULL,3
"Ion receptor (family C GPCR)",Ion,"membrane receptor  7tm3  ion",NULL,3
"Ionotropic glutamate receptor",GLUT,"ion channel  lgic  glut","A class of ligand-gated ion channel receptors that have specificity for GLUTAMATE. They are distinct from METABOTROPIC GLUTAMATE RECEPTORS which act through a G-protein-coupled mechanism. [MESH:D058468]",3
"IP3 receptor",IP3,"ion channel  lgic  ip3","Intracellular receptors that bind to INOSITOL 1,4,5-TRISPHOSPHATE and play an important role in its intracellular signaling. Inositol 1,4,5-trisphosphate receptors are calcium channels that release CALCIUM in response to increased levels of inositol 1,4,5-trisphosphate in the CYTOPLASM. [MESH:D053496]",3
"Lysine demethylase",KDM,"epigenetic regulator  eraser  kdm",NULL,3
"Lysosomal cystine transporter family",LCT,"transporter  electrochemical  lct",NULL,3
"Metallo protease",Metallo,"enzyme  protease  metallo","Proteases which use a metal, normally ZINC, in the catalytic mechanism. This group of enzymes is inactivated by metal CHELATORS. [MESH:D045726]",3
"Methyl-CpG-binding domain",MBD,"epigenetic regulator  reader  mbd","A class of proteins that bind to methylated CpG islands in DNA through a methyl-CpG-binding (MBD) domain",3
"Methyl-lysine/arginine binding protein",Methyl-lysine,"epigenetic regulator  reader  methyl-lysine",NULL,3
"Miscellaneous ion channel",MISC,"ion channel  other  misc",NULL,3
"Mitochondrial and plastid porin family",MPP,"ion channel  other  mpp",NULL,3
"Mitochondrial inner membrane K+/H+ and Ca2+/H+ exchanger family",LETM1,"transporter  electrochemical  letm1",NULL,3
"Mitochondrial protein translocase family",MPT,"transporter  ntpase  mpt",NULL,3
"Mitochondrial pyruvate carrier family",MPC,"transporter  electrochemical  mpc",NULL,3
"Mitochondrial tricarboxylate carrier family",MTC,"transporter  electrochemical  mtc",NULL,3
"Monovalent cation:proton antiporter-2 family",CPA2,"transporter  electrochemical  cpa2",NULL,3
"Multidrug/oligosaccharidyl-lipid/polysaccharide flippase superfamily",MOP,"transporter  electrochemical  mop",NULL,3
"Nicotinic acetylcholine receptor",ACH,"ion channel  lgic  ach",NULL,3
"Nuclear hormone receptor subfamily 0",NR0,"transcription factor  nuclear receptor  nr0",NULL,3
"Nuclear hormone receptor subfamily 1",NR1,"transcription factor  nuclear receptor  nr1",NULL,3
"Nuclear hormone receptor subfamily 2",NR2,"transcription factor  nuclear receptor  nr2",NULL,3
"Nuclear hormone receptor subfamily 3",NR3,"transcription factor  nuclear receptor  nr3",NULL,3
"Nuclear hormone receptor subfamily 4",NR4,"transcription factor  nuclear receptor  nr4",NULL,3
"Nuclear hormone receptor subfamily 5",NR5,"transcription factor  nuclear receptor  nr5",NULL,3
"Nuclear hormone receptor subfamily 6",NR6,"transcription factor  nuclear receptor  nr6",NULL,3
"Nuclear mRNA exporter family",mRNA-E,"transporter  ntpase  nrna-e",NULL,3
"Nuclear pore complex family",NPC,"ion channel  other  npc",NULL,3
Opsin,Opsin,"membrane receptor  7tm1  opsin",NULL,3
"Oxidoreduction-driven transporters",Oxidoreduction,"transporter  ntpase  oxidoreduction",NULL,3
"P-type ATPase","P-type ATPase","transporter  ntpase  p-type atpase",NULL,3
"P2X receptor",P2X,"ion channel  lgic  p2x","A subclass of purinergic P2 receptors that signal by means of a ligand-gated ion channel. They are comprised of three P2X subunits which can be identical (homotrimeric form) or dissimilar (heterotrimeric form). [MESH:D058469]",3
"Paracellular channels",PARACELLULAR,"ion channel  other  paracellular",NULL,3
"Peptide receptor (family A GPCR)",Peptide,"membrane receptor  7tm1  peptide",NULL,3
"Peptide receptor (family B GPCR)",Peptide,"membrane receptor  7tm2  peptide",NULL,3
"Peroxisomal protein importer family",PPI,"transporter  ntpase  ppi",NULL,3
"Phosphodiesterase 1",PDE_1,"enzyme  phosphodiesterase  pde_1","A CALCIUM and CALMODULIN-dependent cyclic nucleotide phosphodiesterase subfamily. The three members of this family are referred to as type 1A, type 1B, and type 1C and are each product of a distinct gene. In addition, multiple enzyme variants of each subtype can be produced due to multiple alternative mRNA splicing. Although the type 1 enzymes are classified as 3',5'-cyclic-AMP phosphodiesterases (EC 3.1.4.17), some members of this class have additional specificity for CYCLIC GMP. [MESH:D054677]",3
"Phosphodiesterase 10",PDE_10,"enzyme  phosphodiesterase  pde_10",NULL,3
"Phosphodiesterase 11",PDE_11,"enzyme  phosphodiesterase  pde_11",NULL,3
"Phosphodiesterase 2",PDE_2,"enzyme  phosphodiesterase  pde_2","A cyclic nucleotide phosphodiesterase subfamily that is activated by the binding of CYCLIC GMP to an allosteric domain found on the enzyme. Multiple enzyme variants of this subtype can be produced due to multiple alternative mRNA splicing. The subfamily is expressed in a broad variety of tissues and may play a role in mediating cross-talk between CYCLIC GMP and CYCLIC CMP pathways. Although the type 2 enzymes are classified as 3',5'-cyclic-AMP phosphodiesterases (EC 3.1.4.17), members of this class have additional specificity for CYCLIC GMP. [MESH:D054678]",3
"Phosphodiesterase 3",PDE_3,"enzyme  phosphodiesterase  pde_3","A cyclic nucleotide phosphodiesterase subfamily that is inhibited by the binding of CYCLIC GMP to an allosteric domain found on the enzyme and through phosphorylation by regulatory kinases such as PROTEIN KINASE A and PROTEIN KINASE B. The two members of this family are referred to as type 3A, and type 3B, and are each product of a distinct gene. In addition multiple enzyme variants of each subtype can be produced due to multiple alternative mRNA splicing. [MESH:D054684]",3
"Phosphodiesterase 4",PDE_4,"enzyme  phosphodiesterase  pde_4","A cyclic nucleotide phosphodiesterase subfamily that is found predominantly in inflammatory cells and may play a role in the regulation of CELL-MEDIATED IMMUNITY. The enzyme family includes over twenty different variants that occur due to multiple ALTERNATIVE SPLICING of the mRNA of at least four different genes. [MESH:D054703]",3
"Phosphodiesterase 5",PDE_5,"enzyme  phosphodiesterase  pde_5","A cyclic nucleotide phosphodiesterase subfamily that is highly specific for CYCLIC GMP. It is found predominantly in vascular tissue and plays an important role in regulating VASCULAR SMOOTH MUSCLE contraction. [MESH:D054706]",3
"Phosphodiesterase 6",PDE_6,"enzyme  phosphodiesterase  pde_6","A cyclic nucleotide phosphodiesterase subfamily that is highly specific for CYCLIC GMP. It is found predominantly in the outer segment PHOTORECEPTOR CELLS of the RETINA. It is comprised of two catalytic subunits, referred to as alpha and beta, that form a dimer. In addition two regulatory subunits, referred to as gamma and delta, modulate the activity and localization of the enzyme. [MESH:D054707]",3
"Phosphodiesterase 7",PDE_7,"enzyme  phosphodiesterase  pde_7","A cyclic nucleotide phosphodiesterase subfamily that is highly specific for CYCLIC AMP. Several isoforms of the enzyme type exist, each with its own tissue localization. The isoforms are encoded by at least two genes and are a product of multiple alternative splicing of their mRNAs. [MESH:D054708]",3
"Phosphodiesterase 8",PDE_8,"enzyme  phosphodiesterase  pde_8",NULL,3
"Phosphodiesterase 9",PDE_9,"enzyme  phosphodiesterase  pde_9",NULL,3
"Phospholemman family",PLM,"ion channel  other  plm",NULL,3
"Plant homeodomain",PHD,"epigenetic regulator  reader  phd",NULL,3
"Pore-forming toxins (proteins and peptides)",TOXIN,"ion channel  other  toxin",NULL,3
"Potassium channels",K,"ion channel  vgc  k",NULL,3
"Protease inhibitor",Inhibitor,"enzyme  protease  inhibitor",NULL,3
"Protease unclassified",Unknown,"enzyme  protease  unknown",NULL,3
"Protein Kinase","Protein Kinase","enzyme  kinase  protein kinase","A family of enzymes that catalyze the conversion of ATP and a protein to ADP and a phosphoprotein. [MESH:D011494]",3
"Protein kinase regulatory subunit",Reg,"enzyme  kinase  reg",NULL,3
"Protein methyltransferase",PMT,"epigenetic regulator  writer  pmt",NULL,3
"Protein Phosphatase","Protein Phosphatase","enzyme  phosphatase  protein phosphatase","A group of hydrolases which catalyze the hydrolysis of monophosphoric esters with the production of one mole of orthophosphate. EC 3.1.3. [MESH:D010744]",3
"Protein-glutamine glutamyl-transferase","Protein-glutamine glutamyl-transferase","enzyme  aminoacyltransferase  protein-glutamine glutamyl-transferase","Transglutaminases catalyze cross-linking of proteins at a GLUTAMINE in one chain with LYSINE in another chain. They include keratinocyte transglutaminase (TGM1 or TGK), tissue transglutaminase (TGM2 or TGC), plasma transglutaminase involved with coagulation (FACTOR XIII and FACTOR XIIIa), hair follicle transglutaminase, and prostate transglutaminase. Although structures differ, they share an active site (YGQCW) and strict CALCIUM dependence. [MESH:D011503]",3
"Reduced folate carrier family",RFC,"transporter  electrochemical  rfc",NULL,3
"Ryanodine receptor",RYR,"ion channel  lgic  ryr",NULL,3
"Serine protease",Serine,"enzyme  protease  serine","Peptide hydrolases that contain at the active site a SERINE residue involved in catalysis. [MESH:D057057]",3
"SLC superfamily of solute carriers",SLC,"transporter  electrochemical  slc",NULL,3
"Small molecule receptor (family A GPCR)",SmallMol,"membrane receptor  7tm1  smallmol",NULL,3
"Small molecule receptor (family C GPCR)",SmallMol,"membrane receptor  7tm3  smallmol",NULL,3
"Smoothened receptor (frizzled family GPCR)",Smoothened,"membrane receptor  7tmfz  smoothened",NULL,3
"Spindlin domain",Spindlin,"epigenetic regulator  reader  spindlin",NULL,3
"Taste receptor (family C GPCR)","Taste receptor","membrane receptor  7tm3  taste receptor",NULL,3
"Taste receptor (taste family GPCR)","Taste receptor","membrane receptor  7tmtas2r  taste receptor",NULL,3
"Threonine protease",Threonine,"enzyme  protease  threonine",NULL,3
"TMS recognition/insertion complex family",TRC,"transporter  ntpase  trc",NULL,3
"Transient receptor potential channel",TRP,"ion channel  vgc  trp",NULL,3
"Vesicle fusion pores",VESICLE,"ion channel  other  vesicle",NULL,3
"Vesicular neurotransmitter transporter family",VNT,"transporter  electrochemical  vnt",NULL,3
"Vitamin A receptor/transporter family",STRA6,"transporter  electrochemical  stra6",NULL,3
"Voltage-gated calcium channel","VG CA","ion channel  vgc  vg ca","Voltage-dependent cell membrane glycoproteins selectively permeable to calcium ions. They are categorized as L-, T-, N-, P-, Q-, and R-types based on the activation and inactivation kinetics, ion specificity, and sensitivity to drugs and toxins. The L- and T-types are present throughout the cardiovascular and central nervous systems and the N-, P-, Q-, & R-types are located in neuronal tissue. [MESH:D015220]",3
"Voltage-gated proton channel","VG H","ion channel  vgc  vg h",NULL,3
"Voltage-gated sodium channel","VG NA","ion channel  vgc  vg na",NULL,3
"YEATS domain",YEATS,"epigenetic regulator  reader  yeats",NULL,3
"Zinc-activated channel",ZAC,"ion channel  lgic  zac",NULL,3
"ABCA subfamily",ABCA,"transporter  ntpase  atp binding cassette  abca",NULL,4
"ABCB subfamily",MDR,"transporter  ntpase  atp binding cassette  mdr","A subfamily of transmembrane proteins from the superfamily of ATP-BINDING CASSETTE TRANSPORTERS that are closely related in sequence to P-GLYCOPROTEIN. When overexpressed, they function as ATP-dependent efflux pumps able to extrude lipophilic drugs, especially ANTINEOPLASTIC AGENTS, from cells causing multidrug resistance (DRUG RESISTANCE, MULTIPLE). Although P-Glycoproteins share functional similarities to MULTIDRUG RESISTANCE-ASSOCIATED PROTEINS they are two distinct subclasses of ATP-BINDING CASSETTE TRANSPORTERS, and have little sequence homology. [MESH:D018435]",4
"ABCC subfamily",MRP,"transporter  ntpase  atp binding cassette  mrp","A sequence-related subfamily of ATP-BINDING CASSETTE TRANSPORTERS that actively transport organic substrates. Although considered organic anion transporters, a subset of proteins in this family have also been shown to convey drug resistance to neutral organic drugs. Their cellular function may have clinical significance for CHEMOTHERAPY in that they transport a variety of ANTINEOPLASTIC AGENTS. Overexpression of proteins in this class by NEOPLASMS is considered a possible mechanism in the development of multidrug resistance (DRUG RESISTANCE, MULTIPLE). Although similar in function to P-GLYCOPROTEINS, the proteins in this class share little sequence homology to the p-glycoprotein family of proteins. [MESH:D027425]",4
"ABCD subfamily",ABCD,"transporter  ntpase  atp binding cassette  abcd",NULL,4
"ABCE subfamily",ABCE,"transporter  ntpase  atp binding cassette  abce",NULL,4
"ABCF subfamily",ABCF,"transporter  ntpase  atp binding cassette  abcf",NULL,4
"ABCG subfamily",ABCG,"transporter  ntpase  atp binding cassette  abcg",NULL,4
"AGC protein kinase group",Agc,"enzyme  kinase  protein kinase  agc",NULL,4
"AMPA receptor",AMPA,"ion channel  lgic  glut  ampa","A class of ionotropic glutamate receptors characterized by their affinity for the agonist AMPA (alpha-amino-3-hydroxy-5-methyl-4-isoxazolepropionic acid). [MESH:D018091]",4
"Anaphylatoxin receptor family","Anaphylatoxin receptor","membrane receptor  7tm1  peptide  anaphylatoxin receptor","A G-protein-coupled receptor that signals an increase in intracellular calcium in response to the potent ANAPHYLATOXIN peptide COMPLEMENT C5A. [MESH:D044087]",4
"Anion channel tweety family",TWEETY,"ion channel  other  misc  tweety",NULL,4
"Anion channel-forming bestrophin family",BESTROPHIN,"ion channel  other  misc  bestrophin",NULL,4
Aquaglyceroporin,AQUAGLYCEROPORIN,"ion channel  other  aquaporin  aquaglyceroporin",NULL,4
"Aquaporin 8","AQUAPORIN 8","ion channel  other  aquaporin  aquaporin 8",NULL,4
"Aspartic protease AA clan",AA,"enzyme  protease  aspartic  aa",NULL,4
"Aspartic protease AD clan",AD,"enzyme  protease  aspartic  ad",NULL,4
"Aspartic protease AF clan",AF,"enzyme  protease  aspartic  af",NULL,4
"Atypical protein kinase group",Atypical,"enzyme  kinase  protein kinase  atypical",NULL,4
"Bcl-2 family",BCL-2,"ion channel  other  misc  bcl-2",NULL,4
"Ca2+ release-activated Ca2+ channel family",CRAC-C,"ion channel  other  misc  crac-c",NULL,4
"Calcitonin-like receptor",Calcitonin-like,"membrane receptor  7tm2  peptide  calcitonin-like","Cell surface proteins that bind CALCITONIN GENE-RELATED PEPTIDE with high affinity and trigger intracellular changes which influence the behavior of cells. CGRP receptors are present in both the CENTRAL NERVOUS SYSTEM and the periphery. They are formed via the heterodimerization of the CALCITONIN RECEPTOR-LIKE PROTEIN and RECEPTOR ACTIVITY-MODIFYING PROTEIN 1. [MESH:D018015]",4
"Calcium ATPase","Ca ATPase","transporter  ntpase  p-type atpase  ca atpase",NULL,4
"Calcium homeostasis modulator Ca2+ channel family",CALHM-C,"ion channel  other  misc  calhm-c",NULL,4
"Calcium sensing receptor","Calcium sensing receptor","membrane receptor  7tm3  ion  calcium sensing receptor","A class of G-protein-coupled receptors that react to varying extracellular CALCIUM levels. Calcium-sensing receptors in the PARATHYROID GLANDS play an important role in the maintenance of calcium HOMEOSTASIS by regulating the release of PARATHYROID HORMONE. They differ from INTRACELLULAR CALCIUM-SENSING PROTEINS which sense intracellular calcium levels. [MESH:D044169]",4
"Calcium-activated chloride channel","CA ACT CL","ion channel  other  chloride  ca act cl",NULL,4
"Calcium-activated potassium channel","CA ACT K","ion channel  vgc  k  ca act k",NULL,4
"CAMK protein kinase group",Camk,"enzyme  kinase  protein kinase  camk","A CALMODULIN-dependent enzyme that catalyzes the phosphorylation of proteins. This enzyme is also sometimes dependent on CALCIUM. A wide range of proteins can act as acceptor, including VIMENTIN; SYNAPSINS; GLYCOGEN SYNTHASE; MYOSIN LIGHT CHAINS; and the MICROTUBULE-ASSOCIATED PROTEINS. (From Enzyme Nomenclature, 1992, p277) [MESH:D017871]",4
"Carboxylic acid receptor","Carboxylic acid","membrane receptor  7tm1  smallmol  carboxylic acid",NULL,4
"CD20 Ca2+ channel family",CD20,"ion channel  other  misc  cd20",NULL,4
"Chemokine receptor","Chemokine receptor","membrane receptor  7tm1  peptide  chemokine receptor","Cell surface glycoproteins that bind to chemokines and thus mediate the migration of pro-inflammatory molecules. The receptors are members of the seven-transmembrane G protein-coupled receptor family. Like the CHEMOKINES themselves, the receptors can be divided into at least three structural branches: CR, CCR, and CXCR, according to variations in a shared cysteine motif. [MESH:D019707]",4
"Chemokine receptor-like","Chemokine receptor-like","membrane receptor  7tm1  peptide  chemokine receptor-like",NULL,4
"Cholesterol uptake protein and double stranded RNA uptake family","CHUP DSRNA","ion channel  other  misc  chup dsrna",NULL,4
Chromodomain,CHROMO,"epigenetic regulator  reader  methyl-lysine  chromo",NULL,4
"CK1 protein kinase group",Ck1,"enzyme  kinase  protein kinase  ck1",NULL,4
"Claudin tight junction family",CLAUDIN,"ion channel  other  paracellular  claudin",NULL,4
"ClC chloride channel",CLC,"ion channel  other  chloride  clc",NULL,4
"CMGC protein kinase group",Cmgc,"enzyme  kinase  protein kinase  cmgc",NULL,4
"Copper ATPase","Cu ATPase","transporter  ntpase  p-type atpase  cu atpase",NULL,4
"CorA metal ion transporter family",MIT,"ion channel  other  misc  mit",NULL,4
"Corticotropin releasing factor receptor","Corticotropin releasing factor receptor","membrane receptor  7tm2  peptide  corticotropin releasing factor receptor","Cell surface proteins that bind corticotropin-releasing hormone with high affinity and trigger intracellular changes which influence the behavior of cells. The corticotropin releasing-hormone receptors on anterior pituitary cells mediate the stimulation of corticotropin release by hypothalamic corticotropin releasing factor. The physiological consequence of activating corticotropin-releasing hormone receptors on central neurons is not well understood. [MESH:D018019]",4
"Cysteine protease CA clan",CA,"enzyme  protease  cysteine  ca",NULL,4
"Cysteine protease CD clan",CD,"enzyme  protease  cysteine  cd",NULL,4
"Cysteine protease CE clan",CE,"enzyme  protease  cysteine  ce",NULL,4
"Cysteine protease CM clan",CM,"enzyme  protease  cysteine  cm",NULL,4
"Cysteine protease PAC clan",PAC,"enzyme  protease  cysteine  pac",NULL,4
"Cysteine protease PCC clan",PCC,"enzyme  protease  cysteine  pcc",NULL,4
"Cystic fibrosis transmembrane conductance regulator",CFTR,"ion channel  other  chloride  cftr","A chloride channel that regulates secretion in many exocrine tissues. Abnormalities in the CFTR gene have been shown to cause cystic fibrosis. (Hum Genet 1994;93(4):364-8) [MESH:D019005]",4
"Cytochrome P450 family 11A",CYP_11A,"enzyme  cytochrome p450  cyp_11  cyp_11a",NULL,4
"Cytochrome P450 family 11B",CYP_11B,"enzyme  cytochrome p450  cyp_11  cyp_11b",NULL,4
"Cytochrome P450 family 17A",CYP_17A,"enzyme  cytochrome p450  cyp_17  cyp_17a","A microsomal cytochrome P450 enzyme that catalyzes the 17-alpha-hydroxylation of progesterone or pregnenolone and subsequent cleavage of the residual two carbons at C17 in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP17 gene, generates precursors for glucocorticoid, androgen, and estrogen synthesis. Defects in CYP17 gene cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL) and abnormal sexual differentiation. [MESH:D013254]",4
"Cytochrome P450 family 19A",CYP_19A,"enzyme  cytochrome p450  cyp_19  cyp_19a","An enzyme that catalyzes the desaturation (aromatization) of the ring A of C19 androgens and converts them to C18 estrogens. In this process, the 19-methyl is removed. This enzyme is membrane-bound, located in the endoplasmic reticulum of estrogen-producing cells of ovaries, placenta, testes, adipose, and brain tissues. Aromatase is encoded by the CYP19 gene, and functions in complex with NADPH-FERRIHEMOPROTEIN REDUCTASE in the cytochrome P-450 system. [MESH:D001141]",4
"Cytochrome P450 family 1A",CYP_1A,"enzyme  cytochrome p450  cyp_1  cyp_1a",NULL,4
"Cytochrome P450 family 1B",CYP_1B,"enzyme  cytochrome p450  cyp_1  cyp_1b",NULL,4
"Cytochrome P450 family 21A",CYP_21A,"enzyme  cytochrome p450  cyp_21  cyp_21a","An adrenal microsomal cytochrome P450 enzyme that catalyzes the 21-hydroxylation of steroids in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP21 gene, converts progesterones to precursors of adrenal steroid hormones (CORTICOSTERONE; HYDROCORTISONE). Defects in CYP21 cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL). [MESH:D013255]",4
"Cytochrome P450 family 24A",CYP_24A,"enzyme  cytochrome p450  cyp_24  cyp_24a",NULL,4
"Cytochrome P450 family 26A",CYP_26A,"enzyme  cytochrome p450  cyp_26  cyp_26a",NULL,4
"Cytochrome P450 family 27A",CYP_27A,"enzyme  cytochrome p450  cyp_27  cyp_27a",NULL,4
"Cytochrome P450 family 27B",CYP_27B,"enzyme  cytochrome p450  cyp_27  cyp_27b",NULL,4
"Cytochrome P450 family 2A",CYP_2A,"enzyme  cytochrome p450  cyp_2  cyp_2a",NULL,4
"Cytochrome P450 family 2B",CYP_2B,"enzyme  cytochrome p450  cyp_2  cyp_2b",NULL,4
"Cytochrome P450 family 2C",CYP_2C,"enzyme  cytochrome p450  cyp_2  cyp_2c",NULL,4
"Cytochrome P450 family 2D",CYP_2D,"enzyme  cytochrome p450  cyp_2  cyp_2d",NULL,4
"Cytochrome P450 family 2E",CYP_2E,"enzyme  cytochrome p450  cyp_2  cyp_2e",NULL,4
"Cytochrome P450 family 3A",CYP_3A,"enzyme  cytochrome p450  cyp_3  cyp_3a","A cytochrome P-450 monooxygenase that is involved in an NADPH-dependent electron transport pathway by oxidizing a variety of structurally unrelated compounds, including STEROIDS; FATTY ACIDS; and XENOBIOTICS. This enzyme has clinical significance due to its ability to metabolize a diverse array of clinically important drugs such as CYCLOSPORINE; VERAPAMIL; and MIDAZOLAM. This enzyme also catalyzes the N-demethylation of ERYTHROMYCIN. [MESH:D051544]",4
"Cytochrome P450 family 4A",CYP_4A,"enzyme  cytochrome p450  cyp_4  cyp_4a","A P450 oxidoreductase that catalyzes the hydroxylation of the terminal carbon of linear hydrocarbons such as octane and FATTY ACIDS in the omega position. The enzyme may also play a role in the oxidation of a variety of structurally unrelated compounds such as XENOBIOTICS, and STEROIDS. [MESH:D042926]",4
"Cytochrome P450 family 4F",CYP_4F,"enzyme  cytochrome p450  cyp_4  cyp_4f",NULL,4
"Cytochrome P450 family 4X",CYP_4X,"enzyme  cytochrome p450  cyp_4  cyp_4x",NULL,4
"Cytochrome P450 family 51A",CYP_51A,"enzyme  cytochrome p450  cyp_51  cyp_51a",NULL,4
"Cytochrome P450 family 5A",CYP_5A,"enzyme  cytochrome p450  cyp_5  cyp_5a","An enzyme found predominantly in platelet microsomes. It catalyzes the conversion of PGG(2) and PGH(2) (prostaglandin endoperoxides) to thromboxane A2. EC 5.3.99.5. [MESH:D013930]",4
"Cytochrome P450 family 7A",CYP_7A,"enzyme  cytochrome p450  cyp_7  cyp_7a","A membrane-bound cytochrome P450 enzyme that catalyzes the 7-alpha-hydroxylation of CHOLESTEROL in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP7, converts cholesterol to 7-alpha-hydroxycholesterol which is the first and rate-limiting step in the synthesis of BILE ACIDS. [MESH:D002790]",4
"Cytochrome P450 family 8A",CYP_8A,"enzyme  cytochrome p450  cyp_8  cyp_8a",NULL,4
"Epithelial chloride channel",E-CLC,"ion channel  other  chloride  e-clc",NULL,4
"F-type ATPase","F-type ATPase","transporter  ntpase  f-type and v-type  f-type atpase",NULL,4
"Gap junction protein alpha","GAP ALPHA","ion channel  other  gap  gap junction protein alpha",NULL,4
"Gap junction protein beta","GAP BETA","ion channel  other  gap  gap junction protein beta",NULL,4
"Gap junction protein delta","GAP DELTA","ion channel  other  gap  gap junction protein delta",NULL,4
"Gap junction protein epsilon","GAP EPSILON","ion channel  other  gap  gap junction protein epsilon",NULL,4
"Gap junction protein gamma","GAP GAMMA","ion channel  other  gap  gap junction protein gamma",NULL,4
"Glucagon-like receptor",Glucagon-like,"membrane receptor  7tm2  peptide  glucagon-like",NULL,4
"Glutamate receptor ionotropic delta-1",GRID,"ion channel  lgic  glut  grid",NULL,4
"Glycohormone receptor","Glycohormone receptor","membrane receptor  7tm1  peptide  glycohormone receptor",NULL,4
"GNAT family",GNAT,"epigenetic regulator  writer  hat  gnat",NULL,4
"Golgi pH regulator family",GPHR,"ion channel  other  misc  gphr",NULL,4
"HDAC class I","HDAC class I","epigenetic regulator  eraser  hdac  hdac class i",NULL,4
"HDAC class IIa","HDAC class IIa","epigenetic regulator  eraser  hdac  hdac class iia",NULL,4
"HDAC class IIb","HDAC class IIb","epigenetic regulator  eraser  hdac  hdac class iib",NULL,4
"HDAC class III","HDAC class III","epigenetic regulator  eraser  hdac  hdac class iii",NULL,4
"HDAC class IV","HDAC class IV","epigenetic regulator  eraser  hdac  hdac class iv",NULL,4
"Homotrimeric cation channel family",TRIC,"ion channel  other  misc  tric",NULL,4
"Hydrogen potassium ATPase","H K ATPase","transporter  ntpase  p-type atpase  h k atpase",NULL,4
"Intracellular chloride channel",CLIC,"ion channel  other  chloride  clic",NULL,4
"Inwardly rectifying potassium channel",KIR,"ion channel  vgc  k  kir","Potassium channels where the flow of K+ ions into the cell is greater than the outward flow. [MESH:D024661]",4
"Ionotropic glutamate receptor-like",GRINL,"ion channel  lgic  glut  grinl",NULL,4
"Jumonji domain-containing",Jumonji,"epigenetic regulator  eraser  kdm  jumonji",NULL,4
"Kainate receptor",KAINATE,"ion channel  lgic  glut  kainate","A class of ionotropic glutamate receptors characterized by their affinity for KAINIC ACID. [MESH:D018092]",4
"Lipid-like ligand receptor (family A GPCR)","Lipid-like ligand receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor",NULL,4
"Lysine-specific demethylase",LSD,"epigenetic regulator  eraser  kdm  lsd",NULL,4
"MBT domain",MBT,"epigenetic regulator  reader  methyl-lysine  mbt",NULL,4
"Mechanical nociceptor piezo family",PIEZO,"ion channel  other  misc  piezo",NULL,4
"Membrane Mg2+ transporter family",MMGT,"ion channel  other  misc  mmgt",NULL,4
"Metallo protease MAE clan",MAE,"enzyme  protease  metallo  mae",NULL,4
"Metallo protease MAM clan",MAM,"enzyme  protease  metallo  mam",NULL,4
"Metallo protease MC clan",MC,"enzyme  protease  metallo  mc",NULL,4
"Metallo protease MD clan",MD,"enzyme  protease  metallo  md",NULL,4
"Metallo protease MF clan",MF,"enzyme  protease  metallo  mf",NULL,4
"Metallo protease MG clan",MG,"enzyme  protease  metallo  mg",NULL,4
"Metallo protease MH clan",MH,"enzyme  protease  metallo  mh",NULL,4
"Metallo protease MJ clan",MJ,"enzyme  protease  metallo  mj",NULL,4
"Metallo protease MP clan",MP,"enzyme  protease  metallo  mp",NULL,4
"Metallo protease unclassified clan",M-,"enzyme  protease  metallo  m-",NULL,4
"Mg2+/Ca2+ uniporter family",MCU,"ion channel  other  misc  mcu",NULL,4
"Mitochondrial EF hand Ca2+ uptake porter/regulator family",MICU,"ion channel  other  misc  micu",NULL,4
"Monoamine receptor","Monoamine receptor","membrane receptor  7tm1  smallmol  monoamine receptor",NULL,4
"Monoamine-derivative receptor (family A GPCR)",Monoamine-derivative,"membrane receptor  7tm1  smallmol  monoamine-derivative",NULL,4
"MYST family",MYST,"epigenetic regulator  writer  hat  myst",NULL,4
"N-formyl methionyl peptide receptor","N-formyl methionyl peptide receptor","membrane receptor  7tm1  peptide  n-formyl methionyl peptide receptor","A family of G-protein-coupled receptors that was originally identified by its ability to bind N-formyl peptides such as N-FORMYLMETHIONINE LEUCYL-PHENYLALANINE. Since N-formyl peptides are found in MITOCHONDRIA and BACTERIA, this class of receptors is believed to play a role in mediating cellular responses to cellular damage and bacterial invasion. However, non-formylated peptide ligands have also been found for this receptor class. [MESH:D044042]",4
"Neurotransmitter receptor (family C GPCR)",Neurotransmitter,"membrane receptor  7tm3  smallmol  neurotransmitter",NULL,4
"Nicotinic acetylcholine receptor alpha subunit","CHRN alpha","ion channel  lgic  ach  chrn alpha",NULL,4
"Nicotinic acetylcholine receptor beta subunit","CHRN beta","ion channel  lgic  ach  chrn beta",NULL,4
"Nicotinic acetylcholine receptor delta subunit","CHRN delta","ion channel  lgic  ach  chrn delta",NULL,4
"Nicotinic acetylcholine receptor epsilon subunit","CHRN epsilon","ion channel  lgic  ach  chrn epsilon",NULL,4
"Nicotinic acetylcholine receptor gamma subunit","CHRN gamma","ion channel  lgic  ach  chrn gamma",NULL,4
"NMDA receptor",NMDA,"ion channel  lgic  glut  nmda","A class of ionotropic glutamate receptors characterized by affinity for N-methyl-D-aspartate. NMDA receptors have an allosteric binding site for glycine which must be occupied for the channel to open efficiently and a site within the channel itself to which magnesium ions bind in a voltage-dependent manner. The positive voltage dependence of channel conductance and the high permeability of the conducting channel to calcium ions (as well as to monovalent cations) are important in excitotoxicity and neuronal plasticity. [MESH:D016194]",4
"Non-selective cation channel-2 family",NSCC2,"ion channel  other  misc  nscc2",NULL,4
"Nuclear hormone receptor subfamily 0 group B",NR0B,"transcription factor  nuclear receptor  nr0  nr0b",NULL,4
"Nuclear hormone receptor subfamily 1 group A",NR1A,"transcription factor  nuclear receptor  nr1  nr1a","Specific high affinity binding proteins for THYROID HORMONES in target cells. They are usually found in the nucleus and regulate DNA transcription. These receptors are activated by hormones that leads to transcription, cell differentiation, and growth suppression. Thyroid hormone receptors are encoded by two genes (GENES, ERBA): erbA-alpha and erbA-beta for alpha and beta thyroid hormone receptors, respectively. [MESH:D011988]",4
"Nuclear hormone receptor subfamily 1 group B",NR1B,"transcription factor  nuclear receptor  nr1  nr1b","Proteins in the nucleus or cytoplasm that specifically bind RETINOIC ACID or RETINOL and trigger changes in the behavior of cells. Retinoic acid receptors, like steroid receptors, are ligand-activated transcription regulators. Several types have been recognized. [MESH:D018168]",4
"Nuclear hormone receptor subfamily 1 group C",NR1C,"transcription factor  nuclear receptor  nr1  nr1c","TRANSCRIPTION FACTORS that are activated by ligands and heterodimerize with RETINOID X RECEPTORS and bind to peroxisome proliferator response elements in the promoter regions of target genes. [MESH:D047492]",4
"Nuclear hormone receptor subfamily 1 group D",NR1D,"transcription factor  nuclear receptor  nr1  nr1d",NULL,4
"Nuclear hormone receptor subfamily 1 group F",NR1F,"transcription factor  nuclear receptor  nr1  nr1f",NULL,4
"Nuclear hormone receptor subfamily 1 group H",NR1H,"transcription factor  nuclear receptor  nr1  nr1h",NULL,4
"Nuclear hormone receptor subfamily 1 group I",NR1I,"transcription factor  nuclear receptor  nr1  nr1i",NULL,4
"Nuclear hormone receptor subfamily 2 group A",NR2A,"transcription factor  nuclear receptor  nr2  nr2a",NULL,4
"Nuclear hormone receptor subfamily 2 group B",NR2B,"transcription factor  nuclear receptor  nr2  nr2b","A subtype of RETINOIC ACID RECEPTORS that are specific for 9-cis-retinoic acid which function as nuclear TRANSCRIPTION FACTORS that regulate multiple signalling pathways. [MESH:D047488]",4
"Nuclear hormone receptor subfamily 2 group C",NR2C,"transcription factor  nuclear receptor  nr2  nr2c",NULL,4
"Nuclear hormone receptor subfamily 2 group E",NR2E,"transcription factor  nuclear receptor  nr2  nr2e",NULL,4
"Nuclear hormone receptor subfamily 2 group F",NR2F,"transcription factor  nuclear receptor  nr2  nr2f",NULL,4
"Nuclear hormone receptor subfamily 3 group A",NR3A,"transcription factor  nuclear receptor  nr3  nr3a","Cytoplasmic proteins that bind estrogens and migrate to the nucleus where they regulate DNA transcription. Evaluation of the state of estrogen receptors in breast cancer patients has become clinically important. [MESH:D011960]",4
"Nuclear hormone receptor subfamily 3 group B",NR3B,"transcription factor  nuclear receptor  nr3  nr3b",NULL,4
"Nuclear hormone receptor subfamily 3 group C",NR3C,"transcription factor  nuclear receptor  nr3  nr3c",NULL,4
"Nuclear hormone receptor subfamily 4 group A",NR4A,"transcription factor  nuclear receptor  nr4  nr4a",NULL,4
"Nuclear hormone receptor subfamily 5 group A",NR5A,"transcription factor  nuclear receptor  nr5  nr5a",NULL,4
"Nuclear hormone receptor subfamily 6 group A",NR6A,"transcription factor  nuclear receptor  nr6  nr6a",NULL,4
"Nucleotide-like receptor (family A GPCR)","Nucleotide-like receptor","membrane receptor  7tm1  smallmol  nucleotide-like receptor",NULL,4
"Other protein kinase group",Other,"enzyme  kinase  protein kinase  other",NULL,4
"p300/CBP family","p300 CBP","epigenetic regulator  writer  hat  p300 cbp",NULL,4
Pannexin,PANNEXIN,"ion channel  other  gap  pannexin",NULL,4
"Parathyroid hormone receptor","Parathyroid hormone receptor","membrane receptor  7tm2  peptide  parathyroid hormone receptor","A parathyroid hormone receptor subtype that recognizes both PARATHYROID HORMONE and PARATHYROID HORMONE-RELATED PROTEIN. It is a G-protein-coupled receptor that is expressed at high levels in BONE and in KIDNEY. [MESH:D044168]",4
"Peptide growth factor receptor (family A GPCR)","Peptide growth factor","membrane receptor  7tm1  peptide  peptide growth factor",NULL,4
"Phosphodiesterase 10A",PDE_10A,"enzyme  phosphodiesterase  pde_10  pde_10a",NULL,4
"Phosphodiesterase 11A",PDE_11A,"enzyme  phosphodiesterase  pde_11  pde_11a",NULL,4
"Phosphodiesterase 1A",PDE_1A,"enzyme  phosphodiesterase  pde_1  pde_1a",NULL,4
"Phosphodiesterase 1B",PDE_1B,"enzyme  phosphodiesterase  pde_1  pde_1b",NULL,4
"Phosphodiesterase 1C",PDE_1C,"enzyme  phosphodiesterase  pde_1  pde_1c",NULL,4
"Phosphodiesterase 2A",PDE_2A,"enzyme  phosphodiesterase  pde_2  pde_2a",NULL,4
"Phosphodiesterase 3A",PDE_3A,"enzyme  phosphodiesterase  pde_3  pde_3a",NULL,4
"Phosphodiesterase 3B",PDE_3B,"enzyme  phosphodiesterase  pde_3  pde_3b",NULL,4
"Phosphodiesterase 4A",PDE_4A,"enzyme  phosphodiesterase  pde_4  pde_4a",NULL,4
"Phosphodiesterase 4B",PDE_4B,"enzyme  phosphodiesterase  pde_4  pde_4b",NULL,4
"Phosphodiesterase 4C",PDE_4C,"enzyme  phosphodiesterase  pde_4  pde_4c",NULL,4
"Phosphodiesterase 4D",PDE_4D,"enzyme  phosphodiesterase  pde_4  pde_4d",NULL,4
"Phosphodiesterase 5A",PDE_5A,"enzyme  phosphodiesterase  pde_5  pde_5a",NULL,4
"Phosphodiesterase 6A",PDE_6A,"enzyme  phosphodiesterase  pde_6  pde_6a",NULL,4
"Phosphodiesterase 6B",PDE_6B,"enzyme  phosphodiesterase  pde_6  pde_6b",NULL,4
"Phosphodiesterase 6C",PDE_6C,"enzyme  phosphodiesterase  pde_6  pde_6c",NULL,4
"Phosphodiesterase 6D",PDE_6D,"enzyme  phosphodiesterase  pde_6  pde_6d",NULL,4
"Phosphodiesterase 6G",PDE_6G,"enzyme  phosphodiesterase  pde_6  pde_6g",NULL,4
"Phosphodiesterase 6H",PDE_6H,"enzyme  phosphodiesterase  pde_6  pde_6h",NULL,4
"Phosphodiesterase 7A",PDE_7A,"enzyme  phosphodiesterase  pde_7  pde_7a",NULL,4
"Phosphodiesterase 7B",PDE_7B,"enzyme  phosphodiesterase  pde_7  pde_7b",NULL,4
"Phosphodiesterase 8A",PDE_8A,"enzyme  phosphodiesterase  pde_8  pde_8a",NULL,4
"Phosphodiesterase 8B",PDE_8B,"enzyme  phosphodiesterase  pde_8  pde_8b",NULL,4
"Phosphodiesterase 9A",PDE_9A,"enzyme  phosphodiesterase  pde_9  pde_9a",NULL,4
"Phospholipid-transporting ATPase","Phospholipid ATPase","transporter  ntpase  p-type atpase  phospholipid atpase",NULL,4
"Plasmolipin family",PLASMOLIPIN,"ion channel  other  misc  plasmolipin",NULL,4
"PR domain",PRDM,"epigenetic regulator  writer  pmt  prdm",NULL,4
"Presenilin ER Ca2+ leak channel family",PRESENILIN,"ion channel  other  misc  presenilin",NULL,4
"Probable cation-transporting ATPase (V subfamily)","cation ATPase","transporter  ntpase  p-type atpase  cation atpase",NULL,4
"Protease inhibitor unclassified clan",I-,"enzyme  protease  inhibitor  i-",NULL,4
"Protease unclassified U family",U-,"enzyme  protease  unknown  u-",NULL,4
"Protease-activated receptor","Protease-activated receptor","membrane receptor  7tm1  peptide  protease-activated receptor","A class of receptors that are activated by the action of PROTEINASES. The most notable examples are the THROMBIN RECEPTORS. The receptors contain cryptic ligands that are exposed upon the selective proteolysis of specific N-terminal cleavage sites. [MESH:D044462]",4
"Protein arginine methyltransferase",PRMT,"epigenetic regulator  writer  pmt  prmt",NULL,4
"Protein phosphatase regulatory subunit",Reg,"enzyme  phosphatase  protein phosphatase  reg",NULL,4
"PWWP domain",PWWP,"epigenetic regulator  reader  methyl-lysine  pwwp",NULL,4
"Receptor guanylate cyclase",Rgc,"enzyme  lyase  guanylate cyclase  receptor guanylate cyclase","A class of cellular membrane receptors that either have an intrinsic guanylate cyclase activity or are closely coupled to specific guanylate cyclases within the cell. [MESH:D050705]",4
"Relaxin-like peptide receptor (family A GPCR)","Relaxin-like peptide","membrane receptor  7tm1  peptide  relaxin-like peptide",NULL,4
Rhodopsin,Rhodopsin,"membrane receptor  7tm1  opsin  rhodopsin",NULL,4
"Serine protease PA clan",PAS,"enzyme  protease  serine  pas",NULL,4
"Serine protease SB clan",SB,"enzyme  protease  serine  sb",NULL,4
"Serine protease SC clan",SC,"enzyme  protease  serine  sc",NULL,4
"Serine protease SE clan",SE,"enzyme  protease  serine  se",NULL,4
"Serine protease SF clan",SF,"enzyme  protease  serine  sf",NULL,4
"Serine protease SH clan",SH,"enzyme  protease  serine  sh",NULL,4
"Serine protease SJ clan",SJ,"enzyme  protease  serine  sj",NULL,4
"Serine protease SK clan",SK,"enzyme  protease  serine  sk",NULL,4
"Serine protease SO clan",SO,"enzyme  protease  serine  so",NULL,4
"Serine protease SP clan",SP,"enzyme  protease  serine  sp",NULL,4
"Serine protease SR clan",SR,"enzyme  protease  serine  sr",NULL,4
"Serine protease SS clan",SS,"enzyme  protease  serine  ss",NULL,4
"Serine protease ST clan",ST,"enzyme  protease  serine  st",NULL,4
"Serine protease unclassified",Unclassified,"enzyme  protease  serine  unclassified",NULL,4
"Serine protein phosphatase",Ser,"enzyme  phosphatase  protein phosphatase  ser",NULL,4
"Serine/threonine protein phosphatase",Ser_Thr,"enzyme  phosphatase  protein phosphatase  ser_thr","A group of enzymes removing the SERINE- or THREONINE-bound phosphate groups from a wide range of phosphoproteins, including a number of enzymes which have been phosphorylated under the action of a kinase. (Enzyme Nomenclature, 1992) [MESH:D010749]",4
"Serine/threonine/tyrosine protein phosphatase",Ser_Thr_Tyr,"enzyme  phosphatase  protein phosphatase  ser_thr_tyr","A sub-class of protein tyrosine phosphatases that contain an additional phosphatase activity which cleaves phosphate ester bonds on SERINE or THREONINE residues that are located on the same protein. [MESH:D054637]",4
"SET domain",SET,"epigenetic regulator  writer  pmt  set",NULL,4
"Short peptide receptor (family A GPCR)","Short Peptide","membrane receptor  7tm1  peptide  short peptide",NULL,4
"SLC01 family of amino acid transporters",SLC01,"transporter  electrochemical  slc  slc01",NULL,4
"SLC02 family of hexose and sugar alcohol transporters",SLC02,"transporter  electrochemical  slc  slc02",NULL,4
"SLC03 and SLC07 families of heteromeric amino acid transporters (HATs)","SLC03 and SLC07","transporter  electrochemical  slc  slc03 and slc07",NULL,4
"SLC04 family of bicarbonate transporters",SLC04,"transporter  electrochemical  slc  slc04",NULL,4
"SLC05 family of sodium-dependent glucose transporters",SLC05,"transporter  electrochemical  slc  slc05",NULL,4
"SLC06 neurotransmitter transporter family",SLC06,"transporter  electrochemical  slc  slc06",NULL,4
"SLC08 family of sodium/calcium exchangers",SLC08,"transporter  electrochemical  slc  slc08",NULL,4
"SLC09 family of sodium/hydrogen exchangers",SLC09,"transporter  electrochemical  slc  slc09",NULL,4
"SLC10 family of sodium-bile acid co-transporters",SLC10,"transporter  electrochemical  slc  slc10",NULL,4
"SLC11 family of proton-coupled metal ion transporters",SLC11,"transporter  electrochemical  slc  slc11",NULL,4
"SLC12 family of cation-coupled chloride transporters",SLC12,"transporter  electrochemical  slc  slc12",NULL,4
"SLC13 family of sodium-dependent sulphate/carboxylate transporters",SLC13,"transporter  electrochemical  slc  slc13",NULL,4
"SLC14 family of facilitative urea transporters",SLC14,"transporter  electrochemical  slc  slc14",NULL,4
"SLC15 family of peptide transporters",SLC15,"transporter  electrochemical  slc  slc15",NULL,4
"SLC16 family of monocarboxylate transporters",SLC16,"transporter  electrochemical  slc  slc16",NULL,4
"SLC17 phosphate and organic anion transporter family",SLC17,"transporter  electrochemical  slc  slc17",NULL,4
"SLC18 family of vesicular amine transporters",SLC18,"transporter  electrochemical  slc  slc18",NULL,4
"SLC19 family of vitamin transporters",SLC19,"transporter  electrochemical  slc  slc19",NULL,4
"SLC20 family of sodium-dependent phosphate transporters",SLC20,"transporter  electrochemical  slc  slc20",NULL,4
"SLC21/SLCO family of organic anion transporting polypeptides",SLC21,"transporter  electrochemical  slc  slc21",NULL,4
"SLC22 family of organic cation and anion transporters",SLC22,"transporter  electrochemical  slc  slc22",NULL,4
"SLC23 family of ascorbic acid transporters",SLC23,"transporter  electrochemical  slc  slc23",NULL,4
"SLC24 family of sodium/potassium/calcium exchangers",SLC24,"transporter  electrochemical  slc  slc24",NULL,4
"SLC25 family of mitochondrial transporters",SLC25,"transporter  electrochemical  slc  slc25",NULL,4
"SLC26 family of anion exchangers",SLC26,"transporter  electrochemical  slc  slc26",NULL,4
"SLC27 family of fatty acid transporters",SLC27,"transporter  electrochemical  slc  slc27",NULL,4
"SLC28 and SLC29 families of nucleoside transporters","SLC28 and SLC29","transporter  electrochemical  slc  slc28 and slc29",NULL,4
"SLC30 zinc transporter family",SLC30,"transporter  electrochemical  slc  slc30",NULL,4
"SLC31 family of copper transporters",SLC31,"transporter  electrochemical  slc  slc31",NULL,4
"SLC32 vesicular inhibitory amino acid transporter",SLC32,"transporter  electrochemical  slc  slc32",NULL,4
"SLC33 acetylCoA transporter",SLC33,"transporter  electrochemical  slc  slc33",NULL,4
"SLC34 family of sodium phosphate co-transporters",SLC34,"transporter  electrochemical  slc  slc34",NULL,4
"SLC35 family of nucleotide sugar transporters",SLC35,"transporter  electrochemical  slc  slc35",NULL,4
"SLC36 family of proton-coupled amino acid transporters",SLC36,"transporter  electrochemical  slc  slc36",NULL,4
"SLC37 family of phosphosugar/phosphate exchangers",SLC37,"transporter  electrochemical  slc  slc37",NULL,4
"SLC38 family of sodium-dependent neutral amino acid transporters",SLC38,"transporter  electrochemical  slc  slc38",NULL,4
"SLC39 family of metal ion transporters",SLC39,"transporter  electrochemical  slc  slc39",NULL,4
"SLC40 iron transporter",SLC40,"transporter  electrochemical  slc  slc40",NULL,4
"SLC41 family of divalent cation transporters",SLC41,"transporter  electrochemical  slc  slc41",NULL,4
"SLC42 Rh ammonium transporter",SLC42,"transporter  electrochemical  slc  slc42",NULL,4
"SLC43 family of large neutral amino acid transporters",SLC43,"transporter  electrochemical  slc  slc43",NULL,4
"SLC44 choline transporter-like family",SLC44,"transporter  electrochemical  slc  slc44",NULL,4
"SLC45 family of putative sugar transporters",SLC45,"transporter  electrochemical  slc  slc45",NULL,4
"SLC46 family of folate transporters",SLC46,"transporter  electrochemical  slc  slc46",NULL,4
"SLC47 family of multidrug and toxin extrusion transporters",SLC47,"transporter  electrochemical  slc  slc47",NULL,4
"SLC48 haem transporter",SLC48,"transporter  electrochemical  slc  slc48",NULL,4
"SLC49 family of FLVCR-related haem transporters",SLC49,"transporter  electrochemical  slc  slc49",NULL,4
"SLC50 sugar transporter",SLC50,"transporter  electrochemical  slc  slc50",NULL,4
"SLC51 family of steroid-derived molecule transporters",SLC51,"transporter  electrochemical  slc  slc51",NULL,4
"SLC52 family of riboflavin transporters",SLC52,"transporter  electrochemical  slc  slc52",NULL,4
"Sodium leak channel, non-selective",SODIUM-LEAK,"ion channel  other  misc  sodium-leak",NULL,4
"Sodium potassium ATPase","Na K ATPase","transporter  ntpase  p-type atpase  na k atpase",NULL,4
"Soluble guanylate cyclase",Sgc,"enzyme  lyase  guanylate cyclase  soluble guanylate cyclase",NULL,4
"SRC family",SRC,"epigenetic regulator  writer  hat  src",NULL,4
"STE protein kinase group",Ste,"enzyme  kinase  protein kinase  ste",NULL,4
"Synaptic vesicle-associated Ca2+ channel flower family",FLOWER,"ion channel  other  misc  flower",NULL,4
"Testis-enhanced gene transfer family",TEGT,"ion channel  other  misc  tegt",NULL,4
"Threonine protease PBT clan",PBT,"enzyme  protease  threonine  pbt",NULL,4
"TK protein kinase group",Tk,"enzyme  kinase  protein kinase  tk","Protein kinases that catalyze the PHOSPHORYLATION of TYROSINE residues in proteins with ATP or other nucleotides as phosphate donors. [MESH:D011505]",4
"TKL protein kinase group",Tkl,"enzyme  kinase  protein kinase  tkl",NULL,4
"Tudor domain",TUDOR,"epigenetic regulator  reader  methyl-lysine  tudor",NULL,4
"Two-pore domain potassium channel",K2P,"ion channel  vgc  k  k2p",NULL,4
"Type A influenza virus matrix-2 channel family",M2-C,"ion channel  other  misc  m2-c",NULL,4
"Tyrosine protein phosphatase",Tyr,"enzyme  phosphatase  protein phosphatase  tyr",NULL,4
"Unorthodox aquaporin",UNORTHODOX,"ion channel  other  aquaporin  unorthodox",NULL,4
"V-type ATPase","V-type ATPase","transporter  ntpase  f-type and v-type  v-type atpase",NULL,4
"Vasoactive intestinal peptide receptor","Vasoactive intestinal peptide receptor","membrane receptor  7tm2  peptide  vasoactive intestinal peptide receptor","Cell surface proteins that bind VASOACTIVE INTESTINAL PEPTIDE; (VIP); with high affinity and trigger intracellular changes which influence the behavior of cells. [MESH:D018005]",4
"Voltage-dependent anion-selective channel",VDAC,"ion channel  other  mpp  vdac",NULL,4
"Voltage-gated potassium channel","VG K","ion channel  vgc  k  vg k","Potassium channel whose permeability to ions is extremely sensitive to the transmembrane potential difference. The opening of these channels is induced by the membrane depolarization of the ACTION POTENTIAL. [MESH:D024642]",4
"Water-specific aquaporin",WATER-SPECIFIC,"ion channel  other  aquaporin  water-specific",NULL,4
"WDR domain",WDR,"epigenetic regulator  reader  methyl-lysine  wdr",NULL,4
"Acetylcholine receptor","Acetylcholine receptor","membrane receptor  7tm1  smallmol  monoamine receptor  acetylcholine receptor","Cell surface proteins that bind acetylcholine with high affinity and trigger intracellular changes influencing the behavior of cells. Cholinergic receptors are divided into two major classes, muscarinic and nicotinic, based originally on their affinity for nicotine and muscarine. Each group is further subdivided based on pharmacology, location, mode of action, and/or molecular biology. [MESH:D011950]",5
"Adenosine receptor","Adenosine receptor","membrane receptor  7tm1  smallmol  nucleotide-like receptor  adenosine receptor","A class of cell surface receptors that prefer ADENOSINE to other endogenous PURINES. Purinergic P1 receptors are widespread in the body including the cardiovascular, respiratory, immune, and nervous systems. There are at least two pharmacologically distinguishable types (A1 and A2, or Ri and Ra). [MESH:D018047]",5
"Adrenergic receptor","Adrenergic receptor","membrane receptor  7tm1  smallmol  monoamine receptor  adrenergic receptor","Cell-surface proteins that bind epinephrine and/or norepinephrine with high affinity and trigger intracellular changes. The two major classes of adrenergic receptors, alpha and beta, were originally discriminated based on their cellular actions but now are distinguished by their relative affinity for characteristic synthetic ligands. Adrenergic receptors may also be classified according to the subtypes of G-proteins with which they bind; this scheme does not respect the alpha-beta distinction. [MESH:D011941]",5
"Adrenomedullin receptor","Adrenomedullin receptor","membrane receptor  7tm1  peptide  short peptide  adrenomedullin receptor","G-protein-coupled cell surface receptors for ADRENOMEDULLIN. They are formed by the heterodimerization of CALCITONIN RECEPTOR-LIKE PROTEIN and either RECEPTOR ACTIVITY-MODIFYING PROTEIN 2 or RECEPTOR ACTIVITY-MODIFYING PROTEIN 3. [MESH:D058265]",5
"AGC protein kinase AKT family",Akt,"enzyme  kinase  protein kinase  agc  akt",NULL,5
"AGC protein kinase DMPK family",Dmpk,"enzyme  kinase  protein kinase  agc  dmpk",NULL,5
"AGC protein kinase GRK family",Grk,"enzyme  kinase  protein kinase  agc  grk","A family of serine-threonine kinases that are specific for G-PROTEIN-COUPLED RECEPTORS. They are regulatory proteins that play a role in G-protein-coupled receptor densensitization. [MESH:D054768]",5
"AGC protein kinase MAST family",Mast,"enzyme  kinase  protein kinase  agc  mast",NULL,5
"AGC protein kinase NDR family",Ndr,"enzyme  kinase  protein kinase  agc  ndr",NULL,5
"AGC protein kinase PDK1 subfamily",Pdk1,"enzyme  kinase  protein kinase  agc  pdk1",NULL,5
"AGC protein kinase PKA family",Pka,"enzyme  kinase  protein kinase  agc  pka","A group of enzymes that are dependent on CYCLIC AMP and catalyze the phosphorylation of SERINE or THREONINE residues on proteins. Included under this category are two cyclic-AMP-dependent protein kinase subtypes, each of which is defined by its subunit composition. [MESH:D017868]",5
"AGC protein kinase PKC family",Pkc,"enzyme  kinase  protein kinase  agc  pkc","An serine-threonine protein kinase that requires the presence of physiological concentrations of CALCIUM and membrane PHOSPHOLIPIDS. The additional presence of DIACYLGLYCEROLS markedly increases its sensitivity to both calcium and phospholipids. The sensitivity of the enzyme can also be increased by PHORBOL ESTERS and it is believed that protein kinase C is the receptor protein of tumor-promoting phorbol esters. [MESH:D011493]",5
"AGC protein kinase PKG family",Pkg,"enzyme  kinase  protein kinase  agc  pkg","A group of enzymes that are dependent on cyclic GMP and catalyzes the phosphorylation of serine or threonine residues of proteins. [MESH:D017869]",5
"AGC protein kinase PKN family",Pkn,"enzyme  kinase  protein kinase  agc  pkn",NULL,5
"AGC protein kinase RSK family",Rsk,"enzyme  kinase  protein kinase  agc  rsk","A family of protein serine/threonine kinases which act as intracellular signalling intermediates. Ribosomal protein S6 kinases are activated through phosphorylation in response to a variety of HORMONES and INTERCELLULAR SIGNALING PEPTIDES AND PROTEINS. Phosphorylation of RIBOSOMAL PROTEIN S6 by enzymes in this class results in increased expression of 5' top MRNAs. Although specific for RIBOSOMAL PROTEIN S6 members of this class of kinases can act on a number of substrates within the cell. The immunosuppressant SIROLIMUS inhibits the activation of ribosomal protein S6 kinases. [MESH:D019893]",5
"AGC protein kinase SGK family",Sgk,"enzyme  kinase  protein kinase  agc  sgk",NULL,5
"AGC protein kinase YANK family",Yank,"enzyme  kinase  protein kinase  agc  yank",NULL,5
"Anaphylatoxin receptor",Anaphylatoxin,"membrane receptor  7tm1  peptide  anaphylatoxin receptor  anaphylatoxin",NULL,5
"Angiotensin receptor","Angiotensin receptor","membrane receptor  7tm1  peptide  short peptide  angiotensin receptor","Cell surface proteins that bind ANGIOTENSINS and trigger intracellular changes influencing the behavior of cells. [MESH:D011945]",5
"Aspartic protease A1A subfamily",A1A,"enzyme  protease  aspartic  aa  a1a","Formed from pig pepsinogen by cleavage of one peptide bond. The enzyme is a single polypeptide chain and is inhibited by methyl 2-diaazoacetamidohexanoate. It cleaves peptides preferentially at the carbonyl linkages of phenylalanine or leucine and acts as the principal digestive enzyme of gastric juice. [MESH:D010434]",5
"Aspartic protease A22A subfamily",A22A,"enzyme  protease  aspartic  ad  a22a","Integral membrane proteins and essential components of the gamma-secretase complex that catalyzes the cleavage of membrane proteins such as NOTCH RECEPTORS and AMYLOID BETA-PEPTIDES precursors. Mutations of presenilins lead to presenile ALZHEIMER DISEASE with onset before age 65 years. [MESH:D053763]",5
"Aspartic protease A26 family",A26,"enzyme  protease  aspartic  af  a26",NULL,5
"Aspartic protease A2A subfamily",A2A,"enzyme  protease  aspartic  aa  a2a",NULL,5
"Atypical protein kinase ABC1 family",Abc1,"enzyme  kinase  protein kinase  atypical  abc1",NULL,5
"Atypical protein kinase alpha family",Alpha,"enzyme  kinase  protein kinase  atypical  alpha",NULL,5
"Atypical protein kinase BCR family",Bcr,"enzyme  kinase  protein kinase  atypical  bcr","Proto-oncogene protein bcr is a serine-threonine kinase that functions as a negative regulator of CELL PROLIFERATION and NEOPLASTIC CELL TRANSFORMATION. It is commonly fused with cellular abl protein to form BCR-ABL FUSION PROTEINS in PHILADELPHIA CHROMOSOME positive LEUKEMIA patients. [MESH:D051562]",5
"Atypical protein kinase PDHK subfamily",Pdhk,"enzyme  kinase  protein kinase  atypical  pdhk",NULL,5
"Atypical protein kinase PIKK family",Pikk,"enzyme  kinase  protein kinase  atypical  pikk",NULL,5
"Atypical protein kinase RIO family",Rio,"enzyme  kinase  protein kinase  atypical  rio",NULL,5
"Bradykinin receptor","Bradykinin receptor","membrane receptor  7tm1  peptide  short peptide  bradykinin receptor","Cell surface receptors that bind BRADYKININ and related KININS with high affinity and trigger intracellular changes which influence the behavior of cells. The identified receptor types (B-1 and B-2, or BK-1 and BK-2) recognize endogenous KALLIDIN; t-kinins; and certain bradykinin fragments as well as bradykinin itself. [MESH:D018002]",5
"Calcitonin gene-related peptide receptor","Calcitonin gene-related peptide receptor","membrane receptor  7tm2  peptide  calcitonin-like  calcitonin gene-related peptide receptor","Cell surface proteins that bind CALCITONIN GENE-RELATED PEPTIDE with high affinity and trigger intracellular changes which influence the behavior of cells. CGRP receptors are present in both the CENTRAL NERVOUS SYSTEM and the periphery. They are formed via the heterodimerization of the CALCITONIN RECEPTOR-LIKE PROTEIN and RECEPTOR ACTIVITY-MODIFYING PROTEIN 1. [MESH:D018015]",5
"Calcitonin receptor","Calcitonin receptor","membrane receptor  7tm2  peptide  calcitonin-like  calcitonin receptor","Cell surface proteins that bind calcitonin and trigger intracellular changes which influence the behavior of cells. Calcitonin receptors outside the nervous system mediate the role of calcitonin in calcium homeostasis. The role of calcitonin receptors in the brain is not well understood. [MESH:D018003]",5
"Calcium sensing receptor","Calcium sensing receptor","membrane receptor  7tm3  ion  calcium sensing receptor  calcium sensing receptor","A class of G-protein-coupled receptors that react to varying extracellular CALCIUM levels. Calcium-sensing receptors in the PARATHYROID GLANDS play an important role in the maintenance of calcium HOMEOSTASIS by regulating the release of PARATHYROID HORMONE. They differ from INTRACELLULAR CALCIUM-SENSING PROTEINS which sense intracellular calcium levels. [MESH:D044169]",5
"CAMK protein kinase CAMK1 family",Camkl,"enzyme  kinase  protein kinase  camk  camkl","A monomeric calcium-calmodulin-dependent protein kinase subtype that is expressed in a broad variety of mammalian cell types. Its expression is regulated by the action of CALCIUM-CALMODULIN-DEPENDENT PROTEIN KINASE KINASE. Several isoforms of this enzyme subtype are encoded by distinct genes. [MESH:D054729]",5
"CAMK protein kinase CAMK2 family",Camk2,"enzyme  kinase  protein kinase  camk  camk2","A multifunctional calcium-calmodulin-dependent protein kinase subtype that occurs as an oligomeric protein comprised of twelve subunits. It differs from other enzyme subtypes in that it lacks a phosphorylatable activation domain that can respond to CALCIUM-CALMODULIN-DEPENDENT PROTEIN KINASE KINASE. [MESH:D054732]",5
"CAMK protein kinase DAPK family",Dapk,"enzyme  kinase  protein kinase  camk  dapk",NULL,5
"CAMK protein kinase DCAMK1 family",Dcamkl,"enzyme  kinase  protein kinase  camk  dcamkl",NULL,5
"CAMK protein kinase MAPKAPK family",Mapkapk,"enzyme  kinase  protein kinase  camk  mapkapk",NULL,5
"CAMK protein kinase MLCK family",Mlck,"enzyme  kinase  protein kinase  camk  mlck","An enzyme that phosphorylates myosin light chains in the presence of ATP to yield myosin-light chain phosphate and ADP, and requires calcium and CALMODULIN. The 20-kDa light chain is phosphorylated more rapidly than any other acceptor, but light chains from other myosins and myosin itself can act as acceptors. The enzyme plays a central role in the regulation of smooth muscle contraction. [MESH:D009219]",5
"CAMK protein kinase PHk family",Phk,"enzyme  kinase  protein kinase  camk  phk","An enzyme that catalyzes the conversion of ATP and PHOSPHORYLASE B to ADP and PHOSPHORYLASE A. [MESH:D010764]",5
"CAMK protein kinase PIM family",Pim,"enzyme  kinase  protein kinase  camk  pim",NULL,5
"CAMK protein kinase PKD family",Pkd,"enzyme  kinase  protein kinase  camk  pkd",NULL,5
"CAMK protein kinase RAD53 family",Rad53,"enzyme  kinase  protein kinase  camk  rad53",NULL,5
"CAMK protein kinase RSKb family",Rskb,"enzyme  kinase  protein kinase  camk  rskb",NULL,5
"CAMK protein kinase TSSK family",Tssk,"enzyme  kinase  protein kinase  camk  tssk",NULL,5
"CAMK protein kinase unique family",Camk-Unique,"enzyme  kinase  protein kinase  camk  camk-unique",NULL,5
"Cannabinoid receptor","Cannabinoid receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  cannabinoid receptor","A class of G-protein-coupled receptors that are specific for CANNABINOIDS such as those derived from CANNABIS. They also bind a structurally distinct class of endogenous factors referred to as ENDOCANNABINOIDS. The receptor class may play a role in modulating the release of signaling molecules such as NEUROTRANSMITTERS and CYTOKINES. [MESH:D043882]",5
"CC chemokine receptor","CC chemokine receptor","membrane receptor  7tm1  peptide  chemokine receptor  cc chemokine receptor","Chemokine receptors that are specific for CC CHEMOKINES. [MESH:D054388]",5
"Chemerin receptor","Chemerin receptor","membrane receptor  7tm1  peptide  chemokine receptor-like  chemerin receptor",NULL,5
"Cholecystokinin receptor","Cholecystokinin receptor","membrane receptor  7tm1  peptide  short peptide  cholecystokinin receptor","Cell surface proteins that bind cholecystokinin (CCK) with high affinity and trigger intracellular changes influencing the behavior of cells. Cholecystokinin receptors are activated by GASTRIN as well as by CCK-4; CCK-8; and CCK-33. Activation of these receptors evokes secretion of AMYLASE by pancreatic acinar cells, acid and PEPSIN by stomach mucosal cells, and contraction of the PYLORUS and GALLBLADDER. The role of the widespread CCK receptors in the central nervous system is not well understood. [MESH:D011949]",5
"CK1 protein kinase CK1 family",Ck1,"enzyme  kinase  protein kinase  ck1  ck1","A casein kinase that was originally described as a monomeric enzyme with a molecular weight of 30-40 kDa. Several ISOENZYMES of casein kinase I have been found which are encoded by separate genes. Many of the casein kinase I isoenzymes have been shown to play distinctive roles in intracellular SIGNAL TRANSDUCTION. [MESH:D047389]",5
"CK1 protein kinase VRK family",VRK,"enzyme  kinase  protein kinase  ck1  vrk",NULL,5
"CMGC protein kinase CDK family",Cdk,"enzyme  kinase  protein kinase  cmgc  cdk","Protein kinases that control cell cycle progression in all eukaryotes and require physical association with CYCLINS to achieve full enzymatic activity. Cyclin-dependent kinases are regulated by phosphorylation and dephosphorylation events. [MESH:D018844]",5
"CMGC protein kinase CDKL family",Cdkl,"enzyme  kinase  protein kinase  cmgc  cdkl",NULL,5
"CMGC protein kinase CK subfamily",Ck,"enzyme  kinase  protein kinase  cmgc  ck",NULL,5
"CMGC protein kinase CLK family",Clk,"enzyme  kinase  protein kinase  cmgc  clk",NULL,5
"CMGC protein kinase DYRK family",Dyrk,"enzyme  kinase  protein kinase  cmgc  dyrk",NULL,5
"CMGC protein kinase GSK family",Gsk,"enzyme  kinase  protein kinase  cmgc  gsk","A class of protein-serine-threonine kinases that was originally found as one of the three types of kinases that phosphorylate GLYCOGEN SYNTHASE. Glycogen synthase kinases along with CA(2+)-CALMODULIN DEPENDENT PROTEIN KINASES and CYCLIC AMP-DEPENDENT PROTEIN KINASES regulate glycogen synthase activity. [MESH:D038341]",5
"CMGC protein kinase MAPK family",Mapk,"enzyme  kinase  protein kinase  cmgc  mapk","A superfamily of PROTEIN-SERINE-THREONINE KINASES that are activated by diverse stimuli via protein kinase cascades. They are the final components of the cascades, activated by phosphorylation by MITOGEN-ACTIVATED PROTEIN KINASE KINASES, which in turn are activated by mitogen-activated protein kinase kinase kinases (MAP KINASE KINASE KINASES). [MESH:D020928]",5
"CMGC protein kinase RCK family",Rck,"enzyme  kinase  protein kinase  cmgc  rck",NULL,5
"CMGC protein kinase SRPK family",Srpk,"enzyme  kinase  protein kinase  cmgc  srpk",NULL,5
"Corticotropin releasing factor receptor","Corticotropin releasing factor receptor","membrane receptor  7tm2  peptide  corticotropin releasing factor receptor  corticotropin releasing factor receptor","Cell surface proteins that bind corticotropin-releasing hormone with high affinity and trigger intracellular changes which influence the behavior of cells. The corticotropin releasing-hormone receptors on anterior pituitary cells mediate the stimulation of corticotropin release by hypothalamic corticotropin releasing factor. The physiological consequence of activating corticotropin-releasing hormone receptors on central neurons is not well understood. [MESH:D018019]",5
"CX3C chemokine receptor","CX3C chemokine receptor","membrane receptor  7tm1  peptide  chemokine receptor  cx3c chemokine receptor",NULL,5
"CXC chemokine receptor","CXC chemokine receptor","membrane receptor  7tm1  peptide  chemokine receptor  cxc chemokine receptor","Chemokine receptors that are specific for CXC CHEMOKINES. [MESH:D054387]",5
"Cysteine protease C1 family",C1,"enzyme  protease  cysteine  ca  c1",NULL,5
"Cysteine protease C11 family",C11,"enzyme  protease  cysteine  cd  c11",NULL,5
"Cysteine protease C12 family",C12,"enzyme  protease  cysteine  ca  c12","A thioester hydrolase which acts on esters formed between thiols such as DITHIOTHREITOL or GLUTATHIONE and the C-terminal glycine residue of UBIQUITIN. [MESH:D043222]",5
"Cysteine protease C13 family",C13,"enzyme  protease  cysteine  cd  c13",NULL,5
"Cysteine protease C14 family",C14,"enzyme  protease  cysteine  cd  c14","A family of intracellular CYSTEINE ENDOPEPTIDASES that play a role in regulating INFLAMMATION and APOPTOSIS. They specifically cleave peptides at a CYSTEINE amino acid that follows an ASPARTIC ACID residue. Caspases are activated by proteolytic cleavage of a precursor form to yield large and small subunits that form the enzyme. Since the cleavage site within precursors matches the specificity of caspases, sequential activation of precursors by activated caspases can occur. [MESH:D020169]",5
"Cysteine protease C18 family",C18,"enzyme  protease  cysteine  cm  c18",NULL,5
"Cysteine protease C19 family",C19,"enzyme  protease  cysteine  ca  c19",NULL,5
"Cysteine protease C1A family",C1A,"enzyme  protease  cysteine  ca  c1a","A proteolytic enzyme obtained from Carica papaya. It is also the name used for a purified mixture of papain and CHYMOPAPAIN that is used as a topical enzymatic debriding agent. EC 3.4.22.2. [MESH:D010206]",5
"Cysteine protease C2 family",C2,"enzyme  protease  cysteine  ca  c2","Cysteine proteinase found in many tissues. Hydrolyzes a variety of endogenous proteins including NEUROPEPTIDES; CYTOSKELETAL PROTEINS; proteins from SMOOTH MUSCLE; CARDIAC MUSCLE; liver; platelets; and erythrocytes. Two subclasses having high and low calcium sensitivity are known. Removes Z-discs and M-lines from myofibrils. Activates phosphorylase kinase and cyclic nucleotide-independent protein kinase. This enzyme was formerly listed as EC 3.4.22.4. [MESH:D002154]",5
"Cysteine protease C25 family",C25,"enzyme  protease  cysteine  cd  c25",NULL,5
"Cysteine protease C26 family",C26,"enzyme  protease  cysteine  pcc  c26","Catalyzes the hydrolysis of pteroylpolyglutamic acids in gamma linkage to pterolylmonoglutamic acid and free glutamic acid. EC 3.4.19.9. [MESH:D011623]",5
"Cysteine protease C2A subfamily",C2A,"enzyme  protease  cysteine  ca  c2a","Cysteine proteinase found in many tissues. Hydrolyzes a variety of endogenous proteins including NEUROPEPTIDES; CYTOSKELETAL PROTEINS; proteins from SMOOTH MUSCLE; CARDIAC MUSCLE; liver; platelets; and erythrocytes. Two subclasses having high and low calcium sensitivity are known. Removes Z-discs and M-lines from myofibrils. Activates phosphorylase kinase and cyclic nucleotide-independent protein kinase. This enzyme was formerly listed as EC 3.4.22.4. [MESH:D002154]",5
"Cysteine protease C3A subfamily",C3A,"enzyme  protease  cysteine  pac  c3a",NULL,5
"Cysteine protease C48 family",C48,"enzyme  protease  cysteine  ce  c48",NULL,5
"Cytochrome P450 11A1",CYP_11A1,"enzyme  cytochrome p450  cyp_11  cyp_11a  cyp_11a1","A mitochondrial cytochrome P450 enzyme that catalyzes the side-chain cleavage of C27 cholesterol to C21 pregnenolone in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP11A1 gene, catalyzes the breakage between C20 and C22 which is the initial and rate-limiting step in the biosynthesis of various gonadal and adrenal steroid hormones. [MESH:D002786]",5
"Cytochrome P450 11B1",CYP_11B1,"enzyme  cytochrome p450  cyp_11  cyp_11b  cyp_11b1","A mitochondrial cytochrome P450 enzyme that catalyzes the 11-beta-hydroxylation of steroids in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP11B1 gene, is important in the synthesis of CORTICOSTERONE and HYDROCORTISONE. Defects in CYP11B1 cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL). [MESH:D013252]",5
"Cytochrome P450 11B2",CYP_11B2,"enzyme  cytochrome p450  cyp_11  cyp_11b  cyp_11b2","A mitochondrial cytochrome P450 enzyme that catalyzes the 18-hydroxylation of steroids in the presence of molecular oxygen and NADPH-specific flavoprotein. This enzyme, encoded by CYP11B2 gene, is important in the conversion of CORTICOSTERONE to 18-hydroxycorticosterone and the subsequent conversion to ALDOSTERONE. [MESH:D019405]",5
"Cytochrome P450 17A1",CYP_17A1,"enzyme  cytochrome p450  cyp_17  cyp_17a  cyp_17a1","A microsomal cytochrome P450 enzyme that catalyzes the 17-alpha-hydroxylation of progesterone or pregnenolone and subsequent cleavage of the residual two carbons at C17 in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP17 gene, generates precursors for glucocorticoid, androgen, and estrogen synthesis. Defects in CYP17 gene cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL) and abnormal sexual differentiation. [MESH:D013254]",5
"Cytochrome P450 19A1",CYP_19A1,"enzyme  cytochrome p450  cyp_19  cyp_19a  cyp_19a1","An enzyme that catalyzes the desaturation (aromatization) of the ring A of C19 androgens and converts them to C18 estrogens. In this process, the 19-methyl is removed. This enzyme is membrane-bound, located in the endoplasmic reticulum of estrogen-producing cells of ovaries, placenta, testes, adipose, and brain tissues. Aromatase is encoded by the CYP19 gene, and functions in complex with NADPH-FERRIHEMOPROTEIN REDUCTASE in the cytochrome P-450 system. [MESH:D001141]",5
"Cytochrome P450 1A1",CYP_1A1,"enzyme  cytochrome p450  cyp_1  cyp_1a  cyp_1a1","A liver microsomal cytochrome P-450 monooxygenase capable of biotransforming xenobiotics such as polycyclic hydrocarbons and halogenated aromatic hydrocarbons into carcinogenic or mutagenic compounds. They have been found in mammals and fish. This enzyme, encoded by CYP1A1 gene, can be measured by using ethoxyresorufin as a substrate for the ethoxyresorufin O-deethylase activity. [MESH:D019363]",5
"Cytochrome P450 1A2",CYP_1A2,"enzyme  cytochrome p450  cyp_1  cyp_1a  cyp_1a2","A cytochrome P-450 monooxygenase that can be induced by polycyclic aromatic xenobiotics in the liver of human and several animal species. This enzyme is of significant clinical interest due to the large number of drug interactions associated with its induction and its metabolism of THEOPHYLLINE. Caffeine is considered to be a model substrate for this enzyme. CYP1A2 activity can also be increased by environmental factors such as cigarette smoking, charbroiled meat, cruciferous vegetables, and a number of drugs including phenytoin, phenobarbital, and omeprazole. [MESH:D019388]",5
"Cytochrome P450 1B1",CYP_1B1,"enzyme  cytochrome p450  cyp_1  cyp_1b  cyp_1b1",NULL,5
"Cytochrome P450 21A2",CYP_21A2,"enzyme  cytochrome p450  cyp_21  cyp_21a  cyp_21a2","An adrenal microsomal cytochrome P450 enzyme that catalyzes the 21-hydroxylation of steroids in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP21 gene, converts progesterones to precursors of adrenal steroid hormones (CORTICOSTERONE; HYDROCORTISONE). Defects in CYP21 cause congenital adrenal hyperplasia (ADRENAL HYPERPLASIA, CONGENITAL). [MESH:D013255]",5
"Cytochrome P450 24A1",CYP_24A1,"enzyme  cytochrome p450  cyp_24  cyp_24a  cyp_24a1",NULL,5
"Cytochrome P450 26A1",CYP_26A1,"enzyme  cytochrome p450  cyp_26  cyp_26a  cyp_26a1",NULL,5
"Cytochrome P450 27A1",CYP_27A1,"enzyme  cytochrome p450  cyp_27  cyp_27a  cyp_27a1",NULL,5
"Cytochrome P450 27B1",CYP_27B1,"enzyme  cytochrome p450  cyp_27  cyp_27a  cyp_27b1",NULL,5
"Cytochrome P450 2A2",CYP_2A2,"enzyme  cytochrome p450  cyp_2  cyp_2a  cyp_2a2",NULL,5
"Cytochrome P450 2A5",CYP_2A5,"enzyme  cytochrome p450  cyp_2  cyp_2a  cyp_2a5",NULL,5
"Cytochrome P450 2A6",CYP_2A6,"enzyme  cytochrome p450  cyp_2  cyp_2a  cyp_2a6",NULL,5
"Cytochrome P450 2B1",CYP_2B1,"enzyme  cytochrome p450  cyp_2  cyp_2b  cyp_2b1","A major cytochrome P-450 enzyme which is inducible by PHENOBARBITAL in both the LIVER and SMALL INTESTINE. It is active in the metabolism of compounds like pentoxyresorufin, TESTOSTERONE, and ANDROSTENEDIONE. This enzyme, encoded by CYP2B1 gene, also mediates the activation of CYCLOPHOSPHAMIDE and IFOSFAMIDE to MUTAGENS. [MESH:D019362]",5
"Cytochrome P450 2B10",CYP_2B10,"enzyme  cytochrome p450  cyp_2  cyp_2b  cyp_2b10",NULL,5
"Cytochrome P450 2B11",CYP_2B11,"enzyme  cytochrome p450  cyp_2  cyp_2b  cyp_2b11",NULL,5
"Cytochrome P450 2B4",CYP_2B4,"enzyme  cytochrome p450  cyp_2  cyp_2b  cyp_2b4",NULL,5
"Cytochrome P450 2B6",CYP_2B6,"enzyme  cytochrome p450  cyp_2  cyp_2b  cyp_2b6",NULL,5
"Cytochrome P450 2C11",CYP_2C11,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c11",NULL,5
"Cytochrome P450 2C18",CYP_2C18,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c18",NULL,5
"Cytochrome P450 2C19",CYP_2C19,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c19",NULL,5
"Cytochrome P450 2C23",CYP_2C23,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c23",NULL,5
"Cytochrome P450 2C5",CYP_2C5,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c5",NULL,5
"Cytochrome P450 2C6",CYP_2C6,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c6",NULL,5
"Cytochrome P450 2C8",CYP_2C8,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c8",NULL,5
"Cytochrome P450 2C9",CYP_2C9,"enzyme  cytochrome p450  cyp_2  cyp_2c  cyp_2c9",NULL,5
"Cytochrome P450 2D1",CYP_2D1,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d1",NULL,5
"Cytochrome P450 2D15",CYP_2D15,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d15",NULL,5
"Cytochrome P450 2D18",CYP_2D18,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d18",NULL,5
"Cytochrome P450 2D2",CYP_2D2,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d2",NULL,5
"Cytochrome P450 2D3",CYP_2D3,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d3",NULL,5
"Cytochrome P450 2D4",CYP_2D4,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d4",NULL,5
"Cytochrome P450 2D6",CYP_2D6,"enzyme  cytochrome p450  cyp_2  cyp_2d  cyp_2d6","A cytochrome P450 enzyme that catalyzes the hydroxylation of many drugs and environmental chemicals, such as DEBRISOQUINE; ADRENERGIC RECEPTOR ANTAGONISTS; and TRICYCLIC ANTIDEPRESSANTS. This enzyme is deficient in up to 10 percent of the Caucasian population. [MESH:D019389]",5
"Cytochrome P450 2E1",CYP_2E1,"enzyme  cytochrome p450  cyp_2  cyp_2e  cyp_2e1","An ethanol-inducible cytochrome P450 enzyme that metabolizes several precarcinogens, drugs, and solvents to reactive metabolites. Substrates include alcohol; NITROSAMINES; BENZENE; URETHANE; and other low molecular weight compounds. CYP2E1 has been used as an enzyme marker in the study of alcohol abuse. [MESH:D019392]",5
"Cytochrome P450 3A1",CYP_3A1,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a1",NULL,5
"Cytochrome P450 3A11",CYP_3A11,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a11",NULL,5
"Cytochrome P450 3A12",CYP_3A12,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a12",NULL,5
"Cytochrome P450 3A2",CYP_3A2,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a2",NULL,5
"Cytochrome P450 3A4",CYP_3A4,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a4",NULL,5
"Cytochrome P450 3A5",CYP_3A5,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a5",NULL,5
"Cytochrome P450 3A6",CYP_3A6,"enzyme  cytochrome p450  cyp_3  cyp_3a  cyp_3a6",NULL,5
"Cytochrome P450 4A1",CYP_4A1,"enzyme  cytochrome p450  cyp_4  cyp_4a  cyp_4a1",NULL,5
"Cytochrome P450 4A11",CYP_4A11,"enzyme  cytochrome p450  cyp_4  cyp_4a  cyp_4a11",NULL,5
"Cytochrome P450 4A3",CYP_4A3,"enzyme  cytochrome p450  cyp_4  cyp_4a  cyp_4a3",NULL,5
"Cytochrome P450 4A4",CYP_4A4,"enzyme  cytochrome p450  cyp_4  cyp_4a  cyp_4a4",NULL,5
"Cytochrome P450 4F2",CYP_4F2,"enzyme  cytochrome p450  cyp_4  cyp_4f  cyp_4f2",NULL,5
"Cytochrome P450 4X1",CYP_4X1,"enzyme  cytochrome p450  cyp_4  cyp_4x  cyp_4x1",NULL,5
"Cytochrome P450 51A1",CYP_51A1,"enzyme  cytochrome p450  cyp_51  cyp_51a  cyp_51a1",NULL,5
"Cytochrome P450 5A1",CYP_5A1,"enzyme  cytochrome p450  cyp_5  cyp_5a  cyp_5a1","An enzyme found predominantly in platelet microsomes. It catalyzes the conversion of PGG(2) and PGH(2) (prostaglandin endoperoxides) to thromboxane A2. EC 5.3.99.5. [MESH:D013930]",5
"Cytochrome P450 7A1",CYP_7A1,"enzyme  cytochrome p450  cyp_7  cyp_7a  cyp_7a1","A membrane-bound cytochrome P450 enzyme that catalyzes the 7-alpha-hydroxylation of CHOLESTEROL in the presence of molecular oxygen and NADPH-FERRIHEMOPROTEIN REDUCTASE. This enzyme, encoded by CYP7, converts cholesterol to 7-alpha-hydroxycholesterol which is the first and rate-limiting step in the synthesis of BILE ACIDS. [MESH:D002790]",5
"Cytochrome P450 8A1",CYP_8A1,"enzyme  cytochrome p450  cyp_8  cyp_8a  cyp_8a1",NULL,5
"Dopamine receptor","Dopamine receptor","membrane receptor  7tm1  smallmol  monoamine receptor  dopamine receptor","Cell-surface proteins that bind dopamine with high affinity and trigger intracellular changes influencing the behavior of cells. [MESH:D011954]",5
"EDG receptor","EDG receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  edg receptor",NULL,5
"Endothelin receptor","Endothelin receptor","membrane receptor  7tm1  peptide  short peptide  endothelin receptor","Cell surface proteins that bind ENDOTHELINS with high affinity and trigger intracellular changes which influence the behavior of cells. [MESH:D017466]",5
"Free fatty acid receptor","Free fatty acid receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  free fatty acid receptor",NULL,5
"GABA-B receptor","GABA-B receptor","membrane receptor  7tm3  smallmol  neurotransmitter  gaba-b receptor","A subset of GABA RECEPTORS that signal through their interaction with HETEROTRIMERIC G-PROTEINS. [MESH:D018080]",5
"Galanin receptor","Galanin receptor","membrane receptor  7tm1  peptide  short peptide  galanin receptor","A family of G-protein-coupled receptors that are specific for GALANIN and galanin peptides. They are generally considered to be coupled to the GI, INHIBITORY G-PROTEIN to meditate the neurological effects of galanin. Several subtypes of galanin receptors occur with differing specificities for the full length galanin, galanin peptide fragments, and galanin-like peptide. [MESH:D044088]",5
"Gastric inhibitory polypeptide receptor","Gastric inhibitory polypeptide receptor","membrane receptor  7tm2  peptide  glucagon-like  gastric inhibitory polypeptide receptor",NULL,5
"Glucagon receptor","Glucagon receptor","membrane receptor  7tm2  peptide  glucagon-like  glucagon receptor","Cell surface receptors that bind glucagon with high affinity and trigger intracellular changes which influence the behavior of cells. Activation of glucagon receptors causes a variety of effects; the best understood is the initiation of a complex enzymatic cascade in the liver which ultimately increases the availability of glucose to body organs. [MESH:D018027]",5
"Glucagon-like peptide receptor","Glucagon-like peptide receptor","membrane receptor  7tm2  peptide  glucagon-like  glucagon-like peptide receptor",NULL,5
"Glycohormone receptor","Glycohormone receptor","membrane receptor  7tm1  peptide  glycohormone receptor  glycohormone receptor",NULL,5
"GnRH receptor","GnRH receptor","membrane receptor  7tm1  peptide  short peptide  gnrh receptor","Receptors with a 6-kDa protein on the surfaces of cells that secrete LUTEINIZING HORMONE or FOLLICLE STIMULATING HORMONE, usually in the adenohypophysis. LUTEINIZING HORMONE-RELEASING HORMONE binds to these receptors, is endocytosed with the receptor and, in the cell, triggers the release of LUTEINIZING HORMONE or FOLLICLE STIMULATING HORMONE by the cell. These receptors are also found in rat gonads. INHIBINS prevent the binding of GnRH to its receptors. [MESH:D011966]",5
"Growth hormone-releasing hormone receptor","Growth hormone-releasing hormone receptor","membrane receptor  7tm2  peptide  glucagon-like  growth hormone-releasing hormone receptor",NULL,5
"GRP-related receptor","GRP-related receptor","membrane receptor  7tm1  peptide  short peptide  grp-related receptor","Cell surface proteins that bind bombesin or closely related peptides with high affinity and trigger intracellular changes influencing the behavior of cells. Gastrin- releasing peptide (GRP); GRP 18-27 (neuromedin C), and neuromedin B are endogenous ligands of bombesin receptors in mammals. [MESH:D018004]",5
"Histamine receptor","Histamine receptor","membrane receptor  7tm1  smallmol  monoamine receptor  histamine receptor","Cell-surface proteins that bind histamine and trigger intracellular changes influencing the behavior of cells. Histamine receptors are widespread in the central nervous system and in peripheral tissues. Three types have been recognized and designated H1, H2, and H3. They differ in pharmacology, distribution, and mode of action. [MESH:D011968]",5
"Hydroxycarboxylic acid receptor","Hydroxycarboxylic acid receptor","membrane receptor  7tm1  smallmol  carboxylic acid  hydroxycarboxylic acid receptor",NULL,5
"Kynurenic acid receptor","Kynurenic acid receptor","membrane receptor  7tm1  smallmol  carboxylic acid  kynurenic acid receptor",NULL,5
"Leukotriene receptor","Leukotriene receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  leukotriene receptor","Cell-surface receptors that bind LEUKOTRIENES with high affinity and trigger intracellular changes influencing the behavior of cells. The leukotriene receptor subtypes have been tentatively named according to their affinities for the endogenous leukotrienes LTB4; LTC4; LTD4; and LTE4. [MESH:D018077]",5
"Lysophosphatidylinositol receptor","Lysophosphatidylinositol receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  lysophosphatidylinositol receptor",NULL,5
"MCH receptor","MCH receptor","membrane receptor  7tm1  peptide  short peptide  mch receptor",NULL,5
"Melanocortin receptor","Melanocortin receptor","membrane receptor  7tm1  peptide  short peptide  melanocortin receptor","A family of G-protein-coupled receptors that have specificity for MELANOCYTE-STIMULATING HORMONES and ADRENOCORTICOTROPIC HORMONE. There are several subtypes of melanocortin receptors, each having a distinct ligand specificity profile and tissue localization. [MESH:D044101]",5
"Melatonin receptor","Melatonin receptor","membrane receptor  7tm1  smallmol  monoamine-derivative  melatonin receptor","A family of G-protein-coupled receptors that are specific for and mediate the effects of MELATONIN. Activation of melatonin receptors has been associated with decreased intracellular CYCLIC AMP and increased hydrolysis of PHOSPHOINOSITIDES. [MESH:D044094]",5
"Metabotropic glutamate receptor","Metabotropic glutamate receptor","membrane receptor  7tm3  smallmol  neurotransmitter  metabotropic glutamate receptor","Cell surface proteins that bind glutamate and act through G-proteins to influence second messenger systems. Several types of metabotropic glutamate receptors have been cloned. They differ in pharmacology, distribution, and mechanisms of action. [MESH:D018094]",5
"Metallo protease M1 family",M1,"enzyme  protease  metallo  mae  m1","A subclass of EXOPEPTIDASES that act on the free N terminus end of a polypeptide liberating a single amino acid residue. EC 3.4.11. [MESH:D000626]",5
"Metallo protease M10A subfamily",M10A,"enzyme  protease  metallo  mam  m10a","A member of the metalloproteinase family of enzymes that is principally responsible for cleaving FIBRILLAR COLLAGEN. It can degrade interstitial collagens, types I, II and III. [MESH:D020781]",5
"Metallo protease M12A subfamily",M12A,"enzyme  protease  metallo  mam  m12a","A bone morphogenetic protein family member that includes an active tolloid-like metalloproteinase domain. The metalloproteinase activity of bone morphogenetic protein 1 is specific for the removal of the C-propeptide of PROCOLLAGEN and may act as a regulator of EXTRACELLULAR MATRIX deposition. Alternative splicing of MRNA for bone morphogenetic protein 1 results in the production of several PROTEIN ISOFORMS. [MESH:D055395]",5
"Metallo protease M12B subfamily",M12B,"enzyme  protease  metallo  mam  m12b","A family of membrane-anchored glycoproteins that contain a disintegrin and metalloprotease domain. They are responsible for the proteolytic cleavage of many transmembrane proteins and the release of their extracellular domain. [MESH:D051722]",5
"Metallo protease M13 family",M13,"enzyme  protease  metallo  mae  m13","Enzyme that is a major constituent of kidney brush-border membranes and is also present to a lesser degree in the brain and other tissues. It preferentially catalyzes cleavage at the amino group of hydrophobic residues of the B-chain of insulin as well as opioid peptides and other biologically active peptides. The enzyme is inhibited primarily by EDTA, phosphoramidon, and thiorphan and is reactivated by zinc. Neprilysin is identical to common acute lymphoblastic leukemia antigen (CALLA Antigen), an important marker in the diagnosis of human acute lymphocytic leukemia. There is no relationship with CALLA PLANT. [MESH:D015260]",5
"Metallo protease M14A subfamily",M14A,"enzyme  protease  metallo  mc  m14a",NULL,5
"Metallo protease M14B subfamily",M14B,"enzyme  protease  metallo  mc  m14b",NULL,5
"Metallo protease M14C subfamily",M14C,"enzyme  protease  metallo  mc  m14c",NULL,5
"Metallo protease M14D subfamily",M14D,"enzyme  protease  metallo  mc  m14d",NULL,5
"Metallo protease M15 family",M15,"enzyme  protease  metallo  md  m15",NULL,5
"Metallo protease M17 family",M17,"enzyme  protease  metallo  mf  m17","A zinc containing enzyme of the hydrolase class that catalyzes the removal of the N-terminal amino acid from most L-peptides, particularly those with N-terminal leucine residues but not those with N-terminal lysine or arginine residues. This occurs in tissue cell cytosol, with high activity in the duodenum, liver, and kidney. The activity of this enzyme is commonly assayed using a leucine arylamide chromogenic substrate such as leucyl beta-naphthylamide. [MESH:D007931]",5
"Metallo protease M18 family",M18,"enzyme  protease  metallo  mh  m18","A ZINC-dependent membrane-bound aminopeptidase that catalyzes the N-terminal peptide cleavage of GLUTAMATE (and to a lesser extent ASPARTATE). The enzyme appears to play a role in the catabolic pathway of the RENIN-ANGIOTENSIN SYSTEM. [MESH:D043384]",5
"Metallo protease M19 family",M19,"enzyme  protease  metallo  mj  m19",NULL,5
"Metallo protease M2 family",M2,"enzyme  protease  metallo  mae  m2",NULL,5
"Metallo protease M20A subfamily",M20A,"enzyme  protease  metallo  mh  m20a",NULL,5
"Metallo protease M24A subfamily",M24A,"enzyme  protease  metallo  mg  m24a",NULL,5
"Metallo protease M24B subfamily",M24B,"enzyme  protease  metallo  mg  m24b",NULL,5
"Metallo protease M27 family",M27,"enzyme  protease  metallo  mae  m27",NULL,5
"Metallo protease M28 family",M28,"enzyme  protease  metallo  mh  m28",NULL,5
"Metallo protease M3 family",M3,"enzyme  protease  metallo  mae  m3",NULL,5
"Metallo protease M34 family",M34,"enzyme  protease  metallo  mae  m34",NULL,5
"Metallo protease M4 family",M4,"enzyme  protease  metallo  mae  m4","A thermostable extracellular metalloendopeptidase containing four calcium ions. (Enzyme Nomenclature, 1992) 3.4.24.27. [MESH:D013820]",5
"Metallo protease M48A subfamily",M48A,"enzyme  protease  metallo  mae  m48a",NULL,5
"Metallo protease M49 family",M49,"enzyme  protease  metallo  mae  m49",NULL,5
"Metallo protease M67 family",M67,"enzyme  protease  metallo  mp  m67",NULL,5
"Metallo protease M79 family",M79,"enzyme  protease  metallo  m-  m79",NULL,5
"Metallo protease M9B subfamily",M9B,"enzyme  protease  metallo  mae  m9b","A metalloproteinase which degrades helical regions of native collagen to small fragments. Preferred cleavage is -Gly in the sequence -Pro-Xaa-Gly-Pro-. Six forms (or 2 classes) have been isolated from Clostridium histolyticum that are immunologically cross-reactive but possess different sequences and different specificities. Other variants have been isolated from Bacillus cereus, Empedobacter collagenolyticum, Pseudomonas marinoglutinosa, and species of Vibrio and Streptomyces. EC 3.4.24.3. [MESH:D003012]",5
"Motilin receptor","Motilin receptor","membrane receptor  7tm1  peptide  short peptide  motilin receptor",NULL,5
"N-formyl methionyl peptide receptor","N-formyl methionyl peptide receptor","membrane receptor  7tm1  peptide  n-formyl methionyl peptide receptor  n-formyl methionyl peptide receptor","A family of G-protein-coupled receptors that was originally identified by its ability to bind N-formyl peptides such as N-FORMYLMETHIONINE LEUCYL-PHENYLALANINE. Since N-formyl peptides are found in MITOCHONDRIA and BACTERIA, this class of receptors is believed to play a role in mediating cellular responses to cellular damage and bacterial invasion. However, non-formylated peptide ligands have also been found for this receptor class. [MESH:D044042]",5
"Neurokinin receptor","Neurokinin receptor","membrane receptor  7tm1  peptide  short peptide  neurokinin receptor","A class of cell surface receptors for tachykinins that prefers neurokinin B (neurokinin beta, neuromedin K) over other tachykinins. Neurokinin-3 (NK-3) receptors have been cloned and are members of the G-protein coupled receptor superfamily. They have been found in the central nervous system and in peripheral tissues. [MESH:D018042]",5
"Neuromedin receptor","Neuromedin receptor","membrane receptor  7tm1  peptide  short peptide  neuromedin receptor",NULL,5
"Neuromedin U receptor","Neuromedin U receptor","membrane receptor  7tm1  peptide  short peptide  neuromedin u receptor",NULL,5
"Neuropeptide receptor","Neuropeptide receptor","membrane receptor  7tm1  peptide  short peptide  neuropeptide receptor","Cell surface receptors that bind specific neuropeptides with high affinity and trigger intracellular changes influencing the behavior of cells. Many neuropeptides are also hormones outside of the nervous system. [MESH:D018013]",5
"Neuropeptide Y receptor","Neuropeptide Y receptor","membrane receptor  7tm1  peptide  short peptide  neuropeptide y receptor","Cell surface proteins that bind neuropeptide Y with high affinity and trigger intracellular changes which influence the behavior of cells. [MESH:D017476]",5
"Neurotensin receptor","Neurotensin receptor","membrane receptor  7tm1  peptide  short peptide  neurotensin receptor","Cell surface proteins that bind neurotensin with high affinity and trigger intracellular changes which influence the behavior of cells. Neurotensin and neurotensin receptors are found in the central nervous system and in the periphery. [MESH:D018028]",5
"Nicotinic acid receptor","Nicotinic acid receptor","membrane receptor  7tm1  smallmol  nucleotide-like receptor  nicotinic acid receptor",NULL,5
"Nuclear hormone receptor subfamily 0 group B member 1",NR0B1,"transcription factor  nuclear receptor  nr0  nr0b  nr0b1",NULL,5
"Nuclear hormone receptor subfamily 0 group B member 2",NR0B2,"transcription factor  nuclear receptor  nr0  nr0b  nr0b2",NULL,5
"Nuclear hormone receptor subfamily 1 group A member 1",NR1A1,"transcription factor  nuclear receptor  nr1  nr1a  nr1a1","High affinity receptors for THYROID HORMONES, especially TRIIODOTHYRONINE. These receptors are usually found in the nucleus where they regulate DNA transcription. They are encoded by the THRA gene (also known as NR1A1, THRA1, ERBA or ERBA1 gene) as several isoforms produced by alternative splicing. [MESH:D037021]",5
"Nuclear hormone receptor subfamily 1 group A member 2",NR1A2,"transcription factor  nuclear receptor  nr1  nr1a  nr1a2","High affinity receptors for THYROID HORMONES, especially TRIIODOTHYRONINE. These receptors are usually found in the nucleus where they regulate DNA transcription. They are encoded by the THRB gene (also known as NR1A2, THRB1, or ERBA2 gene) as several isoforms produced by alternative splicing. Mutations in the THRB gene cause THYROID HORMONE RESISTANCE SYNDROME. [MESH:D037042]",5
"Nuclear hormone receptor subfamily 1 group B member 1",NR1B1,"transcription factor  nuclear receptor  nr1  nr1b  nr1b1",NULL,5
"Nuclear hormone receptor subfamily 1 group B member 2",NR1B2,"transcription factor  nuclear receptor  nr1  nr1b  nr1b2",NULL,5
"Nuclear hormone receptor subfamily 1 group B member 3",NR1B3,"transcription factor  nuclear receptor  nr1  nr1b  nr1b3",NULL,5
"Nuclear hormone receptor subfamily 1 group C member 1",NR1C1,"transcription factor  nuclear receptor  nr1  nr1c  nr1c1","A nuclear transcription factor. Heterodimerization with RETINOID X RECEPTOR GAMMA is important to metabolism of LIPIDS. It is the target of FIBRATES to control HYPERLIPIDEMIAS. [MESH:D047493]",5
"Nuclear hormone receptor subfamily 1 group C member 2",NR1C2,"transcription factor  nuclear receptor  nr1  nr1c  nr1c2","A nuclear transcription factor. It is activated by PROSTACYCLIN. [MESH:D047494]",5
"Nuclear hormone receptor subfamily 1 group C member 3",NR1C3,"transcription factor  nuclear receptor  nr1  nr1c  nr1c3","A nuclear transcription factor. Heterodimerization with RETINOID X RECEPTOR ALPHA is important in regulation of GLUCOSE metabolism and CELL GROWTH PROCESSES. It is a target of THIAZOLIDINEDIONES for control of DIABETES MELLITUS. [MESH:D047495]",5
"Nuclear hormone receptor subfamily 1 group D member 1",NR1D1,"transcription factor  nuclear receptor  nr1  nr1d  nr1d1",NULL,5
"Nuclear hormone receptor subfamily 1 group D member 2",NR1D2,"transcription factor  nuclear receptor  nr1  nr1d  nr1d2",NULL,5
"Nuclear hormone receptor subfamily 1 group F member 1",NR1F1,"transcription factor  nuclear receptor  nr1  nr1f  nr1f1",NULL,5
"Nuclear hormone receptor subfamily 1 group F member 3",NR1F3,"transcription factor  nuclear receptor  nr1  nr1f  nr1f3",NULL,5
"Nuclear hormone receptor subfamily 1 group H member 1",NR1H1,"transcription factor  nuclear receptor  nr1  nr1h  nr1h1",NULL,5
"Nuclear hormone receptor subfamily 1 group H member 3",NR1H3,"transcription factor  nuclear receptor  nr1  nr1h  nr1h3",NULL,5
"Nuclear hormone receptor subfamily 1 group H member 4",NR1H4,"transcription factor  nuclear receptor  nr1  nr1h  nr1h4",NULL,5
"Nuclear hormone receptor subfamily 1 group I member 1",NR1I1,"transcription factor  nuclear receptor  nr1  nr1i  nr1i1","Proteins, usually found in the cytoplasm, that specifically bind calcitriol, migrate to the nucleus, and regulate transcription of specific segments of DNA with the participation of D receptor interacting proteins (called DRIP). Vitamin D is converted in the liver and kidney to calcitriol and ultimately acts through these receptors. [MESH:D018167]",5
"Nuclear hormone receptor subfamily 1 group I member 2",NR1I2,"transcription factor  nuclear receptor  nr1  nr1i  nr1i2",NULL,5
"Nuclear hormone receptor subfamily 1 group I member 3",NR1I3,"transcription factor  nuclear receptor  nr1  nr1i  nr1i3",NULL,5
"Nuclear hormone receptor subfamily 2 group A member 2",NR2A2,"transcription factor  nuclear receptor  nr2  nr2a  nr2a2",NULL,5
"Nuclear hormone receptor subfamily 2 group B member 1",NR2B1,"transcription factor  nuclear receptor  nr2  nr2b  nr2b1","A nuclear transcription factor. Heterodimerization with PPAR GAMMA is important in regulation of GLUCOSE metabolism and CELL GROWTH PROCESSES. [MESH:D047490]",5
"Nuclear hormone receptor subfamily 2 group B member 2",NR2B2,"transcription factor  nuclear receptor  nr2  nr2b  nr2b2",NULL,5
"Nuclear hormone receptor subfamily 2 group B member 3",NR2B3,"transcription factor  nuclear receptor  nr2  nr2b  nr2b3","A nuclear transcription factor. Heterodimerization with PPAR ALPHA is important to metabolism of LIPIDS. [MESH:D047491]",5
"Nuclear hormone receptor subfamily 2 group C member 1",NR2C1,"transcription factor  nuclear receptor  nr2  nr2c  nr2c1",NULL,5
"Nuclear hormone receptor subfamily 2 group C member 2",NR2C2,"transcription factor  nuclear receptor  nr2  nr2c  nr2c2",NULL,5
"Nuclear hormone receptor subfamily 2 group E member 1",NR2E1,"transcription factor  nuclear receptor  nr2  nr2e  nr2e1",NULL,5
"Nuclear hormone receptor subfamily 2 group E member 3",NR2E3,"transcription factor  nuclear receptor  nr2  nr2e  nr2e3",NULL,5
"Nuclear hormone receptor subfamily 2 group F member 1",NR2F1,"transcription factor  nuclear receptor  nr2  nr2f  nr2f1",NULL,5
"Nuclear hormone receptor subfamily 2 group F member 2",NR2F2,"transcription factor  nuclear receptor  nr2  nr2f  nr2f2",NULL,5
"Nuclear hormone receptor subfamily 2 group F member 6",NR2F6,"transcription factor  nuclear receptor  nr2  nr2f  nr2f6",NULL,5
"Nuclear hormone receptor subfamily 3 group A member 1",NR3A1,"transcription factor  nuclear receptor  nr3  nr3a  nr3a1","One of the ESTROGEN RECEPTORS that has marked affinity for ESTRADIOL. Its expression and function differs from, and in some ways opposes, ESTROGEN RECEPTOR BETA. [MESH:D047628]",5
"Nuclear hormone receptor subfamily 3 group A member 2",NR3A2,"transcription factor  nuclear receptor  nr3  nr3a  nr3a2","One of the ESTROGEN RECEPTORS that has greater affinity for ISOFLAVONES than ESTROGEN RECEPTOR ALPHA does. There is great sequence homology with ER alpha in the DNA-binding domain but not in the ligand binding and hinge domains. [MESH:D047629]",5
"Nuclear hormone receptor subfamily 3 group B member 1",NR3B1,"transcription factor  nuclear receptor  nr3  nr3b  nr3b1",NULL,5
"Nuclear hormone receptor subfamily 3 group B member 2",NR3B2,"transcription factor  nuclear receptor  nr3  nr3b  nr3b2",NULL,5
"Nuclear hormone receptor subfamily 3 group B member 3",NR3B3,"transcription factor  nuclear receptor  nr3  nr3b  nr3b3",NULL,5
"Nuclear hormone receptor subfamily 3 group C member 1",NR3C1,"transcription factor  nuclear receptor  nr3  nr3c  nr3c1","Cytoplasmic proteins that specifically bind glucocorticoids and mediate their cellular effects. The glucocorticoid receptor-glucocorticoid complex acts in the nucleus to induce transcription of DNA. Glucocorticoids were named for their actions on blood glucose concentration, but they have equally important effects on protein and fat metabolism. Cortisol is the most important example. [MESH:D011965]",5
"Nuclear hormone receptor subfamily 3 group C member 2",NR3C2,"transcription factor  nuclear receptor  nr3  nr3c  nr3c2","Cytoplasmic proteins that specifically bind aldosterone and mediate its cellular effects. The aldosterone-bound receptor acts in the nucleus to regulate the transcription of specific segments of DNA. [MESH:D017458]",5
"Nuclear hormone receptor subfamily 3 group C member 3",NR3C3,"transcription factor  nuclear receptor  nr3  nr3c  nr3c3","Specific proteins found in or on cells of progesterone target tissues that specifically combine with progesterone. The cytosol progesterone-receptor complex then associates with the nucleic acids to initiate protein synthesis. There are two kinds of progesterone receptors, A and B. Both are induced by estrogen and have short half-lives. [MESH:D011980]",5
"Nuclear hormone receptor subfamily 3 group C member 4",NR3C4,"transcription factor  nuclear receptor  nr3  nr3c  nr3c4","Proteins, generally found in the CYTOPLASM, that specifically bind ANDROGENS and mediate their cellular actions. The complex of the androgen and receptor migrates to the CELL NUCLEUS where it induces transcription of specific segments of DNA. [MESH:D011944]",5
"Nuclear hormone receptor subfamily 4 group A member 1",NR4A1,"transcription factor  nuclear receptor  nr4  nr4a  nr4a1",NULL,5
"Nuclear hormone receptor subfamily 4 group A member 2",NR4A2,"transcription factor  nuclear receptor  nr4  nr4a  nr4a2",NULL,5
"Nuclear hormone receptor subfamily 4 group A member 3",NR4A3,"transcription factor  nuclear receptor  nr4  nr4a  nr4a3",NULL,5
"Nuclear hormone receptor subfamily 5 group A member 1",NR5A1,"transcription factor  nuclear receptor  nr5  nr5a  nr5a1","A transcription factor and member of the nuclear receptor family NR5 that is expressed throughout the adrenal and reproductive axes during development. It plays an important role in sexual differentiation, formation of primary steroidogenic tissues, and their functions in post-natal and adult life. It regulates the expression of key steroidogenic enzymes. [MESH:D054339]",5
"Nuclear hormone receptor subfamily 5 group A member 2",NR5A2,"transcription factor  nuclear receptor  nr5  nr5a  nr5a2",NULL,5
"Nuclear hormone receptor subfamily 6 group A member 1",NR6A1,"transcription factor  nuclear receptor  nr6  nr6a  nr6a1",NULL,5
"Nucleotide-like receptor","Nucleotide-like receptor","membrane receptor  7tm1  smallmol  nucleotide-like receptor  nucleotide-like receptor",NULL,5
"Opioid receptor","Opioid receptor","membrane receptor  7tm1  peptide  short peptide  opioid receptor","Cell membrane proteins that bind opioids and trigger intracellular changes which influence the behavior of cells. The endogenous ligands for opioid receptors in mammals include three families of peptides, the enkephalins, endorphins, and dynorphins. The receptor classes include mu, delta, and kappa receptors. Sigma receptors bind several psychoactive substances, including certain opioids, but their endogenous ligands are not known. [MESH:D011957]",5
"Orexin receptor","Orexin receptor","membrane receptor  7tm1  peptide  short peptide  orexin receptor",NULL,5
"Other protein kinase AUR family",Aur,"enzyme  kinase  protein kinase  other  aur",NULL,5
"Other protein kinase Bud32 family","Bud 32","enzyme  kinase  protein kinase  other  bud 32",NULL,5
"Other protein kinase CAMKK family",Camkk,"enzyme  kinase  protein kinase  other  camkk","A regulatory calcium-calmodulin-dependent protein kinase that specifically phosphorylates CALCIUM-CALMODULIN-DEPENDENT PROTEIN KINASE TYPE 1; CALCIUM-CALMODULIN-DEPENDENT PROTEIN KINASE TYPE 2; CALCIUM-CALMODULIN-DEPENDENT PROTEIN KINASE TYPE 4; and PROTEIN KINASE B. It is a monomeric enzyme that is encoded by at least two different genes. [MESH:D054737]",5
"Other protein kinase CDC7 family",Cdc7,"enzyme  kinase  protein kinase  other  cdc7",NULL,5
"Other protein kinase CK2 family",Ck2,"enzyme  kinase  protein kinase  other  ck2","A ubiquitous casein kinase that is comprised of two distinct catalytic subunits and dimeric regulatory subunit. Casein kinase II has been shown to phosphorylate a large number of substrates, many of which are proteins involved in the regulation of gene expression. [MESH:D047390]",5
"Other protein kinase Haspin family",Haspin,"enzyme  kinase  protein kinase  other  haspin",NULL,5
"Other protein kinase IKK family",Ikk,"enzyme  kinase  protein kinase  other  ikk","A protein serine/threonine kinase that phosphorylates IkappaB, thereby targeting this for proteasomal degradation and allowing the nuclear translocation of kB. Composed of alpha, beta and gamma subunits, the latter not having kinase activity but presumed to play a regulatory role. [GOC:ma] [MESH:]",5
"Other protein kinase MOS family",Mos,"enzyme  kinase  protein kinase  other  mos",NULL,5
"Other protein kinase NAK family",Nak,"enzyme  kinase  protein kinase  other  nak",NULL,5
"Other protein kinase NEK family",Nek,"enzyme  kinase  protein kinase  other  nek",NULL,5
"Other protein kinase NKF1 family",Nkf1,"enzyme  kinase  protein kinase  other  nkf1",NULL,5
"Other protein kinase NKF4 family",Nkf4,"enzyme  kinase  protein kinase  other  nkf4",NULL,5
"Other protein kinase PEK family",Pek,"enzyme  kinase  protein kinase  other  pek","A dsRNA-activated cAMP-independent protein serine/threonine kinase that is induced by interferon. In the presence of dsRNA and ATP, the kinase autophosphorylates on several serine and threonine residues. The phosphorylated enzyme catalyzes the phosphorylation of the alpha subunit of EUKARYOTIC INITIATION FACTOR-2, leading to the inhibition of protein synthesis. [MESH:D019892]",5
"Other protein kinase PLK family",Plk,"enzyme  kinase  protein kinase  other  plk",NULL,5
"Other protein kinase TLK family",Tlk,"enzyme  kinase  protein kinase  other  tlk",NULL,5
"Other protein kinase TOPK family",Topk,"enzyme  kinase  protein kinase  other  topk",NULL,5
"Other protein kinase TTK family",Ttk,"enzyme  kinase  protein kinase  other  ttk",NULL,5
"Other protein kinase ULK family",Ulk,"enzyme  kinase  protein kinase  other  ulk",NULL,5
"Other protein kinase unique family",Other-Unique,"enzyme  kinase  protein kinase  other  other-unique",NULL,5
"Other protein kinase WEE family",Wee,"enzyme  kinase  protein kinase  other  wee",NULL,5
"Other protein kinase Wnk family",Wnk,"enzyme  kinase  protein kinase  other  wnk",NULL,5
"Oxoglutarate receptor","Oxoglutarate receptor","membrane receptor  7tm1  smallmol  carboxylic acid  oxoglutarate receptor",NULL,5
"PAF receptor",PAF,"membrane receptor  7tm1  smallmol  lipid-like ligand receptor  paf",NULL,5
"Parathyroid hormone receptor","Parathyroid hormone receptor","membrane receptor  7tm2  peptide  parathyroid hormone receptor  parathyroid hormone receptor","A parathyroid hormone receptor subtype that recognizes both PARATHYROID HORMONE and PARATHYROID HORMONE-RELATED PROTEIN. It is a G-protein-coupled receptor that is expressed at high levels in BONE and in KIDNEY. [MESH:D044168]",5
"Prokineticin receptor","Prokineticin receptor","membrane receptor  7tm1  peptide  peptide growth factor  prokineticin receptor",NULL,5
"Prolactin-releasing peptide receptor","Prolactin-releasing peptide receptor","membrane receptor  7tm1  peptide  short peptide  prolactin-releasing peptide receptor",NULL,5
"Prostanoid receptor","Prostanoid receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  prostanoid receptor","Cell surface receptors that bind prostaglandins with high affinity and trigger intracellular changes which influence the behavior of cells. Prostaglandin receptor subtypes have been tentatively named according to their relative affinities for the endogenous prostaglandins. They include those which prefer prostaglandin D2 (DP receptors), prostaglandin E2 (EP1, EP2, and EP3 receptors), prostaglandin F2-alpha (FP receptors), and prostacyclin (IP receptors). [MESH:D011982]",5
"Protease inhibitor I49 family",I49,"enzyme  protease  inhibitor  i-  i49",NULL,5
"Protease unclassified U48 family",U48,"enzyme  protease  unknown  u-  u48",NULL,5
"Protease-activated receptor","Protease-activated receptor","membrane receptor  7tm1  peptide  protease-activated receptor  protease-activated receptor","A class of receptors that are activated by the action of PROTEINASES. The most notable examples are the THROMBIN RECEPTORS. The receptors contain cryptic ligands that are exposed upon the selective proteolysis of specific N-terminal cleavage sites. [MESH:D044462]",5
"Purine receptor","Purine receptor","membrane receptor  7tm1  smallmol  nucleotide-like receptor  purine receptor","Cell surface proteins that bind PURINES with high affinity and trigger intracellular changes which influence the behavior of cells. The best characterized classes of purinergic receptors in mammals are the P1 receptors, which prefer ADENOSINE, and the P2 receptors, which prefer ATP or ADP. [MESH:D011983]",5
"Receptor tyrosine-protein phosphatase",Receptor,"enzyme  phosphatase  protein phosphatase  tyr  receptor",NULL,5
"Relaxin receptor",Relaxin,"membrane receptor  7tm1  peptide  relaxin-like peptide  relaxin",NULL,5
"RF amide receptor","RF amide receptor","membrane receptor  7tm1  peptide  short peptide  rf amide receptor",NULL,5
"Secretin receptor receptor","Secretin receptor","membrane receptor  7tm2  peptide  glucagon-like  secretin receptor",NULL,5
"Serine protease S10 family",S10,"enzyme  protease  serine  sc  s10","A carboxypeptidase that catalyzes the release of a C-terminal amino acid with a broad specificity. It also plays a role in the LYSOSOMES by protecting BETA-GALACTOSIDASE and NEURAMINIDASE from degradation. It was formerly classified as EC 3.4.12.1 and EC 3.4.21.13. [MESH:D043402]",5
"Serine protease S11 family",S11,"enzyme  protease  serine  se  s11","A carboxypeptidase that is specific for proteins that contain two ALANINE residues on their C-terminal. Enzymes in this class play an important role in bacterial CELL WALL biosynthesis. [MESH:D046929]",5
"Serine protease S12 family",S12,"enzyme  protease  serine  se  s12",NULL,5
"Serine protease S13 family",S13,"enzyme  protease  serine  se  s13","A carboxypeptidase that is specific for proteins that contain two ALANINE residues on their C-terminal. Enzymes in this class play an important role in bacterial CELL WALL biosynthesis. [MESH:D046929]",5
"Serine protease S14 family",S14,"enzyme  protease  serine  sk  s14",NULL,5
"Serine protease S16 family",S16,"enzyme  protease  serine  sj  s16",NULL,5
"Serine protease S1A subfamily",S1A,"enzyme  protease  serine  pas  s1a","A serine endopeptidase secreted by the pancreas as its zymogen, CHYMOTRYPSINOGEN and carried in the pancreatic juice to the duodenum where it is activated by TRYPSIN. It selectively cleaves aromatic amino acids on the carboxyl side. [MESH:D002918]",5
"Serine protease S1B subfamily",S1B,"enzyme  protease  serine  pas  s1b",NULL,5
"Serine protease S1C subfamily",S1C,"enzyme  protease  serine  pas  s1c",NULL,5
"Serine protease S1E subfamily",S1E,"enzyme  protease  serine  pas  s1e",NULL,5
"Serine protease S21 family",S21,"enzyme  protease  serine  sh  s21",NULL,5
"Serine protease S26A subfamily",S26A,"enzyme  protease  serine  sf  s26a",NULL,5
"Serine protease S26B subfamily",S26B,"enzyme  protease  serine  sf  s26b",NULL,5
"Serine protease S26C subfamily",S26C,"enzyme  protease  serine  sf  s26c",NULL,5
"Serine protease S28 family",S28,"enzyme  protease  serine  sc  s28",NULL,5
"Serine protease S29 family",S29,"enzyme  protease  serine  pas  s29",NULL,5
"Serine protease S33 family",S33,"enzyme  protease  serine  sc  s33",NULL,5
"Serine protease S54 family",S54,"enzyme  protease  serine  st  s54",NULL,5
"Serine protease S6 family",S6,"enzyme  protease  serine  pas  s6",NULL,5
"Serine protease S60 family",S60,"enzyme  protease  serine  sr  s60","An iron-binding protein that was originally characterized as a milk protein. It is widely distributed in secretory fluids and is found in the neutrophilic granules of LEUKOCYTES. The N-terminal part of lactoferrin possesses a serine protease which functions to inactivate the type III secretion system used by bacteria to export virulence proteins for host cell invasion. [MESH:D007781]",5
"Serine protease S8A subfamily",S8A,"enzyme  protease  serine  sb  s8a","A serine endopeptidase isolated from Bacillus subtilis. It hydrolyzes proteins with broad specificity for peptide bonds, and a preference for a large uncharged residue in P1. It also hydrolyzes peptide amides. (From Enzyme Nomenclature, 1992) EC 3.4.21.62. [MESH:D020860]",5
"Serine protease S8B subfamily",S8B,"enzyme  protease  serine  sb  s8b",NULL,5
"Serine protease S9A subfamily",S9A,"enzyme  protease  serine  sc  s9a",NULL,5
"Serine protease S9B subfamily",S9B,"enzyme  protease  serine  sc  s9b","A serine protease that catalyses the release of an N-terminal dipeptide. Several biologically-active peptides have been identified as dipeptidyl peptidase 4 substrates including INCRETINS; NEUROPEPTIDES; and CHEMOKINES. The protein is also found bound to ADENOSINE DEAMINASE on the T-CELL surface and is believed to play a role in T-cell activation. [MESH:D018819]",5
"Serine protease S9C subfamily",S9C,"enzyme  protease  serine  sc  s9c",NULL,5
"Serotonin receptor","Serotonin receptor","membrane receptor  7tm1  smallmol  monoamine receptor  serotonin receptor","Cell-surface proteins that bind SEROTONIN and trigger intracellular changes which influence the behavior of cells. Several types of serotonin receptors have been recognized which differ in their pharmacology, molecular biology, and mode of action. [MESH:D011985]",5
"SLC03 Heavy subunits of the heteromeric amino acid transporters",SLC03,"transporter  electrochemical  slc  slc03 and slc07  slc03",NULL,5
"SLC07 Cationic amino acid transporter/glycoprotein-associated family",SLC07,"transporter  electrochemical  slc  slc03 and slc07  slc07",NULL,5
"SLC28 Na+-coupled nucleoside transport family",SLC28,"transporter  electrochemical  slc  slc28 and slc29  slc28",NULL,5
"SLC29 Facilitative nucleoside transporter family",SLC29,"transporter  electrochemical  slc  slc28 and slc29  slc29",NULL,5
"Somatostatin receptor","Somatostatin receptor","membrane receptor  7tm1  peptide  short peptide  somatostatin receptor","Cell surface proteins that bind somatostatin and trigger intracellular changes which influence the behavior of cells. Somatostatin is a hypothalamic hormone, a pancreatic hormone, and a central and peripheral neurotransmitter. Activated somatostatin receptors on pituitary cells inhibit the release of growth hormone; those on endocrine and gastrointestinal cells regulate the absorption and utilization of nutrients; and those on neurons mediate somatostatin's role as a neurotransmitter. [MESH:D017481]",5
"STE protein kinase STE11 family",Ste11,"enzyme  kinase  protein kinase  ste  ste11","Mitogen-activated protein kinase kinase kinases (MAPKKKs) are serine-threonine protein kinases that initiate protein kinase signaling cascades. They phosphorylate MITOGEN-ACTIVATED PROTEIN KINASE KINASES; (MAPKKs) which in turn phosphorylate MITOGEN-ACTIVATED PROTEIN KINASES; (MAPKs). [MESH:D020930]",5
"STE protein kinase STE20 family",Ste20,"enzyme  kinase  protein kinase  ste  ste20",NULL,5
"STE protein kinase STE7 family",Ste7,"enzyme  kinase  protein kinase  ste  ste7","A serine-threonine protein kinase family whose members are components in protein kinase cascades activated by diverse stimuli. These MAPK kinases phosphorylate MITOGEN-ACTIVATED PROTEIN KINASES and are themselves phosphorylated by MAP KINASE KINASE KINASES. JNK kinases (also known as SAPK kinases) are a subfamily. [MESH:D020929]",5
"STE protein kinase unique family",Ste-Unique,"enzyme  kinase  protein kinase  ste  ste-unique",NULL,5
"Steroid-like ligand receptor","Steroid-like ligand receptor","membrane receptor  7tm1  smallmol  lipid-like ligand receptor  steroid-like ligand receptor",NULL,5
"Succinate receptor","Succinate receptor","membrane receptor  7tm1  smallmol  carboxylic acid  succinate receptor",NULL,5
"Threonine protease T1A subfamily",T1A,"enzyme  protease  threonine  pbt  t1a",NULL,5
"Threonine protease T1B subfamily",T1B,"enzyme  protease  threonine  pbt  t1b",NULL,5
"Threonine protease T2 family",T2,"enzyme  protease  threonine  pbt  t2",NULL,5
"TKL protein kinase IRAK family",Irak,"enzyme  kinase  protein kinase  tkl  irak","A family of intracellular signaling kinases that were identified by their ability to signal from the activated INTERLEUKIN-1 RECEPTORS. Signaling from these kinases involves their interaction with SIGNAL TRANSDUCING ADAPTOR PROTEINS such as MYELOID DIFFERENTIATION FACTOR 88 and TNF RECEPTOR-ASSOCIATED FACTOR 6. [MESH:D053592]",5
"TKL protein kinase LISK family",Lisk,"enzyme  kinase  protein kinase  tkl  lisk",NULL,5
"TKL protein kinase LRRK family",Lrrk,"enzyme  kinase  protein kinase  tkl  lrrk",NULL,5
"TKL protein kinase MLK family",Mlk,"enzyme  kinase  protein kinase  tkl  mlk",NULL,5
"TKL protein kinase RAF family",Raf,"enzyme  kinase  protein kinase  tkl  raf","A family of closely-related serine-threonine kinases that were originally identified as the cellular homologs of the retrovirus-derived V-RAF KINASES. They are MAP kinase kinase kinases that play important roles in SIGNAL TRANSDUCTION. [MESH:D048490]",5
"TKL protein kinase RIPK family",Ripk,"enzyme  kinase  protein kinase  tkl  ripk","A family of serine-threonine kinases that plays a role in intracellular signal transduction by interacting with a variety of signaling adaptor proteins such as CRADD SIGNALING ADAPTOR PROTEIN; TNF RECEPTOR-ASSOCIATED FACTOR 2; and TNF RECEPTOR-ASSOCIATED DEATH DOMAIN PROTEIN. Although they were initially described as death domain-binding adaptor proteins, members of this family may contain other protein-binding domains such as those involving caspase activation and recruitment. [MESH:D053422]",5
"TKL protein kinase STKR family",Stkr,"enzyme  kinase  protein kinase  tkl  stkr",NULL,5
"Trace amine receptor","Trace amine receptor","membrane receptor  7tm1  smallmol  monoamine receptor  trace amine receptor",NULL,5
"Tyrosine protein kinase Abl family",Abl,"enzyme  kinase  protein kinase  tk  abl",NULL,5
"Tyrosine protein kinase Ack family",Ack,"enzyme  kinase  protein kinase  tk  ack",NULL,5
"Tyrosine protein kinase Alk family",Alk,"enzyme  kinase  protein kinase  tk  alk",NULL,5
"Tyrosine protein kinase Axl family",Axl,"enzyme  kinase  protein kinase  tk  axl",NULL,5
"Tyrosine protein kinase Csk family",Csk,"enzyme  kinase  protein kinase  tk  csk",NULL,5
"Tyrosine protein kinase DDR family",Ddr,"enzyme  kinase  protein kinase  tk  ddr",NULL,5
"Tyrosine protein kinase EGFR family",Egfr,"enzyme  kinase  protein kinase  tk  egfr",NULL,5
"Tyrosine protein kinase Eph family",Eph,"enzyme  kinase  protein kinase  tk  eph","A large family of receptor protein-tyrosine kinases that are structurally-related. The name of this family of proteins derives from original protein Eph (now called the EPHA1 RECEPTOR), which was named after the cell line it was first discovered in: Erythropoietin-Producing human Hepatocellular carcinoma cell line. Members of this family have been implicated in regulation of cell-cell interactions involved in nervous system patterning and development. [MESH:D036081]",5
"Tyrosine protein kinase Fak family",Fak,"enzyme  kinase  protein kinase  tk  fak","A family of non-receptor, PROLINE-rich protein-tyrosine kinases. [MESH:D051416]",5
"Tyrosine protein kinase Fer family",Fer,"enzyme  kinase  protein kinase  tk  fer",NULL,5
"Tyrosine protein kinase FGFR family",Fgfr,"enzyme  kinase  protein kinase  tk  fgfr","Specific molecular sites or structures on cell membranes that react with FIBROBLAST GROWTH FACTORS (both the basic and acidic forms), their analogs, or their antagonists to elicit or to inhibit the specific response of the cell to these factors. These receptors frequently possess tyrosine kinase activity. [MESH:D017468]",5
"Tyrosine protein kinase InsR family",InsR,"enzyme  kinase  protein kinase  tk  insr",NULL,5
"Tyrosine protein kinase JakA family",Jaka,"enzyme  kinase  protein kinase  tk  jaka","A family of intracellular tyrosine kinases that participate in the signaling cascade of cytokines by associating with specific CYTOKINE RECEPTORS. They act upon STAT TRANSCRIPTION FACTORS in signaling pathway referred to as the JAK/STAT pathway. The name Janus kinase refers to the fact the proteins have two phosphate-transferring domains. [MESH:D053612]",5
"Tyrosine protein kinase JakB family",Jakb,"enzyme  kinase  protein kinase  tk  jakb","A family of intracellular tyrosine kinases that participate in the signaling cascade of cytokines by associating with specific CYTOKINE RECEPTORS. They act upon STAT TRANSCRIPTION FACTORS in signaling pathway referred to as the JAK/STAT pathway. The name Janus kinase refers to the fact the proteins have two phosphate-transferring domains. [MESH:D053612]",5
"Tyrosine protein kinase Met family",Met,"enzyme  kinase  protein kinase  tk  met",NULL,5
"Tyrosine protein kinase Musk family",Musk,"enzyme  kinase  protein kinase  tk  musk",NULL,5
"Tyrosine protein kinase PDGFR family",Pdgfr,"enzyme  kinase  protein kinase  tk  pdgfr","Specific receptors on cell membranes that react with PLATELET-DERIVED GROWTH FACTOR, its analogs, or antagonists. The alpha PDGF receptor (RECEPTOR, PLATELET-DERIVED GROWTH FACTOR ALPHA) and the beta PDGF receptor (RECEPTOR, PLATELET-DERIVED GROWTH FACTOR BETA) are the two principle types of PDGF receptors. Activation of the protein-tyrosine kinase activity of the receptors occurs by ligand-induced dimerization or heterodimerization of PDGF receptor types. [MESH:D017479]",5
"Tyrosine protein kinase Ret family",Ret,"enzyme  kinase  protein kinase  tk  ret","Receptor protein-tyrosine kinases involved in the signaling of GLIAL CELL-LINE DERIVED NEUROTROPHIC FACTOR ligands. They contain an extracellular cadherin domain and form a receptor complexes with GDNF RECEPTORS. Mutations in ret protein are responsible for HIRSCHSPRUNG DISEASE and MULTIPLE ENDOCRINE NEOPLASIA TYPE 2. [MESH:D051096]",5
"Tyrosine protein kinase Sev family",Sev,"enzyme  kinase  protein kinase  tk  sev",NULL,5
"Tyrosine protein kinase Src family",Src,"enzyme  kinase  protein kinase  tk  src","A PROTEIN-TYROSINE KINASE family that was originally identified by homology to the Rous sarcoma virus ONCOGENE PROTEIN PP60(V-SRC). They interact with a variety of cell-surface receptors and participate in intracellular signal transduction pathways. Oncogenic forms of src-family kinases can occur through altered regulation or expression of the endogenous protein and by virally encoded src (v-src) genes. [MESH:D019061]",5
"Tyrosine protein kinase Syk family",Syk,"enzyme  kinase  protein kinase  tk  syk",NULL,5
"Tyrosine protein kinase Tec family",Tec,"enzyme  kinase  protein kinase  tk  tec",NULL,5
"Tyrosine protein kinase Tie family",Tie,"enzyme  kinase  protein kinase  tk  tie","A family of structurally-related tyrosine kinase receptors that are expressed predominantly in ENDOTHELIAL CELLS and are essential for development of BLOOD VESSELS (NEOVASCULARIZATION, PHYSIOLOGIC). The name derives from the fact that they are tyrosine kinases that contain Ig and EGF domains. [MESH:D042764]",5
"Tyrosine protein kinase Trk family",Trk,"enzyme  kinase  protein kinase  tk  trk","Cell surface receptors that bind NERVE GROWTH FACTOR; (NGF) and a NGF-related family of neurotrophic factors that includes neurotrophins, BRAIN-DERIVED NEUROTROPHIC FACTOR and CILIARY NEUROTROPHIC FACTOR. [MESH:D017475]",5
"Tyrosine protein kinase VEGFR family",Vegfr,"enzyme  kinase  protein kinase  tk  vegfr","A family of closely related RECEPTOR PROTEIN-TYROSINE KINASES that bind vascular endothelial growth factors. They share a cluster of seven extracellular Ig-like domains which are important for ligand binding. They are highly expressed in vascular endothelial cells and are critical for the physiological and pathological growth, development and maintenance of blood and lymphatic vessels. [MESH:D040262]",5
"Vasoactive intestinal peptide receptor","Vasoactive intestinal peptide receptor","membrane receptor  7tm2  peptide  vasoactive intestinal peptide receptor  vasoactive intestinal peptide receptor","Cell surface proteins that bind VASOACTIVE INTESTINAL PEPTIDE; (VIP); with high affinity and trigger intracellular changes which influence the behavior of cells. [MESH:D018005]",5
"Vasopressin and oxytocin receptor","Vasopressin and oxytocin receptor","membrane receptor  7tm1  peptide  short peptide  vasopressin and oxytocin receptor","Specific molecular sites or proteins on or in cells to which VASOPRESSINS bind or interact in order to modify the function of the cells. Two types of vasopressin receptor exist, the V1 receptor in the vascular smooth muscle and the V2 receptor in the kidneys. The V1 receptor can be subdivided into V1a and V1b (formerly V3) receptors. [MESH:D017483]",5
"XC chemokine receptor","XC chemokine receptor","membrane receptor  7tm1  peptide  chemokine receptor  xc chemokine receptor",NULL,5
"AGC protein kinase BARK subfamily",Bark,"enzyme  kinase  protein kinase  agc  grk  bark","G-protein-coupled receptor kinases that mediate agonist-dependent PHOSPHORYLATION and desensitization of BETA-ADRENERGIC RECEPTORS. [MESH:D051552]",6
"AGC protein kinase CRIK subfamily",Crik,"enzyme  kinase  protein kinase  agc  dmpk  crik",NULL,6
"AGC protein kinase GEK subfamily",Gek,"enzyme  kinase  protein kinase  agc  dmpk  gek",NULL,6
"AGC protein kinase GRK subfamily",Grk,"enzyme  kinase  protein kinase  agc  grk  grk",NULL,6
"AGC protein kinase MSK subfamily",Msk,"enzyme  kinase  protein kinase  agc  rsk  msk",NULL,6
"AGC protein kinase p70 subfamily",p70,"enzyme  kinase  protein kinase  agc  rsk  p70","A family of ribosomal protein S6 kinases that are considered the major physiological kinases for RIBOSOMAL PROTEIN S6. Unlike RIBOSOMAL PROTEIN S6 KINASES, 90KDa the proteins in this family are sensitive to the inhibitory effects of RAPAMYCIN and contain a single kinase domain. They are referred to as 70kDa proteins, however ALTERNATIVE SPLICING of mRNAs for proteins in this class also results in 85kDa variants being formed. [MESH:D038762]",6
"AGC protein kinase PKC alpha subfamily",Alpha,"enzyme  kinase  protein kinase  agc  pkc  alpha","A cytoplasmic serine threonine kinase involved in regulating CELL DIFFERENTIATION and CELLULAR PROLIFERATION. Overexpression of this enzyme has been shown to promote PHOSPHORYLATION of BCL-2 PROTO-ONCOGENE PROTEINS and chemoresistance in human acute leukemia cells. [MESH:D051571]",6
"AGC protein kinase PKC delta subfamily",Delta,"enzyme  kinase  protein kinase  agc  pkc  delta","A ubiquitously expressed protein kinase that is involved in a variety of cellular SIGNAL PATHWAYS. Its activity is regulated by a variety of signaling protein tyrosine kinase. [MESH:D051745]",6
"AGC protein kinase PKC eta subfamily",Eta,"enzyme  kinase  protein kinase  agc  pkc  eta",NULL,6
"AGC protein kinase PKC iota subfamily",Iota,"enzyme  kinase  protein kinase  agc  pkc  iota",NULL,6
"AGC protein kinase PKC theta",Theta,"enzyme  kinase  protein kinase  agc  pkc  theta",NULL,6
"AGC protein kinase PKC unclassified",Pkc-Unclassified,"enzyme  kinase  protein kinase  agc  pkc  pkc-unclassified",NULL,6
"AGC protein kinase ROCK subfamily",Rock,"enzyme  kinase  protein kinase  agc  dmpk  rock","A group of intracellular-signaling serine threonine kinases that bind to RHO GTP-BINDING PROTEINS. They were originally found to mediate the effects of rhoA GTP-BINDING PROTEIN on the formation of STRESS FIBERS and FOCAL ADHESIONS. Rho-associated kinases have specificity for a variety of substrates including MYOSIN-LIGHT-CHAIN PHOSPHATASE and LIM KINASES. [MESH:D054460]",6
"AGC protein kinase RSK subfamily",Rsk,"enzyme  kinase  protein kinase  agc  rsk  rsk","A family of ribosomal protein S6 kinases that are structurally distinguished from RIBOSOMAL PROTEIN S6 KINASES, 70-KDA by their apparent molecular size and the fact they contain two functional kinase domains. Although considered RIBOSOMAL PROTEIN S6 KINASES, members of this family are activated via the MAP KINASE SIGNALING SYSTEM and have been shown to act on a diverse array of substrates that are involved in cellular regulation such as RIBOSOMAL PROTEIN S6 and CAMP RESPONSE ELEMENT-BINDING PROTEIN. [MESH:D038744]",6
"AGC protein kinase RSKp70",Rskp70,"enzyme  kinase  protein kinase  agc  rsk  rskp70","A family of ribosomal protein S6 kinases that are considered the major physiological kinases for RIBOSOMAL PROTEIN S6. Unlike RIBOSOMAL PROTEIN S6 KINASES, 90KDa the proteins in this family are sensitive to the inhibitory effects of RAPAMYCIN and contain a single kinase domain. They are referred to as 70kDa proteins, however ALTERNATIVE SPLICING of mRNAs for proteins in this class also results in 85kDa variants being formed. [MESH:D038762]",6
"Aspartic protease A22A regulatory subfamily",Reg,"enzyme  protease  aspartic  ad  a22a  reg",NULL,6
"Atypical protein kinase ABC1-A subfamily",Abc1-A,"enzyme  kinase  protein kinase  atypical  abc1  abc1-a",NULL,6
"Atypical protein kinase FRAP subfamily",Frap,"enzyme  kinase  protein kinase  atypical  pikk  frap",NULL,6
"Atypical protein kinase RIO1 subfamily",Rio1,"enzyme  kinase  protein kinase  atypical  rio  rio1",NULL,6
"Atypical protein kinase RIO2 subfamily",Rio2,"enzyme  kinase  protein kinase  atypical  rio  rio2",NULL,6
"Atypical protein kinase RIO3 subfamily",Rio3,"enzyme  kinase  protein kinase  atypical  rio  rio3",NULL,6
"CAMK protein kinase AMPK subfamily",Ampk,"enzyme  kinase  protein kinase  camk  camkl  ampk","Intracellular signaling protein kinases that play a signaling role in the regulation of cellular energy metabolism. Their activity largely depends upon the concentration of cellular AMP which is increased under conditions of low energy or metabolic stress. AMP-activated protein kinases modify enzymes involved in LIPID METABOLISM, which in turn provide substrates needed to convert AMP into ATP. [MESH:D055372]",6
"CAMK protein kinase BRSK subfamily",Brsk,"enzyme  kinase  protein kinase  camk  camkl  brsk",NULL,6
"CAMK protein kinase CHK1 subfamily",Chk1,"enzyme  kinase  protein kinase  camk  camkl  chk1",NULL,6
"CAMK protein kinase LKB subfamily",Lkb,"enzyme  kinase  protein kinase  camk  camkl  lkb",NULL,6
"CAMK protein kinase MAPKAPK subfamily",Mapkapk,"enzyme  kinase  protein kinase  camk  mapkapk  mapkapk",NULL,6
"CAMK protein kinase MARK subfamily",Mark,"enzyme  kinase  protein kinase  camk  camkl  mark",NULL,6
"CAMK protein kinase MELK subfamily",Melk,"enzyme  kinase  protein kinase  camk  camkl  melk",NULL,6
"CAMK protein kinase MNK subfamily",Mnk,"enzyme  kinase  protein kinase  camk  mapkapk  mnk",NULL,6
"CAMK protein kinase MSKb subfamily",Mskb,"enzyme  kinase  protein kinase  camk  rskb  mskb",NULL,6
"CAMK protein kinase NIM1 subfamily",Nim1,"enzyme  kinase  protein kinase  camk  camkl  nim1",NULL,6
"CAMK protein kinase NuaK subfamily",Nuak,"enzyme  kinase  protein kinase  camk  camkl  nuak",NULL,6
"CAMK protein kinase PASK subfamily",Pask,"enzyme  kinase  protein kinase  camk  camkl  pask",NULL,6
"CAMK protein kinase QIK subfamily",Qik,"enzyme  kinase  protein kinase  camk  camkl  qik",NULL,6
"CAMK protein kinase RSKb subfamily",Rskb,"enzyme  kinase  protein kinase  camk  rskb  rskb","A family of ribosomal protein S6 kinases that are structurally distinguished from RIBOSOMAL PROTEIN S6 KINASES, 70-KDA by their apparent molecular size and the fact they contain two functional kinase domains. Although considered RIBOSOMAL PROTEIN S6 KINASES, members of this family are activated via the MAP KINASE SIGNALING SYSTEM and have been shown to act on a diverse array of substrates that are involved in cellular regulation such as RIBOSOMAL PROTEIN S6 and CAMP RESPONSE ELEMENT-BINDING PROTEIN. [MESH:D038744]",6
"CK1 protein kinase CK1-a",Ck1-a,"enzyme  kinase  protein kinase  ck1  ck1  ck1-a","A casein kinase I isoenzyme that plays a role in intracellular signaling pathways including the WNT SIGNALING PATHWAY, the CELL CYCLE, membrane trafficking, and RNA processing. Multiple isoforms of casein kinase I alpha exist and are due to ALTERNATIVE SPLICING. [MESH:D048128]",6
"CK1 protein kinase CK1-g",Ck1-g,"enzyme  kinase  protein kinase  ck1  ck1  ck1-g",NULL,6
"CMGC protein kinase CDC2 subfamily",Cdc2,"enzyme  kinase  protein kinase  cmgc  cdk  cdc2","Phosphoprotein with protein kinase activity that functions in the G2/M phase transition of the CELL CYCLE. It is the catalytic subunit of the MATURATION-PROMOTING FACTOR and complexes with both CYCLIN A and CYCLIN B in mammalian cells. The maximal activity of cyclin-dependent kinase 1 is achieved when it is fully dephosphorylated. [MESH:D016203]",6
"CMGC protein kinase CDK2",Cdk2,"enzyme  kinase  protein kinase  cmgc  cdk  cdk2",NULL,6
"CMGC protein kinase CDK5 subfamily",Cdk5,"enzyme  kinase  protein kinase  cmgc  cdk  cdk5","A serine-threonine kinase that plays important roles in CELL DIFFERENTIATION; CELL MIGRATION; and CELL DEATH of NERVE CELLS. It is closely related to other CYCLIN-DEPENDENT KINASES but does not seem to participate in CELL CYCLE regulation. [MESH:D051360]",6
"CMGC protein kinase CDK7 subfamily",Cdk7,"enzyme  kinase  protein kinase  cmgc  cdk  cdk7",NULL,6
"CMGC protein kinase CDK8 subfamily",Cdk8,"enzyme  kinase  protein kinase  cmgc  cdk  cdk8","A CYCLIN C dependent kinase that is an important component of the mediator complex. The enzyme is activated by its interaction with CYCLIN C and plays a role in transcriptional regulation by phosphorylating RNA POLYMERASE II. [MESH:D056850]",6
"CMGC protein kinase CDK9 subfamily",Cdk9,"enzyme  kinase  protein kinase  cmgc  cdk  cdk9","A multifunctional CDC2 kinase-related kinase that plays roles in transcriptional elongation, CELL DIFFERENTIATION, and APOPTOSIS. It is found associated with CYCLIN T and is a component of POSITIVE TRANSCRIPTIONAL ELONGATION FACTOR B. [MESH:D042863]",6
"CMGC protein kinase Dyrk1 subfamily",Dyrk1,"enzyme  kinase  protein kinase  cmgc  dyrk  dyrk1",NULL,6
"CMGC protein kinase Dyrk2 subfamily",Dyrk2,"enzyme  kinase  protein kinase  cmgc  dyrk  dyrk2",NULL,6
"CMGC protein kinase ERK subfamily",Erk,"enzyme  kinase  protein kinase  cmgc  mapk  erk","A mitogen-activated protein kinase subfamily that is widely expressed and plays a role in regulation of MEIOSIS; MITOSIS; and post mitotic functions in differentiated cells. The extracellular signal regulated MAP kinases are regulated by a broad variety of CELL SURFACE RECEPTORS and can be activated by certain CARCINOGENS. [MESH:D048049]",6
"CMGC protein kinase ERK1",Erk1,"enzyme  kinase  protein kinase  cmgc  mapk  erk1",NULL,6
"CMGC protein kinase ERK3",Erk3,"enzyme  kinase  protein kinase  cmgc  mapk  erk3",NULL,6
"CMGC protein kinase ERK5",Erk5,"enzyme  kinase  protein kinase  cmgc  mapk  erk5",NULL,6
"CMGC protein kinase HIPK subfamily",Hipk,"enzyme  kinase  protein kinase  cmgc  dyrk  hipk",NULL,6
"CMGC protein kinase JNK subfamily",Jnk,"enzyme  kinase  protein kinase  cmgc  mapk  jnk","A subgroup of mitogen-activated protein kinases that activate TRANSCRIPTION FACTOR AP-1 via the phosphorylation of C-JUN PROTEINS. They are components of intracellular signaling pathways that regulate CELL PROLIFERATION; APOPTOSIS; and CELL DIFFERENTIATION. [MESH:D048031]",6
"CMGC protein kinase MAK",Mak,"enzyme  kinase  protein kinase  cmgc  rck  mak",NULL,6
"CMGC protein kinase nmo subfamily",nmo,"enzyme  kinase  protein kinase  cmgc  mapk  nmo",NULL,6
"CMGC protein kinase p38 subfamily",p38,"enzyme  kinase  protein kinase  cmgc  mapk  p38","A mitogen-activated protein kinase subfamily that regulates a variety of cellular processes including CELL GROWTH PROCESSES; CELL DIFFERENTIATION; APOPTOSIS; and cellular responses to INFLAMMATION. The P38 MAP kinases are regulated by CYTOKINE RECEPTORS and can be activated in response to bacterial pathogens. [MESH:D048051]",6
"CMGC protein kinase PCTAIRE",Pctaire,"enzyme  kinase  protein kinase  cmgc  cdk  pctaire",NULL,6
"CMGC protein kinase PFTAIRE",Pftaire,"enzyme  kinase  protein kinase  cmgc  cdk  pftaire",NULL,6
"CMGC protein kinase PITSLRE subfamily",Pitslre,"enzyme  kinase  protein kinase  cmgc  cdk  pitslre",NULL,6
"CMGC protein kinase TAIRE subfamily",Taire,"enzyme  kinase  protein kinase  cmgc  cdk  taire",NULL,6
"CMGC protein kinase unclassified CDK subfamily",Cdk-Unclassified,"enzyme  kinase  protein kinase  cmgc  cdk  cdk-unclassified",NULL,6
"Cysteine protease C14A subfamily",C14A,"enzyme  protease  cysteine  cd  c14  c14a","A family of intracellular CYSTEINE ENDOPEPTIDASES that play a role in regulating INFLAMMATION and APOPTOSIS. They specifically cleave peptides at a CYSTEINE amino acid that follows an ASPARTIC ACID residue. Caspases are activated by proteolytic cleavage of a precursor form to yield large and small subunits that form the enzyme. Since the cleavage site within precursors matches the specificity of caspases, sequential activation of precursors by activated caspases can occur. [MESH:D020169]",6
"Cysteine protease C2 regulatory subfamily",Reg,"enzyme  protease  cysteine  ca  c2  reg",NULL,6
"Metallo protease M14B regulatory subfamily",Reg,"enzyme  protease  metallo  mc  m14b  reg",NULL,6
"Metallo protease M15D subfamily",M15D,"enzyme  protease  metallo  md  m15  m15d",NULL,6
"Metallo protease M28A subfamily",M28A,"enzyme  protease  metallo  mh  m28  m28a",NULL,6
"Metallo protease M28B subfamily",M28B,"enzyme  protease  metallo  mh  m28  m28b",NULL,6
"Metallo protease M67A subfamily",M67A,"enzyme  protease  metallo  mp  m67  m67a",NULL,6
"Other protein kinase GCN2 subfamily",Gcn2,"enzyme  kinase  protein kinase  other  pek  gcn2",NULL,6
"Other protein kinase HRI",Hri,"enzyme  kinase  protein kinase  other  pek  hri",NULL,6
"Other protein kinase Meta subfamily",Meta,"enzyme  kinase  protein kinase  other  camkk  meta",NULL,6
"Other protein kinase Nek1",Nek1,"enzyme  kinase  protein kinase  other  nek  nek1",NULL,6
"Other protein kinase Nek11",Nek11,"enzyme  kinase  protein kinase  other  nek  nek11",NULL,6
"Other protein kinase PEK subfamily",Pek,"enzyme  kinase  protein kinase  other  pek  pek",NULL,6
"Other protein kinase PKR",Pkr,"enzyme  kinase  protein kinase  other  pek  pkr",NULL,6
"Other protein kinase PLK2",Plk2,"enzyme  kinase  protein kinase  other  plk  plk2",NULL,6
"Other protein kinase WEE1",Wee1,"enzyme  kinase  protein kinase  other  wee  wee1",NULL,6
"Serine protease S29 regulatory subfamily",Reg,"enzyme  protease  serine  pas  s29  reg",NULL,6
"STE protein kinase ASK",Ask,"enzyme  kinase  protein kinase  ste  ste11  ask",NULL,6
"STE protein kinase FRAY subfamily",Fray,"enzyme  kinase  protein kinase  ste  ste20  fray",NULL,6
"STE protein kinase KHS subfamily",Khs,"enzyme  kinase  protein kinase  ste  ste20  khs",NULL,6
"STE protein kinase MEKK2",Mekk2,"enzyme  kinase  protein kinase  ste  ste11  mekk2",NULL,6
"STE protein kinase MSN subfamily",Msn,"enzyme  kinase  protein kinase  ste  ste20  msn",NULL,6
"STE protein kinase MST subfamily",Mst,"enzyme  kinase  protein kinase  ste  ste20  mst",NULL,6
"STE protein kinase NinaC subfamily",NinaC,"enzyme  kinase  protein kinase  ste  ste20  ninac",NULL,6
"STE protein kinase PAKA subfamily",Paka,"enzyme  kinase  protein kinase  ste  ste20  paka",NULL,6
"STE protein kinase PAKB subfamily",Pakb,"enzyme  kinase  protein kinase  ste  ste20  pakb",NULL,6
"STE protein kinase SLK subfamily",Slk,"enzyme  kinase  protein kinase  ste  ste20  slk",NULL,6
"STE protein kinase TAO subfamily",Tao,"enzyme  kinase  protein kinase  ste  ste20  tao",NULL,6
"STE protein kinase YSK subfamily",Ysk,"enzyme  kinase  protein kinase  ste  ste20  ysk",NULL,6
"TKL protein kinase HH498 subfamily",HH498,"enzyme  kinase  protein kinase  tkl  mlk  hh498",NULL,6
"TKL protein kinase ILK subfamily",Ilk,"enzyme  kinase  protein kinase  tkl  mlk  ilk",NULL,6
"TKL protein kinase LIMK subfamily",Limk,"enzyme  kinase  protein kinase  tkl  lisk  limk","Serine protein kinases involved in the regulation of ACTIN polymerization and MICROTUBULE disassembly. Their activity is regulated by phosphorylation of a threonine residue within the activation loop by intracellular signaling kinases such as P21-ACTIVATED KINASES and by RHO KINASE. [MESH:D054461]",6
"TKL protein kinase LZK subfamily",Lzk,"enzyme  kinase  protein kinase  tkl  mlk  lzk",NULL,6
"TKL protein kinase MLK subfamily",Mlk,"enzyme  kinase  protein kinase  tkl  mlk  mlk",NULL,6
"TKL protein kinase STKR Type 1 subfamily",Type1,"enzyme  kinase  protein kinase  tkl  stkr  type1",NULL,6
"TKL protein kinase STKR Type 2 subfamily",Type2,"enzyme  kinase  protein kinase  tkl  stkr  type2",NULL,6
"TKL protein kinase STKR1",Stkr1,"enzyme  kinase  protein kinase  tkl  stkr  stkr1",NULL,6
"TKL protein kinase TAK1 subfamily",Tak1,"enzyme  kinase  protein kinase  tkl  mlk  tak1",NULL,6
"TKL protein kinase TESK subfamily",Tesk,"enzyme  kinase  protein kinase  tkl  lisk  tesk",NULL,6
"Tyrosine protein kinase SrcA",SrcA,"enzyme  kinase  protein kinase  tk  src  srca",NULL,6
"Tyrosine protein kinase Srm",Srm,"enzyme  kinase  protein kinase  tk  src  srm",NULL,6


"""