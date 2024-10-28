import kfp.compiler as compiler
from kidney_disease_pipeline import kidney_disease_pipeline

# Compile pipeline to a YAML file
compiler.Compiler().compile(
    pipeline_func=kidney_disease_pipeline,
    package_path='../k8s/ml_pipeline/kidney_disease_pipeline.yaml'
)