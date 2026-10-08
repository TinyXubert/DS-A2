# Method note

The estimand is the male-minus-female mean body-mass difference within Adelie penguins in
the sampled setting. The sample contrast describes complete records; inference beyond them
assumes representative selection and an appropriate missingness mechanism. Sex is not randomized.

For group means xbar and ybar, sample variances sx² and sy², and sizes nx and ny, let
a=sx²/nx, b=sy²/ny, d=xbar-ybar. Independence gives SE=sqrt(a+b).
Welch degrees of freedom are (a+b)² / [a²/(nx-1)+b²/(ny-1)]. The 95% interval is d plus/minus
the 97.5th percentile of that t distribution times SE. The two-sided null is a zero contrast.
Welch does not require equal group variances. The t approximation still requires suitable
independent sampling; it is not guaranteed for arbitrary distributions.

The percentile bootstrap independently resamples each sex at its original size and reports
the 2.5th and 97.5th percentiles of 10,000 contrasts. This is a sensitivity analysis, not a
validation of independence or a guarantee of correct coverage in the counterexample.

The planned sampling experiment uses independent normal groups, equal sizes n=40, common
SD=400 g, and true difference 200 g. Their sample-mean difference is exactly normal with
mean 200 and SD sqrt(2*400²/40). The Welch interval has approximately 95% repeated-sampling
coverage. All simulation coverage statements refer to the known synthetic truth.

For the power grid, n is 10, 20, 40, 80 or 160 per group; SD is 250, 400 or 600 g; true
difference is 0, 100, 200 or 400 g. Each combination has 5,000 repetitions. The empirical
rejection rate measures Type I error at zero and power otherwise. Monte Carlo SE is
sqrt(p*(1-p)/5000). The effect grid is not inferred from the observed real-data p-value.

The dependence model is Y=mu+U_cluster+epsilon, with variances rho*sigma² and
(1-rho)*sigma². Clusters are independent of each other, both within and across sex groups. However, observations within the same cluster are correlated when rho is greater than zero. With m records per
cluster and k clusters, Var(group mean)=sigma²*[1+(m-1)*rho]/(km). This follows by summing
m marginal variances and m*(m-1) within-cluster covariances for each of k clusters.

The naive analysis treats km records as independent. The corrected analysis uses the k
independent cluster means. Equal cluster sizes preserve the same estimand and sample mean.
At rho=0 it is a negative control; at rho>0 the comparison isolates dependence without
changing marginal variance. Unknown, unequal or informative real cluster membership would
require additional modeling, not blind application of this correction.

The 200 g threshold is a pedagogical assumption. A zero-null rejection alone does not
establish a practically meaningful difference; compare the interval with the threshold.

References: SciPy ttest_ind documentation (equal_var=False),
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html ;
palmerpenguins data documentation, https://allisonhorst.github.io/palmerpenguins/ .
