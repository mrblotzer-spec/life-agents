from autonomous_web_agency.website_auditor import grade_from_score


def test_grade_thresholds():
    assert grade_from_score(95) == "A"
    assert grade_from_score(81) == "B"
    assert grade_from_score(72) == "C"
    assert grade_from_score(60) == "D"
    assert grade_from_score(59) == "F"
