EXPECTED_PLEISTOCENE = {
    "expected_id": "pleistocene",
    "expected_name": "Pleistocene",
    "expected_rank": "Epoch",
    "expected_rank_order": 5,
    "expected_begin_time_ma": 2.58,
    "expected_begin_uncertainty_ma": 0.0,
    "expected_end_time_ma": 0.0117,
    "expected_end_uncertainty_ma": 0.0,
    "expected_parent_id": None
}


EXPECTED_MESOZOIC = {
    "expected_id": "mesozoic",
    "expected_name": "Mesozoic",
    "expected_rank": "Era",
    "expected_rank_order": 3,
    "expected_begin_time_ma": 251.902,
    "expected_begin_uncertainty_ma": 0.024,
    "expected_end_time_ma": 66.0,
    "expected_end_uncertainty_ma": 0.0,
    "expected_parent_id": None
}


EXPECTED_TRIASSIC = {
    "expected_id": "triassic",
    "expected_name": "Triassic",
    "expected_rank": "Period",
    "expected_rank_order": 4,
    "expected_begin_time_ma": 251.902,
    "expected_begin_uncertainty_ma": 0.024,
    "expected_end_time_ma": 201.4,
    "expected_end_uncertainty_ma": 0.2,
    "expected_parent_id": "mesozoic"
}


EXPECTED_JURASSIC = {
    "expected_id": "jurassic",
    "expected_name": "Jurassic",
    "expected_rank": "Period",
    "expected_rank_order": 4,
    "expected_begin_time_ma": 201.4,
    "expected_begin_uncertainty_ma": 0.2,
    "expected_end_time_ma": 143.1,
    "expected_end_uncertainty_ma": 0.6,
    "expected_parent_id": "mesozoic"
}


EXPECTED_EARLY_JURASSIC = {
    "expected_id": "early-jurassic",
    "expected_name": "Early Jurassic",
    "expected_rank": "Epoch",
    "expected_rank_order": 5,
    "expected_begin_time_ma": 201.4,
    "expected_begin_uncertainty_ma": 0.2,
    "expected_end_time_ma": 174.7,
    "expected_end_uncertainty_ma": 0.8,
    "expected_parent_id": "jurassic"
}


EXPECTED_MIDDLE_JURASSIC = {
    "expected_id": "middle-jurassic",
    "expected_name": "Middle Jurassic",
    "expected_rank": "Epoch",
    "expected_rank_order": 5,
    "expected_begin_time_ma": 174.7,
    "expected_begin_uncertainty_ma": 0.8,
    "expected_end_time_ma": 161.5,
    "expected_end_uncertainty_ma": 1.0,
    "expected_parent_id": "jurassic"
}


EXPECTED_AALENIAN = {
    "expected_id": "aalenian",
    "expected_name": "Aalenian",
    "expected_rank": "Age",
    "expected_rank_order": 6,
    "expected_begin_time_ma": 174.7,
    "expected_begin_uncertainty_ma": 0.8,
    "expected_end_time_ma": 170.9,
    "expected_end_uncertainty_ma": 0.8,
    "expected_parent_id": "middle-jurassic"
}


EXPECTED_BAJOCIAN = {
    "expected_id": "bajocian",
    "expected_name": "Bajocian",
    "expected_rank": "Age",
    "expected_rank_order": 6,
    "expected_begin_time_ma": 170.9,
    "expected_begin_uncertainty_ma": 0.8,
    "expected_end_time_ma": 168.2,
    "expected_end_uncertainty_ma": 1.2,
    "expected_parent_id": "middle-jurassic"
}


EXPECTED_BATHONIAN = {
    "expected_id": "bathonian",
    "expected_name": "Bathonian",
    "expected_rank": "Age",
    "expected_rank_order": 6,
    "expected_begin_time_ma": 168.2,
    "expected_begin_uncertainty_ma": 1.2,
    "expected_end_time_ma": 165.3,
    "expected_end_uncertainty_ma": 1.1,
    "expected_parent_id": "middle-jurassic"
}


EXPECTED_CALLOVIAN = {
    "expected_id": "callovian",
    "expected_name": "Callovian",
    "expected_rank": "Age",
    "expected_rank_order": 6,
    "expected_begin_time_ma": 165.3,
    "expected_begin_uncertainty_ma": 1.1,
    "expected_end_time_ma": 161.5,
    "expected_end_uncertainty_ma": 1.0,
    "expected_parent_id": "middle-jurassic"
}


EXPECTED_LATE_JURASSIC = {
    "expected_id": "late-jurassic",
    "expected_name": "Late Jurassic",
    "expected_rank": "Epoch",
    "expected_rank_order": 5,
    "expected_begin_time_ma": 161.5,
    "expected_begin_uncertainty_ma": 1.0,
    "expected_end_time_ma": 143.1,
    "expected_end_uncertainty_ma": 0.6,
    "expected_parent_id": "jurassic"
}


EXPECTED_CRETACEOUS = {
    "expected_id": "cretaceous",
    "expected_name": "Cretaceous",
    "expected_rank": "Period",
    "expected_rank_order": 4,
    "expected_begin_time_ma": 143.1,
    "expected_begin_uncertainty_ma": 0.6,
    "expected_end_time_ma": 66.0,
    "expected_end_uncertainty_ma": 0.0,
    "expected_parent_id": "mesozoic"
}


EXPECTED_UNITS = {
    "pleistocene": EXPECTED_PLEISTOCENE,
    "mesozoic": EXPECTED_MESOZOIC,
    "triassic": EXPECTED_TRIASSIC,
    "jurassic": EXPECTED_JURASSIC,
    "early-jurassic": EXPECTED_EARLY_JURASSIC,
    "middle-jurassic": EXPECTED_MIDDLE_JURASSIC,
    "aalenian": EXPECTED_AALENIAN,
    "bajocian": EXPECTED_BAJOCIAN,
    "bathonian": EXPECTED_BATHONIAN,
    "callovian": EXPECTED_CALLOVIAN,
    "late-jurassic": EXPECTED_LATE_JURASSIC,
    "cretaceous": EXPECTED_CRETACEOUS,
}
