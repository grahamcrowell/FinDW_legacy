# Base Layer

Input: SQL, flat file, ?denodo?

Output: model

- LogicalDataField
  - SourceIdentifier
    - RecordIdentifier 
    - DegenerateDim
    - HierarchyKey
      - SelfReferenceKey
      - ForeignReferenceKey
  - SourceDimLookup
  - SourceFact

# LogicalDataField
  + Name
  + PhysicalDataColumnList : List\<PhysicalDataColumn\>
  + FieldColumnExpression

# SourceKey

Uniquely identifies a source data row/record

Primary/natural/business key

SQL constraint: `COUNT(*) = COUNT(DISTINCT FieldColumnExpression)`

Examples: SourceReferralID, SourceAssessmentHeaderID, VisitID

# HierarchyReferenceKey

Reference to another field in the model

- SourceIdentifierField


# DegenerateDim

