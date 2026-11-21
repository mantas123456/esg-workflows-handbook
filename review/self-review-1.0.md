# Self-review before 1.0

Date: 21 November 2026. Version reviewed: 0.6 (tag `v0.6`).

This is a **desk review by the handbook's author**, reading the tracks in
turn as three reviewers would: a CBAM customs specialist, a GHG verifier
and a CSRD limited-assurance provider. It is not an independent review. No
fact was re-checked against its source during this review; findings marked
**fact check** need a source read before they are fixed. Nothing has been
fixed yet (prompt 7.1).

**Severity**

- **Critical**: a wrong rule or number that could lead a reader to a wrong
  filing, declaration or report. *None found.*
- **Major**: a missing requirement, a fact stated on weaker evidence than
  the page suggests, or two tracks that tell the reader different things.
- **Minor**: unclear wording, a missing detail, a small inconsistency.

Each finding has an id so it can be approved for 7.2.

## Summary

| Reviewer | Critical | Major | Minor |
|---|---|---|---|
| CBAM customs specialist | 0 | 4 | 5 |
| GHG verifier | 0 | 5 | 5 |
| CSRD limited-assurance provider | 0 | 5 | 5 |
| Cross-cutting | 0 | 1 | 2 |
| **Total** | **0** | **15** | **17** |

The three findings I would fix first:

1. **CBAM-1:** the CBAM pages tell readers to reuse CBAM embedded
   emissions in Scope 3 unchanged, while C5 says to adjust them. Two
   tracks, two answers.
2. **CSRD-1:** C1's scope test ignores groups, although its example is a
   group.
3. **GHG-1:** the Gozo inventory counts the same cold-store emissions in
   two categories on purpose.

---

## 1. CBAM customs specialist (CB1-CB10)

Read: CB1-CB10 and the CBAM parts of F1 and F3.

### Major

**CBAM-1. Reuse sections overstate what CBAM data is worth for Scope 3.**
CB3, CB4 and CB9 ("Reuse in other reports") and F3 (worked example) say
the CBAM embedded emissions can be used as they are in Scope 3, and CB9
calls the declared total "a verified number". But:

- for iron and steel and aluminium, CBAM counts direct emissions only, so
  the figure leaves out electricity (C5 adds it back);
- default values carry a mark-up, which is a penalty, not an emission (C5
  removes it);
- in the Melita example, 80.85 of the 341.65 tCO2e are default values, not
  verified.

C5 handles this correctly; the CBAM pages and F3 contradict it.
*Fix:* align CB3, CB4, CB9 and F3 with C5's two cautions.

**CBAM-2. CB1 may miss exclusions inside chapter 72.** CB1 says iron and
steel cover "chapter 72 as a whole, with listed exceptions (for example
some ferro-alloys)". A customs specialist would expect ferrous waste and
scrap to be named if Annex I excludes them, because importers often bring
both. **Fact check:** read the iron and steel rows of Annex I and list
every exclusion.

**CBAM-3. CB2 may miss the guarantee.** CB2 lists the authorisation
criteria (no serious breaches, financial and operational capacity, EORI).
It does not say whether the competent authority may ask for a guarantee,
for example from an applicant not established for a full set of past
financial years. **Fact check:** Article 17 of Regulation (EU) 2023/956
and Implementing Regulation (EU) 2025/486, as amended.

**CBAM-4. The two numbers that drive the cost cannot be worked out from
the handbook.** The free allocation adjustment (CB8) is shown only as a
made-up value per tonne, and the carbon-price-paid conversion (CB7) is not
modelled. Both are flagged on the pages, but a reader cannot get from
their own goods to a real certificate number. *Fix:* explain the
adjustment formula from Implementing Regulation (EU) 2025/2620 and the
conversion from 2026/2498, with a worked example. **Fact check** both.

### Minor

**CBAM-5. CB2 worked example undersells the 2026 rule.** It says the
transitional rule "covered the 68 tonnes it imported in the first
quarter". It covered every import until the decision took effect on
28 May 2026, so also part of Q2.

