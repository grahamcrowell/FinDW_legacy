# Base Layer

Input: SQL, flat file, ?denodo?

Output: model

- LogicalDataField
  - SourceIdentifier
    - RecordIdentifier NK
    - DegenerateDim DD
    - HierarchyKey HK
      - SelfReferenceKey SRK
      - ForeignReferenceKey FRK 
  - SourceDimLookup DL
  - SourceFact F

# LogicalDataField
  + Name
  + PhysicalDataColumnList : List\<PhysicalDataColumn\>
  + FieldColumnExpression

# RecordIdentifier

Uniquely identifies a source data row/record

Primary/natural/business key

SQL constraint: `COUNT(*) = COUNT(DISTINCT FieldColumnExpression)`

Examples: SourceReferralID, SourceAssessmentHeaderID, VisitID

# HierarchyReferenceKey

Reference to another field in the model

## Self Reference Key

Implements recursive self join

# DegenerateDim

