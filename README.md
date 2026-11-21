# Pathway-Activity-Benchmarking-Cancer-Classification
Pathway activity inference converts gene-level expression into interpretable features, however the
inference method affects classifier accuracy and the reproducibility of the selected features is
poorly described. We benchmarked five pathway scoring methods (ssGSEA, GSVA, PLAGE, Z-
score and PROGENy) in combination with four different classifiers (Elastic Net logistic
regression, Random Forest, RBF-kernel SVM and XGBoost) for the task of classifying tumour
versus normal in TCGA-BRCA RNA-seq data covering 1096 tumour and 129 normal samples.
We present a batch-aware preprocessing workflow that includes normalization and plate-level
correction, and we evaluate all pipelines by nested cross-validation, resampling based stability
selection and differential activity testing of the selected pathways. Average precision was broadly
similar across the methods and the best model ROC-AUC ranged from 0.781 to 0.798, with
specificity at the default threshold varying more. Elastic Net with ssGSEA or GSVA was the most
reproducible, with Nogueira indices of 0.783 and 0.758, and SVM-RBF was the least stable for
every method, with indices between 0.061 and 0.127. Eight Hallmark pathways, including DNA
repair, G2M checkpoint, were stable in all four Hallmark-based methods and differed considerably
between tumour and normal tissue. Predictive accuracy and feature reproducibility were therefore
diverse properties, as PLAGE combined near-best accuracy with low stability. Elastic Net paired
with ssGSEA, GSVA or Z-score yielded the most reproducible and biologically coherent
signatures. The aim of this study is to provide a rigorous and reproducibility focused comparison
of pathway scoring methods to assist researchers in selecting appropriate methods for their own
data and to highlight the remaining issues in the field.

Co-authors: Syeda Sidra and Ananya Vakkalanka 
