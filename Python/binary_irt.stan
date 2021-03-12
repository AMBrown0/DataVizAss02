data {
  // numbers of things
  int<lower=1> R;  // responses
  int<lower=1> I;  // items
  int<lower=1> S;  // subjects
  // data
  int<lower=1,upper=I> item[R];
  int<lower=1,upper=S> subject[R];
  int<lower=0,upper=1> grade[R];
}
parameters {
  // parameters
  vector[S] ability;
  vector[I] difficulty;
  // hyperparameters
  real mu_difficulty;
  real<lower=0> sigma_difficulty;
  real<lower=0> sigma_ability;
}
model {
  // priors
  ability ~ normal(0, sigma_ability);
  difficulty ~ normal(0, sigma_difficulty);
  mu_difficulty ~ cauchy(0, 5);
  // data model
  grade ~ bernoulli_logit(ability[subject] - difficulty[item] - mu_difficulty);
}
