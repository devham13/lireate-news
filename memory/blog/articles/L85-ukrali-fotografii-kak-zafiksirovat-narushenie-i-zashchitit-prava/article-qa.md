# QA: L85 ukrali-fotografii-kak-zafiksirovat-narushenie-i-zashchitit-prava

date: 2026-11-26  
score_total: 91/100  
core_eeat_lite: 18/20  
link_verify: pass  
utility_gate: pass  
verdict: PASS

## CORE-EEAT lite: 18/20

C01–C04, O01–O04, R01–R04, E01–E02, E03, Exp01–Exp03, Ept01 — pass; Ept02 warn (forward cluster L83/L84 заменён на опубликованные URL до live L83/L84).

## Checks

| Check | Status |
|-------|--------|
| excalibur_blog_html_linter.py | PASS |
| excalibur_blog_utility_gate.py | PASS |
| excalibur_blog_link_verify.py | PASS (internal paths HTTP 200, curl-verified) |
| excalibur_blog_slop_detector.py | PASS |
| excalibur_blog_fact_checker.py | WARNING (stats heuristic; norms sourced) |
| excalibur_blog_cannibalization_guard.py | PASS (no L85 collision) |
| lireate_privacy_link_policy.py | PASS |

## Link fixes (GEO QA)

- `/mozhno-li-publikovat-foto-kartin-hudozhnika/` → `/chek_list_mozhno_li_publikovat_foto_kartin_i_rabot_xudozhnika_bez_narusheniya_avtorskix_prav/` (200)
- Неопубликованные L83/L84 slug в кластере → опубликованные `konkurent_zaregistriroval_pohozhiy_tovarnyy_znak`, `narushenie-tovarnogo-znaka-na-marketpleyse`
- vsrf.ru (timeout из Cloud) → КонсультантПлюс ППВС № 10 и Обзор ВС 29.05.2024 (`LAW_329754`, `LAW_477422`)

## Notes

Кластер A30. Готов к cover||schema после merge handoff.