**CBAM-6. CB8 rounding.** The page says "the example keeps one decimal
place", but the Q2 2027 holding is shown as 89.25. How the registry rounds
certificates is not covered. **Fact check:** the rounding rule.

**CBAM-7. CB8 sources.** "Regulation (EU) 2023/956, Articles 20, 21, 22,
26 and 31, as amended" links to the amending Regulation (EU) 2025/2083,
not to the consolidated text used elsewhere.

**CBAM-8. CB6 checks only accreditation, scope and period.** A customs
specialist would also check the verification opinion itself (satisfactory
or not) and any site-visit rule. **Fact check:** Implementing Regulation
(EU) 2025/2546.

**CBAM-9. CB9 content and corrections.** The page lists four items in the
declaration. It does not say whether quantities and emissions are given
per installation and country of origin, or how a submitted declaration is
corrected or reviewed. **Fact check:** Articles 6 and 19 and the
implementing rules.

---

## 2. GHG verifier (S1-S9, F2, and the GHG parts of C5)

Read: S1-S9, F2, C5. Not read in this round: V3.

### Major

**GHG-1. Double counting inside the inventory.** Island Cold Store's
emissions appear in category 4 (90 tCO2e, the storage service) and
category 15 (75 tCO2e, the 25% stake), from the same 300 tCO2e. S4 calls
this "counted twice on purpose" and S9 discloses it. A verifier would ask
why the total includes the same emissions twice. **Fact check:** what the
Scope 3 Standard says about double counting between categories of one
inventory. *Fix:* at least show the total with and without the overlap,
or allocate once.

**GHG-2. The GWP set is not stated.** S9 note 10 says all sources "should
use the same IPCC assessment report values; this is checked as factors are
chosen". An inventory must name the GWP values used (for example, which
IPCC report), and the factor register should record them per source.

**GHG-3. Biogenic CO2 is not addressed.** A food processor with farm
inputs and anaerobic digestion of food waste has biogenic CO2 in its value
chain. **Fact check:** whether the Scope 3 Standard and ESRS E1 ask for
biogenic CO2 to be reported separately; add a step and a note to S9.

**GHG-4. Supplier figures without a stated boundary.** S4 step 1 warns
that a supplier's Scope 1 and 2 are not cradle to gate, but the worked
example never says what each of the five suppliers' figures covers, or
what the allocation quantity is (tonnes of which product). A verifier
would ask for both. *Fix:* add a "covers" column (cradle to gate or
Scope 1 and 2 only) and the unit of allocation.

**GHG-5. A final total rests on placeholder factors.** S5 leaves four
factor sources "to choose", and S9 reports **5,780 ± 420 tCO2e** anyway.
The ± does not include the uncertainty of not yet having chosen the factor.
*Fix:* mark those lines as provisional in S9, or widen their uncertainty
and say why.

### Minor

**GHG-6. Correlation ignored in the reported ±.** S9 note 7 admits that
lines sharing DESNZ factors are correlated, so ±7.2% is understated. F2
recommends drawing a shared factor once in Monte Carlo; the worked example
could do that.

**GHG-7. Check the Monte Carlo result.** In F2 the Monte Carlo upper bound
(5,250.2) equals the sum-rule upper bound (5,250.2) to one decimal place.
It is recomputed by a test, but such a close match deserves a second look
(different seed, more draws) before 1.0.

**GHG-8. Unsupported statements in S1.** "Many companies use a control
approach" has no source, and "a control approach is the safer choice"
is advice based on a proposal the page itself calls not final.

**GHG-9. Land use is flagged late.** The Land Sector and Removals Standard
takes effect on 1 January 2027 and may matter most for food companies.
S9 notes it, but S2 (screening) and S4 (methods) should raise it where
the decisions are made.

**GHG-10. C5: what Gozo's "cradle-to-gate" figure contains.** C5 adds
Gozo's Scope 1 and 2 and its categories 1 to 8, which include waste,
business travel and commuting. That is a choice, not a standard boundary
for a product footprint. Say so, or narrow it.

---

## 3. CSRD limited-assurance provider (C1-C9)

Read: C1-C9, the CSRD facts and `data/esrs_datapoints.yml`.

