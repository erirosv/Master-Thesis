
## Realation for doctors
- Kuroda, Y., & Ohashi, J. (2015). Application of microarray-based gene expression profiling in molecular diagnosis of neurological disorders. Journal of human genetics, 60(11), 601-605.
- Baranzini, S. E., Mudge, J., van Velkinburgh, J. C., Khankhanian, P., Khrebtukova, I., Miller, N. A., ... & Pericak-Vance, M. A. (2010). Genome, epigenome and RNA sequences of monozygotic twins discordant for multiple sclerosis. Nature, 464(7293), 1351-1356.
- Shah, S. J., Nelson, M. R., Li, Y., Kardia, S. L., Urbanek, P., Liu, J., ... & Taylor, K. D. (2015). Genetic architecture of atherosclerosis in mice: a systems genetics analysis of common inbred strains. PLoS genetics, 11(10), e1005711.
- Karnani, N., Taylor, M. S., Malhotra, D., Dutta, A., & Panwar, B. (2011). Meta-analysis of gene expression profiles reveals pleiotropic effects of oncogenic KRAS in the molecular subtypes of human cancer. Journal of molecular biology, 405(4), 885-896.

## Writing
DNA microarray data prevents the use of horizontal parti- tioning because of the small sample size. The distributed methods mentioned above based on vertical partitioning have not been designed specifically for dealing with microarray data, so they do not tackle the particularities of this type of data, such as the high redundancy present among the features. The method proposed in does address these issues, but it has the disadvantage of being computationally expensive by interacting with a classifier to select the genes in each subset. In this work we will propose a distributed filter method, suitable for application to microarray data and with a low computational cost (V. Bolón-Canedo).

Microarrays are tools which are capable of reporting, simultaneously and in a single testing, thousands of gene expression levels. A microarray experiment can be used to analyze samples of cells under different clinical conditions. The information obtained helps to determine the functionality of the genes, and/or helps in under- standing biological processes and the effect of certain treatments. However, all of these activities require analyzing and classifying the samples (D.K.Tasoulis,V.P.Plagianakos,M.N.Vrahatis,Differentialevolutionalgorithms for finding predictive gene subsets in microarray data, in: Artificial Intelligence Applications and Innovations).

n a microarray, the samples are complex, highly dimensional and prone to con- tamination with noise. Therefore, the classification requires special techniques such as Machine Learning (ML) algorithms. These techniques construct a classifier using one of at least two main mechanisms: unsupervised and supervised learning (S.B. Kotsiantis, Supervised machine learning: a review of classification tech- niques, Emerg. Artif. Intell).


Usually, the quantity of samples in microarray experiments is several orders of magnitude lower than the number of genes in the samples. Considering the addi- tional complexity, the ML algorithms are prone to suffer the curse of dimensionality. This anomaly affects both the reliability and the predictive ability of the classifier. To alleviate these effects, the reduction of the number of features by using a feature selection (FS) method must be employed during the classifier’s construction ( H. Liu, H. Motoda, Computational Methods of Feature Selection.) In this paper, the second mechanism is employed because all of the samples have an assigned class value label.

Differential Evolution (DE) is one of the simplest and most effective EAs used to solve high-dimensional optimization problems (K.V. Price, R. Storn, J. Lampinen, Differential Evolution: A Practical Approach to
Global Optimization). In microarray problems, DE could take advantage of the usually small number of the most informative features when initializing the population. Considering all the features arranged into a rank, the initial solutions could include only the most relevant features. However, this ini- tialization of the population could cause a premature lack of diversity, and hence DE could converge to a local optimum. To alleviate this pressure, some initial solutions should be randomly generated.

---

DUMP: 

can you describe how to extract microarray data based on this structure:
- sample, purification, RT, coupling, hybridization and washing, scanning, Normalization and analysing
Use this texts as a base