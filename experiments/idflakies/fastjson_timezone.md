# Fastjson Order-Dependent Timezone Test

## Subject

Project: Alibaba Fastjson

Commit:

`e05e9c5e4be580691cc55a59f3256595393203a1`

Target test:

`com.alibaba.json.bvt.date.DateTest_tz.test_codec`

IDoFT category: `OD`

## Initial Observation

Running `DateTest_tz` alone produced a failure:

- Expected timestamp: `1461859200000`
- Actual timestamp: `1461866400000`
- Difference: `7200000 ms` (2 hours)

The experiment environment uses `Asia/Dhaka` (UTC+6), while the test expects behavior corresponding to `Asia/Shanghai` (UTC+8).

## Shared-State Investigation

Several Fastjson tests assign:

`JSON.defaultTimeZone = TimeZone.getTimeZone("Asia/Shanghai")`

`TimestampTest.test_0` was selected as a candidate state-setting test because its `setUp()` changes `JSON.defaultTimeZone` to `Asia/Shanghai` and does not restore the previous value.

## Manual Order Reproduction

The two tests were executed directly using JUnit in the same JVM.

### Order 1

`TimestampTest.test_0 -> DateTest_tz.test_codec`

Result:

`PASS`

### Order 2

`DateTest_tz.test_codec -> TimestampTest.test_0`

Result:

`DateTest_tz.test_codec` failed.

This demonstrates that the outcome of `DateTest_tz.test_codec` depends on whether `TimestampTest.test_0` executes first.

## iDFlakies Experiment

Detector:

`random-class-method`

Rounds:

`5`

The original test order contained:

1. `com.alibaba.json.bvt.TimestampTest.test_0`
2. `com.alibaba.json.bvt.date.DateTest_tz.test_codec`

iDFlakies detected:

`com.alibaba.json.bvt.date.DateTest_tz.test_codec`

as an order-dependent test.

The generated `flaky-lists.json` reports:

- Intended preceding test: `TimestampTest.test_0`
- Intended result: `PASS`
- Revealed preceding order: empty
- Revealed result: `ERROR`
- Type: `OD`

## Interpretation

The experiment indicates that `DateTest_tz.test_codec` relies on shared global Fastjson timezone state.

`TimestampTest.test_0` sets `JSON.defaultTimeZone` to `Asia/Shanghai`. When it executes first in the same JVM, `DateTest_tz.test_codec` passes. Without that preceding state-setting test, the target test fails in the experiment environment.

The manual reproduction and iDFlakies detection therefore agree on the same order-dependent behavior.
