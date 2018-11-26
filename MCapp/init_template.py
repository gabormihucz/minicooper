import crop

t = {}
t["cost"] = {"x1": 990, "x2": 1120, "y1": 600, "y2": 630}
t["tax"] = {"x1": 990, "x2": 1120, "y1": 676, "y2": 700}
t["total"] = {"x1": 990, "x2": 1120, "y1": 790, "y2": 820}


t["address_line1"] = {"x1": 120, "x2": 500, "y1": 328, "y2": 358}
t["address_line2"] = {"x1": 120, "x2": 500, "y1": 370, "y2": 400}

t["city"] = {"x1": 120, "x2": 360, "y1": 406, "y2": 444}
t["post_code"] = {"x1": 120, "x2": 310, "y1": 446, "y2": 480}

crop.save_template(t, "SampleTemplate")