### Major

**CSRD-1. C1 ignores groups and non-EU undertakings.** The example company
is "Mediterranean Logistics Group", but C1 tests it as one company. The
page does not say how the test works for a parent of a group (on
consolidated figures?), for subsidiaries, or for non-EU undertakings with
EU turnover. A group could reach the wrong answer. **Fact check:**
Articles 19a and 29a of Directive 2013/34/EU as amended by Omnibus I, and
the third-country rules.

**CSRD-2. Key facts rest on summaries, not the Official Journal.** EUR-Lex
did not load during 0.5, so these were read through the consolidated CSRD
and secondary sources: Articles 19a, 29a, 29d and 34 (`csrd-management-report`,
`csrd-assurance-scope`), the scope article (`csrd-scope` has no article),
the phase-in years (`esrs-phase-in`), and Scope 2 on both bases
(`esrs-e1-scope2`). The 0.5 acceptance line in DEVELOPMENT_PLAN.md ("all
pages cite the published delegated act article numbers") is not yet met:
most disclosure requirement codes in `esrs_datapoints.yml` are `null`.
**Fact check** all of them.

**CSRD-3. C3's "within the standard" test uses the wrong list.** The cap
is defined by the datapoints in Annex II of Delegated Regulation (EU)
2026/1560. C3 maps questions to `data/vsme_datapoints.yml`, whose basis is
the 2025 Recommendation (`basis: rec-2025`). A question shown as "within"
might not be. **Fact check:** Annex II of 2026/1560.

**CSRD-4. The EU Taxonomy disclosures are missing.** C8 says the assurance
opinion covers them, and C9 says they are tagged, but no page explains what
they are, who must give them after Omnibus I, or how they are prepared.
An assurance provider would expect them in scope. **Fact check:** Article
8 of Regulation (EU) 2020/852 and any Omnibus I changes.

**CSRD-5. Malta remains open.** C1 says the start date of Legal Notice
39 of 2026 was not confirmed and that no Maltese transposition of Omnibus I
was found. Both affect a Maltese company's first year. **Fact check**
before 1.0, and again after 19 March 2027.

### Minor

**CSRD-6. C2 example lacks two things a provider samples.** No time
horizon per item (the IRO register has one, the DMA workbook and page do
not), and no evidence of stakeholder engagement in the worked example.
E1-R1 ("rising fuel and carbon costs") does not say which carbon price
applies to road fuel. **Fact check** if a date is added.

**CSRD-7. C8's provider list will date quickly.** It is labelled practice,
which is right, but the Commission's draft limited assurance standards
(consultation opened 12 November 2026) should be checked against it when
adopted (deadline 1 July 2027).

**CSRD-8. C9 timetable order.** The board approves on 20 March and the
assurance opinion is signed on 25 March. Approval and signing dates
follow national practice; the page should say the order is an assumption.

**CSRD-9. C7 dataset mapping for E5.** `E5-resources-waste` is linked to
`imports_by_cn_code`, which makes no sense for a logistics group whose E5
impact is food waste. The link comes from the datapoint list and should be
`null` or a waste dataset.

**CSRD-10. C6 phase-in column is derived, not read.** "Some datapoints"
is worked out from the words "phase-in applies" in the handbook's own
descriptions. Say so on the page, or replace it with checked entries
(see CSRD-2).

---

## 4. Cross-cutting

### Major

**X-1. No external review.** Every page is `draft`. The 1.0 plan (7.2)
allows `reviewed` only where an external practitioner has reviewed the
page. Until then, 1.0 should say clearly that it is self-reviewed.

### Minor

**X-2. EUR-Lex links are not checked automatically.** EUR-Lex refuses
automated requests (22 links). Open them by hand before 1.0.

**X-3. Next full fact re-check is due by 18 February 2027** (F4). If 1.0 is
tagged later than that, re-check first: the build will warn from that day
and fail from 19 May 2027.

---

## Not covered by this review

- The VSME track (V1-V6), T1 triage, T2 timeline and V3, beyond the
  points above.
- The browser tools and templates beyond what the tests check.
- Accessibility of pages other than the tools.
