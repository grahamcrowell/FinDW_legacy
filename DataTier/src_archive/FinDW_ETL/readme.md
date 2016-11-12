# Business Process 

# Dimension : IField
- IDColumn : IField
- DescColumn : IField
+ TableName


# SourceKey : IField, List<SourceKeyField>

# SourceKeyColumn : IField
- isForiegnKey
- isLocalKey

# IField
- name
- type
- isUnique
- isNullable


every loading folder corresponds to 1 staging table

	%FinDW root%/Data/Loading/<staging_table_name>
staging.<subject_name>
fact.<subject_name>
