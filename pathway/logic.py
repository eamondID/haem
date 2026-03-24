def determine_pathway(fever_resolved, neutro_resolved, stable,
                      enterocolitis, allo_sct, micro_defined):
    AN = {"header", "review72"}
    if fever_resolved:
        AN.add("resolved_fever")
        if micro_defined:
            AN.add("micro_defined"); AN.add("liaise_id")
            if neutro_resolved:
                AN.add("r_neutro_resolved")
                AN.add("target_abx_r"); AN.add("recurrent_fever_r"); AN.add("recurrent_box_r")
            else:
                AN.add("r_neutro_ongoing")
                if enterocolitis:
                    AN.add("r_entero_yes"); AN.add("continue_r")
                else:
                    AN.add("r_entero_no")
                    AN.add("target_abx_o"); AN.add("recurrent_fever_o"); AN.add("recurrent_box_o")
        else:
            AN.add("fever_unknown")
            if neutro_resolved:
                AN.add("l_neutro_resolved"); AN.add("stop_abx")
            else:
                AN.add("l_neutro_ongoing")
                if enterocolitis:
                    AN.add("l_entero_yes"); AN.add("continue_l")
                else:
                    AN.add("l_entero_no")
                    if allo_sct:
                        AN.add("allo_sct"); AN.add("cease_allo")
                    else:
                        AN.add("non_allo"); AN.add("cease_non_allo")
    else:
        AN.add("persistent_fever")
        if stable:
            AN.add("p_stable"); AN.add("p_cont")
        else:
            AN.add("p_unstable"); AN.add("imaging_box")
    return AN
 
 
def get_recommendations(AN):
    recs = []
    if "stop_abx" in AN:
        recs.append(("✅", "Stop antibiotics",
                     "Neutropaenia and fever both resolved — antibiotics can be discontinued."))
    if any(x in AN for x in ("continue_l", "continue_r")):
        recs.append(("💊", "Continue empiric antibiotics",
                     "Clinical situation warrants ongoing broad-spectrum cover."))
    if "p_cont" in AN:
        recs.append(("💊", "Continue empiric therapy",
                     "Fever persisting but clinically stable — continue current empiric regimen."))
    if "cease_allo" in AN:
        recs.append(("⚠️", "Consider ceasing (Allo-SCT)",
                     "Consider ceasing if another cause found. Discuss with ID / haematology."))
    if "cease_non_allo" in AN:
        recs.append(("⚠️", "Consider ceasing (Non-allo-SCT)",
                     "Consider ceasing empiric antibiotics. Discuss with ID / treating team."))
    if any(x in AN for x in ("target_abx_o", "target_abx_r")):
        recs.append(("🎯", "Target antibiotics",
                     "De-escalate to targeted therapy based on identified pathogen / source."))
    if "p_unstable" in AN:
        recs.append(("🚨", "Clinically unstable — escalate",
                     "Consider aminoglycoside. Liaise with ID re MRO coverage. Repeat cultures."))
    if "imaging_box" in AN:
        recs.append(("🖥️", "Consider further investigation",
                     "CT chest ± abdo/pelvis/sinus. MRI brain if CNS signs. Non-infective causes."))
    if any(x in AN for x in ("recurrent_box_o", "recurrent_box_r")):
        recs.append(("🔄", "Recurrent fever",
                     "Restart empiric abx + consider aminoglycoside. Liaise re MRO. Repeat cultures."))
    return recs
