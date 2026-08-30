# Fastjson Implementation-Dependent HashSet Test

## Subject

Project: Alibaba Fastjson

Commit:

`e05e9c5e4be580691cc55a59f3256595393203a1`

Target test:

`com.alibaba.json.bvt.bug.Bug_for_smoothrat6.test_set`

IDoFT category: `ID`

## Baseline

The test was first executed normally using Java 8.

Observed serialized output:

`Set[3L,4L]`

Result:

`PASS`

## NonDex Experiment

Tool:

NonDex Maven Plugin `2.2.1`

Mode:

`FULL`

The initial run using the default 3 shuffled seeds did not expose a failure.

The experiment was then increased to 20 shuffled seeds:

`-DnondexRuns=20`

Several seeds caused the target test to fail.

Observed failing output:

`Set[4L,3L]`

Expected output:

`Set[3L,4L]`

The clean execution continued to pass.

## Failure Mechanism

The target test stores `3L` and `4L` inside a `HashSet` and serializes the set using Fastjson.

The test compares the resulting serialized string against an exact expected order.

NonDex debug narrowed the failure to a nondeterministic invocation involving:

`java.util.HashSet.iterator`

The debug stack also traces the value into Fastjson serialization through:

`com.alibaba.fastjson.serializer.CollectionCodec.write`

Therefore, the observed failure mechanism is:

`HashSet iteration -> Fastjson collection serialization -> exact string comparison`

Under normal execution, the set was serialized as:

`Set[3L,4L]`

Under some NonDex perturbations, iteration changed to:

`Set[4L,3L]`

which caused the assertion to fail.

## Interpretation

The experiment reproduces the implementation-dependent behavior recorded by IDoFT.

The test assumes a deterministic iteration order for a `HashSet`, although that order is not guaranteed by the Java API contract.

NonDex exposes this assumption by exploring another permitted iteration ordering.

Multiple failing debug runs converged on `HashSet.iterator`, supporting the same underlying mechanism.
