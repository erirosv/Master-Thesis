# Microarray data experiment
one-channel microarray experiment, a single sample is labeled with a fluorescent dye (in this case, biotinylated UTP) and hybridized to the microarray slide. The detection step involves using streptavidin-phycoerythrin to detect the labeled targets on the microarray, followed by scanning the slide to capture the fluorescence signal.

On the other hand, in a two-channel microarray experiment, two different samples are labeled with two different fluorescent dyes (e.g., Cy3 and Cy5), and they are co-hybridized to the microarray slide. The fluorescent signals from both channels are captured and compared to measure the relative gene expression levels between the two samples.

## Datasets

- alon: one-channel experiment using Affymetrix oligonucleotide arrays
- borovecki: one-channel microarray experiment
- Burczynski: one-channel microarray experiment using Affymetrix HG-U133A GeneChip arrays.
- Christensen: Not found
    - Variation in tissue-specific methylation relative to differences between tissue types was first explored visually. Scatter plots of methylation values for representative samples from two different tissues were less well correlated than similar plots of two representative samples from the same tissue type, though variation in tissue-specific methylation was also evident (Figure S1). Tissue-specific methylation patterns for adult blood, lung, and pleural tissue samples were then modeled with RPMM to investigate potential associations of age and exposures with methylation profiles. An RPMM of adult bloods (n = 30) resulted in two methylation classes 
    - Two samples missing age data.
- Chin : not specified
- Chowdary: suggest one-channel
- Chiaretti: 

## Single channel

Normalization methods adjust the intensity values to make them comparable across different microarrays within an experiment, allowing meaningful comparisons between samples.

In microarray experiments using the one-channel approach:

Extract and label nucleic acids: Target nucleic acids from samples are labeled with a fluorescent dye.

Hybridize to microarray: The labeled nucleic acids are applied to a microarray slide containing DNA probes. They bind to their complementary probes, forming hybridization complexes.

Scan the microarray: The slide is scanned to measure the fluorescence intensity of each spot, representing gene expression levels.

Analyze the data: Images are analyzed to extract quantitative data. Normalization is applied to account for variations, and statistical analyses are performed to identify differentially expressed genes and explore gene expression patterns.

The one-channel approach provides valuable insights into gene expression and is widely used in genomics research.

## Comprehensive one-channel
n microarray experiments, the one-channel approach refers to a type of data acquisition method used to gather gene expression data. In this approach, a single fluorescent dye is used to label the target nucleic acids (usually cDNA or cRNA), which are then hybridized to the microarray slide containing immobilized DNA probes.

Here's a step-by-step overview of the process of gathering a microarray dataset using the one-channel approach:

Sample preparation: The first step is to extract the target nucleic acids (cDNA or cRNA) from the biological samples of interest. These samples can be derived from different tissues, cell types, or experimental conditions, depending on the study objectives.

Labeling: The target nucleic acids are labeled with a fluorescent dye. The most commonly used dyes are Cy3 (green) or Cy5 (red), but other fluorescent dyes can also be used. The choice of dye depends on the experimental design and the particular microarray platform being used.

Hybridization: The labeled target nucleic acids are then hybridized to the microarray slide. The slide contains an array of small DNA spots, each representing a specific gene or DNA sequence. The labeled targets bind to their complementary DNA probes on the slide, forming stable hybridization complexes.

Scanning: After hybridization, the microarray slide is scanned using a microarray scanner. The scanner measures the fluorescence intensity of each spot on the slide, capturing the signal emitted by the labeled targets bound to the DNA probes. The signal intensity represents the abundance of the corresponding gene in the sample.

Image analysis: The scanned images are subjected to image analysis to extract quantitative data from the microarray spots. This involves identifying and locating each spot on the slide and measuring the fluorescence intensity.

Data normalization: To account for experimental variations and technical biases, data normalization is performed. Normalization methods adjust the intensity values to make them comparable across different microarrays within an experiment, allowing meaningful comparisons between samples.

Data analysis: Once the microarray data is normalized, various statistical and bioinformatic analyses can be applied to identify differentially expressed genes, perform clustering or classification, and explore gene expression patterns associated with specific conditions or treatments.

It's important to note that the one-channel approach is just one of the methods used in microarray experiments. Another commonly used approach is the two-channel approach, where two different fluorescent dyes are used to label two different samples, allowing for direct comparison of gene expression levels between the two samples.

Microarray datasets obtained using the one-channel approach have been widely used in genomics research to gain insights into gene expression patterns and to study various biological phenomena, such as disease mechanisms, drug responses, and developmental processes.