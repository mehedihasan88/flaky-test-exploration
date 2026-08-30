# Flaky Test Exploration

This repository contains a small hands-on experiment using **IDoFT, iDFlakies, and NonDex** on Alibaba Fastjson. We wrote scripts to search the IDoFT dataset for a project containing multiple **order-dependent (OD)** and **implementation-dependent (ID)** flaky tests at the **same commit**, reducing repeated build/setup effort and allowing us to focus on tool behavior. From Fastjson, we selected one OD test and one ID test, inspected their failure mechanisms, manually reproduced the OD behavior, and then verified both cases with the corresponding tools. We also explored advanced features such as **targeted test orders and randomized rounds in iDFlakies**, and **multiple seeds and debug-point localization in NonDex**.

## iDFlakies — OD Test

**Test:** `DateTest_tz.test_codec`

**Procedure**

* Baseline: `mvn -Dtest=DateTest_tz test`
* Manually ran `TimestampTest` and `DateTest_tz` in both orders using JUnit.
* Ran iDFlakies with a targeted two-test order and `5` randomized rounds.

**Finding**

* `DateTest_tz` alone → **FAIL**
* `TimestampTest -> DateTest_tz` → **PASS**
* Reverse order → **FAIL**
* iDFlakies classified the test as **OD** and identified `TimestampTest.test_0` in the passing order.
* Root cause: shared mutable `JSON.defaultTimeZone`.

## NonDex — ID Test

**Test:** `Bug_for_smoothrat6.test_set`

**Procedure**

* Baseline: `mvn -Dtest=Bug_for_smoothrat6 test`
* Ran NonDex first with default settings, then with `-DnondexRuns=20`.
* Used `nondex:debug` to localize the nondeterministic invocation.

**Finding**

* Normal execution → `Set[3L,4L]` → **PASS**
* Several NonDex seeds produced `Set[4L,3L]` → **FAIL**
* NonDex debug traced the failure to `HashSet.iterator` during Fastjson serialization.
* Root cause: the test assumes a fixed `HashSet` iteration order, which Java does not guarantee.

## Overall

The experiments reproduced two different flaky-test mechanisms: **test-order/shared-state dependence** with iDFlakies and **implementation-dependent API behavior** with NonDex.
